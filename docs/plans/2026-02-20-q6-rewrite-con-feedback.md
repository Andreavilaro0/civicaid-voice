# Q6 Rewrite — Incorporar Feedback de 4 Reviews

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Reescribir `docs/prompts/Q6-INTERFAZ-CHAT.md` incorporando 15 fixes de 4 reviews independientes (react-best-practices, category-design, web-typography, ux-heuristics).

**Architecture:** Editar el prompt Q6 existente seccion por seccion. Cada Task modifica una zona del archivo. No se crea codigo nuevo — se modifica el codigo DENTRO del prompt markdown. El archivo resultante es un prompt mejorado que un agente ejecutara para crear la interfaz de chat.

**Tech Stack:** Markdown (prompt), TypeScript/React (codigo dentro del prompt), Tailwind CSS (clases dentro del prompt)

---

## Mapa de Fixes

| ID | Issue | Origen | Severidad | Task |
|----|-------|--------|-----------|------|
| P0 | `addWelcome` dependency loop — cambiar idioma borra conversacion | react-best-practices | Critical | 1 |
| P1 | `formatTimestamp()` dead code — definida pero nunca usada | react-best-practices | Low | 2 |
| P2/U5 | Double-submit — `isLoading` es async, segundo tap pasa | react-best-practices + ux-heuristics | Major | 2 |
| P3/U1/U6 | `[Reintentar]` es texto, no boton. `retryLast()` nunca se llama | react-best-practices + ux-heuristics x2 | Critical | 3 |
| CD1 | Welcome como POV con villain framing | category-design | Enhancement | 4 |
| CD2 | Error messages con tono de companerismo | category-design | Enhancement | 5 |
| CD3 | Principio 8: "category moment" (primera respuesta exitosa) | category-design | Enhancement | 6 |
| T1 | Source links 14px+opacity-80 → 16px+opacity-90 | web-typography | Major | 7 |
| T2 | Mode button labels 14px → 16px | web-typography | Minor | 8 |
| T3 | Sin line-height explicito en burbujas | web-typography | Major | 7 |
| T4 | max-w-[85%] sin cap de caracteres | web-typography | Minor | 7 |
| T6 | Sin text-wrap: balance en burbujas de Clara | web-typography | Minor | 7 |
| T7 | Welcome message sin diferenciacion visual | web-typography | Minor | 4 |
| U3 | "Escribir" necesita estado activo visual | ux-heuristics | Cosmetic | 8 |
| U4 | Mode buttons no usan Button de Q3 | ux-heuristics | Minor | 8 |

---

### Task 1: Fix P0 — addWelcome Dependency Loop

**Files:**
- Modify: `docs/prompts/Q6-INTERFAZ-CHAT.md` — seccion PASO 1 (useChat.ts)

**Problema:**
`addWelcome` depende de `[language]`. El `useEffect` en `page.tsx` depende de `[addWelcome]`. Si el usuario cambia idioma via Header:
1. `language` cambia → `addWelcome` se recrea (nueva referencia)
2. `useEffect` detecta cambio en `addWelcome` → ejecuta `addWelcome()`
3. `addWelcome()` llama `setMessages([...])` → **BORRA toda la conversacion** y pone un nuevo welcome

**Step 1: Localizar el bloque `addWelcome` en useChat.ts**

Buscar en el prompt (lineas ~384-393):
```typescript
  const addWelcome = useCallback(() => {
    setMessages([
      {
        id: createId(),
        sender: "clara",
        text: welcomeMessages[language],
        timestamp: new Date(),
      },
    ]);
  }, [language]);
```

**Step 2: Reemplazar con version segura**

El fix usa un `useRef` para capturar el idioma inicial y un guard `hasWelcomed` para evitar re-ejecucion:

```typescript
  const initialLangRef = useRef<Language>(initialLang);
  const hasWelcomedRef = useRef(false);

  const addWelcome = useCallback(() => {
    if (hasWelcomedRef.current) return;
    hasWelcomedRef.current = true;
    setMessages([
      {
        id: createId(),
        sender: "clara",
        text: welcomeMessages[initialLangRef.current],
        timestamp: new Date(),
      },
    ]);
  }, []); // sin dependencias — solo se ejecuta una vez
```

