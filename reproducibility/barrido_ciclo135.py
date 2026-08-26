# barrido_ciclo135.py — CICLO 135: barrido exploratorio (familia hibrida + acoplamiento no minimo G4(phi,X))
# Ansatz: V = V0(e^{-lam phi} + al phi^2 e^{-be phi}); G4 = (1 + xi phi^2 + eta X/Lam^4)/2
# EOM de fondo: derivadas simbolicamente (derivar_horndeski.py; verificadas en el limite k-essence).
# Criterios: F2a (|w|<0.05, dN>=2, |dw/dN|<0.05) y F2b (orbitas recurrentes hacia w~0).
# w_eff = -1 - 2 Hdot/(3 H^2)  (definicion cinematica; en el limite minimal coincide con w_phi).
# Muestreo: hipercubo latino estratificado + surrogate (GPR) por lotes.
import json
import os
import sys
import time

import numpy as np
from scipy.optimize import brentq
from scipy.stats import qmc
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, ConstantKernel, WhiteKernel

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import derivar_horndeski as DH  # expone E_fn, P_fn, Ef_fn

RANGOS = {
    "lam": (0.5, 3.0), "al": (0.1, 1.5), "be": (0.5, 2.0),
    "xi": (-1.0, 1.0), "eta": (-0.5, 0.5), "Lam": (0.5, 2.0),
}
ORDEN = ["lam", "al", "be", "xi", "eta", "Lam"]
V0 = 1.0
NMAX = 10.0     # e-foldings a integrar
DN = 0.02       # paso en N=ln a
H_MAX = 30.0


def constraint_H(H, a, phi, php, p):
    return DH.E_fn(a, a * H, phi, php, *p)


def solve_H(a, phi, php, p):
    f0 = constraint_H(0.0, a, phi, php, p)
    for Hm in (H_MAX, 60.0, 120.0):
        f1 = constraint_H(Hm, a, phi, php, p)
        if f0 * f1 < 0:
            try:
                return brentq(constraint_H, 0.0, Hm, args=(a, phi, php, p))
            except ValueError:
                return np.nan
    # si no cambia de signo, devolver raiz por minimo de |E|
    hs = np.linspace(0.0, H_MAX, 200)
    vals = np.array([constraint_H(h, a, phi, php, p) for h in hs])
    return float(hs[np.argmin(np.abs(vals))])


def solve_derivs(a, H, phi, php, p):
    ap = a * H
    P0 = DH.P_fn(a, ap, 0.0, phi, php, 0.0, *p)
    E0 = DH.Ef_fn(a, ap, 0.0, phi, php, 0.0, *p)
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
    return np.array([php / H, phpp / H])  # d/dN (phi, php)


def integrar(p, phi0=1.0, php0=0.05, nmax=NMAX, dn=DN):
    a = 1.0
    N = 0.0
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
        serie.append({"N": round(N, 4), "w": float(w), "phi": float(estado[0]), "php": float(estado[1])})
        # RK4 en N
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
        if abs(estado[1]) > 1e6 or abs(estado[0]) > 50:
            break
    return serie


def evaluar_f2(serie):
    """F2a: ventana |w|<0.05 con dN>=2 y max|dw/dN|<0.05. F2b: reentradas a |w|<0.05."""
    if not serie:
        return {"F2a": False, "F2b": False, "dN_max": 0.0, "dw_min": 99.0, "reentradas": 0}
    w = np.array([s["w"] for s in serie])
    N = np.array([s["N"] for s in serie])
    dw = np.abs(np.diff(w)) / np.maximum(np.diff(N), 1e-6)
    en_ventana = np.abs(w) < 0.05
    # ventanas
    ventanas = []
    i = 0
    while i < len(en_ventana):
        if en_ventana[i]:
            j = i
            while j + 1 < len(en_ventana) and en_ventana[j + 1]:
                j += 1
            ventanas.append((N[i], N[j]))
            i = j + 1
        else:
            i += 1
    dN_max = max((b - a for a, b in ventanas), default=0.0)
    # pendiente maxima dentro de la ventana mas larga
    dw_max_ventana = 99.0
    if ventanas:
        a0, b0 = max(ventanas, key=lambda v: v[1] - v[0])
        sel = (N[:-1] >= a0) & (N[:-1] <= b0)
        if np.any(sel):
            dw_max_ventana = float(np.max(dw[sel]))
    f2a = dN_max >= 2.0 and dw_max_ventana < 0.05
    f2b = len(ventanas) >= 2  # reentrada
    return {"F2a": bool(f2a), "F2b": bool(f2b), "dN_max": float(dN_max),
            "dw_max_ventana": float(dw_max_ventana), "reentradas": len(ventanas)}


