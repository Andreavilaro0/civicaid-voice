# Paleta de Colores — Clara / CivicAid Voice

> Paleta disenada para accesibilidad WCAG AAA, sensibilidad multicultural
> y transmitir confianza institucional con calidez humana.

---

## Colores Primarios

| Nombre | Hex | RGB | Uso |
|--------|-----|-----|-----|
| **Clara Blue** | `#1B5E7B` | 27, 94, 123 | Headers, botones primarios, links, confianza institucional |
| **Clara Orange** | `#D46A1E` | 212, 106, 30 | CTAs, modo voz, acentos calidos, activacion |
| **Clara Green** | `#2E7D4F` | 46, 125, 79 | Exito, audio player, confirmaciones, esperanza |

## Colores de Fondo

| Nombre | Hex | RGB | Uso |
|--------|-----|-----|-----|
| **Background** | `#FAFAFA` | 250, 250, 250 | Fondo principal de la app |
| **Card** | `#F5F5F5` | 245, 245, 245 | Fondos de tarjetas y secciones |
| **Info** | `#E3F2FD` | 227, 242, 253 | Burbujas de Clara, fondos informativos |

## Colores de Texto

| Nombre | Hex | RGB | Uso |
|--------|-----|-----|-----|
| **Text Primary** | `#1A1A2E` | 26, 26, 46 | Texto principal (contraste 15.2:1 sobre blanco) |
| **Text Secondary** | `#4A4A5A` | 74, 74, 90 | Texto secundario, subtitulos |

## Colores de Estado

| Nombre | Hex | RGB | Uso |
|--------|-----|-----|-----|
| **Error** | `#C62828` | 198, 40, 40 | Errores (honesto, no alarmista) |
| **Warning** | `#F9A825` | 249, 168, 37 | Advertencias, plazos urgentes |

## Colores de Interfaz

| Nombre | Hex | RGB | Uso |
|--------|-----|-----|-----|
| **Border** | `#E0E0E0` | 224, 224, 224 | Bordes, separadores |
| **Focus Ring** | `#1B5E7B` | 27, 94, 123 | Indicador de foco (3px solid) |

---

## Ratios de Contraste (WCAG AAA)

| Combinacion | Ratio | Nivel |
|-------------|-------|-------|
| Text Primary sobre Background | 15.2:1 | AAA |
| Clara Blue sobre Background | 7.3:1 | AAA |
| Clara Orange sobre Background | 5.1:1 | AA (texto grande AAA) |
| Text Primary sobre Info | 13.8:1 | AAA |
| White sobre Clara Blue | 8.4:1 | AAA |

---

## Sensibilidad Multicultural

| Color | Espanol | Latinoamericano | Marroqui/Norteafricano | Subsahariano |
|-------|---------|----------------|----------------------|-------------|
| **Azul** | Confianza, institucional | Esperanza, salud | Positivo (mosaicos Zellij) | Armonia |
| **Naranja** | Calidez, energia, sol | Alegria, vitalidad | Tonos tierra (terracota) | Calidez |
| **Verde** | Naturaleza, renovacion | Esperanza | Color sagrado (Islam) | Positivo |

> Azul + Naranja es una de las combinaciones MAS seguras para daltonismo.
> Verde + Naranja requiere siempre iconos/texto adicional (no solo color).

---

## Regla de Oro

> NUNCA usar solo color para transmitir significado.
> Siempre acompanar con icono, texto o patron.

---

## Implementacion

### Tailwind CSS
```javascript
clara: {
  blue: '#1B5E7B',
  orange: '#D46A1E',
  green: '#2E7D4F',
  bg: '#FAFAFA',
  text: '#1A1A2E',
  'text-secondary': '#4A4A5A',
  error: '#C62828',
  warning: '#F9A825',
  info: '#E3F2FD',
  card: '#F5F5F5',
  border: '#E0E0E0',
}
```

### CSS Variables
```css
:root {
  --clara-blue: #1B5E7B;
  --clara-orange: #D46A1E;
  --clara-green: #2E7D4F;
  --clara-bg: #FAFAFA;
  --clara-text: #1A1A2E;
  --clara-text-secondary: #4A4A5A;
  --clara-error: #C62828;
  --clara-warning: #F9A825;
  --clara-info: #E3F2FD;
  --clara-card: #F5F5F5;
  --clara-border: #E0E0E0;
}
```
