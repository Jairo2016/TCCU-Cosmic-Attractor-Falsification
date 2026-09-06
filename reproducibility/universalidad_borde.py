# universalidad_borde.py — Campana pre-registrada: universalidad del borde cinetico TCCU-0
# (PREREGISTRO_UNIVERSALIDAD_BORDE_2026-09-05.md). Sistema ORIGINAL Friedmann+KG.
# Checkpoint por config (JSONL + flush), reanudable. Salida: universalidad_borde.jsonl
# + universalidad_borde_resumen.json. Uso: python universalidad_borde.py [--solo 1.66]
import os, sys, json, time, hashlib, argparse
import numpy as np
from scipy.integrate import solve_ivp

BASE = r"C:\Users\Jairo Omar\AGI_Workspace"
OUT_JSONL = os.path.join(BASE, "universalidad_borde.jsonl")
OUT_RES = os.path.join(BASE, "universalidad_borde_resumen.json")

H0 = 1.44e-60; LAMBD = 0.15; Om_m, Om_r = 0.315, 9.0e-5; rho_c0 = 3.0 * H0 ** 2
ALPHA_CRIT = 0.95
N_LIMITE = -50.0   # si llega aqui sin romper -> candidato a refutar

LAMS = [0.5, 0.75, 1.0, 1.25, 1.5, 1.66, 1.75, 1.84, 2.0, 2.25, 2.5, 3.0, 4.0, 5.0, 6.0]
W0S = [-0.5, -0.3, -0.2, 0.0, 0.2, 0.3, 0.5]

def ic(w0, sg, LAM):
    rho_Phi0 = (1 - Om_m - Om_r) * rho_c0
    A0 = (1.0 + w0) * rho_Phi0 / 2.0
    X0 = 2.0 * A0 / (1 + np.sqrt(1 + 8 * A0 / LAMBD ** 4))
    Pi0 = sg * np.sqrt(2 * X0) / H0
    V0 = rho_Phi0 - X0 - 3 * X0 ** 2 / LAMBD ** 4
    return -np.log(V0 / rho_c0) / LAM, Pi0

def derivs_orig(N, y, LAM):
    Phi, Pi, h, m, r = y
    X = 0.5 * (H0 * h * Pi) ** 2
    V = rho_c0 * np.exp(-LAM * Phi)
    rp = X + 3.0 * X ** 2 / LAMBD ** 4 + V
    pp = X + X ** 2 / LAMBD ** 4 - V
    rtn = m + r + rp / rho_c0
    ptn = (pp + r * rho_c0 / 3.0) / rho_c0
    if h <= 0:
        return np.full(5, np.nan)
    dh = -1.5 * (rtn + ptn) / h
    u = 2.0 * X / LAMBD ** 4
    den = 1.0 + 3.0 * u
    dPi = -(dh / h) * Pi - 3.0 * (1.0 + u) * Pi / den + LAM * V / (den * H0 ** 2 * h ** 2)
    return np.array([Pi, dPi, dh, -3.0 * m, -4.0 * r])

def run_config(lam, w0, method="BDF"):
    Phi0, Pi0 = ic(w0, 1.0, lam)
    y0 = np.array([Phi0, Pi0, 1.0, Om_m, Om_r])
    te = np.linspace(0.0, N_LIMITE, 1000)
    try:
        sol = solve_ivp(lambda N, y: derivs_orig(N, y, lam), [0.0, N_LIMITE], y0,
                        method=method, t_eval=te, rtol=1e-11, atol=1e-14, max_step=0.05)
    except Exception as e:
        return {"lam": lam, "w0": w0, "metodo": method, "estado": "error",
                "detalle": str(e)[:80], "N_s": None, "alpha_max": None}
    if not sol.success:
        # fallo del integrador -> marcar (puede ser region de inviabilidad temprana)
        a = sol.y[1] ** 2 / 6.0
        idx = np.where(a > ALPHA_CRIT)[0]
        Ns = float(sol.t[idx[0]]) if len(idx) else float(sol.t[-1])
        return {"lam": lam, "w0": w0, "metodo": method, "estado": "integrador_" + sol.message[:30].replace(" ", "_"),
                "N_s": round(Ns, 4), "alpha_max": round(float(a.max()), 6),
                "N_ult": round(float(sol.t[-1]), 4)}
    a = sol.y[1] ** 2 / 6.0
    idx = np.where(a > ALPHA_CRIT)[0]
    if len(idx):
        Ns = float(sol.t[idx[0]])
        estado = "ruptura"
    else:
        Ns = float(sol.t[-1])
        estado = "sin_ruptura_50" if abs(sol.t[-1] - N_LIMITE) < 1e-6 else "limite"
    return {"lam": lam, "w0": w0, "metodo": method, "estado": estado,
            "N_s": round(Ns, 4), "alpha_max": round(float(a.max()), 6),
            "N_ult": round(float(sol.t[-1]), 4)}

