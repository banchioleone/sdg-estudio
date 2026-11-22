#!/usr/bin/env python3
"""Inline content/*.json and official SVGs into index.html (works on file:// and GitHub Pages)."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CONTENT = ROOT / "content"
SCRIPTS = ROOT / "scripts"
OUT = ROOT / "index.html"
MARKER = "window.SDG_CONTENT = null; /* filled by build.py */"

sys.path.insert(0, str(SCRIPTS))
from texhtml import inline_math, tex_to_html  # noqa: E402


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def clean_svg(text: str) -> str:
    text = re.sub(r"<\?xml[^>]*\?>", "", text)
    text = re.sub(r"<!DOCTYPE[^>]*>", "", text, flags=re.I)
    return text.strip()


def read_svg(rel: str) -> str:
    path = CONTENT / rel
    if not path.exists():
        sys.exit(f"No encuentro la lámina {path}")
    return clean_svg(path.read_text(encoding="utf-8"))


def enrich(obj):
    if isinstance(obj, list):
        for x in obj:
            enrich(x)
        return
    if not isinstance(obj, dict):
        return
    typ = obj.get("type")
    if typ == "formula" and obj.get("tex"):
        obj["html"] = tex_to_html(obj["tex"], block=True)
    if isinstance(obj.get("formula"), str) and not obj.get("formulaHtml"):
        obj["formulaHtml"] = tex_to_html(obj["formula"], block=True)
    if typ == "svg" and obj.get("file") and not obj.get("svg"):
        obj["svg"] = read_svg(obj["file"])
    for key in ("text", "intro", "nota", "title", "caption", "lede"):
        if isinstance(obj.get(key), str) and typ != "svg":
            html_key = "html" if key == "text" else key + "Html"
            if key == "text":
                obj["html"] = inline_math(obj[key])
            else:
                obj[html_key] = inline_math(obj[key])
    if typ == "table":
        obj["headersHtml"] = [inline_math(c) for c in (obj.get("headers") or [])]
        obj["rowsHtml"] = [[inline_math(c) for c in row] for row in (obj.get("rows") or [])]
    if typ == "list":
        obj["itemsHtml"] = [inline_math(i) for i in (obj.get("items") or [])]
    if typ == "glosario":
        for e in obj.get("entries") or []:
            for k in ("simbolo", "nombre", "significado"):
                if isinstance(e.get(k), str):
                    e[k + "Html"] = inline_math(e[k])
    # unit laminas
    if "laminas" in obj and isinstance(obj["laminas"], list):
        for lam in obj["laminas"]:
            if isinstance(lam, dict) and lam.get("file") and not lam.get("svg"):
                lam["svg"] = read_svg(lam["file"])
                if lam.get("caption"):
                    lam["captionHtml"] = inline_math(lam["caption"])
    for v in obj.values():
        enrich(v)


def build_bundle() -> dict:
    index_path = CONTENT / "index.json"
    if not index_path.exists():
        sys.exit(f"No encuentro {index_path}")
    index = load_json(index_path)
    classes: dict = {}
    missing = []
    for unit in index.get("units") or []:
        for cls in unit.get("classes") or []:
            rel = cls.get("file")
            if not rel or cls.get("soon"):
                continue
            path = CONTENT / rel
            if not path.exists():
                missing.append(str(path))
                continue
            data = load_json(path)
            cid = data.get("id") or cls["id"]
            data["id"] = cid
            classes[cid] = data
    if missing:
        sys.exit("Faltan archivos de clase:\n  " + "\n  ".join(missing))
    bundle = {"index": index, "classes": classes}
    enrich(bundle)
    return bundle


def splice_payload(html: str, payload: str) -> str:
    """Replace the marker or a previous inline assignment. index.html is shell and output."""
    lines = html.splitlines(keepends=True)
    for i, line in enumerate(lines):
        body = line.rstrip("\r\n")
        if body == MARKER or body.startswith("window.SDG_CONTENT = "):
            lines[i] = "window.SDG_CONTENT = " + payload + ";" + line[len(body):]
            return "".join(lines)
    sys.exit(f"No encuentro el marcador de contenido en {OUT.name}")


def main() -> None:
    if not OUT.exists():
        sys.exit(f"No encuentro {OUT}")
    html = OUT.read_text(encoding="utf-8")
    bundle = build_bundle()
    payload = json.dumps(bundle, ensure_ascii=False, separators=(",", ":"))
    html = splice_payload(html, payload)
    html = html.replace(
        "<title>Sistemas de Gestión · Prototipo v3</title>",
        "<title>Sistemas de Gestión · Estudio</title>",
        1,
    )
    OUT.write_text(html, encoding="utf-8")
    n = len(bundle["classes"])
    print(f"OK {OUT} ({OUT.stat().st_size} bytes, {n} clase/s)")


if __name__ == "__main__":
    main()
