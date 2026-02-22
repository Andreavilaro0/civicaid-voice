"use client";

import { useState, useRef, useEffect } from "react";
import type { Language } from "@/lib/types";
import Button from "@/components/ui/Button";

/* ------------------------------------------------------------------ */
/*  Props                                                              */
/* ------------------------------------------------------------------ */

interface DocumentUploadProps {
  visible: boolean;
  language: Language;
  onUpload: (imageBase64: string) => void;
  onCancel: () => void;
}

/* ------------------------------------------------------------------ */
/*  Labels bilingues                                                   */
/* ------------------------------------------------------------------ */

const labels: Record<Language, {
  title: string;
  desc: string;
  camera: string;
  gallery: string;
  cancel: string;
  send: string;
  preview: string;
  change: string;
  error_read: string;
  error_size: string;
}> = {
  es: {
    title: "Subir documento",
    desc: "Sube una foto de tu documento o carta. Clara te explicara que dice.",
    camera: "Hacer foto",
    gallery: "Elegir de galeria",
    cancel: "Cancelar",
    send: "Enviar a Clara",
    preview: "Vista previa del documento",
    change: "Cambiar foto",
    error_read: "No se pudo leer la imagen. Prueba con otra foto.",
    error_size: "La imagen es muy grande. Prueba con una foto mas pequena.",
  },
  en: {
    title: "Upload document",
    desc: "Upload a photo of your document or letter. Clara will explain what it says.",
    camera: "Take photo",
    gallery: "Choose from gallery",
    cancel: "Cancel",
    send: "Send to Clara",
    preview: "Document preview",
    change: "Change photo",
    error_read: "Could not read the image. Try another photo.",
    error_size: "The image is too large. Try a smaller photo.",
  },
  fr: {
    title: "Envoyer un document",
    desc: "Envoie une photo de ton document ou courrier. Clara t'expliquera ce qu'il dit.",
    camera: "Prendre une photo",
    gallery: "Choisir dans la galerie",
    cancel: "Annuler",
    send: "Envoyer a Clara",
    preview: "Apercu du document",
    change: "Changer la photo",
    error_read: "Impossible de lire l'image. Essaie avec une autre photo.",
    error_size: "L'image est trop grande. Essaie avec une photo plus petite.",
  },
  pt: {
    title: "Enviar documento",
    desc: "Envia uma foto do teu documento ou carta. Clara vai explicar-te o que diz.",
    camera: "Tirar foto",
    gallery: "Escolher da galeria",
    cancel: "Cancelar",
    send: "Enviar à Clara",
    preview: "Pré-visualização do documento",
    change: "Mudar foto",
    error_read: "Não foi possível ler a imagem. Tenta com outra foto.",
    error_size: "A imagem é muito grande. Tenta com uma foto mais pequena.",
  },
  ro: {
    title: "Încarcă document",
    desc: "Încarcă o fotografie a documentului sau scrisorii tale. Clara îți va explica ce scrie.",
    camera: "Fă o fotografie",
    gallery: "Alege din galerie",
    cancel: "Anulează",
    send: "Trimite la Clara",
    preview: "Previzualizare document",
    change: "Schimbă fotografia",
    error_read: "Nu s-a putut citi imaginea. Încearcă cu altă fotografie.",
    error_size: "Imaginea este prea mare. Încearcă cu o fotografie mai mică.",
  },
  ca: {
    title: "Pujar document",
    desc: "Puja una foto del teu document o carta. Clara t'explicarà què diu.",
    camera: "Fer foto",
    gallery: "Triar de la galeria",
    cancel: "Cancel·lar",
    send: "Enviar a Clara",
    preview: "Vista prèvia del document",
    change: "Canviar foto",
    error_read: "No s'ha pogut llegir la imatge. Prova amb una altra foto.",
    error_size: "La imatge és massa gran. Prova amb una foto més petita.",
  },
  zh: {
    title: "上传文件",
    desc: "上传你的文件或信件的照片。Clara会为你解释内容。",
    camera: "拍照",
    gallery: "从相册选择",
    cancel: "取消",
    send: "发送给Clara",
    preview: "文件预览",
    change: "更换照片",
    error_read: "无法读取图片。请尝试其他照片。",
    error_size: "图片太大。请尝试较小的照片。",
  },
  ar: {
    title: "رفع مستند",
    desc: "ارفع صورة لمستندك أو رسالتك. كلارا ستشرح لك ما يقوله.",
    camera: "التقط صورة",
    gallery: "اختر من المعرض",
    cancel: "إلغاء",
    send: "إرسال إلى كلارا",
    preview: "معاينة المستند",
    change: "تغيير الصورة",
    error_read: "تعذرت قراءة الصورة. جرب صورة أخرى.",
    error_size: "الصورة كبيرة جداً. جرب صورة أصغر.",
  },
};

