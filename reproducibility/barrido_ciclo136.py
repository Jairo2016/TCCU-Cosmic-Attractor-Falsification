# -*- coding: utf-8 -*-
"""
CICLO 136 — Test DBI / cinetica pura + offset constante.  v2: integracion en eps=1-u
(evita perdida de precision float64 cerca del limite DBI u~1).
Modelo: G2(X) = L^4*(1 - sqrt(1 - X/L^4)) - V0,  G4 = 1/2, G3 = G5 = 0.
Escala: L^4 = 1.  u = X/L^4 (u en [0,1)),  s = sqrt(1-u) = sqrt(eps),  v = V0/L^4.
Friedmann: 3H^2 = rho = (1/s - 1) + v.
KG (puro cinetico): du/dN = -6u(1-u)  =>  deps/dN = +6(1-eps)eps.
EoS: w = (1 - s - v)/(1/s - 1 + v).
Criterio F2 congelado: |w| < 0.05  y  |dln rho/dN + 3| < 0.05, ventana contigua dN >= 4.
F2a: dN >= 2 y |dw/dN| < 0.05.
Clases CI: (a) near-bound u0 = 1-eps0, eps0 log-uniforme en [1e-14, 1e-2];
          (b) generic u0 uniforme en (0, 0.999].
Salida: ciclo136_barrido.json + resumen consola.
"""
import json, math
import numpy as np

SEED = 136
rng = np.random.default_rng(SEED)
dN = 0.002
NMAX = 80.0

def w_of_eps(eps, v):
    s = math.sqrt(max(eps, 1e-30))
    return (1.0 - s - v) / ((1.0 / s) - 1.0 + v)

def rho_of_eps(eps, v):
    s = math.sqrt(max(eps, 1e-30))
    return (1.0 / s) - 1.0 + v

def eps_closed(eps0, n):
    K = (1.0 - eps0) / eps0
    return 1.0 / (1.0 + K * math.exp(-6.0 * n))

def integrate(eps0):
    Ns = [0.0]; Es = [eps0]
    e = eps0; n = 0.0
    while n < NMAX and e < 1.0 - 1e-13:
        k1 = 6.0 * (1.0 - e) * e
        k2 = 6.0 * (1.0 - (e + 0.5 * dN * k1)) * (e + 0.5 * dN * k1)
        k3 = 6.0 * (1.0 - (e + 0.5 * dN * k2)) * (e + 0.5 * dN * k2)
        k4 = 6.0 * (1.0 - (e + dN * k3)) * (e + dN * k3)
        e = e + (dN / 6.0) * (k1 + 2.0 * k2 + 2.0 * k3 + k4)
        n += dN
        Ns.append(n); Es.append(e)
    return np.array(Ns), np.array(Es)

def longest_run(Ns, mask):
    best = 0.0; cur = None
    for i, o in enumerate(mask):
        if o:
            if cur is None: cur = Ns[i]
        else:
            if cur is not None:
                best = max(best, Ns[i - 1] - cur); cur = None
    if cur is not None:
        best = max(best, Ns[-1] - cur)
    return best

def measure(Ns, Es, v):
    n = len(Es)
    ws = np.array([w_of_eps(e, v) for e in Es])
    rs = np.array([rho_of_eps(e, v) for e in Es])
    dlnr = np.zeros(n)
    for i in range(1, n - 1):
        dlnr[i] = (math.log(rs[i + 1]) - math.log(rs[i - 1])) / (2.0 * dN)
    dlnr[0] = dlnr[1]; dlnr[-1] = dlnr[-2]
    dw = np.zeros(n)
    for i in range(1, n - 1):
        dw[i] = (ws[i + 1] - ws[i - 1]) / (2.0 * dN)
    dw[0] = dw[1]; dw[-1] = dw[-2]
    m_w005 = np.abs(ws) < 0.05
    m_f2 = m_w005 & (np.abs(dlnr + 3.0) < 0.05)
    m_f2a = m_w005 & (np.abs(dw) < 0.05)
    return {
        "dN_w005": longest_run(Ns, m_w005),
        "dN_F2": longest_run(Ns, m_f2),
        "dN_F2a": longest_run(Ns, m_f2a),
    }

V_GRID = [0.90, 0.92, 0.94, 0.95, 0.96, 0.97, 0.98, 0.99, 0.995]
EPS_LOG_LO, EPS_LOG_HI = -14.0, -2.0
N_PER_V = 20

configs = []
for v in V_GRID:
    for _ in range(N_PER_V):
        eps0 = 10.0 ** rng.uniform(EPS_LOG_LO, EPS_LOG_HI)
        configs.append({"v": v, "eps0": eps0, "cls": "near"})
    for _ in range(N_PER_V):
        u0 = float(rng.uniform(0.0, 0.999))
        configs.append({"v": v, "eps0": 1.0 - u0, "cls": "generic"})

results = []
ver_max = 0.0; ver_arg = None
for c in configs:
    Ns, Es = integrate(c["eps0"])
    for i in range(0, len(Es), 50):
        d = abs(Es[i] - eps_closed(c["eps0"], Ns[i]))
        if d > ver_max:
            ver_max = d; ver_arg = (c["v"], c["eps0"], Ns[i])
    m = measure(Ns, Es, c["v"])
    c.update(m)
    results.append(c)

