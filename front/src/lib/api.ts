/* ================================================================== */
/*  api.ts — Cliente HTTP para el backend Flask de Clara              */
/*  Fuente: POST /api/chat, GET /api/health (src/routes/api_chat.py)  */
/* ================================================================== */

import { API_BASE_URL, API_TIMEOUT_MS } from "./constants";
import type {
  ChatRequest,
  ChatResponse,
  HealthResponse,
  Language,
  ErrorCategory,
  ErrorAction,
} from "./types";

/* ------------------------------------------------------------------ */
/*  Error tipado                                                      */
/* ------------------------------------------------------------------ */

/**
 * Error de API con codigo HTTP, categoria y accion sugerida.
 *
 * Codigos conocidos del backend:
 * - 400: "text or audio_base64 required"
 * - 422: "audio_transcription_failed"
 * - 500: "audio_processing_error"
 * - 0: error de red / timeout (fetch fallo)
 */
export class ApiError extends Error {
  readonly status: number;
  readonly category: ErrorCategory;
  readonly suggestedAction: ErrorAction;

  constructor(status: number, message: string) {
    super(message);
    this.name = "ApiError";
    this.status = status;

    // Clasificar automaticamente
    if (status === 0) {
      this.category = message === "request_timeout" ? "timeout" : "network";
      this.suggestedAction = message === "request_timeout" ? "wait" : "check_connection";
    } else if (status === 422) {
      this.category = "audio";
      this.suggestedAction = "try_text";
    } else {
      this.category = "server";
      this.suggestedAction = "retry";
    }
  }
}

/* ------------------------------------------------------------------ */
/*  Fetch con timeout                                                 */
/* ------------------------------------------------------------------ */

async function fetchWithTimeout(
  url: string,
  options: RequestInit,
  timeoutMs: number = API_TIMEOUT_MS,
): Promise<Response> {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), timeoutMs);

  try {
    return await fetch(url, { ...options, signal: controller.signal });
  } catch (error) {
    if (error instanceof DOMException && error.name === "AbortError") {
      throw new ApiError(0, "request_timeout");
    }
    throw new ApiError(0, "network_error");
  } finally {
    clearTimeout(timer);
  }
}

/* ------------------------------------------------------------------ */
/*  Funciones publicas — API                                          */
/* ------------------------------------------------------------------ */

/**
 * Envia un mensaje al backend de Clara.
 *
 * @example
 * const response = await sendMessage({
 *   text: "Que es el IMV?",
 *   language: "es",
 *   input_type: "text",
 *   session_id: "web_m2k8f_a7x3",
 * });
 */
