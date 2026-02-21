# CLARA — Guion de Presentacion
## OdiseIA4Good · UDIT · Febrero 2026
## Duracion total: 6:00 minutos
## Presentadora: Andrea

---

> **NOTAS GENERALES ANTES DE EMPEZAR**
> - Habla despacio. Los silencios valen oro.
> - Cuando digas el nombre de una persona real (Maria, Ahmed, Fatima), mira al publico — no a la pantalla.
> - La demo es en vivo. Si algo falla, sonries y dices: "Esto en produccion funciona — y eso es lo que importa."
> - Tono: cercano, firme, emocionado pero contenido. No vendas. Cuenta.

---

## SLIDE 1 — GANCHO: EL MOMENTO DE MARIA
**Tiempo: 0:00 – 0:25**

*(Pausa de 2 segundos antes de hablar. Deja que la sala se calme.)*

"Maria tiene 74 anos. Vive sola en Vallecas.
Le tiemblan las manos — un poco la izquierda, mas la derecha.
Y un dia le dijeron que podia cobrar el Ingreso Minimo Vital.

Maria no sabe que es eso.
Solo sabe que cada fin de mes falta algo."

*(Pausa.)*

"Llamo a una oficina. Le dijeron que esperara.
Llamo a otra. Le dijeron que no era la correcta.
Entro en una web. No entendia las palabras.

Maria se rindio.

Y eso — eso no deberia pasar nunca."

---

## SLIDE 2 — EL PROBLEMA
**Tiempo: 0:25 – 0:45**

"En Espana hay mas de 11 millones de personas en riesgo de exclusion social.
Ayudas que existen. Derechos que estan escritos en papel.
Pero entre el papel y la persona — hay un muro.

Un muro hecho de formularios inaccesibles.
De llamadas que no contestan.
De webs que asumen que sabes leer, que tienes ordenador, que hablas espanol.

Ese muro no es culpa de nadie. Es un fallo de diseno.

Y yo vengo a cambiar el diseno."

---

## SLIDE 3 — LAS PERSONAS
**Tiempo: 0:45 – 1:30**

"Antes de contaros lo que he construido, quiero que conozcais a tres personas.

Porque Clara no existe para impresionar a un jurado.
Clara existe para ellas."

*(Cambias al slide con los tres perfiles. Senalas cada uno mientras hablas.)*

"**Maria, 74 anos.** Espanola. Le tiemblan las manos.
No puede teclear bien. No entiende los formularios.
Quiere saber si tiene derecho al IMV — y no quiere llamar a nadie mas."

*(Breve pausa.)*

"**Ahmed, 28 anos.** Lleva dos anos en Espana, viene de Senegal.
Su idioma es el frances. Necesita empadronarse — es el primer paso para todo.
Pero las instrucciones estan solo en espanol."

*(Breve pausa.)*

"**Fatima, 45 anos.** Vino de Marruecos.
Habla, pero no lee en espanol. Necesita la tarjeta sanitaria para su hijo.
No sabe por donde empezar."

*(Miras al publico.)*

"Tres personas. Tres situaciones distintas. Un problema comun:
el sistema no esta disenado para ellas.

Yo si."

---

## SLIDE 4 — LA SOLUCION: CLARA
**Tiempo: 1:30 – 2:30**

"Clara es un asistente conversacional.
Pero antes de explicaros como funciona, dejadme deciros por que importa *como* lo he hecho.

Maria no tiene smartphone de ultima generacion.
Pero si tiene WhatsApp. Como el 90% de los adultos en Espana.

Ahmed no puede escribir bien en espanol.
Pero puede hablar. Puede mandar una nota de voz.

Fatima no puede leer una respuesta larga en pantalla.
Pero si puede escuchar.

Por eso Clara vive en WhatsApp.
Por eso Clara entiende voz — gracias a Whisper, la IA de transcripcion de OpenAI.
Por eso Clara responde en espanol y en frances, y pronto en mas idiomas.
Por eso Clara puede analizar una foto de un documento y decirte que significa.

Clara no pide que las personas se adapten al sistema.
Clara se adapta a las personas."

*(Una pausa corta, deliberada.)*

"Eso es lo que llamo Civic Tenderness.
Calidez institucional. No es marketing — es una decision de diseno.
Cada palabra que Clara dice fue escrita pensando en Maria, en Ahmed, en Fatima."

---

## SLIDE 5 — DEMO: WHATSAPP
**Tiempo: 2:30 – 3:15**

*(Aqui arranca la demo en vivo. Mantente calmada. Habla mientras haces.)*

"Os voy a mostrar Clara en accion.

Imagina que eres Maria.
Abres WhatsApp — lo que ya tienes en el movil.
Escribes, o simplemente mandas una nota de voz:"

*(Envias el mensaje de voz o texto: "Hola, quiero saber si tengo derecho al Ingreso Minimo Vital")*

"Clara escucha. Transcribe. Entiende.
Y responde — no con un manual de 40 paginas, sino con lo que necesitas saber ahora."

*(Muestras la respuesta de Clara en pantalla.)*

"Fijaos en el tono. No es un chatbot corporativo.
Es alguien que te habla con respeto y con claridad.
Que te dice el siguiente paso. Solo el siguiente paso.

Porque Maria no necesita saberlo todo.
Maria necesita saber que hacer manana por la manana."

*(Si hay tiempo, muestra el caso de Ahmed con nota de voz en frances.)*

