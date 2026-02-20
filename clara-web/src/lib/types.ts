/* ================================================================== */
/*  types.ts — Contratos TypeScript para Clara                        */
/*  Fuente de verdad: src/routes/api_chat.py + src/core/models.py     */
/* ================================================================== */

/* ------------------------------------------------------------------ */
/*  Primitivos                                                        */
/* ------------------------------------------------------------------ */

/** Idiomas soportados en Fase 1 */
export type Language = "es" | "fr";

/** Modos de entrada — concepto UI (lo que el usuario elige) */
export type InputMode = "text" | "voice" | "image";

/**
 * Tipos de entrada — concepto API (lo que el backend recibe).
 * IMPORTANTE: "voice" (UI) se mapea a "audio" (API).
 * Q7 debe hacer: input_type: mode === "voice" ? "audio" : mode
 */
export type ApiInputType = "text" | "audio" | "image";

/** Quien envia el mensaje en el chat */
export type MessageSender = "clara" | "user";

/** Origenes de la respuesta del backend */
export type ResponseSource = "cache" | "llm" | "fallback" | "guardrail";

/* ------------------------------------------------------------------ */
/*  API Request / Response                                            */
/* ------------------------------------------------------------------ */

/** POST /api/chat — request body */
export interface ChatRequest {
  /**
   * Texto del usuario. Requerido para input_type="text".
   * Para audio: pasar "" — el backend transcribe con Whisper.
   * Para image: pasar descripcion o "".
   */
  text: string;
  language: Language;
  input_type: ApiInputType;
  /** Audio grabado codificado en base64. Solo cuando input_type="audio" */
  audio_base64?: string | null;
  /** Imagen de documento codificada en base64. Solo cuando input_type="image" */
  image_base64?: string | null;
  /** Identificador de sesion para continuidad de conversacion */
  session_id: string;
}

/** POST /api/chat — response body (200 OK) */
export interface ChatResponse {
  response: string;
  audio_url: string | null;
  source: ResponseSource;
  language: Language;
  duration_ms: number;
  sources: Source[];
}

/** Fuente de informacion citada por Clara */
export interface Source {
  name: string;
  url: string;
}

/** GET /api/health — response body */
export interface HealthResponse {
  status: "ok";
  features: {
    whisper: boolean;
    llm: boolean;
    guardrails: boolean;
    demo_mode: boolean;
  };
}

/* ------------------------------------------------------------------ */
/*  Estado interno del chat (UI)                                      */
/* ------------------------------------------------------------------ */

/** Contexto de carga — determina QUE mensaje y animacion mostrar */
export type LoadingContext = "listening" | "thinking" | "reading";

/**
 * Metadata para reproduccion de audio (Q8 AudioPlayer).
 * Mas rico que un simple string URL.
 */
export interface AudioPlayback {
  url: string;
  /** Duracion total en segundos (si disponible) */
  duration_s?: number;
  /** Estado de reproduccion */
  state: "idle" | "playing" | "paused";
}

/** Un mensaje en la conversacion (local, no se envia al backend) */
export interface Message {
  id: string;
  sender: MessageSender;
  text: string;
  /** Audio de la respuesta de Clara (Q8 lo renderiza) */
  audio?: AudioPlayback;
  sources?: Source[];
  timestamp: Date;
  /**
   * Contexto de carga — si presente, se muestra LoadingState en vez de texto.
   * "listening" = "Clara esta escuchando..."
   * "thinking" = "Clara esta buscando informacion..."
   * "reading" = "Clara esta leyendo tu documento..."
   */
  loading?: LoadingContext;
}

/* ------------------------------------------------------------------ */
/*  Errores tipados                                                   */
/* ------------------------------------------------------------------ */

/** Categorias de error — determina icono y estilo visual */
export type ErrorCategory = "network" | "audio" | "server" | "timeout";

/** Accion sugerida al usuario tras un error */
export type ErrorAction = "retry" | "wait" | "check_connection" | "try_text";

/** Parametros para feedback auditivo via Web Audio API */
export interface AudioFeedbackParams {
  frequency: number;
  duration: number;
  type: OscillatorType;
}