export async function sendMessage(
  request: ChatRequest,
): Promise<ChatResponse> {
  const res = await fetchWithTimeout(`${API_BASE_URL}/api/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(request),
  });

  if (!res.ok) {
    const body = await res.json().catch(() => ({ error: "unknown_error" }));
    throw new ApiError(res.status, body.error || "request_failed");
  }

  // Defensive: guard against proxy/CDN returning 200 with non-JSON
  try {
    return await res.json();
  } catch {
    throw new ApiError(200, "invalid_response");
  }
}

/**
 * Verifica el estado del backend y sus features habilitadas.
 *
 * @example
 * const health = await checkHealth();
 * if (health.features.whisper) { /* voz disponible *\/ }
 */
export async function checkHealth(): Promise<HealthResponse> {
  const res = await fetchWithTimeout(
    `${API_BASE_URL}/api/health`,
    { method: "GET" },
    5_000,
  );

  if (!res.ok) {
    throw new ApiError(res.status, "health_check_failed");
  }

  try {
    return await res.json();
  } catch {
    throw new ApiError(200, "invalid_response");
  }
}

/* ------------------------------------------------------------------ */
/*  Helpers publicos                                                  */
/* ------------------------------------------------------------------ */

/**
 * Genera un session ID unico y legible.
 * Patron: web_{timestamp_base36}_{random_4chars}
 *
 * @example generateSessionId() // "web_m2k8f_a7x3"
 */
export function generateSessionId(): string {
  const timestamp = Date.now().toString(36);
  const random = Math.random().toString(36).slice(2, 6);
  return `web_${timestamp}_${random}`;
}

/**
 * Resuelve audio_url del backend a URL completa.
 * Maneja: null, URL relativa, URL absoluta.
 *
 * @example
 * resolveAudioUrl(null)                    // null
 * resolveAudioUrl("/static/cache/imv.mp3") // "http://localhost:5000/static/cache/imv.mp3"
 * resolveAudioUrl("https://cdn.example/a") // "https://cdn.example/a"
 */
export function resolveAudioUrl(audioUrl: string | null): string | null {
  if (!audioUrl) return null;
  if (audioUrl.startsWith("http")) return audioUrl;
  return `${API_BASE_URL}${audioUrl}`;
}

/**
 * Genera audio TTS desde el backend (misma voz Gemini que WhatsApp).
 * Llama a POST /api/tts — el backend usa el cascade ElevenLabs → Gemini → gTTS.
 *
 * @example
 * const url = await generateTTS("Hola, soy Clara", "es");
 * if (url) new Audio(url).play();
 */
export async function generateTTS(
  text: string,
  language: Language,
): Promise<string | null> {
  try {
    const res = await fetchWithTimeout(
      `${API_BASE_URL}/api/tts`,
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text, language }),
      },
      15_000,
    );

    if (!res.ok) return null;
    const data = await res.json();
    return resolveAudioUrl(data.audio_url);
  } catch {
    return null;
  }
}

/**
 * Traduce un ApiError a mensaje humano en el idioma del usuario.
 * Q6 llama esto en el catch de sendMessage().
 *
 * @example
 * catch (error) {
 *   if (error instanceof ApiError) {
 *     showError(getErrorMessage(error, currentLang));
 *   }
 * }
 */
export function getErrorMessage(
  error: ApiError,
  lang: Language,
): { message: string; action: ErrorAction; actionLabel: string } {
  const messages: Record<Language, Record<ErrorCategory, {
    message: string;
    actionLabel: string;
  }>> = {
    es: {
      network: {
        message: "Parece que no hay conexion. Revisa tu wifi o datos moviles.",
        actionLabel: "Reintentar",
      },
      timeout: {
        message: "Esta tardando mas de lo normal. Un momento...",
        actionLabel: "Esperar",
      },
      audio: {
        message: "No he podido entender el audio. Puedes repetir o escribir?",
        actionLabel: "Escribir",
      },
      server: {
        message: "Algo ha salido mal. Intenta de nuevo.",
        actionLabel: "Reintentar",
      },
    },
    en: {
      network: {
        message: "It seems there's no connection. Check your wifi or mobile data.",
        actionLabel: "Retry",
      },
      timeout: {
        message: "This is taking longer than usual. One moment...",
        actionLabel: "Wait",
      },
      audio: {
        message: "I couldn't understand the audio. Can you repeat or type?",
        actionLabel: "Type",
      },
      server: {
        message: "Something went wrong. Try again.",
        actionLabel: "Retry",
      },
    },
    fr: {
      network: {
        message: "Il semble qu'il n'y ait pas de connexion. Verifie ton wifi.",
        actionLabel: "Reessayer",
      },
      timeout: {
        message: "Cela prend plus de temps que prevu. Un moment...",
        actionLabel: "Attendre",
      },
      audio: {
        message: "Je n'ai pas pu comprendre l'audio. Peux-tu repeter ou ecrire?",
        actionLabel: "Ecrire",
      },
      server: {
        message: "Quelque chose s'est mal passe. Reessaie.",
        actionLabel: "Reessayer",
      },
    },
    pt: {
      network: {
        message: "Parece que não há conexão. Verifica o teu wifi ou dados móveis.",
        actionLabel: "Tentar novamente",
      },
      timeout: {
        message: "Está a demorar mais do que o normal. Um momento...",
        actionLabel: "Esperar",
      },
      audio: {
        message: "Não consegui entender o áudio. Podes repetir ou escrever?",
        actionLabel: "Escrever",
      },
      server: {
        message: "Algo correu mal. Tenta novamente.",
        actionLabel: "Tentar novamente",
      },
    },
    ro: {
      network: {
        message: "Se pare că nu există conexiune. Verifică wifi-ul sau datele mobile.",
        actionLabel: "Reîncearcă",
      },
      timeout: {
        message: "Durează mai mult decât de obicei. Un moment...",
        actionLabel: "Așteaptă",
      },
      audio: {
        message: "Nu am putut înțelege audio-ul. Poți repeta sau scrie?",
        actionLabel: "Scrie",
      },
      server: {
        message: "Ceva nu a mers bine. Încearcă din nou.",
        actionLabel: "Reîncearcă",
      },
    },
    ca: {
      network: {
        message: "Sembla que no hi ha connexió. Revisa el teu wifi o dades mòbils.",
        actionLabel: "Reintentar",
      },
      timeout: {
        message: "Està trigant més del normal. Un moment...",
        actionLabel: "Esperar",
      },
      audio: {
        message: "No he pogut entendre l'àudio. Pots repetir o escriure?",
        actionLabel: "Escriure",
      },
      server: {
        message: "Alguna cosa ha anat malament. Torna-ho a provar.",
        actionLabel: "Reintentar",
      },
    },
    zh: {
      network: {
        message: "似乎没有网络连接。请检查你的WiFi或移动数据。",
        actionLabel: "重试",
      },
      timeout: {
        message: "这比平常花费的时间更长。请稍等...",
        actionLabel: "等待",
      },
      audio: {
        message: "我无法理解音频。你能重复一遍或者打字吗？",
        actionLabel: "打字",
      },
      server: {
        message: "出了点问题。请再试一次。",
        actionLabel: "重试",
      },
    },
    ar: {
      network: {
        message: "يبدو أنه لا يوجد اتصال. تحقق من الواي فاي أو بيانات الهاتف.",
        actionLabel: "إعادة المحاولة",
      },
      timeout: {
        message: "يستغرق الأمر وقتاً أطول من المعتاد. لحظة...",
        actionLabel: "انتظار",
      },
      audio: {
        message: "لم أتمكن من فهم الصوت. هل يمكنك الإعادة أو الكتابة؟",
        actionLabel: "كتابة",
      },
      server: {
        message: "حدث خطأ ما. حاول مرة أخرى.",
        actionLabel: "إعادة المحاولة",
      },
    },
  };

  const display = messages[lang][error.category];
  return {
    message: display.message,
    action: error.suggestedAction,
    actionLabel: display.actionLabel,
  };
}
