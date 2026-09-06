# diagnosticar_errores_universalidad.py — Reclasifica configs 'error'/'colgados' de la
# campana universalidad: verifica si alpha>0.95 se alcanzo ANTES del fallo del integrador
# (overflow exp(-lambda Phi) en float64 del sistema ORIGINAL).
import json, os, sys, time, warnings
import numpy as np
from scipy.integrate import solve_ivp
warnings.simplefilter("ignore", RuntimeWarning)

BASE = r"C:\Users\Jairo Omar\AGI_Workspace"
H0 = 1.44e-60; LAMBD = 0.15; Om_m, Om_r = 0.315, 9.0e-5; rho_c0 = 3.0 * H0 ** 2
ALPHA_CRIT = 0.95

def derivs_orig(N, y, LAM):
    Phi, Pi, h, m, r = y
    # proteccion: si Phi muy negativo, V desborda -> devolver nan (detectado por solver)
    arg = -LAM * Phi
    V = rho_c0 * np.exp(arg) if arg < 700 else np.nan
    if not np.isfinite(V):
        return np.full(5, np.nan)
    X = 0.5 * (H0 * h * Pi) ** 2
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

def ic(w0, sg, LAM):
    rho_Phi0 = (1 - Om_m - Om_r) * rho_c0
    A0 = (1.0 + w0) * rho_Phi0 / 2.0
    X0 = 2.0 * A0 / (1 + np.sqrt(1 + 8 * A0 / LAMBD ** 4))
    Pi0 = sg * np.sqrt(2 * X0) / H0
    V0 = rho_Phi0 - X0 - 3 * X0 ** 2 / LAMBD ** 4
    return -np.log(V0 / rho_c0) / LAM, Pi0

# configs que dieron 'error' en la campana (de universalidad_borde.jsonl) + el colgado
error_candidates = [(2.25, -0.2), (2.5, -0.3), (3.0, -0.3), (3.0, 0.0),
                    (4.0, -0.5), (4.0, -0.3), (4.0, -0.2), (4.0, 0.2), (4.0, 0.5),
                    (5.0, -0.3), (6.0, 0.3), (6.0, 0.5)]

print("Diagnostico de configs 'error'/'colgados' (sistema ORIGINAL, overflow exp):")
for lam, w0 in error_candidates:
    Phi0, Pi0 = ic(w0, 1.0, lam)
    y0 = np.array([Phi0, Pi0, 1.0, Om_m, Om_r])
    t0 = time.time()
    try:
        # malla gruesa, sin t_eval para dejar que el solver elija; capturar estado final
        sol = solve_ivp(lambda N, y: derivs_orig(N, y, lam), [0.0, -50.0], y0,
                        method="BDF", rtol=1e-10, atol=1e-13, max_step=0.1, dense_output=True)
        ult = float(sol.t[-1])
        if sol.success:
            a = sol.y[1] ** 2 / 6.0
            idx = np.where(a > ALPHA_CRIT)[0]
            Ns = float(sol.t[idx[0]]) if len(idx) else None
            print("lam=%.2f w0=%+.2f: OK N_ult=%.2f N_s=%s alpha_max=%.6f (%.0fs)" % (
                lam, w0, ult, ("%.2f" % Ns) if Ns is not None else "nunca",
                float(a.max()) if len(a) else -1, time.time() - t0), flush=True)
        else:
            # fallo: examinar ultimo estado valido
            a = sol.y[1] ** 2 / 6.0
            idx = np.where(a > ALPHA_CRIT)[0]
            Ns = float(sol.t[idx[0]]) if len(idx) else None
            Phi_last = float(sol.y[0][-1]) if len(sol.y[0]) else float("nan")
            estado = "ruptura_antes_fallo" if (Ns is not None and Ns <= ult) else "sin_ruptura_antes_fallo"
            print("lam=%.2f w0=%+.2f: FALLO N_ult=%.2f N_s=%s alpha_max=%.6f Phi_last=%.1f -> %s (%.0fs)" % (
                lam, w0, ult, ("%.2f" % Ns) if Ns is not None else "nunca",
                float(a.max()) if len(a) else -1, Phi_last, estado, time.time() - t0), flush=True)
    except Exception as e:
        print("lam=%.2f w0=%+.2f: EXC %s (%.0fs)" % (lam, w0, str(e)[:60], time.time() - t0), flush=True)
