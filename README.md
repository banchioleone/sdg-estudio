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
  gen_*.py          generadores de clases
  audit_fix.py      ajustes puntuales de contenido
```

## Agregar o editar una clase

1. Editá el JSON de la clase, o creá uno nuevo, como dice [content/FORMATO.md](content/FORMATO.md). Una clase = un archivo, adentro de la carpeta de su unidad (`content/u1/`, `content/u2/`, …).
2. Si es nueva, agregala en `content/index.json` con `"file"` y `"soon": false`.
3. Desde la raíz del repo regenerá el HTML:

```bash
python3 build.py
```

4. Commiteá el JSON (y la lámina, si sumaste una) junto con el `index.html` que salió.
