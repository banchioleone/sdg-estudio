# Sistemas de Gestión · Estudio

Sitio estático para estudiar **Sistemas de Gestión** (UTN FRRo, Ingeniería en Sistemas). Cada clase vive en su JSON y `build.py` la incrusta, junto con las láminas SVG, en un solo `index.html`. Así se abre directo en el navegador (`file://`) y también se publica en GitHub Pages, sin servidor ni dependencias.

Sitio: https://banchioleone.github.io/sdg-estudio/

## Estructura

```
index.html          entrada del sitio (la genera build.py)
build.py            incrusta content/ en index.html
.nojekyll           Pages sirve los archivos tal cual, sin Jekyll
content/
  index.json        unidades y clases, en el orden del programa
  FORMATO.md        cómo está armado el JSON de una clase
  u1/               Unidad 1, un JSON por clase
  u2/               Unidad 2, un JSON por clase
  u2/img/           láminas SVG
scripts/
  texhtml.py        fórmulas a HTML (lo usa build.py)
  mdparse.py        parser de apuntes
  gen_*.py          generadores históricos de clases (ver nota)
  audit_fix.py      ajustes puntuales de contenido (histórico)
  reorden_u2.py     orden por bloques de la U2, renombres y auditoría de textos
  siglas_historias.py  Clase 0.1: una tarjeta por sigla + tabla rápida
```

## Cómo se usa el sitio

- **Inicio** (`#/`): barra de historias (un círculo por clase; anillo de color = sin ver, gris = vista), «La materia» con las 7 unidades, su avance y cuánto cayó cada tema en finales, y un feed con una publicación por clase («Ver story» / «Leer teoría»).
- **Unidad** (`#/u2`): sus historias, láminas y clases agrupadas por bloque.
- **Clase** (`#/u2/c6`): teoría completa y el círculo de su historia.
- **Historia abierta** (`#/s/c6`): la ✕ vuelve a donde estabas. El encabezado «Sistemas de Gestión» queda fijo arriba y siempre vuelve al Inicio; el botón atrás del navegador funciona.
- Los enlaces viejos (`#c6`, `#c3a`) siguen andando, y el progreso guardado con ids viejos (`c3a`, `c2bteoria`) se migra solo.

## Orden de la Unidad 2

Introducción (0, 0.1) · Bloque A · Base estadística (1, 1.b) · Bloque B · Demanda, datos y patrones (2, 3, 3.b, 4, 4.b, Integrador) · Bloque C · Métodos de series de tiempo (5 a 10) · Bloque D · Regresión (11 a 14). El orden y los bloques viven en `content/index.json` (`blocks` en la unidad, `block` en cada clase).

**Nota sobre los generadores:** `gen_clases.py`, `gen_c0.py`, `gen_c5.py`, `gen_u2_cierre.py` y `audit_fix.py` armaron la primera versión y usan los ids y nombres viejos. No los vuelvas a correr: pisarían la teoría y las historias vigentes. El contenido se edita directo en `content/`. `gen_u2_historias.py` (4.b y 6–14) y los dos scripts nuevos sí reproducen el contenido actual.

## Agregar o editar una clase

1. Editá el JSON de la clase, o creá uno nuevo, como dice [content/FORMATO.md](content/FORMATO.md). Una clase = un archivo, adentro de la carpeta de su unidad (`content/u1/`, `content/u2/`, …).
2. Si es nueva, agregala en `content/index.json` con `"file"` y `"soon": false`.
3. Desde la raíz del repo regenerá el HTML:

```bash
python3 build.py
```

4. Commiteá el JSON (y la lámina, si sumaste una) junto con el `index.html` que salió.
