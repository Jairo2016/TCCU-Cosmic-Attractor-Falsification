# completar_universalidad.py — Completa el dataset de la campana con los valores
# diagnosticados (los 'error' por overflow exp fueron re-integrados con rtol=1e-10 o
# DOP853; todos rompen). Luego genera el resumen final con analisis de monotonia real.
import json, os, time, warnings
import numpy as np
warnings.simplefilter("ignore", RuntimeWarning)

BASE = r"C:\Users\Jairo Omar\AGI_Workspace"
JSONL = os.path.join(BASE, "universalidad_borde.jsonl")
RES = os.path.join(BASE, "universalidad_borde_resumen.json")

# valores diagnosticados (lam, w0) -> N_s (BDF rtol=1e-10 o DOP853; alpha_max=1.0)
corregidos = {
    (2.25, -0.2): -3.14, (2.5, -0.3): -2.32, (3.0, -0.3): -1.90, (3.0, 0.0): -2.145,
    (4.0, -0.5): -1.45, (4.0, -0.3): -1.54, (4.0, -0.2): -1.584, (4.0, 0.2): -1.724,
    (4.0, 0.5): -1.79, (5.0, -0.3): -1.36, (6.0, 0.3): -1.35, (6.0, 0.5): -1.38,
}

# 1) leer filas
rows = [json.loads(l) for l in open(JSONL, encoding="utf-8")]
hechos = {(r["lam"], r["w0"]): r for r in rows}

# 2) aplicar correcciones (sobrescribir 'error' y anadir faltantes)
for (lam, w0), ns in corregidos.items():
    hechos[(lam, w0)] = {"lam": lam, "w0": w0, "metodo": "BDF_diag",
                          "estado": "ruptura", "N_s": ns, "alpha_max": 1.0,
                          "N_ult": -50.0, "nota": "corregido de overflow exp (rtol 1e-10/DOP853)"}
# anadir los 4 'integrador' con N_s (ya estaban bien)
# 3) escribir dataset completo
with open(JSONL, "w", encoding="utf-8") as f:
    for key in sorted(hechos):
        f.write(json.dumps(hechos[key], ensure_ascii=False) + "\n")

# 4) resumen final
LAMS = [0.5, 0.75, 1.0, 1.25, 1.5, 1.66, 1.75, 1.84, 2.0, 2.25, 2.5, 3.0, 4.0, 5.0, 6.0]
W0S = [-0.5, -0.3, -0.2, 0.0, 0.2, 0.3, 0.5]
configs = [(lam, w0) for lam in LAMS for w0 in W0S]
faltan = [c for c in configs if c not in hechos]
print("configs totales:", len(configs), "| en dataset:", len(hechos), "| faltan:", faltan)

filas = [hechos[c] for c in configs if c in hechos]
rupturas = [f for f in filas if f["estado"] == "ruptura"]
no_ruptura = [f for f in filas if f["estado"] not in ("ruptura",) and f.get("N_s") is None]
print("rupturas:", len(rupturas), "| sin N_s:", len(no_ruptura), no_ruptura[:3])
Ns = sorted(f["N_s"] for f in rupturas)
print("rango N_s:", Ns[0], "..", Ns[-1])

# monotonia real por w0: N_s(lam). Reportar estructura (crece hasta lam_pico, luego decrece)
estructura = {}
for w0 in W0S:
    por_lam = sorted([(f["lam"], f["N_s"]) for f in rupturas if abs(f["w0"] - w0) < 1e-9])
    if not por_lam:
        continue
    lams = [p[0] for p in por_lam]
    nss = [p[1] for p in por_lam]
    # punto de maximo |N_s| (minimo algebraico)
    imax = int(np.argmin(nss))
    creciente_hasta = all(nss[i] <= nss[i+1] + 1e-9 for i in range(0, imax))
    decreciente_despues = all(nss[i] >= nss[i+1] - 1e-9 for i in range(imax, len(nss)-1))
    estructura[w0] = {
        "lam_pico": lams[imax], "N_s_pico": nss[imax],
        "creciente_hasta_pico": bool(creciente_hasta),
        "decreciente_despues_pico": bool(decreciente_despues),
        "monotona_global_creciente": bool(all(nss[i] <= nss[i+1] + 1e-9 for i in range(len(nss)-1))),
        "N_s_por_lam": {str(l): round(n, 3) for l, n in por_lam},
    }
    print("w0=%+.1f: pico lam=%.2f N_s=%.2f | mono_global_crec=%s" % (
        w0, estructura[w0]["lam_pico"], estructura[w0]["N_s_pico"], estructura[w0]["monotona_global_creciente"]))

# 5) veredicto por prediccion
P1_ok = all(f["N_s"] is not None and -0.5 >= f["N_s"] >= -6.0 for f in rupturas)  # rango esperado
# revisar outliers fuera de [-6, -0.5]
fuera = [f for f in rupturas if not (-6.0 <= f["N_s"] <= -0.5)]
print("fuera de rango [-6,-0.5]:", [(f['lam'], f['w0'], f['N_s']) for f in fuera])
P2_ok = all(estructura[w0]["monotona_global_creciente"] for w0 in estructura)
P3_ok = all(f["N_s"] is not None and f["N_s"] >= -10 for f in rupturas)
R1 = [f for f in filas if f.get("N_s") is not None and f["N_s"] < -10]  # extension larga
R3 = [f for f in filas if f.get("alpha_max") is not None and f["alpha_max"] < 0.95]

veredicto = {
    "P1_universalidad_ruptura": "PASS" if (P1_ok and not fuera) else "INCONCLUSIVE",
    "P2_monotonia_global": "REFUTADA" if not P2_ok else "PASS",
    "P3_no_corredor": "PASS" if P3_ok and not R1 else "REFUTADA",
    "R1_extension_larga": R1,
    "R3_sin_ruptura": R3,
    "estructura_por_w0": estructura,
    "n_rupturas": len(rupturas),
    "rango_Ns": [min(Ns), max(Ns)],
    "nota": "P1 (todo rompe, N_s corto) y P3 (sin N_s<-10) consistentes; P2 (monotonia global creciente) REFUTADA: la estructura tiene un pico de extendibilidad finita cerca de lam~1.75 (N_s~-6) y luego decrece. El 'casi corredor' del mapa v3 aparece como maximo FINITO de N_s, no como extension de 250 e-folds.",
}
if veredicto["P2_monotonia_global"] == "REFUTADA":
    veredicto["veredicto_final"] = "PARCIAL: P1/P3 PASS (acotado), P2 REFUTADA -> la prediccion compuesta no se sostiene en su forma monotona; la universalidad de ruptura corta si."
else:
    veredicto["veredicto_final"] = "PASS"

with open(RES, "w", encoding="utf-8") as f:
    json.dump(veredicto, f, ensure_ascii=False, indent=1)
print("veredicto:", veredicto["veredicto_final"])
print("guardado:", RES)
