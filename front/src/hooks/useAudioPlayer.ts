"use client";

import { useState, useRef, useEffect, useCallback } from "react";

/* ------------------------------------------------------------------ */
/*  Singleton: solo un audio a la vez en toda la app                  */
/* ------------------------------------------------------------------ */

let activePlayer: HTMLAudioElement | null = null;
let activeCleanup: (() => void) | null = null;

function claimPlayback(
  audio: HTMLAudioElement,
  cleanup: () => void,
): void {
  if (activePlayer && activePlayer !== audio) {
    activePlayer.pause();
    activeCleanup?.();
  }
  activePlayer = audio;
  activeCleanup = cleanup;
}

function releasePlayback(audio: HTMLAudioElement): void {
  if (activePlayer === audio) {
    activePlayer = null;
    activeCleanup = null;
  }
}

/* ------------------------------------------------------------------ */
/*  Feedback auditivo sutil al tocar play                             */
/* ------------------------------------------------------------------ */

function playClickFeedback(): void {
  if (typeof AudioContext === "undefined") return;
  // Respect reduced-motion preference
  if (typeof window !== "undefined" && window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
  try {
    const ctx = new AudioContext();
    const osc = ctx.createOscillator();
    const gain = ctx.createGain();
    osc.type = "triangle";
    osc.frequency.value = 800;
    gain.gain.value = 0.05;
    osc.connect(gain).connect(ctx.destination);
    osc.start();
    osc.stop(ctx.currentTime + 0.08);
    osc.onended = () => ctx.close();
  } catch { /* silent fail — no audio context available */ }
}

/* ------------------------------------------------------------------ */
/*  Velocidades                                                       */
/* ------------------------------------------------------------------ */

const SPEEDS = [0.75, 1, 1.25] as const;
type Speed = (typeof SPEEDS)[number];

/* ------------------------------------------------------------------ */
/*  Estado del reproductor                                            */
/* ------------------------------------------------------------------ */

interface PlayerState {
  isPlaying: boolean;
  isLoading: boolean;
  hasError: boolean;
  hasEnded: boolean;
  progress: number;       // 0-100
  currentTime: number;    // segundos
  duration: number;       // segundos
  speed: Speed;
}

const INITIAL_STATE: PlayerState = {
  isPlaying: false,
  isLoading: true,
  hasError: false,
  hasEnded: false,
  progress: 0,
  currentTime: 0,
  duration: 0,
  speed: 1,
};

/* ------------------------------------------------------------------ */
/*  Hook                                                              */
/* ------------------------------------------------------------------ */

export function useAudioPlayer(src: string, options?: { autoPlay?: boolean }) {
  const audioRef = useRef<HTMLAudioElement | null>(null);
  const [state, setState] = useState<PlayerState>(INITIAL_STATE);
  const speedIdxRef = useRef(1); // indice en SPEEDS
  const autoPlayedRef = useRef(false);

  // Crear audio element una sola vez
  useEffect(() => {
    autoPlayedRef.current = false;
    const audio = new Audio();
    audio.preload = "metadata";
    audio.src = src;
    audioRef.current = audio;

    /* --- Event listeners --- */

    const onLoadedMetadata = () => {
      setState((s) => ({
        ...s,
        duration: audio.duration || 0,
        isLoading: false,
      }));
    };

    const onTimeUpdate = () => {
      const progress = audio.duration
        ? (audio.currentTime / audio.duration) * 100
        : 0;
      setState((s) => ({
        ...s,
        currentTime: audio.currentTime,
        progress,
      }));
    };

    const onPlay = () => {
      setState((s) => ({ ...s, isPlaying: true, hasEnded: false }));
    };

    const onPause = () => {
      setState((s) => ({ ...s, isPlaying: false }));
    };

    const onEnded = () => {
      setState((s) => ({
        ...s,
        isPlaying: false,
        hasEnded: true,
        progress: 100,
      }));
      releasePlayback(audio);
    };

    const onError = () => {
      setState((s) => ({
        ...s,
        isLoading: false,
        hasError: true,
        isPlaying: false,
      }));
      releasePlayback(audio);
    };

    const onWaiting = () => {
      setState((s) => ({ ...s, isLoading: true }));
    };

    const onCanPlay = () => {
      setState((s) => ({ ...s, isLoading: false }));
    };

    audio.addEventListener("loadedmetadata", onLoadedMetadata);
    audio.addEventListener("timeupdate", onTimeUpdate);
    audio.addEventListener("play", onPlay);
    audio.addEventListener("pause", onPause);
    audio.addEventListener("ended", onEnded);
    audio.addEventListener("error", onError);
    audio.addEventListener("waiting", onWaiting);
    audio.addEventListener("canplay", onCanPlay);

    // Auto-play: misma experiencia que WhatsApp (Clara habla automaticamente)
    if (options?.autoPlay && !autoPlayedRef.current) {
      const onCanPlayThrough = () => {
        if (autoPlayedRef.current) return;
        autoPlayedRef.current = true;
        claimPlayback(audio, () => {
          setState((s) => ({ ...s, isPlaying: false }));
        });
        audio.play().catch(() => { /* browser blocked autoplay */ });
      };
      audio.addEventListener("canplaythrough", onCanPlayThrough, { once: true });
    }

    return () => {
      audio.pause();
      audio.removeEventListener("loadedmetadata", onLoadedMetadata);
      audio.removeEventListener("timeupdate", onTimeUpdate);
      audio.removeEventListener("play", onPlay);
      audio.removeEventListener("pause", onPause);
      audio.removeEventListener("ended", onEnded);
      audio.removeEventListener("error", onError);
      audio.removeEventListener("waiting", onWaiting);
      audio.removeEventListener("canplay", onCanPlay);
      releasePlayback(audio);
      audio.src = "";
      audioRef.current = null;
    };
  }, [src]);

  /* --- Acciones --- */

  const togglePlay = useCallback(async () => {
    const audio = audioRef.current;
    if (!audio || state.hasError) return;

    if (state.hasEnded) {
      audio.currentTime = 0;
    }

    if (audio.paused) {
      claimPlayback(audio, () => {
        setState((s) => ({ ...s, isPlaying: false }));
      });
      playClickFeedback();
      try {
        await audio.play();
      } catch {
        // Browser blocked autoplay — ignore, user will retry
      }
    } else {
      audio.pause();
    }
  }, [state.hasError, state.hasEnded]);

  const seek = useCallback((percent: number) => {
    const audio = audioRef.current;
    if (!audio || !audio.duration) return;
    const clamped = Math.max(0, Math.min(100, percent));
    audio.currentTime = (clamped / 100) * audio.duration;
    setState((s) => ({
      ...s,
      progress: clamped,
      currentTime: audio.currentTime,
      hasEnded: false,
    }));
  }, []);

  const cycleSpeed = useCallback(() => {
    const audio = audioRef.current;
    if (!audio) return;
    const nextIdx = (speedIdxRef.current + 1) % SPEEDS.length;
    speedIdxRef.current = nextIdx;
    const newSpeed = SPEEDS[nextIdx];
    audio.playbackRate = newSpeed;
    setState((s) => ({ ...s, speed: newSpeed }));
  }, []);

  return {
    ...state,
    togglePlay,
    seek,
    cycleSpeed,
  };
}
