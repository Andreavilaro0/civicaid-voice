"use client";

import { useState, useRef, useEffect } from "react";
import { useAudioRecorder } from "@/hooks/useAudioRecorder";
import type { Language } from "@/lib/types";

/* ------------------------------------------------------------------ */
/*  Props                                                              */
/* ------------------------------------------------------------------ */

interface VoiceRecorderProps {
  visible: boolean;
  language: Language;
  onRecordingComplete: (audioBase64: string) => void;
  onCancel: () => void;
}

/* ------------------------------------------------------------------ */
/*  Labels bilingues                                                   */
/* ------------------------------------------------------------------ */

const labels: Record<Language, { speak: string; cancel: string; send: string; warning: string; tap_start: string; tap_stop: string; mic_error: string; try_again: string; use_text: string }> = {
  es: {
    speak: "Habla ahora...",
    cancel: "Cancelar",
    send: "Enviar",
    warning: "Quedan pocos segundos",
    tap_start: "Toca para grabar",
    tap_stop: "Toca para parar",
    mic_error:
      "No se pudo acceder al microfono. Asegurate de dar permiso en tu navegador.",
    try_again: "Probar de nuevo",
    use_text: "Escribir en su lugar",
  },
  en: {
    speak: "Speak now...",
    cancel: "Cancel",
    send: "Send",
    warning: "Few seconds left",
    tap_start: "Tap to record",
    tap_stop: "Tap to stop",
    mic_error:
      "Could not access the microphone. Make sure to grant permission in your browser.",
    try_again: "Try again",
    use_text: "Type instead",
  },
  fr: {
    speak: "Parle maintenant...",
    cancel: "Annuler",
    send: "Envoyer",
    warning: "Il reste peu de secondes",
    tap_start: "Appuie pour enregistrer",
    tap_stop: "Appuie pour arreter",
    mic_error:
      "Impossible d'acceder au micro. Assure-toi de donner la permission dans ton navigateur.",
    try_again: "Reessayer",
    use_text: "Ecrire a la place",
  },
  pt: {
    speak: "Fala agora...",
    cancel: "Cancelar",
    send: "Enviar",
    warning: "Restam poucos segundos",
    tap_start: "Toca para gravar",
    tap_stop: "Toca para parar",
    mic_error:
      "Não foi possível aceder ao microfone. Certifica-te de dar permissão no teu navegador.",
    try_again: "Tentar novamente",
    use_text: "Escrever em vez disso",
  },
  ro: {
    speak: "Vorbește acum...",
    cancel: "Anulează",
    send: "Trimite",
    warning: "Mai sunt puține secunde",
    tap_start: "Apasă pentru a înregistra",
    tap_stop: "Apasă pentru a opri",
    mic_error:
      "Nu s-a putut accesa microfonul. Asigură-te că ai acordat permisiunea în browser.",
    try_again: "Încearcă din nou",
    use_text: "Scrie în schimb",
  },
  ca: {
    speak: "Parla ara...",
    cancel: "Cancel·lar",
    send: "Enviar",
    warning: "Queden pocs segons",
    tap_start: "Toca per gravar",
    tap_stop: "Toca per aturar",
    mic_error:
      "No s'ha pogut accedir al micròfon. Assegura't de donar permís al teu navegador.",
    try_again: "Tornar a provar",
    use_text: "Escriure en lloc d'això",
  },
  zh: {
    speak: "请说话...",
    cancel: "取消",
    send: "发送",
    warning: "剩余时间不多",
    tap_start: "点击录音",
    tap_stop: "点击停止",
    mic_error:
      "无法访问麦克风。请确保在浏览器中授予权限。",
    try_again: "再试一次",
    use_text: "改为打字",
  },
  ar: {
    speak: "تحدث الآن...",
    cancel: "إلغاء",
    send: "إرسال",
    warning: "بقي وقت قليل",
    tap_start: "اضغط للتسجيل",
    tap_stop: "اضغط للإيقاف",
    mic_error:
      "تعذر الوصول إلى الميكروفون. تأكد من منح الإذن في متصفحك.",
    try_again: "حاول مرة أخرى",
    use_text: "اكتب بدلاً من ذلك",
  },
};

/** Alturas seeded una sola vez — no re-randomize en cada render (D3) */
const BAR_HEIGHTS = Array.from({ length: 12 }, () => 16 + Math.random() * 20);

