"use client";

import { useCallback, useRef, useMemo } from "react";
import { useAudioPlayer } from "@/hooks/useAudioPlayer";
import type { Language } from "@/lib/types";

/* ------------------------------------------------------------------ */
/*  Labels bilingues                                                  */
/* ------------------------------------------------------------------ */

const labels = {
  es: {
    play: "Escuchar respuesta",
    playWithDuration: (d: string) => `Escuchar respuesta, ${d}`,
    pause: "Pausar audio",
    resume: "Continuar audio",
    replay: "Volver a escuchar",
    speed: (s: number) => `Velocidad ${s} equis`,
    error: "Audio no disponible",
    loading: "Cargando audio...",
    progress: "Progreso del audio",
  },
  en: {
    play: "Listen to response",
    playWithDuration: (d: string) => `Listen to response, ${d}`,
    pause: "Pause audio",
    resume: "Resume audio",
    replay: "Listen again",
    speed: (s: number) => `Speed ${s}x`,
    error: "Audio not available",
    loading: "Loading audio...",
    progress: "Audio progress",
  },
  fr: {
    play: "Écouter la réponse",
    playWithDuration: (d: string) => `Écouter la réponse, ${d}`,
    pause: "Mettre en pause",
    resume: "Reprendre l'audio",
    replay: "Réécouter",
    speed: (s: number) => `Vitesse ${s} fois`,
    error: "Audio non disponible",
    loading: "Chargement de l'audio...",
    progress: "Progression de l'audio",
  },
  pt: {
    play: "Ouvir resposta",
    playWithDuration: (d: string) => `Ouvir resposta, ${d}`,
    pause: "Pausar áudio",
    resume: "Continuar áudio",
    replay: "Ouvir novamente",
    speed: (s: number) => `Velocidade ${s}x`,
    error: "Áudio não disponível",
    loading: "A carregar áudio...",
    progress: "Progresso do áudio",
  },
  ro: {
    play: "Ascultă răspunsul",
    playWithDuration: (d: string) => `Ascultă răspunsul, ${d}`,
    pause: "Pauză audio",
    resume: "Continuă audio",
    replay: "Ascultă din nou",
    speed: (s: number) => `Viteză ${s}x`,
    error: "Audio indisponibil",
    loading: "Se încarcă audio...",
    progress: "Progresul audio",
  },
  ca: {
    play: "Escoltar resposta",
    playWithDuration: (d: string) => `Escoltar resposta, ${d}`,
    pause: "Pausar àudio",
    resume: "Continuar àudio",
    replay: "Tornar a escoltar",
    speed: (s: number) => `Velocitat ${s}x`,
    error: "Àudio no disponible",
    loading: "Carregant àudio...",
    progress: "Progrés de l'àudio",
  },
  zh: {
    play: "收听回复",
    playWithDuration: (d: string) => `收听回复，${d}`,
    pause: "暂停音频",
    resume: "继续音频",
    replay: "重新收听",
    speed: (s: number) => `速度 ${s}倍`,
    error: "音频不可用",
    loading: "正在加载音频...",
    progress: "音频进度",
  },
  ar: {
    play: "استمع للرد",
    playWithDuration: (d: string) => `استمع للرد، ${d}`,
    pause: "إيقاف مؤقت",
    resume: "متابعة الصوت",
    replay: "إعادة الاستماع",
    speed: (s: number) => `السرعة ${s} مرات`,
    error: "الصوت غير متاح",
    loading: "جاري تحميل الصوت...",
    progress: "تقدم الصوت",
  },
} as const;

/* ------------------------------------------------------------------ */
/*  Utility                                                           */
/* ------------------------------------------------------------------ */

function formatTime(seconds: number): string {
  if (!isFinite(seconds) || seconds < 0) return "0:00";
  const m = Math.floor(seconds / 60);
  const s = Math.floor(seconds % 60);
  return `${m}:${s.toString().padStart(2, "0")}`;
}

/* ------------------------------------------------------------------ */
/*  Waveform bars — pseudo-random heights for visual interest          */
/* ------------------------------------------------------------------ */

const WAVEFORM_BARS = 28;

function generateBarHeights(seed: number): number[] {
  const bars: number[] = [];
  let x = seed;
  for (let i = 0; i < WAVEFORM_BARS; i++) {
    x = ((x * 1103515245 + 12345) & 0x7fffffff) >>> 0;
    const h = 0.2 + (x % 100) / 125; // 0.2 – 1.0
    bars.push(h);
  }
  return bars;
}

/* ------------------------------------------------------------------ */
/*  Props                                                             */
/* ------------------------------------------------------------------ */

interface AudioPlayerProps {
  src: string;
  language: Language;
  autoPlay?: boolean;
}

/* ------------------------------------------------------------------ */
/*  Component                                                         */
/* ------------------------------------------------------------------ */