**Step 3: Actualizar la tabla de decisiones del PASO 1**

Agregar fila:
```markdown
| `hasWelcomedRef` guard | Previene que cambiar idioma borre la conversacion. `addWelcome` solo se ejecuta una vez al montar | react-best-practices |
```

**Step 4: Actualizar el useEffect en page.tsx (PASO 5)**

Buscar (lineas ~1058-1060):
```typescript
  useEffect(() => {
    addWelcome();
  }, [addWelcome]);
```

Reemplazar con:
```typescript
  useEffect(() => {
    addWelcome();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []); // solo al montar — addWelcome tiene su propio guard interno
```

**Step 5: Verificar coherencia**

Confirmar que:
- `addWelcome` ya no tiene `[language]` como dependencia
- El `useEffect` tiene `[]` como dependencias
- `initialLangRef` se inicializa con `initialLang` del parametro del hook

---

### Task 2: Fix P1 + P2 — Dead Code + Double-Submit Guard

**Files:**
- Modify: `docs/prompts/Q6-INTERFAZ-CHAT.md` — seccion PASO 1 (useChat.ts)

**Step 1: Eliminar `formatTimestamp()` dead code (P1)**

Buscar y ELIMINAR (lineas ~320-325):
```typescript
function formatTimestamp(): string {
  return new Date().toLocaleTimeString([], {
    hour: "2-digit",
    minute: "2-digit",
  });
}
```

Los timestamps se formatean en MessageList via `msg.timestamp.toLocaleTimeString()`. Esta funcion no se usa en ningun lugar.

**Step 2: Agregar `isSendingRef` para double-submit guard (P2/U5)**

Despues de `lastRequestRef`, agregar:
```typescript
  const isSendingRef = useRef(false);
```

**Step 3: Agregar guard al inicio de `send()`**

Buscar el inicio de la funcion `send`:
```typescript
  const send = useCallback(
    async (text: string, audioBase64?: string, imageBase64?: string) => {
      // Guardar request para posible retry
      lastRequestRef.current = { text, audioBase64, imageBase64 };
```

Reemplazar con:
```typescript
  const send = useCallback(
    async (text: string, audioBase64?: string, imageBase64?: string) => {
      // Guard sincronico contra double-submit (Maria tiene temblor en las manos)
      if (isSendingRef.current) return;
      isSendingRef.current = true;

      // Guardar request para posible retry
      lastRequestRef.current = { text, audioBase64, imageBase64 };
```

**Step 4: Reset del guard en `finally`**

Buscar:
```typescript
    } finally {
      setIsLoading(false);
    }
```

Reemplazar con:
```typescript
    } finally {
      setIsLoading(false);
      isSendingRef.current = false;
    }
```

**Step 5: Actualizar tabla de decisiones del PASO 1**

Agregar filas:
```markdown
| `isSendingRef` sincronico | `setState` es async — segundo tap de Maria llega antes del re-render. `useRef` es sincronico = bloqueo inmediato | react-best-practices |
| Eliminar `formatTimestamp()` | Dead code: timestamps se formatean en MessageList. No hay consumidores | DRY |
```

---

### Task 3: Fix P3/U1/U6 — Error Rendering como Boton Real

**Files:**
- Modify: `docs/prompts/Q6-INTERFAZ-CHAT.md` — seccion PASO 1 (useChat.ts) + PASO 3 (MessageList.tsx)

**Problema:**
El error se renderiza como texto plano:
```typescript
text: `${errorText}\n\n[${actionLabel}]`,
```
El `[Reintentar]` parece texto, no es clickeable, y `retryLast()` existe en el hook pero NADA en la UI lo llama. Maria ve "Reintentar" entre corchetes y no sabe que hacer.

**Step 1: Agregar campo `error` a la interfaz Message**

Primero, en la seccion CONTEXTO TECNICO, dentro del bloque de `Message` interface, agregar:

```typescript
interface Message {
  id: string; sender: MessageSender; text: string;
  audio?: AudioPlayback; sources?: Source[]; timestamp: Date;
  loading?: LoadingContext;
  error?: {                    // NUEVO — estructura para error actionable
    action: ErrorAction;
    actionLabel: string;
  };
}
```

> **Nota:** Esto requiere que Q5 actualice `types.ts` para agregar el campo `error` a `Message`. Agregar una nota al principio del prompt indicando esta dependencia.