def muestrear(n, semilla=135):
    """hipercubo latino en los 6 parametros -> lista de dicts."""
    u = qmc.LatinHypercube(d=6, seed=semilla).random(n)
    out = []
    for fila in u:
        cfg = {}
        for j, k in enumerate(ORDEN):
            lo, hi = RANGOS[k]
            cfg[k] = float(lo + fila[j] * (hi - lo))
        out.append(cfg)
    return out


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--total", type=int, default=200)
    ap.add_argument("--lote", type=int, default=20)
    ap.add_argument("--semilla", type=int, default=135)
    ap.add_argument("--salida", default="ciclo135_barrido.json")
    args = ap.parse_args()

    print("CICLO 135 | total=%d lote=%d" % (args.total, args.lote))
    t0 = time.time()
    pool = muestrear(args.total, semilla=args.semilla)
    kernel = ConstantKernel(1.0) * RBF(np.ones(6) * 0.5) + WhiteKernel(1e-3)
    resultados = []
    evaluadas = []
    idx = 0
    while idx < args.total:
        lote = pool[idx:idx + args.lote]
        if evaluadas and len(evaluadas) >= 20:
            # surrogate: predecir 'promesa' (dN_max) sobre el pool restante y reordenar
            try:
                X = np.array([[c[k] for k in ORDEN] for c in evaluadas])
                y = np.array([r["dN_max"] for r in evaluadas])
                gp = GaussianProcessRegressor(kernel=kernel, normalize_y=True, n_restarts_optimizer=1)
                gp.fit(X, y)
                rest = pool[idx + args.lote:]
                Xr = np.array([[c[k] for k in ORDEN] for c in rest])
                yp, sp = gp.predict(Xr, return_std=True)
                orden = np.argsort(-(yp - 1.0 * sp))  # UCB: promesa + exploracion
                rest = [rest[i] for i in orden]
                pool[idx + args.lote:] = rest
                print(f"  surrogate GP aplicado (lote {len(evaluadas)//args.lote})")
            except Exception as e:
                print("  surrogate skip:", str(e)[:60])
        for cfg in lote:
            p = tuple(cfg[k] for k in ORDEN) + (V0,)
            serie = integrar(p)
            f2 = evaluar_f2(serie)
            res = {**cfg, **f2}
            resultados.append({**res, "configs_evaluadas": len(resultados) + 1})
            evaluadas.append(res)
            idx += 1
            if len(resultados) % args.lote == 0:
                n_f2a = sum(1 for r in resultados if r["F2a"])
                n_f2b = sum(1 for r in resultados if r["F2b"])
                dN_best = max((r["dN_max"] for r in resultados), default=0.0)
                print(f"  [{len(resultados)}/200] F2a={n_f2a} F2b={n_f2b} dN_max_best={dN_best:.3f} ({(time.time()-t0)/60:.1f} min)")
    # resumen
    n_f2a = sum(1 for r in resultados if r["F2a"])
    n_f2b = sum(1 for r in resultados if r["F2b"])
    dN_max = max((r["dN_max"] for r in resultados), default=0.0)
    best5 = sorted(resultados, key=lambda r: -r["dN_max"])[:5]
    with open(args.salida, "w", encoding="utf-8") as f:
        json.dump({"ciclo": 135, "total": len(resultados), "F2a": n_f2a, "F2b": n_f2b,
                   "dN_max_global": dN_max, "resultados": resultados, "best5": best5}, f, indent=1, ensure_ascii=False)
    print("=" * 60)
    print(f"CICLO 135 COMPLETADO: {len(resultados)} configs | F2a={n_f2a} F2b={n_f2b} | dN_max={dN_max:.4f}")
    for b in best5:
        print("  top:", {k: round(b[k], 4) for k in ORDEN}, "dN_max=", round(b["dN_max"], 4), "F2a=", b["F2a"])
    print("guardado:", args.salida)


if __name__ == "__main__":
    main()
