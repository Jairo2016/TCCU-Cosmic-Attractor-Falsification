# TCCU_Eternity_Test_v1.5.22.py
# Correcciones de la auditoria independiente (v1.5.21 -> v1.5.22):
#  [1] KG original con signo correcto: Pi' = -(h'/h)Pi - 3(1+u)Pi/(1+3u) + LAM*V/((1+3u) H0^2 h^2)
#  [2] S' exacta:  S' = [2 + 1.5 D/E^2 - 3(1+u)/(1+3u)] S + 3 L sqrt(k) z e^{6N}/((1+3u) E^2)
#  [3] EF2 exacta: E^2 = Om_m e^N + Om_r + E^2 S^2 e^{-4N}/(6k) + E^4 S^4 e^{-12N}/(4k) + z e^{4N}
#  [4] Formas log-estables para u, D, EF2 (N -> -1000 sin overflow)
#  [5] Bateria de identidades algebraicas automatica (Nivel 0) ANTES de integrar
#  [6] signo de S: se integra |S| via logS y el cruce - -> + se detecta (b>0 siempre)
#  [7] Convergencia: criterios relativo + absoluto + estabilidad de la cola (20% final)
#
# IMPORTANTE (26-08, CIERRE TCCU-0): la bateria de identidades de ESTE archivo quedo
# CERTIFICADA (8/8 PASS). Sin embargo, la campana profunda aqui (N=-1000, K-slope 8/ln10)
# queda SUPERSEDED: con la KG corregida el fondo TCCU-0 (lambda=5) se rompe en el borde
# cinetico Pi^2=6 a N_s ~ -0.08..-0.50 (ver v1.5.23c y CIERRE_TCCU0.md). No ejecutar
# esta campana como test de eternidad; usar TCCU_Eternity_Test_v1.5.23c.py (medidor N_s).
import numpy as np
from scipy.integrate import solve_ivp
from collections import defaultdict
import sys, time

# =============================================================================
# 1. PARAMETROS FIJOS (TCCU-0)
# =============================================================================
M_P = 1.0
H0 = 1.44e-60
LAMBDA = 0.15 * M_P
LAM = 5.0
kappa = H0 ** 2 / LAMBDA ** 4
sqrt_kappa = np.sqrt(kappa)

Omega_m0 = 0.315
Omega_r0 = 9.0e-5
Omega_Phi0 = 1.0 - Omega_m0 - Omega_r0
rho_c0 = 3.0 * M_P ** 2 * H0 ** 2

LN10 = np.log(10.0)

# =============================================================================
# 2. CONDICIONES INICIALES (identicas a v1.5.21)
# =============================================================================
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
    Pi0 = q0
    Z0 = np.log(v0)
    if not np.isfinite(Z0):
        return None
    return Phi0, Pi0, v0, Z0

# =============================================================================
# 3. SISTEMA ORIGINAL NORMALIZADO (KG CORREGIDA)
# =============================================================================
def derivatives_original_corrected(N, y):
    Phi, Pi, h, m, r, tau, ell = y
    X = 0.5 * (H0 * h * Pi) ** 2
    L4 = LAMBDA ** 4
    V = rho_c0 * np.exp(-LAM * Phi)
    rho_phi = X + 3.0 * X ** 2 / L4 + V
    p_phi = X + X ** 2 / L4 - V
    rho_tot_n = m + r + rho_phi / rho_c0
    p_tot_n = (p_phi + r * rho_c0 / 3.0) / rho_c0
    if h > 0:
        dh = -1.5 * (rho_tot_n + p_tot_n) / h
    else:
        dh = 0.0
    u = 2.0 * X / L4
    denom = 1.0 + 3.0 * u
    if denom == 0:
        return np.zeros(7)
    hpH = dh / h if h > 0 else 0.0
    dPi = (-hpH * Pi - 3.0 * (1.0 + u) * Pi / denom
           + (LAM * V) / (denom * H0 ** 2 * h ** 2))   # SIGNO + (V_phi = -LAM V)
    dPhi = Pi
    dm = -3.0 * m
    dr = -4.0 * r
    dtau = 1.0 / h
    dell = np.exp(N) / h
    return np.array([dPhi, dPi, dh, dm, dr, dtau, dell])

# =============================================================================
# 4. SISTEMA ESCALADO CORREGIDO (S = sqrt(k) Pi e^{2N}, E = h e^{2N})
# =============================================================================
def logadd(x, y):
    m = np.maximum(x, y)
    return m + np.log1p(np.exp(-np.abs(x - y))) if np.abs(x - y) < 700 else m