**Step 2: Modificar el catch en `send()` de useChat.ts**

Buscar (lineas ~462-490):
```typescript
      } catch (error) {
        // Error → burbuja de Clara con mensaje humano
        let errorText: string;
        let errorAction: ErrorAction = "retry";
        let actionLabel: string;

        if (error instanceof ApiError) {
          const errInfo = getErrorMessage(error, language);
          errorText = errInfo.message;
          errorAction = errInfo.action;
          actionLabel = errInfo.actionLabel;
        } else {
          errorText =
            language === "fr"
              ? "Quelque chose s'est mal passe. Reessaie."
              : "Algo ha salido mal. Intenta de nuevo.";
          actionLabel = language === "fr" ? "Reessayer" : "Reintentar";
        }

        const errorMsg: Message = {
          id: createId(),
          sender: "clara",
          text: `${errorText}\n\n[${actionLabel}]`,
          timestamp: new Date(),
        };
```

Reemplazar con:
```typescript
      } catch (err) {
        // Error → burbuja de Clara con mensaje humano y boton de accion
        let errorText: string;
        let errorAction: ErrorAction = "retry";
        let actionLabel: string;

        if (err instanceof ApiError) {
          const errInfo = getErrorMessage(err, language);
          errorText = errInfo.message;
          errorAction = errInfo.action;
          actionLabel = errInfo.actionLabel;
        } else {
          errorText =
            language === "fr"
              ? "Desolee, quelque chose s'est mal passe."
              : "Perdona, algo no ha ido bien. Sigo aqui contigo.";
          actionLabel = language === "fr" ? "Reessayer" : "Reintentar";
        }

        const errorMsg: Message = {
          id: createId(),
          sender: "clara",
          text: errorText,
          timestamp: new Date(),
          error: { action: errorAction, actionLabel },
        };
```

Cambios clave:
- `error` renombrado a `err` para no colisionar con el tipo `Error`
- `text` ya NO incluye `[actionLabel]` — el texto y la accion son datos separados
- Nuevo campo `error: { action, actionLabel }` con datos estructurados
- Tono companero: "Sigo aqui contigo" (category-design)

**Step 3: Agregar renderizado de error action en MessageList.tsx**

En la seccion PASO 3 (MessageList.tsx), buscar el bloque de renderizado dentro de `<ChatBubble>`:
```typescript
          <ChatBubble
            key={msg.id}
            sender={msg.sender}
            timestamp={msg.timestamp.toLocaleTimeString([], {
              hour: "2-digit",
              minute: "2-digit",
            })}
          >
            {/* Texto del mensaje */}
            <p className="whitespace-pre-wrap">{msg.text}</p>
```

Despues del `<p>` del texto, agregar el bloque de error action:
```typescript
            {/* Texto del mensaje */}
            <p className="whitespace-pre-wrap">{msg.text}</p>

            {/* Boton de accion en errores — REAL button, no texto */}
            {msg.error && (
              <button
                onClick={onRetry}
                className="mt-3 px-4 py-2 bg-clara-blue text-white rounded-lg
                           text-label font-medium min-h-touch-sm
                           hover:bg-[#164d66] transition-colors duration-150
                           focus:outline focus:outline-[3px] focus:outline-clara-blue focus:outline-offset-2"
              >
                {msg.error.actionLabel}
              </button>
            )}
```

**Step 4: Agregar prop `onRetry` a MessageListProps**

Buscar:
```typescript
interface MessageListProps {
  messages: Message[];
  language: Language;
  getLoadingMessage: (context: LoadingContext) => string;
}
```

Reemplazar con:
```typescript
interface MessageListProps {
  messages: Message[];
  language: Language;
  getLoadingMessage: (context: LoadingContext) => string;
  onRetry: () => void;
}
```

**Step 5: Pasar `retryLast` desde page.tsx**

En PASO 5 (chat/page.tsx), buscar:
```typescript
      <MessageList
        messages={messages}
        language={language}
        getLoadingMessage={getLoadingMessage}
      />
```

Reemplazar con:
```typescript
      <MessageList
        messages={messages}
        language={language}
        getLoadingMessage={getLoadingMessage}
        onRetry={retryLast}
      />
```

