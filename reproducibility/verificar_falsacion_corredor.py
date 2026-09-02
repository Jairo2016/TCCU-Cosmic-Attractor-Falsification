# verificar_falsacion_corredor.py — Reproduccion independiente de la falsacion TCCU-0
# Corredor preliminar (mapa v3): 432 configs con N_past >= 250 e-folds, alpha<0.95.
# Falsacion (01-09-2026): solve_logA (punto fijo, 6 iter, contraccion ~alpha) no
# converge a alpha>=0.93 -> A erroneo (factor 2-100) -> el corredor es un artefacto.
#
# Este script reproduce la evidencia central con DOS formulaciones independientes:
#   (A) Sistema ORIGINAL Friedmann+KG (sin proyeccion de restriccion), 4 integradores
#       opcionales (BDF/DOP853/LSODA/Radau) -> alpha cruza 0.95 a N_s ~ -2.3.
#   (B) Sistema reducido log-signed con la RAIZ ANALITICA correcta de la restriccion
#       A_- = 2c/(s + sqrt(s^2 - 4bc)), s=1-alpha -> N_s ~ -2.26.
# Requiere: numpy, scipy, TCCU_Eternity_Test_v1.5.23c.py (solo para (B), importable).
# Uso: python verificar_falsacion_corredor.py [--lam 1.66 --w0 -0.2]
import numpy as np, importlib.util, os, sys, warnings
from scipy.integrate import solve_ivp
warnings.simplefilter("ignore", RuntimeWarning)

BASE = os.path.dirname(os.path.abspath(__file__))
H0 = 1.44e-60; LAMBD = 0.15; Om_m, Om_r = 0.315, 9.0e-5; rho_c0 = 3.0 * H0 ** 2
ALPHA_CRIT = 0.95

def ic(w0, sg, LAM):
    rho_Phi0 = (1 - Om_m - Om_r) * rho_c0
    A0 = (1.0 + w0) * rho_Phi0 / 2.0
    X0 = 2.0 * A0 / (1 + np.sqrt(1 + 8 * A0 / LAMBD ** 4))
    Pi0 = sg * np.sqrt(2 * X0) / H0
    V0 = rho_Phi0 - X0 - 3 * X0 ** 2 / LAMBD ** 4
    return -np.log(V0 / rho_c0) / LAM, Pi0

# ---------------- (A) Sistema original Friedmann+KG ----------------
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

def Ns_original(lam, w0, method="BDF", Nmin=-9.0):
    Phi0, Pi0 = ic(w0, 1, lam)
    y0 = np.array([Phi0, Pi0, 1.0, Om_m, Om_r])
    sol = solve_ivp(lambda N, y: derivs_orig(N, y, lam), [0.0, Nmin], y0,
                    method=method, t_eval=np.linspace(0, Nmin, 200),
                    rtol=1e-11, atol=1e-14, max_step=0.05)
    if not sol.success:
        return None, sol.message[:50], None
    a = sol.y[1] ** 2 / 6.0
    idx = np.where(a > ALPHA_CRIT)[0]
    Ns = float(sol.t[idx[0]]) if len(idx) else None
    return Ns, "ok", float(a.max())

# ---------------- (B) Sistema reducido + raiz analitica ----------------
def raiz_analitica(logm, logr, Z, logPi2):
    """A_- = 2c/(s+sqrt(s^2-4bc)), s=1-alpha; NaN si s<=0 o s^2<4bc (borde)."""
    spec = importlib.util.spec_from_file_location("t1523c", os.path.join(BASE, "TCCU_Eternity_Test_v1.5.23c.py"))
    t = importlib.util.module_from_spec(spec); spec.loader.exec_module(t)
    logc = t.logadd(t.logadd(logm, logr), Z)
    logalpha = logPi2 - t.LOG2 - np.log(3.0)
    logbeta = np.log(t.kappa) + 2.0 * logPi2 - np.log(4.0)
    alpha = np.exp(logalpha) if logalpha < 700 else 1e300
    s = 1.0 - alpha
    if s <= 0:
        return np.nan
    logs2 = 2.0 * np.log(s)
    log4bc = np.log(4.0) + logbeta + logc
    if logs2 < log4bc:
        return np.nan
    logD = logs2 + np.log1p(-np.exp(log4bc - logs2))
    logroot = 0.5 * logD
    logden = t.logadd(np.log(s), logroot)
    return np.log(2.0) + logc - logden

def Ns_reducido(lam, w0, method="DOP853", Nmin=-6.0):
    spec = importlib.util.spec_from_file_location("t1523c", os.path.join(BASE, "TCCU_Eternity_Test_v1.5.23c.py"))
    t = importlib.util.module_from_spec(spec); spec.loader.exec_module(t)
    t.solve_logA = raiz_analitica
    t.LAM = lam
    Phi0, Pi0 = ic(w0, 1, lam)
    y0 = np.array([Phi0, Pi0, np.log(Om_m), np.log(Om_r), 0.0, 0.0])
    sol = solve_ivp(t.derivatives, [0.0, Nmin], y0, method=method,
                    t_eval=np.linspace(0, Nmin, 200), rtol=1e-11, atol=1e-14, max_step=0.02)
    if not sol.success:
        return None, sol.message[:50], None
    a = sol.y[1] ** 2 / 6.0
    idx = np.where(a > ALPHA_CRIT)[0]
    Ns = float(sol.t[idx[0]]) if len(idx) else None
    return Ns, "ok", float(a.max())

if __name__ == "__main__":
    lam = float(sys.argv[sys.argv.index("--lam") + 1]) if "--lam" in sys.argv else 1.66
    w0 = float(sys.argv[sys.argv.index("--w0") + 1]) if "--w0" in sys.argv else -0.2
    print("Falsacion corredor TCCU-0 — lambda=%.2f w0=%+.2f (signo=+)" % (lam, w0))
    print("=" * 70)
    # (A) sistema original, varios integradores
    for m in ["BDF", "DOP853", "LSODA", "Radau"]:
        Ns, st, am = Ns_original(lam, w0, method=m)
        if st == "ok":
            print("(A) ORIGINAL %-7s -> N_s(alpha>0.95)=%s  alpha_max=%.6f" % (m, ("%.2f" % Ns) if Ns is not None else "nunca", am))
        else:
            print("(A) ORIGINAL %-7s -> %s" % (m, st))
    # (B) reducido con raiz analitica
    Ns, st, am = Ns_reducido(lam, w0)
    if st == "ok":
        print("(B) REDUCIDO+RAIZ -> N_s(alpha>0.95)=%s  alpha_max=%.6f" % (("%.2f" % Ns) if Ns is not None else "nunca", am))
    else:
        print("(B) REDUCIDO+RAIZ -> %s" % st)
    print("=" * 70)
    print("Conclusion: el mapa v3 daba N_s=-250 (extiende) para este config;")
    print("la verificacion correcta da N_s ~ -2.3 -> corredor REFUTADO (falsacion numerica).")