def scale_terms(N, logS, E, Z):
    """Terminos comunes en log-estable. Devuelve dict con cantidades y logs."""
    eN = np.exp(N)
    e2N = eN * eN
    e4N = e2N * e2N
    logE = np.log(np.abs(E))
    # log|S|
    lS = logS
    # log u = 2 ln|E| + 2 ln|S| - 8N
    logu = 2.0 * logE + 2.0 * lS - 8.0 * N
    # inv_denom = 1/(1+3u) estable
    if logu > 700:
        log_denom = logu + np.log(3.0)
        inv_denom = np.exp(-log_denom)
        u = np.inf
    else:
        u = np.exp(logu)
        inv_denom = 1.0 / (1.0 + 3.0 * u)
    # D = Om_m e^N + 4/3 Om_r + E^2 S^2 e^{-4N}/(3k) + E^4 S^4 e^{-12N}/(3k)
    ld_m = N + np.log(Omega_m0)
    ld_r = np.log(4.0 * Omega_r0 / 3.0)
    ld_k1 = 2.0 * logE + 2.0 * lS - 4.0 * N - np.log(3.0 * kappa)
    ld_k2 = 4.0 * logE + 4.0 * lS - 12.0 * N - np.log(3.0 * kappa)
    lD = logadd(logadd(ld_m, ld_r), logadd(ld_k1, ld_k2))
    D = np.exp(lD) if lD < 700 else np.inf
    # EF2 (Friedmann escalado): Om_m e^N + Om_r + E^2S^2e^{-4N}/(6k) + E^4S^4e^{-12N}/(4k) + z e^{4N}
    lf_m = N + np.log(Omega_m0)
    lf_r = np.log(Omega_r0)
    lf_k1 = 2.0 * logE + 2.0 * lS - 4.0 * N - np.log(6.0 * kappa)
    lf_k2 = 4.0 * logE + 4.0 * lS - 12.0 * N - np.log(4.0 * kappa)
    lf_z = Z + 4.0 * N
    lEF2 = logadd(logadd(logadd(lf_m, lf_r), logadd(lf_k1, lf_k2)), lf_z)
    EF2 = np.exp(lEF2) if lEF2 < 700 else np.inf
    return dict(eN=eN, e2N=e2N, e4N=e4N, logu=logu, u=u, inv_denom=inv_denom,
                D=D, lD=lD, EF2=EF2, lEF2=lEF2)

def derivatives_scaled_corrected(N, y, sign_state):
    """y = [Phi, logS, E, Z, tau, ell]. sign_state = [sign] mutable (cruce - -> +)."""
    Phi, logS, E, Z, tau, ell = y
    if not np.all(np.isfinite(y)):
        return np.full(6, np.nan)
    if E <= 0:
        return np.full(6, np.nan)
    st = scale_terms(N, logS, E, Z)
    if not np.isfinite(st["D"]):
        return np.full(6, np.nan)

    sign = sign_state[0]
    # Pi = S e^{-2N}/sqrt(k) ; h = E e^{-2N}
    S = sign * np.exp(logS)
    e2N = st["e2N"]
    Pi = S * np.exp(-2.0 * N) / sqrt_kappa
    z = np.exp(Z) if Z < 700 else np.inf
    if not np.isfinite(z):
        return np.full(6, np.nan)

    dPhi = Pi
    dZ = -LAM * Pi

    # E' = 2E - 1.5 D/E
    dE = 2.0 * E - 1.5 * st["D"] / E

    # S' exacta:  S' = [2 + 1.5D/E^2 - 3(1+u)/(1+3u)] S + 3 L sqrt(k) z e^{6N}/((1+3u) E^2)
    a = 2.0 + 1.5 * st["D"] / E ** 2 - 3.0 * (1.0 + st["u"]) * st["inv_denom"]
    b = 3.0 * LAM * sqrt_kappa * z * np.exp(6.0 * N) * st["inv_denom"] / E ** 2
    dS = a * S + b
    # log|S|: dlogS = dS / S  (estable; si S ~ 0 el cruce - -> + se detecta)
    if S != 0.0:
        dlogS = dS / S
    else:
        dlogS = 0.0
    # deteccion de cruce: b > 0 siempre => el cruce solo puede ser - -> +
    if sign < 0 and logS < -700.0:
        sign_state[0] = 1.0
        sign = 1.0
        dlogS = a + b / np.exp(-700.0)   # |S| recien cruzado: S' = a*0 + b > 0
        dlogS = 0.0 if not np.isfinite(dlogS) else dlogS

    dtau = e2N / E
    dell = st["eN"] * e2N / E
    return np.array([dPhi, dlogS, dE, dZ, dtau, dell])