Y agregar `retryLast` al destructuring del hook:
```typescript
  const {
    messages,
    isLoading,
    language,
    setLanguage,
    send,
    addWelcome,
    retryLast,
    getLoadingMessage,
  } = useChat(initialLang);
```

**Step 6: Actualizar tablas de decisiones**

PASO 1 tabla:
```markdown
| Error como dato estructurado, no texto | `msg.error = { action, actionLabel }` permite renderizar un BOTON real. `[Reintentar]` como texto plano no es clickeable — Maria no sabe que es una accion | ux-heuristics (H9) |
```

PASO 3 tabla:
```markdown
| `onRetry` como prop | MessageList no importa logica de retry — solo la invoca. Separation of concerns. El boton llama `retryLast()` del hook via prop | react-best-practices |
| Boton `min-h-touch-sm` con focus ring | Touch target accesible (48px). Focus visible para teclado. Clara blue para consistencia con boton de envio | WCAG + brand |
```

---

### Task 4: Rewrite Welcome Message — POV + Diferenciacion Visual

**Files:**
- Modify: `docs/prompts/Q6-INTERFAZ-CHAT.md` — seccion PASO 1 (useChat.ts, `welcomeMessages`)

**Step 1: Reemplazar `welcomeMessages` con version POV**

Buscar (lineas ~331-334):
```typescript
const welcomeMessages: Record<Language, string> = {
  es: "Hola, soy Clara. Estoy aqui para ayudarte con tramites en Espana. Puedes hablarme o escribirme en tu idioma.\n\nPuedo informarte sobre:\n- Ingreso Minimo Vital\n- Empadronamiento\n- Tarjeta sanitaria\n- Y mas tramites",
  fr: "Bonjour, je suis Clara. Je suis la pour t'aider avec les demarches en Espagne. Tu peux me parler ou m'ecrire dans ta langue.\n\nJe peux t'informer sur :\n- Revenu Minimum Vital\n- Inscription municipale\n- Carte sanitaire\n- Et d'autres demarches",
};
```

Reemplazar con (framing del villano — category-design):
```typescript
const welcomeMessages: Record<Language, string> = {
  es: "Hola, soy Clara.\n\nLos tramites no deberian ser tan complicados. Estoy aqui para ayudarte a entenderlos, paso a paso, en tu idioma.\n\nPreguntame sobre el Ingreso Minimo Vital, el empadronamiento, la tarjeta sanitaria, o lo que necesites.",
  fr: "Bonjour, je suis Clara.\n\nLes demarches ne devraient pas etre si compliquees. Je suis la pour t'aider a les comprendre, etape par etape, dans ta langue.\n\nDemande-moi sur le Revenu Minimum Vital, l'inscription municipale, la carte sanitaire, ou ce dont tu as besoin.",
};
```

Cambios:
- **Villain framing:** "Los tramites no deberian ser tan complicados" — el enemigo es la burocracia, no la persona (category-design)
- **Eliminado "Y mas tramites"** — vago, crea pregunta (ux-heuristics U2)
- **"paso a paso, en tu idioma"** — refuerza la propuesta de valor
- **Sin bullet list** — prosa fluida en lugar de formato tipo FAQ

**Step 2: Agregar nota de diferenciacion visual del welcome (T7)**

Despues del bloque `welcomeMessages`, agregar un comentario y nota en la tabla de decisiones:

```markdown
| Welcome como POV | "Los tramites no deberian ser tan complicados" enmarca el villano (burocracia). Clara no lista features — declara una posicion. El primer mensaje define la categoria | category-design |
| Primer `\n\n` separa saludo de POV | "Hola, soy Clara" en la primera linea. La segunda linea es el statement del villano. Estructura: nombre → posicion → invitacion | web-typography |
```

Y agregar en MessageList.tsx una clase especial para el primer mensaje:
```typescript
            {/* Texto del mensaje — welcome usa font-display para saludo */}
            <p className={`whitespace-pre-wrap leading-relaxed ${
              msg.sender === "clara" && msg.text.startsWith("Hola") ? "first-line:font-display first-line:font-bold" : ""
            }`}>
              {msg.text}
            </p>
```

> **Nota:** `first-line:font-display` es un plugin de Tailwind que puede no existir. Alternativa: separar el saludo como span. Dejar como nota para el implementador.

