"""Turn the class markdown notes into teoria blocks, faithfully."""
from __future__ import annotations
import re
from pathlib import Path

HEAD_RE = re.compile(r"^(#{1,6})\s+(.*)$")


def is_table_line(s: str) -> bool:
    s = s.strip()
    return s.startswith("|") and s.count("|") >= 2


def is_sep_row(s: str) -> bool:
    s = s.strip().strip("|").replace(" ", "")
    return bool(s) and all(c in "-:" for c in s)


def split_row(s: str) -> list[str]:
    s = s.strip()
    if s.startswith("|"):
        s = s[1:]
    if s.endswith("|"):
        s = s[:-1]
    return [c.strip() for c in s.split("|")]


def parse_md(text: str) -> list[dict]:
    lines = text.replace("\r\n", "\n").split("\n")
    blocks: list[dict] = []
    i, n = 0, len(lines)

    def flush_para(buf: list[str]):
        raw = "\n".join(buf).strip()
        if raw:
            blocks.append({"type": "paragraph", "text": raw})

    while i < n:
        line = lines[i]
        if not line.strip():
            i += 1
            continue
        if line.strip() == "---":
            i += 1
            continue
        m = HEAD_RE.match(line.strip())
        if m:
            blocks.append({"type": "heading", "level": len(m.group(1)), "text": m.group(2).strip()})
            i += 1
            continue
        if line.strip().startswith("$$") or (line.strip() == "$$"):
            raw = line.strip()
            if raw.count("$$") >= 2 and len(raw) > 4:
                tex = raw.strip("$").strip()
                blocks.append({"type": "formula", "tex": tex})
                i += 1
                continue
            buf = []
            if raw != "$$":
                buf.append(raw[2:])
            i += 1
            while i < n and "$$" not in lines[i]:
                buf.append(lines[i])
                i += 1
            if i < n:
                after = lines[i]
                # content before closing $$
                if after.strip() != "$$":
                    buf.append(after[: after.find("$$")])
                i += 1
            tex = "\n".join(buf).strip().strip("$").strip()
            if tex:
                blocks.append({"type": "formula", "tex": tex})
            continue
        if is_table_line(line):
            rows = []
            while i < n and is_table_line(lines[i]):
                rows.append(lines[i])
                i += 1
            parsed = [split_row(r) for r in rows]
            # drop separator
            headers = parsed[0]
            body = [r for r, raw in zip(parsed[1:], rows[1:]) if not is_sep_row(raw)]
            blocks.append({"type": "table", "headers": headers, "rows": body})
            continue
        if line.lstrip().startswith(">"):
            buf = []
            while i < n and lines[i].lstrip().startswith(">"):
                q = re.sub(r"^\s*>\s?", "", lines[i])
                buf.append(q)
                i += 1
            text = "\n".join(buf).strip()
            kind = "idea"
            if text.startswith("⚠") or "Advertencia" in text or text.startswith("**⚠"):
                kind = "aviso"
            elif "examen" in text.lower() or "justifique" in text.lower() or "redacción" in text.lower():
                kind = "examen"
            blocks.append({"type": "callout", "kind": kind, "text": text})
            continue
        # lists
        if re.match(r"^(\s*)([-*]|\d+[.)])\s+", line):
            items = []
            ordered = bool(re.match(r"^\s*\d+[.)]\s+", line))
            while i < n and re.match(r"^(\s*)([-*]|\d+[.)])\s+", lines[i]):
                item = re.sub(r"^(\s*)([-*]|\d+[.)])\s+", "", lines[i]).rstrip()
                # continuation lines
                i += 1
                while i < n and lines[i].startswith("  ") and not re.match(r"^(\s*)([-*]|\d+[.)])\s+", lines[i]) and not is_table_line(lines[i]) and not lines[i].strip().startswith("#") and lines[i].strip() != "---":
                    item += " " + lines[i].strip()
                    i += 1
                items.append(item)
            blocks.append({"type": "list", "ordered": ordered, "items": items})
            continue
        # paragraph
        buf = [line]
        i += 1
        while i < n and lines[i].strip() and not HEAD_RE.match(lines[i].strip()) and lines[i].strip() != "---" and not is_table_line(lines[i]) and not lines[i].lstrip().startswith(">") and not (lines[i].strip().startswith("$$")) and not re.match(r"^(\s*)([-*]|\d+[.)])\s+", lines[i]):
            buf.append(lines[i])
            i += 1
        flush_para(buf)
    return blocks


def heading_text(b: dict) -> str:
    return (b.get("text") or "") if b.get("type") == "heading" else ""


def split_at_heading(blocks: list[dict], pred) -> tuple[list[dict], list[dict], dict | None]:
    for i, b in enumerate(blocks):
        if b.get("type") == "heading" and pred(b.get("text") or ""):
            return blocks[:i], blocks[i + 1 :], b
    return blocks, [], None


def slice_sections(blocks: list[dict]) -> list[tuple[str, int, list[dict]]]:
    """Return (heading, level, body-including-heading) for each h2/h1."""
    out = []
    current = None
    buf: list[dict] = []
    title = ""
    level = 1
    for b in blocks:
        if b.get("type") == "heading" and b.get("level", 3) <= 2:
            if current is not None:
                out.append((title, level, buf))
            title = b.get("text") or ""
            level = b.get("level") or 2
            buf = [b]
            current = title
        else:
            if current is None:
                title, level, buf = "(intro)", 1, [b]
                current = title
            else:
                buf.append(b)
    if current is not None:
        out.append((title, level, buf))
    return out


if __name__ == "__main__":
    root = Path("/workspace/sdg/clases_previas/SG")
    for p in sorted(root.glob("*.md")):
        blocks = parse_md(p.read_text())
        types = {}
        for b in blocks:
            types[b["type"]] = types.get(b["type"], 0) + 1
        heads = [b["text"] for b in blocks if b["type"] == "heading"]
        print(p.name, "blocks", len(blocks), types)
        for h in heads:
            print("  -", h)
