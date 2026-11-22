"""Arma las clases de la U5 (content/u5/*.json) y actualiza content/index.json."""
import json
from u5lib import ROOT, BLOCKS, write
from gen_u5_a import c0, c1
from gen_u5_b import c2, c3
from gen_u5_c import c4, c5
from gen_u5_d import c6, c7
from gen_u5_e import c8, c9
from gen_u5_f import c10, integ
from gen_u5_historias import HIST

SHORT = {"u5c0": ("Mapa", "🗺️"), "u5c1": ("Inventario", "1"), "u5c2": ("EOQ", "2"), "u5c3": ("Descuentos", "3"),
         "u5c4": ("Q vs P", "4"), "u5c5": ("Seguridad", "5"), "u5c6": ("Período fijo", "6"), "u5c7": ("ABC", "7"),
         "u5c8": ("Compras", "8"), "u5c9": ("Almacenes", "9"), "u5c10": ("Cadena", "10"), "u5int": ("Integrador", "🧩")}

def main():
    classes = [c0(), c1(), c2(), c3(), c4(), c5(), c6(), c7(), c8(), c9(), c10(), integ()]
    entries = []
    for i, c in enumerate(classes):
        fname = "integrador.json" if c["id"] == "u5int" else f"clase{i:02d}.json"
        h = HIST[c["id"]]
        assert 9 <= len(h) <= 16 and h[-1]["type"] == "cierre", c["id"]
        for card in h:
            assert "$" not in str(card), (c["id"], card.get("title"))
            if card["type"] == "pregunta": assert 0 <= card["correct"] < len(card["options"])
        c["historias"] = h
        write(fname, c)
        short, emoji = SHORT[c["id"]]
        entries.append({"id": c["id"], "title": c["title"], "file": "u5/" + fname, "soon": False, "visto": False,
                        "name": c["name"], "short": short, "emoji": emoji, "block": c["block"]})
        print(fname, c["id"], "next=", c["next"], "bloques:", len(c["teoria"]), "historias:", len(c["historias"]), "svg:", sum(1 for x in c["historias"] if x.get("svg")), "preguntas:", sum(1 for x in c["historias"] if x["type"] == "pregunta"))
    idx_path = ROOT / "content" / "index.json"
    idx = json.loads(idx_path.read_text(encoding="utf-8"))
    u = next(x for x in idx["units"] if x["id"] == "u5")
    u.update({
        "title": "U5 · Logística", "kind": "Práctica + teoría",
        "lede": ("Unidad 5 del programa: logística e inventarios. Arranca con la Clase 0 · Mapa de la unidad y sigue en tres bloques. "
                 "Bloque A · Inventario y modelos determinísticos: concepto de inventario, lote económico (EOQ) y punto de pedido, descuentos por cantidad, perpetuo vs. periódico. "
                 "Bloque B · Modelos estocásticos y control: stock de seguridad y nivel de servicio, período fijo, período único y rotación, ABC y conteo cíclico. "
                 "Bloque C · Compras, almacenes y logística: compras y proveedores, almacenes, distribución (DRP) y trazabilidad, cadena de suministro y ubicación de plantas. "
                 "Cierra con el Integrador de ejercicios tipo examen."),
        "blocks": [{"id": k, "title": v} for k, v in BLOCKS.items()],
        "classes": entries,
        "oldIds": {"u5-intro": "u5c0"},
    })
    idx_path.write_text(json.dumps(idx, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

if __name__ == "__main__":
    main()