/* ------------------------------------------------------------------ */
/*  Componente                                                        */
/* ------------------------------------------------------------------ */

export default function VoiceRecorder({
  visible,
  language,
  onRecordingComplete,
  onCancel,
}: VoiceRecorderProps) {
  const { isRecording, seconds, isWarning, error, start, stop, cancel } =
    useAudioRecorder();
  const t = labels[language];

  const overlayRef = useRef<HTMLDivElement>(null);

  /* ---- Entry/exit animation (D1) ---- */
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    if (visible) setMounted(true);
  }, [visible]);

  function handleTransitionEnd() {
    if (!visible) setMounted(false);
  }

  /* ---- Cancel: descarta grabacion y cierra overlay ---- */
  function handleCancel() {
    cancel();
    onCancel();
  }

  /* ---- Escape key cierra overlay (U1) ---- */
  useEffect(() => {
    if (!mounted) return;
    function onKeyDown(e: KeyboardEvent) {
      if (e.key === "Escape") {
        handleCancel();
      }
    }
    document.addEventListener("keydown", onKeyDown);
    return () => document.removeEventListener("keydown", onKeyDown);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [mounted]);

  /* ---- Focus trap: Tab no escapa del overlay (U2) ---- */
  useEffect(() => {
    if (!mounted) return;
    const overlay = overlayRef.current;
    if (!overlay) return;

    const focusable = overlay.querySelectorAll<HTMLElement>(
      'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
    );
    if (focusable.length === 0) return;

    const first = focusable[0];
    const last = focusable[focusable.length - 1];

    first.focus();

    function trapFocus(e: KeyboardEvent) {
      if (e.key !== "Tab") return;
      if (e.shiftKey) {
        if (document.activeElement === first) {
          e.preventDefault();
          last.focus();
        }
      } else {
        if (document.activeElement === last) {
          e.preventDefault();
          first.focus();
        }
      }
    }

    overlay.addEventListener("keydown", trapFocus);
    return () => overlay.removeEventListener("keydown", trapFocus);
  }, [mounted]);

  /* ---- Back button cierra overlay — Android (U3) ---- */
  useEffect(() => {
    if (!mounted) return;
    history.pushState({ voiceOverlay: true }, "");
    function onPopState() {
      handleCancel();
    }
    window.addEventListener("popstate", onPopState);
    return () => window.removeEventListener("popstate", onPopState);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [mounted]);

  /* ---- Toggle: tap para empezar, tap para parar ---- */
  async function handleToggle() {
    if (isRecording) {
      // Guard: grabacion < 1s = probable double-tap accidental (U4)
      if (seconds < 1) return;
      const base64 = await stop();
      if (base64) onRecordingComplete(base64);
    } else {
      await start();
    }
  }

  /* ---- Send: para y envia (cuando ya esta grabando) ---- */
  async function handleSend() {
    const base64 = await stop();
    if (base64) onRecordingComplete(base64);
  }

  /* ---- Timer display ---- */
  const minutes = Math.floor(seconds / 60);
  const secs = seconds % 60;
  const timeDisplay = `${minutes}:${secs.toString().padStart(2, "0")}`;

  if (!mounted) return null;

  return (
    <div
      ref={overlayRef}
      className="fixed inset-0 bg-clara-bg z-50 flex flex-col items-center justify-center px-6"
      role="dialog"
      aria-label={isRecording ? t.speak : t.tap_start}
      aria-modal="true"
      style={{
        opacity: visible ? 1 : 0,
        transform: visible ? "scale(1)" : "scale(0.97)",
        transition: visible
          ? "opacity 500ms cubic-bezier(0.16, 1, 0.3, 1), transform 500ms cubic-bezier(0.16, 1, 0.3, 1)"
          : "opacity 300ms cubic-bezier(0.55, 0, 1, 0.45)",
        pointerEvents: visible ? "auto" : "none",
      }}
      onTransitionEnd={handleTransitionEnd}
    >
      {/* Titulo — cambia segun estado */}
      <p className="font-display font-bold text-h2 text-clara-text mb-8 text-center">
        {isRecording ? t.speak : t.tap_start}
      </p>

      {/* Onda de audio animada — 12 barras naranja (D2, D3, D5) */}
      {isRecording && (
        <div
          className="flex items-end gap-1.5 mb-6 h-10"
          aria-hidden="true"
        >
          {BAR_HEIGHTS.map((h, i) => (
            <span
              key={i}
              className="w-1.5 bg-clara-orange rounded-full"
              style={{
                height: `${h}px`,
                transformOrigin: "bottom",
                animation: `waveBar 1.2s ease-in-out ${i * 80}ms infinite`,
              }}
            />
          ))}
        </div>
      )}

      {/* Timer — tabular-nums, rojo cuando warning (T1) */}
      <p
        className={`font-body text-[24px] tabular-nums mb-8 ${
          isWarning
            ? "text-clara-error font-bold"
            : "text-clara-text-secondary"
        }`}
        aria-live="polite"
      >
        {timeDisplay}
        {isWarning && <span className="sr-only">{t.warning}</span>}
      </p>

      {/* Boton microfono grande — 96x96px, toggle (D4, D7) */}
      <button
        onClick={handleToggle}
        aria-label={isRecording ? t.tap_stop : t.tap_start}
        className="w-touch-lg h-touch-lg rounded-full flex items-center justify-center mb-10
                   focus-visible:outline focus-visible:outline-[3px] focus-visible:outline-clara-blue focus-visible:outline-offset-2"
        style={{
          backgroundColor: isRecording ? "#C62828" : "#1B5E7B",
          transition: "background-color 300ms cubic-bezier(0.16, 1, 0.3, 1)",
          animation: isRecording
            ? "gentlePulse 2s ease-in-out infinite"
            : "none",
        }}
      >
        <svg
          width="48"
          height="48"
          viewBox="0 0 24 24"
          fill="white"
          aria-hidden="true"
        >
          <path d="M12 14c1.66 0 3-1.34 3-3V5c0-1.66-1.34-3-3-3S9 3.34 9 5v6c0 1.66 1.34 3 3 3z" />
          <path d="M17 11c0 2.76-2.24 5-5 5s-5-2.24-5-5H5c0 3.53 2.61 6.43 6 6.92V21h2v-3.08c3.39-.49 6-3.39 6-6.92h-2z" />
        </svg>
      </button>

      {/* Cancelar / Enviar (D6, D7) */}
      <div className="flex gap-4 w-full max-w-sm">
        <button
          onClick={handleCancel}
          aria-label={t.cancel}
          className="flex-1 h-touch bg-white border-2 border-clara-border rounded-xl
                     text-button font-medium text-clara-text-secondary
                     hover:border-clara-text hover:text-clara-text
                     transition-colors duration-150
                     focus-visible:outline focus-visible:outline-[3px] focus-visible:outline-clara-blue focus-visible:outline-offset-2"
        >
          {t.cancel}
        </button>
        {isRecording && (
          <button
            onClick={handleSend}
            aria-label={t.send}
            className="flex-1 h-touch bg-clara-green text-white rounded-xl
                       text-button font-medium hover:bg-[#256940]
                       transition-colors duration-150
                       focus-visible:outline focus-visible:outline-[3px] focus-visible:outline-clara-green focus-visible:outline-offset-2"
          >
            {t.send}
          </button>
        )}
      </div>

      {/* Error de microfono — amable, con opciones (T2, T3, T4) */}
      {error && (
        <div role="alert" className="mt-6 text-left max-w-sm">
          <p className="text-clara-error text-body text-left mb-4">
            {t.mic_error}
          </p>
          <div className="flex gap-3 justify-center">
            <button
              onClick={() => void start()}
              className="px-4 min-h-touch-sm bg-clara-blue text-white rounded-lg
                         text-body-sm font-medium hover:bg-[#164d66]
                         transition-colors duration-150
                         focus-visible:outline focus-visible:outline-[3px] focus-visible:outline-clara-blue focus-visible:outline-offset-2"
            >
              {t.try_again}
            </button>
            <button
              onClick={onCancel}
              className="px-4 min-h-touch-sm border-2 border-clara-border rounded-lg
                         text-body-sm font-medium text-clara-text-secondary
                         hover:border-clara-blue hover:text-clara-blue
                         transition-colors duration-150
                         focus-visible:outline focus-visible:outline-[3px] focus-visible:outline-clara-blue focus-visible:outline-offset-2"
            >
              {t.use_text}
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
