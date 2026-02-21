# Personas 3D Pipeline — Manual Guide

> **Pipeline:** Image-to-3D (Dilum Sanjaya workflow) para las 3 personas de Clara

**Goal:** Convertir Maria, Ahmed y Fatima en modelos 3D animados con idle animation para el sitio web.

**Status actual:** 3D Parallax Cards CSS implementadas como fallback inmediato. Este documento guia la creacion de modelos 3D reales cuando haya tiempo.

---

## Step 1: Generar Character Portraits (vista frontal, fondo blanco)

Ir a **https://hunyuan3d.tencent.com** o usar cualquier generador de imagenes.

### Prompts para cada personaje:

**Maria (58, Marruecos):**
```
Professional portrait photo of Maria, a 58-year-old Moroccan immigrant woman
wearing an orange-brown hijab. Warm gentle expression. Looking directly at
camera, front-facing T-pose view, upper body shot. Clean white background.
Photorealistic, high detail. Studio lighting.
```

**Ahmed (34, Senegal):**
```
Professional portrait photo of Ahmed, a 34-year-old Senegalese man with short
hair. Confident expression. Wearing a light blue collared shirt. Looking
directly at camera, front-facing T-pose view, upper body shot. Clean white
background. Photorealistic, high detail. Studio lighting.
```

**Fatima (42, Marruecos):**
```
Professional portrait photo of Fatima, a 42-year-old Moroccan immigrant woman
wearing a green hijab. Kind caring expression with warm smile. Looking directly
at camera, front-facing T-pose view, upper body shot. Clean white background.
Photorealistic, high detail. Studio lighting.
```

**Alternativas gratuitas:** Leonardo.ai, Ideogram, Playground AI, Bing Image Creator

---

## Step 2: Convertir a 3D con Hunyuan3D

1. Ir a **https://hunyuan3d.tencent.com** (gratis)
2. Subir cada portrait PNG
3. Seleccionar "Image to 3D"
4. Parametros: Quality=High, Texture=Enable
5. Descargar como **GLB**
6. Repetir para los 3 personajes

**Alternativa:** TripoSR (https://www.tripo3d.ai) — mas rapido, menos detalle

---

## Step 3: Rigging con Mixamo (opcional, para animaciones)

1. Ir a **https://www.mixamo.com** (Adobe, gratis)
2. Subir el mesh FBX (exportar desde Blender si es necesario)
3. Posicionar markers (chin, wrists, elbows, knees, groin)
4. Auto-rig
5. Seleccionar animacion "Idle" (breathing)
6. Descargar como FBX with skin
7. Convertir a GLB con Blender o gltf-transform

---

## Step 4: Optimizar para web

```bash
# Instalar gltf-transform
npm install -g @gltf-transform/cli

# Optimizar cada modelo (target: < 2MB cada uno)
npx @gltf-transform/cli optimize maria.glb maria-opt.glb --compress draco
npx @gltf-transform/cli optimize ahmed.glb ahmed-opt.glb --compress draco
npx @gltf-transform/cli optimize fatima.glb fatima-opt.glb --compress draco
```

Copiar a: `front/public/media/personas/3d/`

---

## Step 5: Integrar en el sitio

Una vez que los GLB estan listos, la integracion seria:

### Opcion A: `<model-viewer>` (mas simple)

```bash
npm install @google/model-viewer
```

```tsx
// En PersonasSection.tsx, reemplazar <img> por:
<model-viewer
  src={`/media/personas/3d/${persona.id}.glb`}
  auto-rotate
  camera-controls
  shadow-intensity="0.5"
  style={{ width: "72px", height: "72px" }}
/>
```

### Opcion B: React Three Fiber (mas control)

```bash
npm install @react-three/fiber @react-three/drei
```

```tsx
import { Canvas } from '@react-three/fiber'
import { useGLTF, useAnimations, OrbitControls } from '@react-three/drei'

function PersonaModel({ url }: { url: string }) {
  const { scene, animations } = useGLTF(url)
  const { actions } = useAnimations(animations, scene)
  useEffect(() => { actions['idle']?.play() }, [])
  return <primitive object={scene} scale={0.5} />
}

// Uso:
<Canvas style={{ width: 72, height: 72 }}>
  <ambientLight intensity={0.6} />
  <directionalLight position={[2, 2, 2]} />
  <PersonaModel url={`/media/personas/3d/${persona.id}.glb`} />
  <OrbitControls enableZoom={false} autoRotate autoRotateSpeed={2} />
</Canvas>
```

---

## Checklist

- [ ] Generar 3 character portraits (fondo blanco, vista frontal)
- [ ] Convertir a 3D en Hunyuan3D (3x GLB)
- [ ] (Opcional) Rigging + idle en Mixamo
- [ ] Optimizar con gltf-transform (< 2MB cada uno)
- [ ] Copiar a `front/public/media/personas/3d/`
- [ ] Instalar model-viewer o react-three-fiber
- [ ] Actualizar PersonasSection.tsx
- [ ] Verificar mobile performance
- [ ] Build clean

---

## Tiempo estimado

| Paso | Tiempo |
|------|--------|
| Generar portraits | 10 min |
| Hunyuan3D x3 | 15 min |
| Mixamo rig x3 | 20 min |
| Optimizar GLB | 5 min |
| Integrar codigo | 15 min |
| **Total** | **~65 min** |
