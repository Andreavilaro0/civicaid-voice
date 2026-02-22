"use client";

import { useCallback, useRef } from "react";
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
    play: "Ecouter la reponse",
    playWithDuration: (d: string) => `Ecouter la reponse, ${d}`,
    pause: "Mettre en pause",
    resume: "Reprendre l'audio",
    replay: "Reecouter",
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
/*  Utilidad: formatear tiempo                                        */
/* ------------------------------------------------------------------ */

function formatTime(seconds: number): string {
  if (!isFinite(seconds) || seconds < 0) return "0:00";
  const m = Math.floor(seconds / 60);
  const s = Math.floor(seconds % 60);
  return `${m}:${s.toString().padStart(2, "0")}`;
}

/* ------------------------------------------------------------------ */
/*  Props                                                             */
/* ------------------------------------------------------------------ */

interface AudioPlayerProps {
  /** URL resuelta del audio (ya procesada con resolveAudioUrl) */
  src: string;
  /** Idioma para labels bilingues */
  language: Language;
  /** Auto-reproducir al cargar (misma experiencia que WhatsApp) */
  autoPlay?: boolean;
}

/* ------------------------------------------------------------------ */
/*  Componente                                                        */
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

  const progressBarRef = useRef<HTMLDivElement>(null);
  const l = labels[language];

  /* --- Seek al hacer click/touch en la barra --- */

  const handleSeek = useCallback(
    (e: React.MouseEvent<HTMLDivElement> | React.TouchEvent<HTMLDivElement>) => {
      const bar = progressBarRef.current;
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

  /* --- Keyboard en la barra de progreso --- */

  const handleProgressKeyDown = useCallback(
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

  /* --- Aria label dinamico para play/pause --- */

  const playButtonLabel = (() => {
    if (hasError) return l.error;
    if (hasEnded) return l.replay;
    if (isPlaying) return l.pause;
    if (progress > 0) return l.resume;
    if (duration > 0) return l.playWithDuration(formatTime(duration));
    return l.play;
  })();

  /* --- Idle state: invitar a Maria a tocar play --- */
  const isIdle = !isPlaying && !hasEnded && !isLoading && progress === 0;

  /* --- Estado de error --- */

  if (hasError) {
    return (
      <div
        className="flex items-center gap-3 bg-clara-error/10 rounded-xl px-3 py-2.5 mt-2"
        role="alert"
      >
        <div className="min-w-[48px] min-h-[48px] flex items-center justify-center
                        bg-clara-text-secondary/20 rounded-full">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor"
               className="text-clara-text-secondary" aria-hidden="true">
            <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 15v-2h2v2h-2zm0-4V7h2v6h-2z" />
          </svg>
        </div>
        <span className="text-[16px] text-clara-text-secondary">{l.error}</span>
      </div>
    );
  }

  return (
    <div className="flex items-center gap-3 bg-clara-green/10 rounded-xl px-3 py-2.5 mt-2">
      {/* ---- Boton Play/Pause ---- */}
      <button
        onClick={togglePlay}
        disabled={isLoading && !isPlaying}
        aria-label={playButtonLabel}
        className="min-w-[48px] min-h-[48px] flex items-center justify-center
                   bg-clara-green text-white rounded-full shrink-0
                   hover:bg-[#256B42] active:scale-95
                   transition-[background-color,transform] duration-150
                   [transition-timing-function:cubic-bezier(0.16,1,0.3,1)]
                   focus-visible:outline focus-visible:outline-[3px]
                   focus-visible:outline-clara-green focus-visible:outline-offset-2
                   disabled:opacity-50 disabled:cursor-not-allowed"
        style={isIdle ? { animation: "playHintPulse 2s ease-in-out infinite" } : undefined}
      >
        {isLoading && !isPlaying ? (
          /* Spinner de carga — 3 dots animados */
          <div className="flex gap-1" aria-hidden="true">
            <span className="w-1.5 h-1.5 bg-white rounded-full animate-pulse" />
            <span className="w-1.5 h-1.5 bg-white rounded-full animate-pulse [animation-delay:150ms]" />
            <span className="w-1.5 h-1.5 bg-white rounded-full animate-pulse [animation-delay:300ms]" />
          </div>
        ) : (
          <span
            className="inline-flex transition-[transform,opacity] duration-150"
            style={{ transitionTimingFunction: "cubic-bezier(0.16, 1, 0.3, 1)" }}
            aria-hidden="true"
          >
            {hasEnded ? (
              /* Icono replay */
              <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
                <path d="M12 5V1L7 6l5 5V7c3.31 0 6 2.69 6 6s-2.69 6-6 6-6-2.69-6-6H4c0 4.42 3.58 8 8 8s8-3.58 8-8-3.58-8-8-8z" />
              </svg>
            ) : isPlaying ? (
              /* Icono pause */
              <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
                <path d="M6 19h4V5H6v14zm8-14v14h4V5h-4z" />
              </svg>
            ) : (
              /* Icono play */
              <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
                <path d="M8 5v14l11-7z" />
              </svg>
            )}
          </span>
        )}
      </button>

      {/* ---- Barra de progreso + tiempo ---- */}
      <div className="flex-1 min-w-0">
        {/* Zona seekable — area tactil de 32px, barra visual de 8px */}
        <div
          ref={progressBarRef}
          role="slider"
          aria-label={l.progress}
          aria-valuemin={0}
          aria-valuemax={100}
          aria-valuenow={Math.round(progress)}
          tabIndex={0}
          onClick={handleSeek}
          onTouchStart={handleSeek}
          onKeyDown={handleProgressKeyDown}
          className="relative h-8 flex items-center cursor-pointer group
                     focus-visible:outline focus-visible:outline-[3px]
                     focus-visible:outline-clara-green focus-visible:outline-offset-1
                     rounded"
        >
          {/* Track */}
          <div className="relative w-full h-2 bg-clara-border rounded-full overflow-visible">
            {/* Fill */}
            <div
              className="h-full bg-clara-green rounded-full transition-[width] duration-250 [transition-timing-function:cubic-bezier(0.16,1,0.3,1)]"
              style={{ width: `${progress}%` }}
            />
            {/* Thumb indicator — appears on hover/focus */}
            <div
              className="absolute top-1/2 -translate-y-1/2 w-4 h-4 bg-clara-green rounded-full
                         shadow-sm opacity-0 group-hover:opacity-100 group-focus-visible:opacity-100
                         transition-opacity duration-200 pointer-events-none"
              style={{ left: `calc(${progress}% - 8px)` }}
              aria-hidden="true"
            />
          </div>
        </div>

        {/* Tiempo */}
        <div className="flex justify-between text-[13px] text-clara-text-secondary -mt-1">
          <span className="tabular-nums">{formatTime(currentTime)}</span>
          <span className="tabular-nums">{formatTime(duration)}</span>
        </div>
      </div>

      {/* ---- Boton velocidad ---- */}
      <button
        onClick={cycleSpeed}
        aria-label={l.speed(speed)}
        className="min-w-[44px] min-h-[44px] flex items-center justify-center shrink-0
                   text-[14px] font-bold text-clara-green tabular-nums
                   border border-clara-green/30 rounded-lg
                   hover:bg-clara-green/10 active:scale-95
                   transition-[background-color,transform] duration-150
                   focus-visible:outline focus-visible:outline-[3px]
                   focus-visible:outline-clara-green focus-visible:outline-offset-2"
      >
        {speed}x
      </button>
    </div>
  );
}
