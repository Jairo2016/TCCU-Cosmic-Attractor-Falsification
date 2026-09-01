# TCCU_Eternity_Test_v1.5.23c.py
# Sistema reducido con restriccion EXACTA y aritmetica LOG-SIGNED (N -> -1000 sin overflow):
#   A = h^2 : punto fijo logA = logsumexp([log(m+r+z), log((Pi^2/6) A), log((kappa Pi^4/4) A^2)])
#   P/rho_c0 = (Pi^2/6)A + (kappa A^2 Pi^4)/12 - z + r/3   (signos separados)
#   A' = -3(A + P/rho_c0)  [continuidad];  h'/h = A'/(2A)
#   KG: Pi' = -hpH Pi - 3(1+u)Pi/(1+3u) + LAM V/((1+3u) H0^2 A)   (signo +, V_phi = -LAM V)
# Estado: [Phi, Pi, logm, logr, tau, ell]
import numpy as np
from scipy.integrate import solve_ivp
import sys, time

M_P = 1.0
H0 = 1.44e-60
LAMBDA = 0.15 * M_P
LAM = 5.0
kappa = H0 ** 2 / LAMBDA ** 4
Omega_m0, Omega_r0 = 0.315, 9.0e-5
Omega_Phi0 = 1.0 - Omega_m0 - Omega_r0
rho_c0 = 3.0 * M_P ** 2 * H0 ** 2
LN10 = np.log(10.0)
LOG2 = np.log(2.0); LOG3 = np.log(3.0)

def logadd(x, y):
    m = max(x, y)
    return m + np.log1p(np.exp(-abs(x - y))) if abs(x - y) < 700 else m

def slogadd(vals):
    """vals = [(signo, logmagnitud), ...] -> (signo, logmagnitud) de la suma."""
    lm = [v[1] for v in vals if v[1] > -1e300]
    if not lm:
        return 1.0, -np.inf
    m = max(lm)
    s = sum(sg * np.exp(l - m) for sg, l in vals if l > -1e300)
    if s == 0:
        return 1.0, -np.inf
    return (1.0 if s > 0 else -1.0), m + np.log(abs(s))

def solve_logA(logm, logr, Z, logPi2):
    """Punto fijo: logA = logsumexp([logc, log(alpha)+logA, log(beta)+2 logA])"""
    logc = logadd(logadd(logm, logr), Z)          # m + r + z (todos positivos)
    logalpha = logPi2 - LOG2 - np.log(3.0)         # Pi^2/6
    logbeta = np.log(kappa) + 2.0 * logPi2 - np.log(4.0)  # kappa Pi^4/4
    logA = logc
    for _ in range(6):
        t1 = logalpha + logA
        t2 = logbeta + 2.0 * logA
        logA_new = logadd(logadd(logc, t1), t2)
        if abs(logA_new - logA) < 1e-14:
            logA = logA_new
            break
        logA = logA_new
    return logA

def derivatives(N, y):
    Phi, Pi, logm, logr, tau, ell = y
    if not np.all(np.isfinite(y)):
        return np.full(6, np.nan)
    logPi2 = 2.0 * np.log(abs(Pi) + 1e-300)
    Z = -LAM * Phi
    logA = solve_logA(logm, logr, Z, logPi2)
    if not np.isfinite(logA):
        return np.full(6, np.nan)
    # u = kappa A Pi^2
    logu = np.log(kappa) + logA + logPi2
    log1u = logadd(0.0, logu)
    log1_3u = logadd(0.0, logu + LOG3)
    # P/rho_c0 = (Pi^2/6)A + (kappa A^2 Pi^4)/12 - z + r/3
    lp_alpha = logPi2 - LOG2 - np.log(3.0) + logA                 # + (Pi^2/6) A
    lp_beta = np.log(kappa) + 2.0 * logA + 2.0 * logPi2 - np.log(12.0)  # + kappa A^2 Pi^4/12
    lp_z = Z                                                       # - z
    lp_r = logr - np.log(3.0)                                      # + r/3
    sP, lP = slogadd([(1.0, lp_alpha), (1.0, lp_beta), (-1.0, lp_z), (1.0, lp_r)])
    # S = A + P/rho_c0
    sS, lS = slogadd([(1.0, logA), (sP, lP)])
    # A' = -3 S ;  h'/h = A'/(2A)
    sAp = -sS
    lAp = LOG3 + lS
    lhpH = lAp - LOG2 - logA
    shpH = sAp
    # KG
    # term1 = -hpH * Pi
    st1, lt1 = -shpH, lhpH + np.log(abs(Pi) + 1e-300)
    # term2 = -3(1+u)Pi/(1+3u)
    st2, lt2 = -np.sign(Pi) if Pi != 0 else 1.0, LOG3 + log1u - log1_3u + np.log(abs(Pi) + 1e-300)
    # term3 = + LAM V/((1+3u) H0^2 A)  = LAM rho_c0 e^{Z}/((1+3u) H0^2 A)
    st3, lt3 = 1.0, np.log(LAM) + np.log(rho_c0) + Z - log1_3u - 2.0 * np.log(H0) - logA
    sPi, lPi = slogadd([(st1, lt1), (st2, lt2), (st3, lt3)])
    dPi = sPi * np.exp(lPi) if lPi > -700 else 0.0
    dPhi = Pi
    dlogm = -3.0
    dlogr = -4.0
    half = 0.5 * logA
    dtau = np.exp(N - half)
    dell = np.exp(2.0 * N - half)
    return np.array([dPhi, dPi, dlogm, dlogr, dtau, dell])