# =============================================================================
# 5. BATERIA DE IDENTIDADES ALGEBRAICAS (Nivel 0) — PUERTA DE ENTRADA
# =============================================================================
def algebraic_identity_test(n_pts=10000, seed=13522):
    rng = np.random.default_rng(seed)
    maxd = defaultdict(float)
    for _ in range(n_pts):
        Nv = rng.uniform(-60.0, 0.0)
        Zv = rng.uniform(-20.0, 10.0)
        Piv = rng.uniform(-2.0, 2.0)
        Phiv = -Zv / LAM
        mv = Omega_m0 * np.exp(-3.0 * Nv)
        rv = Omega_r0 * np.exp(-4.0 * Nv)
        # h on-shell desde la constraint
        X = 0.5 * (H0 * Piv) ** 2
        Vn = np.exp(Zv)
        rho_phi_n = (X + 3.0 * X ** 2 / LAMBDA ** 4) / rho_c0 + Vn
        h2 = mv + rv + rho_phi_n
        hv = np.sqrt(max(h2, 1e-300))
        E = hv * np.exp(2.0 * Nv)
        S = sqrt_kappa * Piv * np.exp(2.0 * Nv)
        logS = np.log(np.abs(S)) if S != 0 else -1000.0
        # ground truth (EOM originales corregidas)
        Xh = 0.5 * (H0 * hv * Piv) ** 2
        u_ex = 2.0 * Xh / LAMBDA ** 4
        rho_phi = Xh + 3.0 * Xh ** 2 / LAMBDA ** 4 + rho_c0 * np.exp(-LAM * Phiv)
        p_phi = Xh + Xh ** 2 / LAMBDA ** 4 - rho_c0 * np.exp(-LAM * Phiv)
        rtn = mv + rv + rho_phi / rho_c0
        ptn = (p_phi + rv * rho_c0 / 3.0) / rho_c0
        hpH = -1.5 * (rtn + ptn) / hv ** 2
        Pi_p = (-hpH * Piv - 3.0 * (1.0 + u_ex) * Piv / (1.0 + 3.0 * u_ex)
                + LAM * rho_c0 * np.exp(-LAM * Phiv) / ((1.0 + 3.0 * u_ex) * H0 ** 2 * hv ** 2))
        D_ex = np.exp(4.0 * Nv) * (rtn + ptn)
        E_p_ex = np.exp(2.0 * Nv) * (hpH * hv + 2.0 * hv)
        S_p_ex = sqrt_kappa * np.exp(2.0 * Nv) * (Pi_p + 2.0 * Piv)
        EF2_ex = np.exp(4.0 * Nv) * rtn
        # formulas v1.5.22
        st = scale_terms(Nv, logS, E, Zv)
        u_c = st["u"] if st["logu"] < 700 else np.inf
        D_c = st["D"]
        E_p_c = 2.0 * E - 1.5 * D_c / E
        sign = np.sign(S) if S != 0 else 1.0
        a = 2.0 + 1.5 * D_c / E ** 2 - 3.0 * (1.0 + u_c) * st["inv_denom"]
        b = 3.0 * LAM * sqrt_kappa * np.exp(Zv) * np.exp(6.0 * Nv) * st["inv_denom"] / E ** 2
        S_p_c = a * (sign * np.exp(logS)) + b
        EF2_c = st["EF2"]
        Z_p_c = -LAM * Piv
        # d(tau)/dN = 1/h ; d(ell)/dN = e^N/h  (en escalado: e^{2N}/E y e^{3N}/E = 1/h y e^N/h)
        tau_c = np.exp(2.0 * Nv) / E
        ell_c = np.exp(3.0 * Nv) / E
        d = {
            "u": abs(u_ex - u_c) / (abs(u_ex) + 1e-300),
            "D": abs(D_ex - D_c) / (abs(D_ex) + 1e-300),
            "E'": abs(E_p_ex - E_p_c) / (abs(E_p_ex) + 1e-300),
            "S'": abs(S_p_ex - S_p_c) / (abs(S_p_ex) + 1e-300),
            "EF2": abs(EF2_ex - EF2_c) / (abs(EF2_ex) + 1e-300),
            "Z'": abs(-LAM * Piv - Z_p_c) / (abs(-LAM * Piv) + 1e-300),
            "tau'": abs(1.0 / hv - tau_c) / (abs(1.0 / hv) + 1e-300),
            "ell'": abs(np.exp(Nv) / hv - ell_c) / (abs(np.exp(Nv) / hv) + 1e-300),
        }
        for k in d:
            maxd[k] = max(maxd[k], d[k])
    ok_all = all(maxd[k] < 1e-8 for k in maxd)
    return ok_all, {k: float(v) for k, v in maxd.items()}

