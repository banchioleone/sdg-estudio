"""Minimal TeX-to-HTML for the formulas in the class notes. No KaTeX, works offline."""
from __future__ import annotations
import re

SIMPLE = {
    "\\times": "×",
    "\\cdot": "·",
    "\\pm": "±",
    "\\mp": "∓",
    "\\approx": "≈",
    "\\leq": "≤",
    "\\geq": "≥",
    "\\neq": "≠",
    "\\infty": "∞",
    "\\mu": "μ",
    "\\sigma": "σ",
    "\\alpha": "α",
    "\\beta": "β",
    "\\gamma": "γ",
    "\\theta": "θ",
    "\\lambda": "λ",
    "\\pi": "π",
    "\\delta": "δ",
    "\\Delta": "Δ",
    "\\Sigma": "Σ",
    "\\ldots": "…",
    "\\dots": "…",
    "\\quad": "&nbsp;&nbsp;",
    "\\qquad": "&nbsp;&nbsp;&nbsp;&nbsp;",
    "\\,": "&#8239;",
    "\\;": "&nbsp;",
    "\\!": "",
    "\\ ": " ",
    "\\%": "%",
}


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _brace(s: str, i: int) -> tuple[str, int]:
    if i >= len(s):
        return "", i
    if s[i] != "{":
        if s[i] == "\\":
            m = re.match(r"\\[a-zA-Z]+", s[i:])
            if m:
                return m.group(0), i + len(m.group(0))
        return s[i], i + 1
    depth = 0
    j = i
    while j < len(s):
        if s[j] == "\\" and j + 1 < len(s):
            j += 2
            continue
        if s[j] == "{":
            depth += 1
        elif s[j] == "}":
            depth -= 1
            if depth == 0:
                return s[i + 1 : j], j + 1
        j += 1
    return s[i + 1 :], len(s)


def convert(s: str) -> str:
    out: list[str] = []
    i = 0
    n = len(s)
    while i < n:
        # \frac / \dfrac
        if s.startswith("\\dfrac", i) or s.startswith("\\frac", i):
            i += 6 if s.startswith("\\dfrac", i) else 5
            while i < n and s[i] in " \t":
                i += 1
            num, i = _brace(s, i)
            while i < n and s[i] in " \t":
                i += 1
            den, i = _brace(s, i)
            out.append(
                '<span class="frac"><span class="num">'
                + convert(num)
                + '</span><span class="den">'
                + convert(den)
                + "</span></span>"
            )
            continue
        if s.startswith("\\sqrt", i):
            i += 5
            idx = ""
            if i < n and s[i] == "[":
                j = s.find("]", i)
                idx, i = s[i + 1 : j], j + 1
            body, i = _brace(s, i)
            pre = f"<sup>{convert(idx)}</sup>" if idx else ""
            out.append(pre + '√<span class="rad">' + convert(body) + "</span>")
            continue
        if s.startswith("\\bar{", i) or s.startswith("\\overline{", i):
            i += 4 if s.startswith("\\bar{", i) else 9
            body, i = _brace(s, i)
            out.append('<span class="ov">' + convert(body) + "</span>")
            continue
        if s.startswith("\\hat{", i) or s.startswith("\\widehat{", i):
            i += 4 if s.startswith("\\hat{", i) else 8
            body, i = _brace(s, i)
            out.append('<span class="hat">' + convert(body) + "</span>")
            continue
        if s.startswith("\\mathbf{", i) or s.startswith("\\boldsymbol{", i):
            i = s.find("{", i)
            body, i = _brace(s, i)
            out.append("<b>" + convert(body) + "</b>")
            continue
        if s.startswith("\\mathrm{", i) or s.startswith("\\text{", i) or s.startswith("\\textrm{", i):
            i = s.find("{", i)
            body, i = _brace(s, i)
            out.append('<span class="mathrm">' + convert(body) + "</span>")
            continue
        if s.startswith("\\left", i):
            i += 5
            if i < n and s[i] == "\\":
                m = re.match(r"\\[a-zA-Z]+", s[i:])
                token = m.group(0) if m else s[i : i + 1]
                i += len(token)
                out.append(SIMPLE.get(token, esc(token.lstrip("\\"))))
            else:
                delim = s[i]
                i += 1
                if delim != ".":
                    out.append(esc(delim))
            continue
        if s.startswith("\\right", i):
            i += 6
            if i < n and s[i] == "\\":
                m = re.match(r"\\[a-zA-Z]+", s[i:])
                token = m.group(0) if m else s[i : i + 1]
                i += len(token)
                out.append(SIMPLE.get(token, esc(token.lstrip("\\"))))
            else:
                delim = s[i]
                i += 1
                if delim != ".":
                    out.append(esc(delim))
            continue
        if s.startswith("\\sum", i):
            i += 4
            if s.startswith("\\limits", i):
                i += 7
            sub = sup = ""
            while i < n and s[i] in "_^":
                kind = s[i]
                i += 1
                body, i = _brace(s, i)
                if kind == "_":
                    sub = body
                else:
                    sup = body
            piece = "Σ"
            if sub or sup:
                piece = (
                    '<span class="op">'
                    + piece
                    + ('<sub>' + convert(sub) + "</sub>" if sub else "")
                    + ('<sup>' + convert(sup) + "</sup>" if sup else "")
                    + "</span>"
                )
            out.append(piece)
            continue
        if s.startswith("\\limits", i):
            i += 7
            continue
        # generic command
        if s[i] == "\\":
            m = re.match(r"\\[a-zA-Z]+", s[i:])
            if m:
                cmd = m.group(0)
                i += len(cmd)
                if cmd in SIMPLE:
                    out.append(SIMPLE[cmd])
                else:
                    out.append(esc(cmd[1:]))
                continue
            # escaped char
            if i + 1 < n:
                out.append(esc(s[i + 1]))
                i += 2
                continue
        if s[i] in "^_":
            kind = s[i]
            i += 1
            body, i = _brace(s, i)
            tag = "sup" if kind == "^" else "sub"
            out.append(f"<{tag}>" + convert(body) + f"</{tag}>")
            continue
        if s[i] == "{":
            body, i = _brace(s, i)
            out.append(convert(body))
            continue
        if s[i] == "}":
            i += 1
            continue
        # unicode-friendly punctuation
        if s[i] == "~":
            out.append("&nbsp;")
            i += 1
            continue
        if s[i] == "&":
            out.append("&nbsp;")  # align tab — ignore
            i += 1
            continue
        out.append(esc(s[i]))
        i += 1
    return "".join(out)


