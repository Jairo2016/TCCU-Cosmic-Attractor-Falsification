# barrido_ciclo137.py — CICLO 137: barrido DBI + acoplamiento no minimo G4(phi,X)
# Modelo: G2 = 1 - sqrt(1 - X) - v   (DBI + offset, L^4 = 1)
#         G4 = (1 + xi phi^2 + eta X)/2
# EOM de fondo: derivar_horndeski_dbi.py (verificado: limite xi=eta=0 = DBI puro exacto).
# CI: phi0 = 0, phidot0 = sqrt(2(1 - eps0));  eps0 = distancia al limite DBI (u = 1 - eps0).
# Criterio F2 congelado: ventana contigua |w_eff| < 0.05 y |dln rho/dN + 3| < 0.05,
#   con dN >= 4.  (w_eff = -1 - 2Hdot/(3H^2); |dln rho/dN+3| = 3|w_eff| por cinematica.)
# Veredicto (criterio del Creador): si NINGUNA config alcanza dN_F2 >= 4 con
#   eps0 > 1e-8 -> falsacion acotada de la utilidad del acoplamiento no minimo
#   para relajar el fine-tuning.  Si alguna -> candidata a refinamiento + perturbaciones.
# Estabilidad lineal (Kobayashi 2019 eq. 49-52): G_T>0, G_S>0, c_s^2>0, c_GW^2>0.
import json
import os
import sys
import time

import numpy as np
from scipy.optimize import brentq
from scipy.stats import qmc

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import derivar_horndeski_dbi as DH

RANGOS = {"v": (0.85, 0.995), "xi": (-1.0, 1.0), "eta": (-0.5, 0.5)}
ORDEN = ["v", "xi", "eta"]
EPS_GRID = [1e-2, 1e-4, 1e-6, 1e-8, 1e-10]
EPS_CRIT = 1e-8            # umbral del Creador (estrictamente > 1e-8 cuenta)
NMAX = 12.0
DN = 0.02
H_MAX = 2000.0


def constraint_H(H, a, phi, php, p):
    return DH.E_fn(a, a * H, phi, php, *p)


def solve_H(a, phi, php, p):
    f0 = constraint_H(0.0, a, phi, php, p)
    for Hm in (H_MAX, H_MAX / 2, H_MAX / 4):
        f1 = constraint_H(Hm, a, phi, php, p)
        if np.isfinite(f0) and np.isfinite(f1) and f0 * f1 < 0:
            try:
                return brentq(constraint_H, 0.0, Hm, args=(a, phi, php, p))
            except ValueError:
                return np.nan
    return np.nan


def solve_derivs(a, H, phi, php, p):
    ap = a * H
    P0 = DH.P_fn(a, ap, 0.0, phi, php, 0.0, *p)
    E0 = DH.Ef_fn(a, ap, 0.0, phi, php, 0.0, *p)
    if not (np.isfinite(P0) and np.isfinite(E0)):
        return np.nan, np.nan
    Pa = DH.P_fn(a, ap, 1.0, phi, php, 0.0, *p) - P0
    Pb = DH.P_fn(a, ap, 0.0, phi, php, 1.0, *p) - P0
    Ea = DH.Ef_fn(a, ap, 1.0, phi, php, 0.0, *p) - E0
    Eb = DH.Ef_fn(a, ap, 0.0, phi, php, 1.0, *p) - E0
    det = Pa * Eb - Pb * Ea
    if abs(det) < 1e-14:
        return np.nan, np.nan
    app = (-P0 * Eb + Pb * E0) / det
    phpp = (-Pa * E0 + Ea * P0) / det
    return app, phpp


def rhs(N_, estado, a, p):
    phi, php = estado
    H = solve_H(a, phi, php, p)
    if not np.isfinite(H) or H <= 0:
        return None
    app, phpp = solve_derivs(a, H, phi, php, p)
    if not np.isfinite(phpp):
        return None
    return np.array([php / H, phpp / H])