def cargar_hechos():
    hechos = {}
    if os.path.exists(OUT_JSONL):
        with open(OUT_JSONL, encoding="utf-8") as f:
            for line in f:
                try:
                    c = json.loads(line)
                    hechos[(c["lam"], c["w0"])] = c
                except Exception:
                    pass
    return hechos

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--solo", type=float, default=None)
    ap.add_argument("--metodo2_cada", type=int, default=10, help="cada N configs se corre DOP853 como control")
    args = ap.parse_args()

    configs = [(lam, w0) for lam in LAMS for w0 in W0S]
    if args.solo is not None:
        configs = [(lam, w0) for lam, w0 in configs if abs(lam - args.solo) < 1e-9]

    hechos = cargar_hechos()
    t0 = time.time()
    print("Campana universalidad del borde | %d configs | BDF primario + DOP853 control cada %d" % (len(configs), args.metodo2_cada), flush=True)
    pendientes = [c for c in configs if c not in hechos]
    print("hechos: %d | pendientes: %d" % (len(hechos), len(pendientes)), flush=True)

    for i, (lam, w0) in enumerate(configs):
        if (lam, w0) in hechos:
            continue
        metodo2 = "DOP853" if (configs.index((lam, w0)) % args.metodo2_cada == 0) else None
        res = run_config(lam, w0, "BDF")
        if metodo2 and res["estado"] in ("ruptura", "sin_ruptura_50"):
            res2 = run_config(lam, w0, metodo2)
            res["control"] = {"metodo": metodo2, "estado": res2["estado"], "N_s": res2["N_s"]}
            res["control_ok"] = (res2["estado"] == res["estado"]) or (
                res2["estado"] == "ruptura" and res["estado"] == "ruptura"
                and abs(res2["N_s"] - res["N_s"]) < 0.5)
        with open(OUT_JSONL, "a", encoding="utf-8") as f:
            f.write(json.dumps(res, ensure_ascii=False) + "\n")
            f.flush()
        hechos[(lam, w0)] = res
        print("[%3d/%3d] lam=%5.2f w0=%+5.2f -> %-16s N_s=%s alpha_max=%s (%.0f s)" % (
            i + 1, len(configs), lam, w0, res["estado"], res["N_s"], res["alpha_max"], time.time() - t0), flush=True)

    # ---- resumen ----
    filas = [hechos[c] for c in configs if c in hechos]
    rupturas = [f for f in filas if f["estado"] == "ruptura"]
    sin_ruptura = [f for f in filas if f["estado"] == "sin_ruptura_50"]
    errores = [f for f in filas if f["estado"] not in ("ruptura", "sin_ruptura_50", "limite")]
    # monotonía en lambda por w0 (entre configs con ruptura)
    mono = {}
    for w0 in W0S:
        por_lam = sorted([(f["lam"], f["N_s"]) for f in rupturas if abs(f["w0"] - w0) < 1e-9])
        viol = []
        for j in range(1, len(por_lam)):
            if por_lam[j][1] < por_lam[j - 1][1] - 1.0:  # descenso local > 1 e-fold
                viol.append((por_lam[j - 1], por_lam[j]))
        mono[w0] = {"n": len(por_lam), "violaciones": viol}
    r1 = sin_ruptura  # candidatos a extension larga
    r2 = {w0: v["violaciones"] for w0, v in mono.items() if v["violaciones"]}
    r3 = [f for f in sin_ruptura if f.get("alpha_max", 1) < ALPHA_CRIT]
    resumen = {
        "pre_registro": "PREREGISTRO_UNIVERSALIDAD_BORDE_2026-09-05.md",
        "fecha": time.strftime("%Y-%m-%d %H:%M:%S"),
        "n_configs_total": len(configs),
        "n_completados": len(filas),
        "n_ruptura": len(rupturas),
        "n_sin_ruptura_50": len(sin_ruptura),
        "n_errores": len(errores),
        "refutacion_R1": [{"lam": f["lam"], "w0": f["w0"], "N_s": f["N_s"]} for f in r1],
        "refutacion_R2": r2,
        "refutacion_R3": [{"lam": f["lam"], "w0": f["w0"], "alpha_max": f["alpha_max"]} for f in r3],
        "monotonia_por_w0": mono,
        "rango_Ns_observado": [min((f["N_s"] for f in rupturas), default=None),
                               max((f["N_s"] for f in rupturas), default=None)],
        "veredicto": None,
    }
    if not r1 and not r2 and not r3:
        resumen["veredicto"] = "PASS — universalidad consistente en el dominio barrido (sin R1/R2/R3)"
    elif r1 or r2 or r3:
        resumen["veredicto"] = "REFUTADA — se encontro al menos un candidato R1/R2/R3"
    else:
        resumen["veredicto"] = "INCONCLUSIVE — barrido incompleto"
    with open(OUT_RES, "w", encoding="utf-8") as f:
        json.dump(resumen, f, ensure_ascii=False, indent=1)
    print("RESUMEN:", json.dumps({k: v for k, v in resumen.items() if k in
          ("n_ruptura", "n_sin_ruptura_50", "n_errores", "rango_Ns_observado", "veredicto")}, ensure_ascii=False), flush=True)

if __name__ == "__main__":
    main()