---

### Task 5: Error Tone — Companerismo (Category-Design)

**Files:**
- Modify: `docs/prompts/Q6-INTERFAZ-CHAT.md` — seccion PASO 1 (useChat.ts, fallback errors)

**Step 1: Actualizar mensajes de error fallback**

Ya hecho parcialmente en Task 3 Step 2. Verificar que el fallback generico dice:
```typescript
          errorText =
            language === "fr"
              ? "Desolee, quelque chose s'est mal passe."
              : "Perdona, algo no ha ido bien. Sigo aqui contigo.";
```

**Step 2: Agregar nota en la seccion PRINCIPIOS DE DISENO**

Despues del Principio 4 ("Los errores son conversaciones"), agregar tono:

```markdown
El tono de los errores refuerza que Clara es una **companera, no un sistema**:
- "Perdona, algo no ha ido bien. Sigo aqui contigo." (no "Error 500")
- "No he podido conectarme. Revisa tu wifi y vuelve a intentarlo." (no "ECONNREFUSED")
- "Necesito un momento. Intenta de nuevo en unos segundos." (no "Timeout")

Clara nunca se disculpa con lenguaje corporativo ("Lamentamos las molestias"). Clara habla como una persona que realmente quiere ayudar.
```

---

### Task 6: Agregar Principio 8 — Category Moment

**Files:**
- Modify: `docs/prompts/Q6-INTERFAZ-CHAT.md` — seccion PRINCIPIOS DE DISENO

**Step 1: Agregar despues del Principio 7**

```markdown
**8. La primera respuesta exitosa es el "category moment":**
La primera vez que Clara responde con informacion util — con fuentes, con claridad, quizas con audio — es el momento donde Maria pasa de "otro chatbot" a "esto me sirve". Este momento debe sentirse **completo**: texto legible, fuentes citadas visibles, boton de audio presente (aunque sea stub). La burbuja de respuesta no es solo informacion — es la promesa cumplida de "los tramites no deberian ser tan complicados, y mira: acabo de demostrartelo". Cada componente de la burbuja (texto + fuentes + audio) trabaja junto para crear esa sensacion de "esto es para mi".
```

**Step 2: Agregar a la tabla de Nielsen en PASO 8**

Agregar fila en la tabla de Nielsen:
```markdown
| 6 | Recognition rather than recall | La primera respuesta muestra TODO lo que Clara puede hacer (texto + fuentes + audio). Maria no tiene que adivinar — lo ve. |
```

---

### Task 7: Fix Typography en MessageList — T1, T3, T4, T6

**Files:**
- Modify: `docs/prompts/Q6-INTERFAZ-CHAT.md` — seccion PASO 3 (MessageList.tsx)

**Step 1: Fix T3 — Agregar `leading-relaxed` al texto de burbujas**

Buscar:
```typescript
            <p className="whitespace-pre-wrap">{msg.text}</p>
```

Reemplazar con:
```typescript
            <p className="whitespace-pre-wrap leading-relaxed">{msg.text}</p>
```

`leading-relaxed` = `line-height: 1.625`. Clara envia respuestas de 4-6 lineas con listas. Sin line-height explicito, el texto se siente apretado para Maria.

**Step 2: Fix T1 — Source links de 14px a 16px**

Buscar:
```typescript
              <p className="text-[14px] mt-2 opacity-80">
```

Reemplazar con:
```typescript
              <p className="text-label mt-2 text-clara-text-secondary">
```

Cambios:
- `text-[14px]` → `text-label` (16px) — cumple minimo tipografico
- `opacity-80` → `text-clara-text-secondary` — usa token de color, mejor contraste

**Step 3: Fix T6 — `text-wrap: balance` en burbujas de Clara**

Buscar el `<p>` del texto (ya modificado en Step 1):
```typescript
            <p className="whitespace-pre-wrap leading-relaxed">{msg.text}</p>
```

Reemplazar con:
```typescript
            <p className={`whitespace-pre-wrap leading-relaxed ${
              msg.sender === "clara" ? "text-wrap-balance" : ""
            }`}>
              {msg.text}
            </p>
```