def diagnostico(N, y):
    Phi, Pi, logm, logr, tau, ell = y
    logPi2 = 2.0 * np.log(abs(Pi) + 1e-300)
    Z = -LAM * Phi
    logA = solve_logA(logm, logr, Z, logPi2)
    logu = np.log(kappa) + logA + logPi2
    log1u = logadd(0.0, logu)
    # w = P/rho  ;  rho/rho_c0 = A (restriccion)
    lp_alpha = logPi2 - LOG2 - np.log(3.0) + logA
    lp_beta = np.log(kappa) + 2.0 * logA + 2.0 * logPi2 - np.log(12.0)
    sP, lP = slogadd([(1.0, lp_alpha), (1.0, lp_beta), (-1.0, Z), (1.0, logr - np.log(3.0))])
    sS, lS = slogadd([(1.0, logA), (sP, lP)])
    lw = lP - logA                      # w = (P/rho_c0)/A  (P/rho_c0 = P_n, rho/rho_c0 = A)
    w = sP * np.exp(lw) if lw > -700 else 0.0
    sAp, lAp = -sS, LOG3 + lS
    lhpH = lAp - LOG2 - logA
    dlogh = sAp * np.exp(lhpH) if lhpH > -700 else 0.0
    # K = 12 A^2 [(dlogh+1)^2 + 1]   (A = h^2)
    logK = np.log(12.0) + 2.0 * logA + np.log((dlogh + 1.0) ** 2 + 1.0)
    return dict(logA=logA, logu=logu, w=w, logK=logK, dlogh=dlogh)

def compute_initial_quantities(w0, sign_q):
    rho_Phi0 = Omega_Phi0 * rho_c0
    A0 = (1.0 + w0) * rho_Phi0 / 2.0
    X0 = (2.0 * A0) / (1.0 + np.sqrt(1.0 + 8.0 * A0 / LAMBDA ** 4))
    q0 = sign_q * np.sqrt(2.0 * X0) / H0
    V_eff0 = rho_Phi0 - X0 - 3.0 * X0 ** 2 / LAMBDA ** 4
    if V_eff0 <= 0:
        return None
    v0 = V_eff0 / rho_c0
    Phi0 = -np.log(v0) / LAM
    return Phi0, q0

def run_trajectory(w0, sign_q, N_min=-1000, method='BDF', tol=1e-10, max_step=0.1):
    init = compute_initial_quantities(w0, sign_q)
    if init is None:
        return None
    Phi0, Pi0 = init
    y0 = np.array([Phi0, Pi0, np.log(Omega_m0), np.log(Omega_r0), 0.0, 0.0])
    N_control = -np.logspace(0, np.log10(-N_min), 400)
    t_eval = np.r_[0.0, np.sort(N_control)[::-1]]
    return solve_ivp(derivatives, [0.0, N_min], y0, method=method,
                     t_eval=t_eval, rtol=tol, atol=tol * 1e-3, max_step=max_step)

def auditar_config(w0, sign_q, N_min=-1000, method='BDF', tol=1e-10):
    sol = run_trajectory(w0, sign_q, N_min, method, tol)
    if sol is None:
        return {'status': 'FAIL', 'reason': 'Invalid IC'}
    if not sol.success:
        return {'status': 'FAIL', 'reason': '%s (N_ult=%.1f)' % (sol.message, sol.t[-1])}
    N = sol.t
    diag = diagnostico(N, sol.y)
    I_tau = -sol.y[4]; I_ell = -sol.y[5]
    n_tail = max(30, len(N) // 4)
    x = -N[-n_tail:]; yk = diag['logK'][-n_tail:] / LN10
    mask = np.isfinite(yk)
    if np.sum(mask) < 30:
        slope, r2 = np.nan, 0.0
    else:
        slope, b0 = np.polyfit(x[mask], yk[mask], 1)
        yf = slope * x[mask] + b0
        ss_res = np.sum((yk[mask] - yf) ** 2); ss_tot = np.sum((yk[mask] - np.mean(yk[mask])) ** 2)
        r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else 0.0
    w_tail = diag['w'][-n_tail:]
    w_mean = float(np.mean(w_tail[np.isfinite(w_tail)])) if np.any(np.isfinite(w_tail)) else np.nan
    return {'status': 'OK', 'w0': w0, 'sign': sign_q, 'method': method,
            'N_ultimo': float(N[-1]),
            'I_tau_final': float(I_tau[-1]), 'I_ell_final': float(I_ell[-1]),
            'K_slope': slope, 'K_r2': r2, 'w_cola': w_mean,
            'logA_final': float(diag['logA'][-1]), 'Phi_final': float(sol.y[0][-1]),
            'Pi_final': float(sol.y[1][-1])}

if __name__ == "__main__":
    print("TCCU-0 v1.5.23c: restriccion exacta + log-signed (N=-1000)")
    for w0 in [-0.3, -0.1, 0.0, 0.1]:
        for sg in [1, -1]:
            r = auditar_config(w0, sg, -1000.0, 'BDF', 1e-10)
            if r['status'] == 'OK':
                print("  w0=%+.2f sign=%+d -> N_ult=%.1f slope=%.3f r2=%.4f w_cola=%.3f tau=%.3e ell=%.3e logA_f=%.1f Pi_f=%.2e" % (
                    w0, sg, r['N_ultimo'], r['K_slope'], r['K_r2'], r['w_cola'],
                    r['I_tau_final'], r['I_ell_final'], r['logA_final'], r['Pi_final']))
            else:
                print("  w0=%+.2f sign=%+d -> %s" % (w0, sg, r.get('reason', '?')))