def tex_to_html(tex: str, block: bool = True) -> str:
    raw = tex.strip()
    raw = raw.strip("$").strip()
    # flatten $$ wrappers if leftover
    raw = raw.replace("\n", " ")
    html = convert(raw)
    cls = "eq-block" if block else "eq-inline"
    return f'<span class="{cls}">{html}</span>'


def inline_math(text: str) -> str:
    """Replace $...$ and **bold** / *em* in a prose string."""
    parts: list[str] = []
    i = 0
    s = text
    # First extract display $$ if any slipped in
    def subst_math(m):
        return tex_to_html(m.group(1), block=False)

    s = s.replace("\\$", "\x00")  # \$ = signo pesos literal
    s = re.sub(r"\$\$(.+?)\$\$", lambda m: tex_to_html(m.group(1), True), s, flags=re.S)
    s = re.sub(r"(?<!\$)\$(?!\$)(.+?)\$", subst_math, s, flags=re.S)

    # markdown inline — after math so we don't touch tex
    def md(s: str) -> str:
        # escape HTML first except our tags
        # split by existing tags
        chunks = re.split(r"(<[^>]+>)", s)
        out = []
        for i, ch in enumerate(chunks):
            if ch.startswith("<"):
                out.append(ch)
                continue
            ch = esc(ch)
            ch = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", ch)
            ch = re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", r"<em>\1</em>", ch)
            ch = re.sub(r"`(.+?)`", r"<code>\1</code>", ch)
            out.append(ch)
        return "".join(out)

    return md(s).replace("\x00", "$")


if __name__ == "__main__":
    tests = [
        r"\bar{X} = \frac{\sum X}{n}",
        r"s = \sqrt{\frac{\sum (X - \bar{X})^2}{n-1}}",
        r"s^2",
        r"Z = \frac{X - \mu}{\sigma}",
        r"X = \mu + Z\cdot\sigma",
        r"r = \frac{n\sum XY - \sum X \sum Y}{\sqrt{\left[n\sum X^2 - (\sum X)^2\right]\cdot\left[n\sum Y^2 - (\sum Y)^2\right]}}",
        r"r = \frac{1.725}{1.760,7} \approx \mathbf{0,98}",
        r"Y = T + C + S + I",
        r"Y = T \times C \times S \times I",
        r"r_k = \frac{\sum_{t=k+1}^{n}(Y_t - \bar{Y})(Y_{t-k} - \bar{Y})}{\sum_{t=1}^{n}(Y_t - \bar{Y})^2}",
        r"\pm \frac{2}{\sqrt{n}}",
        r"e_t = Y_t - \hat{Y}_t",
        r"MAD = \frac{\sum |Y_t - \hat{Y}_t|}{n}",
        r"MSE = \frac{\sum (Y_t - \hat{Y}_t)^2}{n}",
        r"MAPE = \frac{\sum \left|\dfrac{Y_t - \hat{Y}_t}{Y_t}\right|}{n} \times 100",
        r"PME = \frac{\sum \dfrac{Y_t - \hat{Y}_t}{Y_t}}{n} \times 100",
    ]
    for t in tests:
        print("TEZ", t)
        print(" ->", tex_to_html(t))
        print()