export default function AudioPlayer({ src, language, autoPlay }: AudioPlayerProps) {
  const {
    isPlaying,
    isLoading,
    hasError,
    hasEnded,
    progress,
    currentTime,
    duration,
    speed,
    togglePlay,
    seek,
    cycleSpeed,
  } = useAudioPlayer(src, { autoPlay });

  const waveformRef = useRef<HTMLDivElement>(null);
  const l = labels[language];

  // Stable bar heights based on src hash
  const barHeights = useMemo(() => {
    let hash = 0;
    for (let i = 0; i < src.length; i++) hash = ((hash << 5) - hash + src.charCodeAt(i)) | 0;
    return generateBarHeights(Math.abs(hash));
  }, [src]);

  /* --- Seek via waveform click/touch --- */
  const handleSeek = useCallback(
    (e: React.MouseEvent<HTMLDivElement> | React.TouchEvent<HTMLDivElement>) => {
      const bar = waveformRef.current;
      if (!bar || !duration) return;
      let clientX: number;
      if ("touches" in e) {
        clientX = e.touches[0].clientX;
      } else {
        clientX = e.clientX;
      }
      const rect = bar.getBoundingClientRect();
      const percent = ((clientX - rect.left) / rect.width) * 100;
      seek(percent);
    },
    [seek, duration],
  );

  /* --- Keyboard on waveform --- */
  const handleKeyDown = useCallback(
    (e: React.KeyboardEvent) => {
      if (e.key === "ArrowRight") {
        e.preventDefault();
        seek(Math.min(100, progress + 5));
      } else if (e.key === "ArrowLeft") {
        e.preventDefault();
        seek(Math.max(0, progress - 5));
      }
    },
    [seek, progress],
  );

  const playButtonLabel = (() => {
    if (hasError) return l.error;
    if (hasEnded) return l.replay;
    if (isPlaying) return l.pause;
    if (progress > 0) return l.resume;
    if (duration > 0) return l.playWithDuration(formatTime(duration));
    return l.play;
  })();

  const isIdle = !isPlaying && !hasEnded && !isLoading && progress === 0;

  /* --- Error state --- */
  if (hasError) {
    return (
      <div className="flex items-center gap-3 bg-clara-error/10 rounded-xl px-3 py-2.5 mt-2" role="alert">
        <div className="min-w-[40px] min-h-[40px] flex items-center justify-center bg-clara-text-secondary/20 rounded-full">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"
               className="text-clara-text-secondary" aria-hidden="true">
            <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 15v-2h2v2h-2zm0-4V7h2v6h-2z" />
          </svg>
        </div>
        <span className="text-[14px] text-clara-text-secondary">{l.error}</span>
      </div>
    );
  }

  const filledBars = Math.floor((progress / 100) * WAVEFORM_BARS);

  return (
    <div className="flex items-center gap-3 rounded-xl px-3 py-3 mt-2 bg-clara-blue/[0.06]">
      {/* ---- Play/Pause button ---- */}
      <button
        onClick={togglePlay}
        disabled={isLoading && !isPlaying}
        aria-label={playButtonLabel}
        className="min-w-[42px] min-h-[42px] flex items-center justify-center
                   bg-clara-blue text-white rounded-full shrink-0
                   hover:bg-[var(--color-clara-blue-hover)] active:scale-95
                   transition-[background-color,transform] duration-150
                   focus-visible:outline focus-visible:outline-[3px]
                   focus-visible:outline-clara-blue focus-visible:outline-offset-2
                   disabled:opacity-50 disabled:cursor-not-allowed"
        style={isIdle ? { animation: "playHintPulse 2s ease-in-out infinite" } : undefined}
      >
        {isLoading && !isPlaying ? (
          <div className="flex gap-1" aria-hidden="true">
            <span className="w-1.5 h-1.5 bg-white rounded-full animate-pulse" />
            <span className="w-1.5 h-1.5 bg-white rounded-full animate-pulse [animation-delay:150ms]" />
            <span className="w-1.5 h-1.5 bg-white rounded-full animate-pulse [animation-delay:300ms]" />
          </div>
        ) : (
          <span className="inline-flex" aria-hidden="true">
            {hasEnded ? (
              <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                <path d="M12 5V1L7 6l5 5V7c3.31 0 6 2.69 6 6s-2.69 6-6 6-6-2.69-6-6H4c0 4.42 3.58 8 8 8s8-3.58 8-8-3.58-8-8-8z" />
              </svg>
            ) : isPlaying ? (
              <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                <path d="M6 19h4V5H6v14zm8-14v14h4V5h-4z" />
              </svg>
            ) : (
              <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                <path d="M8 5v14l11-7z" />
              </svg>
            )}
          </span>
        )}
      </button>

      {/* ---- Waveform + time ---- */}
      <div className="flex-1 min-w-0">
        <div
          ref={waveformRef}
          role="slider"
          aria-label={l.progress}
          aria-valuemin={0}
          aria-valuemax={100}
          aria-valuenow={Math.round(progress)}
          tabIndex={0}
          onClick={handleSeek}
          onTouchStart={handleSeek}
          onKeyDown={handleKeyDown}
          className="relative h-8 flex items-center gap-[2px] cursor-pointer group
                     focus-visible:outline focus-visible:outline-[3px]
                     focus-visible:outline-clara-blue focus-visible:outline-offset-1 rounded"
        >
          {barHeights.map((h, i) => {
            const isFilled = i < filledBars;
            return (
              <span
                key={i}
                className="flex-1 rounded-full transition-colors duration-100"
                style={{
                  height: `${h * 24}px`,
                  minHeight: "4px",
                  backgroundColor: isFilled
                    ? "var(--color-clara-blue)"
                    : "color-mix(in srgb, var(--color-clara-blue) 25%, transparent)",
                }}
              />
            );
          })}
        </div>

        <div className="flex justify-between text-[12px] text-clara-text-secondary/70 -mt-0.5">
          <span className="tabular-nums">{formatTime(currentTime)}</span>
          <span className="tabular-nums">{formatTime(duration)}</span>
        </div>
      </div>

      {/* ---- Speed button ---- */}
      <button
        onClick={cycleSpeed}
        aria-label={l.speed(speed)}
        className="min-w-[38px] min-h-[38px] flex items-center justify-center shrink-0
                   text-[13px] font-bold text-clara-blue tabular-nums
                   border border-clara-blue/20 rounded-lg
                   hover:bg-clara-blue/10 active:scale-95
                   transition-[background-color,transform] duration-150
                   focus-visible:outline focus-visible:outline-[3px]
                   focus-visible:outline-clara-blue focus-visible:outline-offset-2"
      >
        {speed}x
      </button>
    </div>
  );
}
