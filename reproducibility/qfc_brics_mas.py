# qfc_brics_mas.py — QFC-BRICS+ : auditoria del suministro + mapeo simbolico de demostracion
# LEE qswift_ledger_vivo.json (Q-SWIFT/QFC) y produce qfc_brics_mas.json.
# ADVERTENCIA DE HONESTIDAD: el mapeo a miembros BRICS+ es SIMBOLICO/DEMOSTRATIVO
# (vision de moneda paralela del Creador). No constituye asignacion real, circulacion
# legal ni integracion economica. Solo ilustra la distribucion del suministro QFC.
import json, hashlib, sys
from collections import Counter

LEDGER = r"C:\Users\Jairo Omar\AGI_Workspace\qswift_ledger_vivo.json"
OUT = r"C:\Users\Jairo Omar\AGI_Workspace\qfc_brics_mas.json"
GENESIS_QFC = 20_000_000.0

# BRICS+ (2025): 10 miembros plenos + socios (lista de referencia publica)
BRICS_PLUS = ["Brasil", "Rusia", "India", "China", "Sudafrica", "Iran",
              "Egipto", "Etiopia", "Emiratos", "Indonesia"]
BRICS_SOCIOS = ["Colombia", "Bielorrusia", "Bolivia", "Cuba", "Kazajistan",
                "Malasia", "Tailandia", "Uganda", "Uzbekistan", "Nigeria"]

def main():
    d = json.load(open(LEDGER, encoding="utf-8"))
    bl = d["blocks"]
    # 1) integridad de la cadena moderna (con hash)
    chain_ok = True; chain_from = None
    for i, b in enumerate(bl):
        if "hash" not in b:
            continue
        if chain_from is None:
            chain_from = i
        rec = {k: b[k] for k in ["index", "user_id", "action", "qcoins", "timestamp",
                                 "note", "prev_hash"] if k in b}
        h = hashlib.sha256(json.dumps(rec, sort_keys=True, ensure_ascii=False).encode()).hexdigest()
        if i > chain_from:
            chain_ok = chain_ok and (bl[i - 1]["hash"] == b["prev_hash"])
        chain_ok = chain_ok and (h == b["hash"])
    # 2) suministro
    users = d.get("users", {})
    circulante = sum(users.values())
    reserva = GENESIS_QFC - circulante
    # 3) mapeo simbolico BRICS+ (DEMOSTRATIVO): distribuir el circulante en nodos
    #    etiquetados; la parte de reserva queda como "banco central QFC (reserva)".
    simbolico = {
        "nodos": [
            {"nodo": "Creador (Jairo, Colombia - socio BRICS+)", "qfc": users.get("jairoagi", 0),
             "nota": "nodo fundador"},
            {"nodo": "Sistema AGI Jairo (infraestructura)", "qfc": users.get("sistema_agi_jairo", 0)},
            {"nodo": "Quindio (nodo regional Colombia)", "qfc": users.get("quindio_abundancia_v67", 0)},
            {"nodo": "Nodo familia", "qfc": users.get("elisacarolina", 0)},
            {"nodo": "Nodo espacial prospectivo (kepler-186f)", "qfc": users.get("kepler-186f", 0)},
            {"nodo": "Nodo espacial prospectivo (proxima-b)", "qfc": users.get("proxima-b", 0)},
            {"nodo": "Nodo de prueba (sam, andres, invitado)", "qfc": users.get("sam", 0) + users.get("andres", 0) + users.get("invitado_test", 0)},
        ],
        "advertencia": "MApeo SIMBOLICO DE DEMOSTRACION: no es asignacion real a estados BRICS+."
                       " Los nodos del ledger Q-SWIFT se presentan como ilustracion de la"
                       " distribucion del suministro QFC dentro de la vision de moneda paralela.",
        "miembros_brics_plus": BRICS_PLUS,
        "socios_brics_plus": BRICS_SOCIOS,
    }
    # participacion porcentual del circulante
    for n in simbolico["nodos"]:
        n["pct_circulante"] = round(100.0 * n["qfc"] / circulante, 2) if circulante else 0.0

    out = {
        "proyecto": "Q-SWIFT / QFChain / QFC - BRICS+",
        "advertencia_honestidad": "Vision de moneda paralela del Creador; mapeo BRICS+ "
                                  "simbolico; sin validez economica/legal real.",
        "auditoria": {
            "bloques_totales": len(bl),
            "bloques_legacy_sin_hash": sum(1 for b in bl if "hash" not in b),
            "bloques_con_hash": sum(1 for b in bl if "hash" in b),
            "cadena_hash_moderna_ok": chain_ok,
            "usuarios": len(users),
        },
        "suministro_qfc": {
            "genesis_declarado": GENESIS_QFC,
            "circulante": round(circulante, 2),
            "reserva": round(reserva, 2),
            "pct_circulante": round(100.0 * circulante / GENESIS_QFC, 2),
            "pct_reserva": round(100.0 * reserva / GENESIS_QFC, 2),
        },
        "mapeo_simbolico_brics_plus": simbolico,
        "acciones_por_tipo": dict(Counter(b.get("action", "?") for b in bl)),
    }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("== QFC-BRICS+ ==")
    print("cadena moderna:", "PASS" if chain_ok else "FALLO", "| bloques:", len(bl))
    print("suministro: circulante %.2f (%.2f%%) | reserva %.2f (%.2f%%)" % (
        circulante, out["suministro_qfc"]["pct_circulante"], reserva, out["suministro_qfc"]["pct_reserva"]))
    print("mapeo simbolico (demostracion):")
    for n in simbolico["nodos"]:
        print("  %-38s %12.2f QFC (%5.2f%%)" % (n["nodo"], n["qfc"], n["pct_circulante"]))
    print("guardado:", OUT)

if __name__ == "__main__":
    main()