# =============================================================================
# 6. PRUEBA DE EQUIVALENCIA Original <-> Escalado (Nivel 1)
# =============================================================================
def run_equivalence_test(w0, sign_q, N_min=-30, tol=1e-10):
    """El rango es corto ([0, -30]) a proposito: el sistema ORIGINAL es stiff a
    N profundo (h ~ e^{-2N}); la identidad algebraica ya se verifica sobre
    [-60, 0] en el Nivel 0. Aqui solo se valida la INTEGRACION del transform."""
    init = compute_initial_quantities(w0, sign_q)
    if init is None:
        return False, "Invalid IC"
    Phi0, Pi0, _, Z0 = init
    S0 = sqrt_kappa * Pi0
    sign = np.sign(S0) if S0 != 0 else 1.0
    logS0 = np.log(np.abs(S0))
    E0, tau0, ell0 = 1.0, 0.0, 0.0
    init_orig = np.array([Phi0, Pi0, 1.0, Omega_m0, Omega_r0, 0.0, 0.0])
    init_scaled = np.array([Phi0, logS0, E0, Z0, tau0, ell0], dtype=float)
    sign_state = [sign]

    N_control = -np.logspace(0, np.log10(-N_min), 200)
    t_eval = np.sort(N_control)[::-1]

    def dw(N, y):
        return derivatives_scaled_corrected(N, y, sign_state)

    sol_o = solve_ivp(derivatives_original_corrected, [0.0, N_min], init_orig,
                      method='BDF', t_eval=t_eval, rtol=tol, atol=tol * 1e-3, max_step=0.05)
    sol_s = solve_ivp(dw, [0.0, N_min], init_scaled,
                      method='BDF', t_eval=t_eval, rtol=tol, atol=tol * 1e-3, max_step=0.05)
    if not sol_o.success or not sol_s.success:
        return False, "Integration failed: %s / %s" % (sol_o.message, sol_s.message)

    N = sol_o.t
    Phi_o, Pi_o, h_o = sol_o.y[:3]
    Phi_s, logS_s, E_s, Z_s = sol_s.y[:4]
    S_s = sign_state[0] * np.exp(logS_s)
    Pi_s = S_s * np.exp(-2.0 * N) / sqrt_kappa
    h_s = E_s * np.exp(-2.0 * N)

    e_Phi = np.max(np.abs(Phi_o - Phi_s))
    e_Pi = np.max(np.abs(Pi_o - Pi_s))
    e_h = np.max(np.abs(h_o - h_s))
    return (e_Phi < 1e-6 and e_Pi < 1e-6 and e_h < 1e-6,
            "err_Phi=%.2e err_Pi=%.2e err_h=%.2e" % (e_Phi, e_Pi, e_h))

