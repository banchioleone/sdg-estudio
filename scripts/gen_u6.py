"""Arma las clases de la U6 (content/u6/*.json) y actualiza content/index.json."""
import json
from u6lib import ROOT, BLOCKS, write
from gen_u6_a import c0, c1, c2, c3, c4
from gen_u6_b import c5, c6
from gen_u6_c import c7, c8, c9, c10
from gen_u6_d import c11, c12, integ
from gen_u6_historias import HIST

SHORT = {"u6c0": ("Mapa", "🗺️"), "u6c1": ("Tipos", "1"), "u6c2": ("Plan agregado", "2"), "u6c3": ("Planilla PA", "3"),
         "u6c4": ("MPS", "4"), "u6c5": ("Capacidad", "5"), "u6c6": ("RRP → CRP", "6"), "u6c7": ("MRP", "7"),
         "u6c8": ("MRP examen", "8"), "u6c9": ("Lotes", "9"), "u6c10": ("MRP II / ERP", "10"), "u6c11": ("Balanceo", "11"),
         "u6c12": ("PAC", "12"), "u6int": ("Integrador", "🧩")}


def svgs(blocks):
    out = []
    for b in blocks:
        if isinstance(b, dict):
            if b.get("type") == "svg":
                out.append(b["file"])
            for k in ("blocks", "solucion"):
                if isinstance(b.get(k), list):
                    out += svgs(b[k])
    return out


def main():
    classes = [c0(), c1(), c2(), c3(), c4(), c5(), c6(), c7(), c8(), c9(), c10(), c11(), c12(), integ()]
    entries = []
    for i, c in enumerate(classes):
        fname = "integrador.json" if c["id"] == "u6int" else f"clase{i:02d}.json"
        c["next"] = classes[i + 1]["title"] if i + 1 < len(classes) else None
        if not c["laminas"]:
            c["laminas"] = list(dict.fromkeys(svgs(c["teoria"])))
        h = HIST[c["id"]]
        assert 9 <= len(h) <= 16 and h[-1]["type"] == "cierre", c["id"]
        for card in h:
            assert "$" not in str(card), (c["id"], card.get("title"))
            if card["type"] == "pregunta": assert 0 <= card["correct"] < len(card["options"])
        c["historias"] = h
        write(fname, c)
        short, emoji = SHORT[c["id"]]
        entries.append({"id": c["id"], "title": c["title"], "file": "u6/" + fname, "soon": False, "visto": False,
                        "name": c["name"], "short": short, "emoji": emoji, "block": c["block"]})
        print(fname, c["id"], "next=", c["next"], "bloques:", len(c["teoria"]), "láminas:", len(c["laminas"]), "historias:", len(h),
              "svg:", sum(1 for x in h if x.get("svg")), "preguntas:", sum(1 for x in h if x["type"] == "pregunta"))
    idx_path = ROOT / "content" / "index.json"
    idx = json.loads(idx_path.read_text(encoding="utf-8"))
    u = next(x for x in idx["units"] if x["id"] == "u6")
    u.update({
        "title": "U6 · Planificación y control", "kind": "Práctica + teoría",
        "lede": ("Unidad 6 del programa: planificación y control de la producción. Arranca con la Clase 0 · Mapa de la unidad y sigue en cuatro bloques. "
                 "Bloque A · Plan agregado y programa maestro: tipos de producción, estrategias y costos del plan agregado, la planilla período a período y el MPS. "
                 "Bloque B · Capacidad: medida, RGE y capacidad de una estación; de RRP a CRP. "
                 "Bloque C · MRP y MRP II: el registro MRP, los ejercicios de final, las reglas de lote y MRP II / ERP. "
                 "Bloque D · Balanceo y control de la producción: balanceo de línea y PAC. "
                 "Cierra con el Integrador de ejercicios tipo examen."),
        "blocks": [{"id": k, "title": v} for k, v in BLOCKS.items()],
        "classes": entries,
        "oldIds": {"u6-intro": "u6c0"},
    })
    idx_path.write_text(json.dumps(idx, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
