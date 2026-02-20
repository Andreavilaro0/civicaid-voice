"use client";

import { useState, useRef, useCallback, useEffect } from "react";
import {
  AUDIO_FEEDBACK,
  MAX_RECORDING_SECONDS,
  RECORDING_WARNING_SECONDS,
} from "@/lib/constants";
import type { AudioFeedbackParams } from "@/lib/types";

/* ------------------------------------------------------------------ */
/*  Audio feedback — Web Audio API beep (zero dependencies)            */
/* ------------------------------------------------------------------ */

/** AudioContext reusable — reusar evita Safari "user gesture" policy en auto-stop */
let sharedAudioCtx: AudioContext | null = null;

function getAudioContext(): AudioContext {
  if (!sharedAudioCtx || sharedAudioCtx.state === "closed") {
    sharedAudioCtx = new AudioContext();
  }
  // Resume si esta suspendido (Safari policy)
  if (sharedAudioCtx.state === "suspended") {
    sharedAudioCtx.resume();
  }
  return sharedAudioCtx;
}

function playBeep(params: AudioFeedbackParams): void {
  try {
    const ctx = getAudioContext();
    const osc = ctx.createOscillator();
    const gain = ctx.createGain();
    const now = ctx.currentTime;
    const dur = params.duration / 1000;

    osc.type = params.type;
    osc.frequency.value = params.frequency;

    // Amplitude envelope — "rounded corners for sound" (Civic Tenderness)
    // 20ms attack ramp: silence → 0.3 (no click al inicio)
    gain.gain.setValueAtTime(0, now);
    gain.gain.linearRampToValueAtTime(0.3, now + 0.02);
    // 30ms release ramp: 0.3 → silence (no click al final)
    gain.gain.linearRampToValueAtTime(0, now + dur);

    osc.connect(gain);
    gain.connect(ctx.destination);

    osc.start(now);
    osc.stop(now + dur + 0.01); // +10ms buffer para release

    // Haptic feedback — tercer canal sensorial (no soportado en iOS Safari)
    if (navigator.vibrate) navigator.vibrate(50);
  } catch {
    // AudioContext no soportado — silencio graceful
  }
}

/* ------------------------------------------------------------------ */
/*  Estado del recorder                                                */
/* ------------------------------------------------------------------ */

interface RecorderState {
  isRecording: boolean;
  seconds: number;
  isWarning: boolean;
  error: string | null;
}

/* ------------------------------------------------------------------ */
/*  Hook                                                              */
/* ------------------------------------------------------------------ */

export function useAudioRecorder() {
  const [state, setState] = useState<RecorderState>({
    isRecording: false,
    seconds: 0,
    isWarning: false,
    error: null,
  });

  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const chunksRef = useRef<Blob[]>([]);
  const timerRef = useRef<ReturnType<typeof setInterval> | null>(null);

  /* ---- Cleanup: para grabacion + cierra tracks ---- */
  const cleanup = useCallback(() => {
    if (timerRef.current) clearInterval(timerRef.current);
    if (mediaRecorderRef.current?.state === "recording") {
      mediaRecorderRef.current.stop();
    }
    mediaRecorderRef.current?.stream
      .getTracks()
      .forEach((track) => track.stop());
  }, []);

  /* ---- Cleanup al desmontar — NUNCA dejar stream abierto ---- */
  useEffect(() => {
    return cleanup;
  }, [cleanup]);

  /* ---- Start: pide microfono, inicia grabacion ---- */
  const start = useCallback(async () => {
    try {
      chunksRef.current = [];
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const recorder = new MediaRecorder(stream, {
        mimeType: MediaRecorder.isTypeSupported("audio/webm;codecs=opus")
          ? "audio/webm;codecs=opus"
          : "audio/webm",
      });
      mediaRecorderRef.current = recorder;

      recorder.ondataavailable = (e) => {
        if (e.data.size > 0) chunksRef.current.push(e.data);
      };

      // Handler de error mid-recording (stream interrumpido, bluetooth desconectado)
      recorder.onerror = () => {
        cleanup();
        setState((prev) => ({
          ...prev,
          isRecording: false,
          error: "La grabacion se interrumpio. Intenta de nuevo.",
        }));
      };

      recorder.start(100); // chunks cada 100ms
      playBeep(AUDIO_FEEDBACK.recordStart); // beep ascendente — "te escucho"
      setState({ isRecording: true, seconds: 0, isWarning: false, error: null });

      // Timer: cada segundo actualiza counter, warning beep a 50s, auto-stop a 60s
      timerRef.current = setInterval(() => {
        setState((prev) => {
          const next = prev.seconds + 1;
          if (next >= MAX_RECORDING_SECONDS) {
            cleanup();
            playBeep(AUDIO_FEEDBACK.recordStop); // AudioContext compartido — funciona en Safari
            return { ...prev, isRecording: false, seconds: next };
          }
          // Warning beep a 50s — doble pulso para atencion auditiva
          if (next === RECORDING_WARNING_SECONDS) {
            playBeep(AUDIO_FEEDBACK.recordWarning);
            setTimeout(() => playBeep(AUDIO_FEEDBACK.recordWarning), 250);
          }
          return {
            ...prev,
            seconds: next,
            isWarning: next >= RECORDING_WARNING_SECONDS,
          };
        });
      }, 1000);
    } catch {
      setState((prev) => ({
        ...prev,
        error: "No se pudo acceder al microfono",
      }));
    }
  }, [cleanup]);

  /* ---- Stop: para grabacion, retorna base64 ---- */
  const stop = useCallback((): Promise<string> => {
    return new Promise((resolve) => {
      const recorder = mediaRecorderRef.current;
      if (!recorder || recorder.state !== "recording") {
        resolve("");
        return;
      }

      // Timeout: si conversion tarda > 5s, algo fallo
      const timeout = setTimeout(() => {
        cleanup();
        setState((prev) => ({ ...prev, isRecording: false, error: "Error al procesar audio" }));
        resolve("");
      }, 5000);

      recorder.onstop = async () => {
        try {
          if (timerRef.current) clearInterval(timerRef.current);
          const blob = new Blob(chunksRef.current, { type: "audio/webm" });
          const buffer = await blob.arrayBuffer();
          const base64 = btoa(
            new Uint8Array(buffer).reduce(
              (data, byte) => data + String.fromCharCode(byte),
              ""
            )
          );
          clearTimeout(timeout);
          setState((prev) => ({ ...prev, isRecording: false }));
          recorder.stream.getTracks().forEach((track) => track.stop());
          resolve(base64);
        } catch {
          clearTimeout(timeout);
          cleanup();
          setState((prev) => ({ ...prev, isRecording: false, error: "Error al procesar audio" }));
          resolve(""); // resolve vacio, no reject — overlay cierra limpiamente
        }
      };

      playBeep(AUDIO_FEEDBACK.recordStop); // beep descendente — "listo"
      recorder.stop();
    });
  }, [cleanup]);

  /* ---- Cancel: descarta todo sin enviar ---- */
  const cancel = useCallback(() => {
    cleanup();
    chunksRef.current = [];
    setState({ isRecording: false, seconds: 0, isWarning: false, error: null });
  }, [cleanup]);

  return { ...state, start, stop, cancel };
}