# =============================================================================
# 7. AUDITORIA PROFUNDA (Nivel 2) hasta N=-1000
# =============================================================================
def run_deep_audit(w0, sign_q, N_min_list, method='BDF', tol=1e-10):
    init = compute_initial_quantities(w0, sign_q)
    if init is None:
        return {'status': 'FAIL', 'reason': 'Invalid IC'}
    Phi0, Pi0, _, Z0 = init
    S0 = sqrt_kappa * Pi0
    sign = np.sign(S0) if S0 != 0 else 1.0
    logS0 = np.log(np.abs(S0))
    init_scaled = np.array([Phi0, logS0, 1.0, Z0, 0.0, 0.0], dtype=float)

    results_by_N = {}
    for Nm in sorted(N_min_list):
        sign_state = [sign]
        def dw(N, y, st=sign_state):
            return derivatives_scaled_corrected(N, y, st)
        N_control = -np.logspace(0, np.log10(-Nm), 200)
        t_eval = np.r_[0.0, np.sort(N_control)[::-1]]
        sol = solve_ivp(dw, [0.0, Nm], init_scaled, method=method,
                        t_eval=t_eval, rtol=tol, atol=tol * 1e-3, max_step=0.05)
        if not sol.success:
            return {'status': 'FAIL', 'reason': 'Scaled N=%s: %s' % (Nm, sol.message)}
        N = sol.t
        Phi, logS, E, Z, tau, ell = sol.y
        st = scale_terms(N, logS, E, Z)
        resid_F = np.abs(E ** 2 - st["EF2"]) / (np.abs(st["EF2"]) + 1e-300)
        S = sign_state[0] * np.exp(logS)
        # K = 12 e^{-8N} [ (E^2 - 1.5D)^2 + E^4 ]  (log10)
        E2 = E ** 2
        term1 = E2 - 1.5 * st["D"]
        term2 = E2
        logK = np.log10(12.0) - 8.0 * N / LN10 + np.log10(np.sqrt(term1 ** 2 + term2 ** 2) + 1e-300)
        results_by_N[Nm] = {'N': N, 'logS': logS, 'E': E, 'Z': Z,
                            'I_tau': -tau, 'I_ell': -ell,
                            'I_tau_final': float(-tau[-1]), 'I_ell_final': float(-ell[-1]),
                            'max_resid': float(np.max(resid_F)), 'logK': logK,
                            'sign_cruzo': sign_state[0] != sign}

    # ---- convergencia: relativo + absoluto + estabilidad de la cola ----
    N_list_sorted = sorted(N_min_list)
    tau_vals = [results_by_N[Nm]['I_tau_final'] for Nm in N_list_sorted]
    ell_vals = [results_by_N[Nm]['I_ell_final'] for Nm in N_list_sorted]
    tau_conv = ell_conv = False
    if len(tau_vals) >= 3:
        tl, el = tau_vals[-3:], ell_vals[-3:]
        rel_t = abs(tl[-1] - tl[-2]) / (abs(tl[-1]) + 1e-300)
        rel_e = abs(el[-1] - el[-2]) / (abs(el[-1]) + 1e-300)
        abs_t = abs(tl[-1] - tl[-2]); abs_e = abs(el[-1] - el[-2])
        stab_t = abs(tl[-1] - tl[-2]) / (abs(tl[-2] - tl[-3]) + 1e-300)
        stab_e = abs(el[-1] - el[-2]) / (abs(el[-2] - el[-3]) + 1e-300)
        tau_conv = rel_t < 1e-8 and abs_t < 1e-8 and stab_t < 2.0
        ell_conv = rel_e < 1e-8 and abs_e < 1e-8 and stab_e < 2.0

    # ---- K: pendiente en la cola (20% final) ----
    res_deep = results_by_N[max(N_min_list)]
    N = res_deep['N']; logK = res_deep['logK']
    n_tail = max(20, len(N) // 5)
    x = -N[-n_tail:]; y = logK[-n_tail:]
    mask = np.isfinite(y)
    if np.sum(mask) < 20:
        slope, r2 = np.nan, 0.0
    else:
        slope, b0 = np.polyfit(x[mask], y[mask], 1)
        yf = slope * x[mask] + b0
        ss_res = np.sum((y[mask] - yf) ** 2)
        ss_tot = np.sum((y[mask] - np.mean(y[mask])) ** 2)
        r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else 0.0
    expected = 8.0 / LN10
    K_ok = np.isfinite(slope) and abs(slope - expected) / expected < 0.05 and r2 > 0.99
    F_ok = res_deep['max_resid'] < 1e-6

    if not F_ok:
        cl = 'FALLA FRIEDMANN'
    elif not (tau_conv and ell_conv):
        cl = 'INTEGRALES NO CONVERGEN'
    elif not K_ok:
        cl = 'K NO DIVERGE (pendiente o R2)'
    else:
        cl = 'PASADO INCOMPLETO (K->inf, integrales finitas)'

    return {'status': 'OK' if cl == 'PASADO INCOMPLETO (K->inf, integrales finitas)' else 'FAIL',
            'classification': cl, 'max_resid': res_deep['max_resid'],
            'K_slope': slope, 'K_r2': r2,
            'tau_converged': tau_conv, 'ell_converged': ell_conv,
            'I_tau_final': tau_vals[-1], 'I_ell_final': ell_vals[-1],
            'w0': w0, 'sign': sign_q, 'method': method, 'N_min_deep': max(N_min_list),
            'sign_cruzo': res_deep['sign_cruzo']}

# =============================================================================
# 8. MAIN
# =============================================================================
if __name__ == "__main__":
    w_vals = np.linspace(-0.3, 0.1, 9)
    signs = [1, -1]
    methods = ['DOP853', 'BDF', 'Radau']
    N_min_list_deep = [-50, -100, -200, -300, -500, -700, -1000]

    print("=" * 80)
    print("TCCU-0 v1.5.22: AUDITORIA CON IDENTIDADES CORREGIDAS")
    print("=" * 80)

    # ---- Nivel 0: bateria algebraica ----
    print("\n[NIVEL 0] Bateria de identidades algebraicas (10000 puntos on-shell)")
    t0 = time.time()
    ok_ids, maxd = algebraic_identity_test()
    for k in ["u", "D", "E'", "S'", "EF2", "Z'", "tau'", "ell'"]:
        print("  %-5s max rel diff = %.3e  %s" % (k, maxd[k], "OK" if maxd[k] < 1e-8 else "FALLO"))
    print("  -> %s (%.1f s)" % ("IDENTIDADES VERIFICADAS" if ok_ids else "IDENTIDADES FALLAN", time.time() - t0))
    if not ok_ids:
        sys.exit(1)

    # ---- Nivel 1: equivalencia ----
    print("\n[NIVEL 1] Equivalencia Original <-> Escalado (N_min=-100)")
    equiv_ok = True
    for w0 in w_vals:
        for sg in signs:
            ok, msg = run_equivalence_test(w0, sg, N_min=-100, tol=1e-10)
            print("  w0=%.3f sign=%+d -> %s %s" % (w0, sg, "OK" if ok else "FALLO", msg))
            equiv_ok = equiv_ok and ok
    if not equiv_ok:
        print("  Equivalencia FALLIDA -> abortando campana")
        sys.exit(1)

    # ---- Nivel 2: campana profunda ----
    print("\n[NIVEL 2] Campana profunda (9 w0 x 2 signos x 3 metodos x 7 extensiones)")
    total = len(w_vals) * len(signs) * len(methods)
    results, fails = [], 0
    counter = 0
    for w0 in w_vals:
        for sg in signs:
            for meth in methods:
                counter += 1
                res = run_deep_audit(w0, sg, N_min_list_deep, method=meth, tol=1e-10)
                if res and res.get('status') == 'OK':
                    results.append(res)
                    print("  [%d/%d] w0=%.3f sign=%+d %-6s -> %s (slope=%.4f r2=%.4f)" % (
                        counter, total, w0, sg, meth, res['classification'],
                        res['K_slope'], res['K_r2']))
                else:
                    fails += 1
                    print("  [%d/%d] w0=%.3f sign=%+d %-6s -> FALLO: %s" % (
                        counter, total, w0, sg, meth, (res or {}).get('classification', '?')))

    # ---- consistencia ----
    grouped = defaultdict(list)
    for r in results:
        grouped[(r['w0'], r['sign'])].append(r)
    consistent = sum(1 for g in grouped.values() if len(set(x['classification'] for x in g)) == 1)
    no_go = sum(1 for g in grouped.values()
                if len(set(x['classification'] for x in g)) == 1 and 'PASADO INCOMPLETO' in g[0]['classification'])
    cruces = sum(1 for r in results if r.get('sign_cruzo'))

    print("\n" + "=" * 80)
    print("VEREDICTO TCCU-0 (v1.5.22)")
    print("=" * 80)
    print("Bateria identidades: %s | Equivalencia: %s" % ("PASS" if ok_ids else "FAIL",
                                                          "PASS" if equiv_ok else "FAIL"))
    print("Exitosas: %d/%d | Fallos: %d" % (len(results), total, fails))
    print("Grupos consistentes: %d/%d | NO-GO: %d | cruces de signo S: %d" % (
        consistent, len(grouped), no_go, cruces))
    if ok_ids and equiv_ok and fails == 0 and len(grouped) > 0 and consistent == len(grouped) and no_go == len(grouped):
        print("""\nNO-GO PROVISIONAL (dominio explorado):
  El modelo TCCU-0 resulta integralmente incompleto hacia N -> -inf bajo las
  hipotesis especificadas (K -> inf con pendiente 8/ln10; integrales de horizonte
  I_tau, I_ell finitas; consistencia entre integradores). Esto no implica una
  singularidad del universo real ni refuta la cosmologia estandar: acota el
  modelo en el criterio geometrico adoptado.""")
    else:
        print("\nNO-GO NO ESTABLECIDO — se requiere revision (ver fallos arriba).")
    print("=" * 80)