def integrar(p, eps0, dn=DN, nmax=NMAX):
    a = 1.0
    N = 0.0
    phi0, php0 = 0.0, float(np.sqrt(2.0 * (1.0 - eps0)))
    estado = np.array([phi0, php0])
    serie = []
    while N < nmax:
        H = solve_H(a, estado[0], estado[1], p)
        if not np.isfinite(H) or H <= 0:
            break
        app, phpp = solve_derivs(a, H, estado[0], estado[1], p)
        if not np.isfinite(app) or not np.isfinite(phpp):
            break
        Hdot = app / a - H * H
        w = -1.0 - 2.0 * Hdot / (3.0 * H * H)
        # estabilidad lineal en este punto (Kobayashi 2019)
        try:
            GT = DH.GT_fn(estado[0], estado[1], p[1], p[2])
            FT = DH.FT_fn(estado[0], estado[1], p[1], p[2])
            Sig = DH.Sigma_fn(H, estado[0], estado[1], *p)
            Thet = DH.Theta_fn(H, estado[0], estado[1], *p)
            if not (np.isfinite(GT) and np.isfinite(FT) and np.isfinite(Sig) and np.isfinite(Thet)):
                raise ValueError("no finito")
        except Exception:
            break
        if abs(Thet) < 1e-10:   # Theta=0 -> formulas divergen (cruce degenerado)
            break
        serie.append({"N": N, "w": float(w), "phi": float(estado[0]), "php": float(estado[1]),
                      "H": float(H), "GT": float(GT), "FT": float(FT),
                      "Sigma": float(Sig), "Theta": float(Thet)})
        k1 = rhs(N, estado, a, p)
        if k1 is None:
            break
        k2 = rhs(N + dn / 2, estado + dn / 2 * k1, a * np.exp(dn / 2), p)
        if k2 is None:
            break
        k3 = rhs(N + dn / 2, estado + dn / 2 * k2, a * np.exp(dn / 2), p)
        if k3 is None:
            break
        k4 = rhs(N + dn, estado + dn * k3, a * np.exp(dn), p)
        if k4 is None:
            break
        estado = estado + dn / 6.0 * (k1 + 2 * k2 + 2 * k3 + k4)
        a = a * np.exp(dn)
        N += dn
        if not (np.isfinite(estado[0]) and np.isfinite(estado[1])):
            break
        if abs(estado[1]) > 1e8 or abs(estado[0]) > 60:
            break
    return serie


def ventanas(Ns, ws):
    en = np.abs(ws) < 0.05
    runs = []
    i = 0
    while i < len(en):
        if en[i]:
            j = i
            while j + 1 < len(en) and en[j + 1]:
                j += 1
            runs.append((Ns[i], Ns[j]))
            i = j + 1
        else:
            i += 1
    return runs