thresholds = {}
for v in [0.90, 0.95, 0.98, 0.99]:
    best_ok = None
    for e in np.arange(-14.0, -6.99, 0.1):
        e0 = 10.0 ** e
        Ns, Es = integrate(e0)
        m = measure(Ns, Es, v)
        if m["dN_F2"] >= 4.0:
            best_ok = e0
    thresholds[str(v)] = {"max_eps0_F2": best_ok}

agg = {}
for v in V_GRID:
    sub = [r for r in results if r["v"] == v]
    agg[str(v)] = {
        "F2_near": int(sum(1 for r in sub if r["cls"] == "near" and r["dN_F2"] >= 4.0)),
        "F2_generic": int(sum(1 for r in sub if r["cls"] == "generic" and r["dN_F2"] >= 4.0)),
        "F2a_near": int(sum(1 for r in sub if r["cls"] == "near" and r["dN_F2a"] >= 2.0)),
        "F2a_generic": int(sum(1 for r in sub if r["cls"] == "generic" and r["dN_F2a"] >= 2.0)),
        "dNmax_F2_near": float(max(r["dN_F2"] for r in sub if r["cls"] == "near")),
        "dNmax_F2_generic": float(max(r["dN_F2"] for r in sub if r["cls"] == "generic")),
        "dNmax_w005_near": float(max(r["dN_w005"] for r in sub if r["cls"] == "near")),
        "dNmax_w005_generic": float(max(r["dN_w005"] for r in sub if r["cls"] == "generic")),
    }
best_near = max((r for r in results if r["cls"] == "near"), key=lambda r: r["dN_F2"])
best_gen = max((r for r in results if r["cls"] == "generic"), key=lambda r: r["dN_F2"])
n_near = int(sum(1 for r in results if r["cls"] == "near"))
n_gen = int(sum(1 for r in results if r["cls"] == "generic"))

out = {
    "ciclo": 136, "modelo": "DBI pura cinetica + offset: G2 = L^4(1-sqrt(1-X/L^4)) - V0, G4=1/2",
    "integracion": "eps=1-u (precisa cerca del limite DBI)", "seed": SEED,
    "n_configs": len(results),
    "verificacion_RK4_vs_cerrada_max": ver_max, "verificacion_argmax": ver_arg,
    "por_v": agg,
    "umbral_eps0_para_F2": thresholds,
    "mejor_near": best_near,
    "mejor_generic": best_gen,
    "resumen": {
        "F2_total_near": int(sum(1 for r in results if r["cls"] == "near" and r["dN_F2"] >= 4.0)),
        "F2_total_generic": int(sum(1 for r in results if r["cls"] == "generic" and r["dN_F2"] >= 4.0)),
        "F2a_total_near": int(sum(1 for r in results if r["cls"] == "near" and r["dN_F2a"] >= 2.0)),
        "F2a_total_generic": int(sum(1 for r in results if r["cls"] == "generic" and r["dN_F2a"] >= 2.0)),
        "dNmax_F2_global": float(max(r["dN_F2"] for r in results)),
        "dNmax_w005_global": float(max(r["dN_w005"] for r in results)),
    },
}
with open(r"C:\Users\Jairo Omar\AGI_Workspace\ciclo136_barrido.json", "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=2)

print("CICLO 136 v2 (eps=1-u) - DBI pura cinetica + offset")
print("verificacion RK4 vs cerrada (max |de|): %.3e en %s" % (ver_max, ver_arg))
print("=" * 78)
print("  v    F2_near F2_gen F2a_near F2a_gen dNmax_near dNmax_gen w005_near w005_gen")
for v in V_GRID:
    a = agg[str(v)]
    print(" %.3f  %5d %6d  %7d %7d   %8.2f  %8.2f  %8.2f  %8.2f" % (
        v, a["F2_near"], a["F2_generic"], a["F2a_near"], a["F2a_generic"],
        a["dNmax_F2_near"], a["dNmax_F2_generic"], a["dNmax_w005_near"], a["dNmax_w005_generic"]))
print("=" * 78)
print("mejor near: v=%.3f eps0=%.3e dN_F2=%.2f dN_w005=%.2f" % (
    best_near["v"], best_near["eps0"], best_near["dN_F2"], best_near["dN_w005"]))
print("mejor generic: v=%.3f eps0=%.5f dN_F2=%.2f dN_w005=%.2f" % (
    best_gen["v"], best_gen["eps0"], best_gen["dN_F2"], best_gen["dN_w005"]))
print("F2 total: near=%d/%d  generic=%d/%d   F2a: near=%d/%d generic=%d/%d" % (
    out["resumen"]["F2_total_near"], n_near, out["resumen"]["F2_total_generic"], n_gen,
    out["resumen"]["F2a_total_near"], n_near, out["resumen"]["F2a_total_generic"], n_gen))
print("umbral eps0 (max con dN_F2>=4):")
for k, t in thresholds.items():
    val = t["max_eps0_F2"]
    print("  v=%s -> eps0 <= %s" % (k, ("%.2e" % val) if val is not None else "ninguno en [1e-14,1e-7]"))