> **Nota:** `text-wrap: balance` es CSS nativo (Chrome 114+, Firefox 121+). Si Tailwind no tiene clase `text-wrap-balance`, usar `style={{ textWrap: "balance" }}` o agregar utilidad custom. Verificar soporte en el tailwind.config.

Alternativa mas simple si `text-wrap: balance` no esta en Tailwind:
```typescript
            <p
              className="whitespace-pre-wrap leading-relaxed"
              style={msg.sender === "clara" ? { textWrap: "balance" } : undefined}
            >
              {msg.text}
            </p>
```

**Step 4: Fix T4 — Cap de caracteres en burbujas**

Esto es un cambio en ChatBubble (Q3), NO en Q6. Agregar una **nota al implementador** en la seccion RESTRICCIONES:

```markdown
> **Nota para implementador (T4):** ChatBubble de Q3 usa `max-w-[85%]`. En pantallas anchas (tablet/desktop), esto puede crear lineas de 80+ caracteres. Considerar agregar `max-w-prose` (65ch) como cap adicional: `max-w-[min(85%,_65ch)]`. Este cambio va en Q3, no en Q6.
```

**Step 5: Actualizar tabla de decisiones del PASO 3**

Agregar filas:
```markdown
| `leading-relaxed` en `<p>` | Line-height 1.625 para respuestas de Clara de 4-6 lineas. Sin esto, el texto se siente apretado para ojos de 74 anos | web-typography |
| `text-label` en fuentes | 16px minimo para texto funcional. 14px con opacity-80 no cumple contraste para Maria | web-typography (WCAG) |
| `text-wrap: balance` en Clara | Evita palabras huerfanas en la ultima linea. Detalle de craft que hace cada respuesta mas compuesta | web-typography |
```

---

### Task 8: Fix ChatInput — T2, U4, U3

**Files:**
- Modify: `docs/prompts/Q6-INTERFAZ-CHAT.md` — seccion PASO 4 (ChatInput.tsx)

**Step 1: Fix T2 — Mode button labels de 14px a 16px**

Buscar todas las instancias (hay 3):
```typescript
          <span className="text-[14px] mt-1">{l.write}</span>
```
```typescript
          <span className="text-[14px] mt-1">{l.voice}</span>
```
```typescript
          <span className="text-[14px] mt-1">{l.photo}</span>
```

Reemplazar TODAS con `text-label`:
```typescript
          <span className="text-label mt-1">{l.write}</span>
```
```typescript
          <span className="text-label mt-1">{l.voice}</span>
```
```typescript
          <span className="text-label mt-1">{l.photo}</span>
```

`text-label` = 16px. Los labels de modo son texto funcional — Maria necesita leerlos para entender sus opciones.

**Step 2: Fix U3 — Estado activo en boton "Escribir"**

Actualmente los 3 botones de modo se ven iguales (excepto Voz con naranja). "Escribir" deberia indicar que es el modo ACTIVO actual.

Agregar prop `activeMode` a ChatInputProps:
```typescript
interface ChatInputProps {
  onSendText: (text: string) => void;
  onStartVoice: () => void;
  onOpenCamera: () => void;
  disabled: boolean;
  language: Language;
  activeMode?: "text" | "voice" | "photo"; // NUEVO — modo activo actual
}
```

Default: `activeMode = "text"`.

Modificar el boton Escribir para mostrar estado activo:
```typescript
        <button
          type="button"
          onClick={() => inputRef.current?.focus()}
          disabled={disabled}
          aria-label={l.write}
          aria-pressed={activeMode === "text"}
          className={`flex flex-col items-center justify-center min-w-touch min-h-touch rounded-xl
                     border-2 transition-colors duration-150
                     disabled:opacity-50 disabled:cursor-not-allowed
                     ${activeMode === "text"
                       ? "border-clara-blue text-clara-blue bg-clara-blue/5 font-medium"
                       : "border-clara-border text-clara-text-secondary hover:border-clara-blue hover:text-clara-blue"
                     }`}
        >
```

El modo activo tiene:
- `border-clara-blue` — borde azul
- `bg-clara-blue/5` — fondo muy sutil
- `font-medium` — texto semi-bold
- `aria-pressed="true"` — accesibilidad

**Step 3: Fix U4 — Nota sobre Button de Q3**