/** Max 10MB antes de base64 encoding */
const MAX_FILE_SIZE = 10 * 1024 * 1024;

/* ------------------------------------------------------------------ */
/*  Shutter click feedback via Web Audio API (sonic-branding)          */
/* ------------------------------------------------------------------ */

function playShutterFeedback() {
  if (typeof AudioContext === "undefined") return;
  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
  try {
    const ctx = new AudioContext();
    const osc = ctx.createOscillator();
    const gain = ctx.createGain();
    osc.type = "sine";
    osc.frequency.value = 1200;
    gain.gain.setValueAtTime(0.06, ctx.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.08);
    osc.connect(gain).connect(ctx.destination);
    osc.start();
    osc.stop(ctx.currentTime + 0.08);
    osc.onended = () => ctx.close();
  } catch {
    /* silent fail */
  }
}

/* ------------------------------------------------------------------ */
/*  Componente                                                        */
/* ------------------------------------------------------------------ */

export default function DocumentUpload({
  visible,
  language,
  onUpload,
  onCancel,
}: DocumentUploadProps) {
  const [preview, setPreview] = useState<string | null>(null);
  const [base64, setBase64] = useState("");
  const [error, setError] = useState<string | null>(null);
  const cameraRef = useRef<HTMLInputElement>(null);
  const galleryRef = useRef<HTMLInputElement>(null);
  const overlayRef = useRef<HTMLDivElement>(null);
  const t = labels[language];

  /* ---- Entry/exit animation (patron VoiceRecorder) ---- */
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    if (visible) setMounted(true);
  }, [visible]);

  function handleTransitionEnd() {
    if (!visible) setMounted(false);
  }

  /* ---- Escape key cierra overlay ---- */
  useEffect(() => {
    if (!mounted) return;
    function onKeyDown(e: KeyboardEvent) {
      if (e.key === "Escape") handleCancel();
    }
    document.addEventListener("keydown", onKeyDown);
    return () => document.removeEventListener("keydown", onKeyDown);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [mounted]);

  /* ---- Focus trap ---- */
  useEffect(() => {
    if (!mounted) return;
    const overlay = overlayRef.current;
    if (!overlay) return;

    const focusable = overlay.querySelectorAll<HTMLElement>(
      'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])',
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
  }, [mounted, preview]);

  /* ---- Android back button ---- */
  useEffect(() => {
    if (!mounted) return;
    history.pushState({ documentOverlay: true }, "");
    function onPopState() {
      handleCancel();
    }
    window.addEventListener("popstate", onPopState);
    return () => window.removeEventListener("popstate", onPopState);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [mounted]);

  /* ---- File handling ---- */
  function handleFile(file: File) {
    setError(null);

    if (file.size > MAX_FILE_SIZE) {
      setError(t.error_size);
      return;
    }

    const reader = new FileReader();
    reader.onload = () => {
      const result = reader.result as string;
      setPreview(result);
      setBase64(result.split(",")[1]);
      playShutterFeedback();
    };
    reader.onerror = () => {
      setError(t.error_read);
    };
    reader.readAsDataURL(file);
  }

  function handleChange(e: React.ChangeEvent<HTMLInputElement>) {
    const file = e.target.files?.[0];
    if (file) handleFile(file);
    e.target.value = "";
  }

  function handleCancel() {
    setPreview(null);
    setBase64("");
    setError(null);
    onCancel();
  }

  function handleSend() {
    if (base64) onUpload(base64);
  }

  function handleChangePhoto() {
    setPreview(null);
    setBase64("");
    setError(null);
  }

  if (!mounted) return null;

  return (
    <div
      ref={overlayRef}
      className="fixed inset-0 bg-clara-bg z-50 flex flex-col px-6 py-8"
      role="dialog"
      aria-label={t.title}
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
      {/* Header — boton atras + titulo */}
      <div className="flex items-center mb-6">
        <button
          onClick={handleCancel}
          aria-label={t.cancel}
          className="min-w-touch-sm min-h-touch-sm flex items-center justify-center
                     rounded-lg transition-colors duration-150
                     hover:bg-clara-card
                     focus-visible:outline focus-visible:outline-[3px]
                     focus-visible:outline-clara-blue focus-visible:outline-offset-2"
        >
          <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
            <path d="M20 11H7.83l5.59-5.59L12 4l-8 8 8 8 1.41-1.41L7.83 13H20v-2z" />
          </svg>
        </button>
        <h2 className="font-display font-bold text-h2 text-clara-text ml-2">
          {t.title}
        </h2>
      </div>

      {/* Descripcion */}
      <p className="text-body text-clara-text-secondary mb-8 leading-relaxed">
        {t.desc}
      </p>

      {/* Hidden file inputs */}
      <input
        ref={cameraRef}
        type="file"
        accept="image/*"
        capture="environment"
        onChange={handleChange}
        className="hidden"
        aria-hidden="true"
        tabIndex={-1}
      />
      <input
        ref={galleryRef}
        type="file"
        accept="image/*"
        onChange={handleChange}
        className="hidden"
        aria-hidden="true"
        tabIndex={-1}
      />

      {/* Error state */}
      {error && (
        <div role="alert" className="mb-6 p-4 bg-red-50 border-2 border-clara-error/20 rounded-xl">
          <p className="text-body text-clara-error">{error}</p>
        </div>
      )}

      {/* Estado: Preview de la imagen capturada */}
      {preview ? (
        <div className="flex-1 flex flex-col items-center justify-center">
          <div
            className="relative mb-6 w-full max-w-sm"
            style={{ animation: "previewEnter 400ms cubic-bezier(0.16, 1, 0.3, 1)" }}
          >
            <img
              src={preview}
              alt={t.preview}
              className="w-full max-h-[50vh] rounded-xl border-2 border-clara-green/50 object-contain shadow-lg shadow-clara-green/10"
            />
          </div>

          {/* Acciones: Cambiar / Enviar */}
          <div className="flex gap-4 w-full max-w-sm">
            <Button
              variant="secondary"
              fullWidth
              onPress={handleChangePhoto}
            >
              {t.change}
            </Button>
            <Button
              variant="primary"
              fullWidth
              onPress={handleSend}
            >
              {t.send}
            </Button>
          </div>
        </div>
      ) : (
        /* Estado: Seleccion de fuente (camara o galeria) */
        <div className="flex-1 flex flex-col items-center justify-center gap-4 max-w-sm mx-auto w-full">
          {/* Boton Camara — grande, prominente */}
          <Button
            variant="primary"
            fullWidth
            onPress={() => cameraRef.current?.click()}
            icon={
              <svg width="28" height="28" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
                <path d="M12 12m-3.2 0a3.2 3.2 0 1 0 6.4 0a3.2 3.2 0 1 0-6.4 0" />
                <path d="M9 2L7.17 4H4c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2h-3.17L15 2H9zm3 15c-2.76 0-5-2.24-5-5s2.24-5 5-5 5 2.24 5 5-2.24 5-5 5z" />
              </svg>
            }
            className="h-[72px]"
          >
            {t.camera}
          </Button>

          {/* Boton Galeria — secundario */}
          <Button
            variant="secondary"
            fullWidth
            onPress={() => galleryRef.current?.click()}
            icon={
              <svg width="28" height="28" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
                <path d="M21 19V5c0-1.1-.9-2-2-2H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2zM8.5 13.5l2.5 3.01L14.5 12l4.5 6H5l3.5-4.5z" />
              </svg>
            }
          >
            {t.gallery}
          </Button>

          {/* Cancelar — texto sutil */}
          <button
            onClick={handleCancel}
            className="mt-4 text-body-sm text-clara-text-secondary underline underline-offset-4
                       min-h-touch-sm flex items-center
                       hover:text-clara-text transition-colors duration-150
                       focus-visible:outline focus-visible:outline-[3px]
                       focus-visible:outline-clara-blue focus-visible:outline-offset-2"
          >
            {t.cancel}
          </button>
        </div>
      )}
    </div>
  );
}