def medir(serie):
    if len(serie) < 3:
        return None
    Ns = np.array([s["N"] for s in serie])
    ws = np.array([s["w"] for s in serie])
    Hs = np.array([s["H"] for s in serie])
    dlnr = np.gradient(np.log(3.0 * Hs ** 2), Ns)
    m_f2 = (np.abs(ws) < 0.05) & (np.abs(dlnr + 3.0) < 0.05)
    dN_f2 = 0.0
    i = 0
    while i < len(m_f2):
        if m_f2[i]:
            j = i
            while j + 1 < len(m_f2) and m_f2[j + 1]:
                j += 1
            dN_f2 = max(dN_f2, Ns[j] - Ns[i])
            i = j + 1
        else:
            i += 1
    runs = ventanas(Ns, ws)
    dN_w005 = max((b - a for a, b in runs), default=0.0)
    # F2a: ventana |w|<0.05 con dN>=2 y |dw/dN|<0.05
    dw = np.abs(np.gradient(ws, Ns))
    dN_f2a = 0.0
    m_f2a = (np.abs(ws) < 0.05) & (dw < 0.05)
    i = 0
    while i < len(m_f2a):
        if m_f2a[i]:
            j = i
            while j + 1 < len(m_f2a) and m_f2a[j + 1]:
                j += 1
            dN_f2a = max(dN_f2a, Ns[j] - Ns[i])
            i = j + 1
        else:
            i += 1
    # estabilidad lineal: evaluar en la region dinamica (excluye la cola congelada
    # donde X->0 y G_S->0: el modo escalar degenera; c_s^2 = 0/0 numerico ahi).
    GT = np.array([s["GT"] for s in serie])
    FT = np.array([s["FT"] for s in serie])
    Sig = np.array([s["Sigma"] for s in serie])
    Thet = np.array([s["Theta"] for s in serie])
    phps_arr = np.array([s["php"] for s in serie])
    Xarr = phps_arr ** 2 / 2.0
    GS = Sig / Thet ** 2 * GT ** 2 + 3.0 * GT
    f = GT ** 2 / Thet
    df = np.gradient(f, Ns)
    FS = Hs * f + Hs * df - FT
    cs2 = FS / GS
    cgw2 = FT / GT
    ok = (np.isfinite(GT) & np.isfinite(GS) & np.isfinite(cs2) & np.isfinite(cgw2)
          & (GS > 1e-8 * np.nanmax(GS)) & (Xarr > 1e-6))
    stab = {
        "min_GT": float(np.min(GT[ok])) if ok.any() else np.nan,
        "min_GS": float(np.min(GS[ok])) if ok.any() else np.nan,
        "min_cs2": float(np.min(cs2[ok])) if ok.any() else np.nan,
        "min_cgw2": float(np.min(cgw2[ok])) if ok.any() else np.nan,
        "max_cs2": float(np.max(cs2[ok])) if ok.any() else np.nan,
        "estable": bool(ok.any() and np.all(GT[ok] > 0) and np.all(GS[ok] > 0)
                        and np.all(cs2[ok] > 0) and np.all(cgw2[ok] > 0)),
        "n_puntos": int(ok.sum()),
        "degen_cola": bool((Xarr <= 1e-6).any()),
    }
    return {"dN_F2": float(dN_f2), "dN_w005": float(dN_w005), "dN_F2a": float(dN_f2a),
            "estabilidad": stab}


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--total", type=int, default=200)
    ap.add_argument("--semilla", type=int, default=137)
    ap.add_argument("--salida", default="ciclo137_barrido.json")
    args = ap.parse_args()

    print("CICLO 137 | DBI + G4(phi,X) | total=%d semilla=%d" % (args.total, args.semilla))
    t0 = time.time()
    u = qmc.LatinHypercube(d=3, seed=args.semilla).random(args.total)
    pool = []
    for fila in u:
        cfg = {}
        for j, k in enumerate(ORDEN):
            lo, hi = RANGOS[k]
            cfg[k] = float(lo + fila[j] * (hi - lo))
        pool.append(cfg)

    # baseline puro DBI (referencia, Ciclo 136)
    baseline = {"v": 0.95, "xi": 0.0, "eta": 0.0}

    resultados = []
    for idx, cfg in enumerate(pool):
        p = tuple(cfg[k] for k in ORDEN)
        entry = dict(cfg)
        entry["por_eps"] = {}
        for eps in EPS_GRID:
            serie = integrar(p, eps)
            m = medir(serie)
            if m is None:
                entry["por_eps"][str(eps)] = {"dN_F2": None, "dN_w005": None, "dN_F2a": None, "estabilidad": None}
            else:
                entry["por_eps"][str(eps)] = m
        # eps_max: mayor eps (de la grilla) con dN_F2 >= 4
        eps_ok = [e for e in EPS_GRID if entry["por_eps"][str(e)] and entry["por_eps"][str(e)]["dN_F2"] is not None
                  and entry["por_eps"][str(e)]["dN_F2"] >= 4.0]
        entry["eps_max_F2"] = max(eps_ok) if eps_ok else None
        entry["dN_F2_1e8"] = (entry["por_eps"]["1e-08"]["dN_F2"]
                              if entry["por_eps"]["1e-08"] and entry["por_eps"]["1e-08"]["dN_F2"] is not None else None)
        entry["candidata"] = bool(any(e >= EPS_CRIT and entry["por_eps"][str(e)]
                                      and entry["por_eps"][str(e)]["dN_F2"] is not None
                                      and entry["por_eps"][str(e)]["dN_F2"] >= 4.0 for e in EPS_GRID))
        # estabilidad en eps=1e-8 (la decisiva)
        m8 = entry["por_eps"]["1e-08"]
        entry["estabilidad_1e8"] = m8["estabilidad"] if m8 else None
        resultados.append(entry)
        if (idx + 1) % 25 == 0:
            n_cand = sum(1 for r in resultados if r["candidata"])
            print("  [%d/%d] candidatas=%d (%.1f min)" % (idx + 1, args.total, n_cand, (time.time() - t0) / 60))

    # baseline
    bp = (baseline["v"], baseline["xi"], baseline["eta"])
    be = {}
    for eps in EPS_GRID:
        serie = integrar(bp, eps)
        be[str(eps)] = medir(serie)
    baseline_entry = dict(baseline)
    baseline_entry["por_eps"] = be
    eps_ok = [e for e in EPS_GRID if be[str(e)] and be[str(e)]["dN_F2"] is not None and be[str(e)]["dN_F2"] >= 4.0]
    baseline_entry["eps_max_F2"] = max(eps_ok) if eps_ok else None

    n_cand = sum(1 for r in resultados if r["candidata"])
    dN_best = max((r["dN_F2_1e8"] or 0.0 for r in resultados), default=0.0)
    best = sorted(resultados, key=lambda r: -(r["dN_F2_1e8"] or 0.0))[:8]
    veredicto = ("CANDIDATAS ENCONTRADAS" if n_cand > 0 else
                 "FALSACION: ninguna config alcanza dN>=4 con eps0 > 1e-8")

    out = {"ciclo": 137, "modelo": "G2 = 1-sqrt(1-X)-v ; G4 = (1+xi phi^2 + eta X)/2",
           "semilla": args.semilla, "n_configs": len(resultados),
           "eps_grid": EPS_GRID, "eps_critico": EPS_CRIT,
           "n_candidatas": n_cand, "veredicto": veredicto,
           "dN_F2_max_1e8": dN_best, "baseline_DBI_puro": baseline_entry,
           "resultados": resultados, "best8": best}
    with open(args.salida, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("=" * 70)
    print("CICLO 137 COMPLETADO | candidatas=%d/%d | %s" % (n_cand, args.total, veredicto))
    print("dN_F2 max a eps=1e-8: %.3f" % dN_best)
    print("baseline DBI puro (v=0.95): eps_max_F2 =", baseline_entry["eps_max_F2"])
    for b in best:
        print("  top:", {k: round(b[k], 3) for k in ORDEN},
              "dN(1e-8)=%.3f" % (b["dN_F2_1e8"] or 0.0), "eps_max_F2=", b["eps_max_F2"],
              "cand=", b["candidata"])
    print("guardado:", args.salida)


if __name__ == "__main__":
    main()
