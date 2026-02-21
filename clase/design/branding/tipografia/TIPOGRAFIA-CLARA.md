# Tipografia — Clara / CivicAid Voice

> Tipografia disenada para maxima legibilidad, accesibilidad WCAG AAA,
> y comodidad para usuarios mayores y con baja alfabetizacion.

---

## Fuentes

### Display: Atkinson Hyperlegible Next
- **Creador:** Braille Institute (febrero 2025 — version Next)
- **Licencia:** Gratis, Google Fonts
- **Uso:** Titulares, logo, numeros destacados, botones principales
- **Por que:** Disenada especificamente para personas con baja vision. Caracteres con formas unicas que evitan confusion (I/l/1, O/0, etc.)
- **Pesos disponibles:** Light, Regular, Medium, SemiBold, Bold, ExtraBold (7 pesos)
- **Cobertura idiomas:** 150+ idiomas (cubre ES, FR, AR latin)
- **Variante monoespaciada:** Si (para datos/numeros)
- **Google Fonts:** `Atkinson+Hyperlegible`

### Body: Inter
- **Creador:** Rasmus Andersson
- **Licencia:** SIL Open Font License, Google Fonts
- **Uso:** Texto de cuerpo, descripciones, contenido largo
- **Por que:** Excelente legibilidad en pantalla, x-height alta, numerales tabulares
- **Pesos usados:** Regular (400), Medium (500), SemiBold (600)
- **Google Fonts:** `Inter`

---

## Escala Tipografica

| Elemento | Fuente | Peso | Tamano | Line-height | Uso |
|----------|--------|------|--------|-------------|-----|
| **H1 / Hero** | Atkinson Hyperlegible | Bold (700) | 36px | 1.2 | Titulos de pagina, hero text |
| **H2 / Section** | Atkinson Hyperlegible | Bold (700) | 28px | 1.3 | Titulos de seccion |
| **H3 / Subsection** | Atkinson Hyperlegible | SemiBold (600) | 22px | 1.4 | Subtitulos |
| **Body Large** | Inter | Regular (400) | 20px | 1.6 | Texto principal (minimo para elderly) |
| **Body** | Inter | Regular (400) | 18px | 1.6 | Texto general |
| **Body Small** | Inter | Regular (400) | 16px | 1.5 | Notas, timestamps |
| **Button** | Atkinson Hyperlegible | SemiBold (600) | 18px | 1.0 | Texto de botones |
| **Caption** | Inter | Medium (500) | 14px | 1.4 | Etiquetas, meta info |
| **Number** | Atkinson Hyperlegible | Bold (700) | 48px+ | 1.0 | Estadisticas grandes en slides |

---

## Reglas de Uso

### Accesibilidad
- **Tamano minimo de cuerpo:** 18px (20px preferido para usuarios mayores)
- **Ancho maximo de linea:** 70 caracteres (ch) para lectura comoda
- **Contraste minimo:** 7:1 texto normal (AAA), 4.5:1 texto grande (AAA)
- **Espaciado entre parrafos:** 1.5x el tamano de fuente
- **Numeros tabulares:** Activar `font-variant-numeric: tabular-nums` para tiempos/datos

### Jerarquia
- Solo 2 familias: Atkinson para impacto, Inter para lectura
- Maximo 3 pesos por pagina para evitar ruido visual
- Titulares en azul `#1B5E7B`, texto en `#1A1A2E`

### Idiomas
- **Espanol:** Atkinson e Inter cubren todos los caracteres (n, acentos)
- **Frances:** Completo (cedilla, acentos graves/agudos/circunflejos)
- **Arabe (futuro):** Requiere fuente adicional (Noto Sans Arabic recomendada)

---

## Implementacion

### Google Fonts Link
```html
<link href="https://fonts.googleapis.com/css2?family=Atkinson+Hyperlegible:ital,wght@0,400;0,700;1,400;1,700&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
```

### Next.js (next/font)
```typescript
import { Atkinson_Hyperlegible } from 'next/font/google';
import { Inter } from 'next/font/google';

const atkinson = Atkinson_Hyperlegible({
  subsets: ['latin'],
  weight: ['400', '700'],
  variable: '--font-atkinson',
  display: 'swap',
});

const inter = Inter({
  subsets: ['latin'],
  weight: ['400', '500', '600'],
  variable: '--font-inter',
  display: 'swap',
});
```

### Tailwind CSS
```javascript
fontFamily: {
  display: ['Atkinson Hyperlegible', 'system-ui', 'sans-serif'],
  body: ['Inter', 'system-ui', 'sans-serif'],
}
```

### CSS Variables
```css
:root {
  --font-display: 'Atkinson Hyperlegible', system-ui, sans-serif;
  --font-body: 'Inter', system-ui, sans-serif;
}
```