"Y si Ahmed manda su pregunta en frances — Clara responde en frances.
Sin que Ahmed tenga que pedirlo. Clara lo detecta sola."

---

## SLIDE 6 — DEMO: WEB APP
**Tiempo: 3:15 – 4:00**

"Ademas de WhatsApp, he construido una interfaz web.
Pensada para trabajadoras sociales, ONGs, mediadores comunitarios.

Personas que acompanan a usuarios como Maria todos los dias
y que ahora pueden tener a Clara como copiloto."

*(Muestras la web app brevemente.)*

"Desde aqui pueden iniciar conversaciones, revisar historiales,
y personalizar las respuestas para contextos especificos.

Porque Clara no es solo para el usuario final.
Es una herramienta para todo el ecosistema de atencion social."

---

## SLIDE 7 — ARQUITECTURA (BREVE)
**Tiempo: 4:00 – 4:45**

"Un momento rapido sobre lo que hay debajo.

He construido el backend en Python y Flask.
He desplegado todo via Twilio y Render — Clara esta viva ahora mismo, no es un prototipo.
He construido la base de conocimiento y he escrito 469 tests — si, cuatrocientos sesenta y nueve.

El motor de IA es Gemini 1.5 Flash — potente, eficiente, economico.
Whisper se encarga de convertir voz a texto.
Todo corre en Docker, y esta desplegado en produccion.

No es un demo. Es un producto."

*(Una pausa.)*

"Y tiene 469 tests porque cuando el usuario es una persona mayor que necesita informacion critica —
no puedes permitirte fallar."

---

## SLIDE 8 — IMPACTO Y ESCALABILIDAD
**Tiempo: 4:45 – 5:30**

"Hablemos de impacto real.

WhatsApp tiene 2.000 millones de usuarios en el mundo.
En Espana, el 87% de los adultos lo usa.
No necesitas descargar nada. No necesitas aprender nada nuevo.
Clara llega donde las apps no llegan.

El modelo es escalable: la base de conocimiento puede actualizarse para cualquier comunidad autonoma, para cualquier pais hispanohablante, para cualquier idioma.

Hoy ayudo a Maria con el IMV.
Manana puedo ayudar a alguien en Colombia a entender su sistema de salud.
O a alguien en un campo de refugiados a entender sus derechos.

El coste marginal de llegar a una persona mas es casi cero.
El impacto de llegar a esa persona — es enorme.

Y lo mas importante:
Clara no reemplaza a los trabajadores sociales.
Los amplifica. Les da tiempo para lo que las maquinas no pueden hacer:
el abrazo, la escucha, el acompanamiento humano."

---

## SLIDE 9 — CIERRE Y CALL TO ACTION
**Tiempo: 5:30 – 6:00**

*(Cambia el tono. Mas lento. Mas directo. Mira al jurado.)*

"Hay una cosa que me ha quedado clara en este hackathon.

La inteligencia artificial no vale nada si no llega a quien mas la necesita.

Maria no va a venir a una conferencia de tecnologia.
Ahmed no va a leer un paper sobre modelos de lenguaje.
Fatima no va a descargar una app de la App Store.

Pero si van a abrir WhatsApp manana por la manana.

Clara va a estar ahi."

*(Pausa de dos segundos.)*

"Tu voz tiene poder.
Ese es el mensaje que Clara le da a cada persona que la usa.

Y ese es el mensaje que yo
quiero dejar aqui hoy.

Soy Andrea Avila.
Soy Clara.

Y creo que la tecnologia mas poderosa del mundo
es la que hace que una persona de 74 anos
sienta que el sistema — por fin — la esta escuchando."

*(Pausa final. Sonries.)*

"Gracias."

---

## NOTAS DE PRODUCCION

### Slides recomendados (orden)
| Slide | Titulo sugerido | Visual |
|-------|----------------|--------|
| 1 | *(Solo la foto de Maria — o una imagen de manos temblorosas sobre un telefono)* | Foto evocadora, sin texto |
| 2 | "11 millones de personas. Un muro invisible." | Dato grande, fondo oscuro |
| 3 | Maria · Ahmed · Fatima | Tres columnas con foto/icono y datos clave |
| 4 | "Clara" | Logo + WhatsApp + voz + idiomas |
| 5 | Demo WhatsApp | Pantalla real del chat |
| 6 | Demo Web App | Captura de la interfaz web |
| 7 | Stack tecnico | Diagrama simple de arquitectura |
| 8 | Impacto y escala | Mapa / numeros de alcance potencial |
| 9 | "Tu voz tiene poder." | Frase sola, tipografia grande, fondo negro |

### Ensayos recomendados
- Primer ensayo: solo el texto, sin slides, cronometrado
- Segundo ensayo: con slides, practicar transiciones
- Tercer ensayo: con demo en vivo — simular un fallo y recuperarte
- Ensayo final: grabarte en video y revisar ritmo y pausas

### Palabras clave a enfatizar (voz mas lenta, mas grave)
- "Maria se rindio." — pausa despues
- "Ese muro no es culpa de nadie. Es un fallo de diseno."
- "Clara se adapta a las personas."
- "No es un demo. Es un producto."
- "Tu voz tiene poder."

### Si la demo falla
Tienes esta frase preparada:
> "La tecnologia a veces nos recuerda que somos humanos. Lo que veis aqui funciona en produccion — lo que importa es que Maria puede usarlo desde su movil ahora mismo."

---

*Guion redactado para OdiseIA4Good · UDIT · Febrero 2026*
*Clara — Andrea Avila*
