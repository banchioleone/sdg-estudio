# Formato de contenido

Una clase = un JSON. El índice lista unidades y clases en orden. `build.py` (en la raíz del repo) incrusta los JSON y las láminas SVG en `index.html`, para que funcione también abriendo el archivo en el navegador (`file://`, sin `fetch` y sin KaTeX).

## Archivos

- `content/index.json` — unidades y clases, en el orden del programa. Una unidad puede traer `lede` y `laminas` (página de la unidad).
- `content/u2/clase01.json`, `clase01b.json`, `clase02.json`, … — una clase cada uno.
- `content/u2/img/` — láminas SVG oficiales.

Para agregar una clase: creá el JSON (o generalo desde el apunte con `scripts/gen_clases.py`), agregala en `index.json` con `"file"` y `"soon": false`, y desde la raíz del repo corré:

```bash
python3 build.py
```

Sale `index.html` en la raíz.

## `index.json`

Cada clase: `id`, `title`, `file` (si está cargada), `soon`, `visto` (ya la vimos en el estudio), `name`.

Las láminas generales de la unidad (mapa, árbol decisorio) van en `units[].laminas`.

## Una clase

Campos: `id`, `unitId`, `unitLabel`, `unitTitle`, `title`, `name`, `lede`, `visto`, `source`, `laminas`, `next`, `teoria`, `historias`.

Hay **dos lecturas** de la misma clase:

- `teoria` — desarrollo completo, fiel al apunte: se muestra en la página LMS.
- `historias` — repaso corto, visual, una idea por tarjeta (modo historias).

### Bloques de `teoria` (en orden)

| `type` | Campos | Uso |
|---|---|---|
| `heading` | `level`, `text` | Títulos del apunte |
| `paragraph` | `text` | Párrafo. Acepta `**negrita**`, `*cursiva*` y `$math$` |
| `formula` | `tex` (LaTeX simple) | Fórmula destacada. `build.py` la convierte a HTML (fracciones, raíces, sub/superíndices). Sin KaTeX. |
| `table` | `headers`, `rows`, `caption` opcional | Tablas del apunte |
| `svg` | `file` (ruta bajo `content/`), `caption` | Lámina oficial; el build la incrusta |
| `callout` | `kind` (`idea`, `aviso`, `examen`), `text` | Idea central, advertencia, molde de examen |
| `list` | `ordered`, `items` | Listas |
| `ejemplo` | `title`, `blocks` | Ejemplo resuelto (visible) |
| `ejercicio` | `title`, `blocks`, `estado`, `nota`, `solucion` opcional | Ejercicio. Si no hay resolución en el material, `estado: "para resolver"` y no se inventa. Si hay, va en `solucion` y se muestra plegada. |
| `glosario` | `title`, `intro`, `entries` (`simbolo`, `nombre`, `significado`) | Glosario de símbolos |

### Tarjetas de `historias`

Igual que antes: `concepto` (`k`, `title`, `text`, `formula`, `svg`, `chartLabel`, `ejemplo`), `pregunta` (`title`, `options`, `correct`, `feedback`) y `cierre`. Textos cortos, voseo rioplatense. Preguntas bloqueantes cada 3–4 tarjetas.

El contenido tiene que salir del material de la cátedra o de los apuntes de clase. Si se agrega un dato general, hay que marcarlo.