Los mode buttons no usan el componente `Button` de Q3 porque `Button` no soporta layout `flex-col` (icono arriba, texto abajo). Esto es aceptable si documentamos la decision.

Agregar en la tabla de decisiones del PASO 4:
```markdown
| Mode buttons con `<button>` raw, no `Button` Q3 | `Button` de Q3 es `flex-row` (icono + texto horizontal). Los mode buttons son `flex-col` (icono arriba + texto abajo). Forzar Button Q3 requeriria `variant="custom"` que no existe. Decision: botones raw con clases consistentes con el design system | ux-heuristics + pragmatismo |
| `aria-pressed` en modo activo | Screen reader anuncia "Escribir, presionado" — Maria con lector de pantalla sabe que modo esta activo | WCAG 4.1.2 |
```

---

### Task 9: Actualizar Checklists y Definition of Done

**Files:**
- Modify: `docs/prompts/Q6-INTERFAZ-CHAT.md` — secciones PASO 8 y DEFINICION DE TERMINADO

**Step 1: Agregar items a checklist de accesibilidad**

En la seccion "Checklist de accesibilidad (22 puntos)", agregar:
```markdown
- [ ] Line-height `leading-relaxed` (1.625) en texto de burbujas
- [ ] Source links en `text-label` (16px), no 14px
- [ ] Mode button labels en `text-label` (16px), no 14px
- [ ] Error action es boton real con `min-h-touch-sm`, no texto plano
- [ ] `aria-pressed` en boton de modo activo
```

Total: 27 puntos (antes 22).

**Step 2: Agregar items a checklist de marca**

En la seccion "Checklist de marca (6 puntos)", agregar:
```markdown
- [ ] Welcome message enmarca el villano ("Los tramites no deberian..."), no lista features
- [ ] Errores con tono de companerismo ("Sigo aqui contigo"), no corporativo
- [ ] Primera respuesta exitosa se siente completa (texto + fuentes + audio stub)
```

Total: 9 puntos (antes 6).

**Step 3: Actualizar Definition of Done**

En la seccion DEFINICION DE TERMINADO, agregar al final de "Verificaciones":
```markdown
- [ ] P0 fix verificado: cambiar idioma NO borra la conversacion
- [ ] P2 fix verificado: tap rapido doble NO envia mensaje duplicado
- [ ] P3 fix verificado: error muestra boton real "Reintentar" (no texto plano)
- [ ] T1 fix verificado: source links son 16px legibles
- [ ] T3 fix verificado: texto en burbujas tiene line-height 1.625
```

**Step 4: Agregar seccion de NOTAS PARA Q5**

Al final del prompt, antes de "Siguiente:", agregar:
```markdown
> **Dependencia Q5:** Este Q requiere que `Message` en `types.ts` tenga campo opcional `error?: { action: ErrorAction; actionLabel: string }`. Si Q5 no lo incluye, el implementador debe agregarlo a `types.ts` como primer paso antes de useChat.
```

---

## Resumen de Cambios por Archivo (dentro del prompt)

| Archivo en el prompt | Cambios |
|---------------------|---------|
| **useChat.ts** | Fix addWelcome (P0), eliminar formatTimestamp (P1), agregar isSendingRef (P2), error como dato estructurado (P3), welcome POV (CD1), error tone (CD2) |
| **MessageList.tsx** | Agregar `onRetry` prop (P3), boton error real (U1/U6), leading-relaxed (T3), source links 16px (T1), text-wrap balance (T6) |
| **ChatInput.tsx** | Mode labels 16px (T2), activeMode prop (U3), aria-pressed (U3) |
| **chat/page.tsx** | Fix useEffect deps (P0), pasar retryLast a MessageList (P3) |
| **Principios** | Agregar Principio 8 (CD3), tono de errores (CD2) |
| **Checklists** | +5 accesibilidad, +3 marca, +5 verificaciones |

---

## Orden de Ejecucion

```
Task 1 (P0) → Task 2 (P1+P2) → Task 3 (P3) → Task 4 (CD1) → Task 5 (CD2) → Task 6 (CD3) → Task 7 (T1-T6) → Task 8 (T2+U3+U4) → Task 9 (checklists)
```

Cada task es independiente a nivel de seccion del prompt, pero el orden respeta dependencias logicas (fix bugs criticos primero, luego enhancements, luego documentacion).
