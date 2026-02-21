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
  public readonly category: ErrorCategory;
  public readonly suggestedAction: ErrorAction;

  constructor(
    public readonly status: number,
    message: string,
  ) {
    super(message);
    this.name = "ApiError";

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
