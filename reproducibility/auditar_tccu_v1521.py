# auditar_tccu_v1521.py — AUDITORIA ALGEBRAICA de la v1.5.21 (v2, numerica vectorizada)
# Ground truth: EOM originales (k-essence + V exponencial) con la KG correcta:
#   Pi' = -(h'/h)Pi - 3(1+u)Pi/(1+3u) + LAM*V/((1+3u) H0^2 h^2)   [V_phi = -LAM V]
# y h'/h = -1.5 (rho_tot+p_tot)/rho_c0 / h^2 (Friedmann derivada).
# Se comparan las formulas del codigo v1.5.21 (u, D, E', S', EF2) contra los
# valores exactos reconstruidos desde las definiciones S=sqrt(k)Pi e^{2N}, E=h e^{2N}.
import numpy as np

H0 = 1.44e-60
LAM = 5.0
LAMBD = 0.15
kappa = H0 ** 2 / LAMBD ** 4
sqk = np.sqrt(kappa)
Om_m, Om_r = 0.315, 9.0e-5
rho_c0 = 3.0 * H0 ** 2

def rho_phi_p_phi(Phi, Pi, h):
    X = 0.5 * (H0 * h * Pi) ** 2
    V = rho_c0 * np.exp(-LAM * Phi)
    return X + 3.0 * X ** 2 / LAMBD ** 4 + V, X + X ** 2 / LAMBD ** 4 - V

def exact_derivs(N, Phi, Pi, h, m, r):
    """Derivadas exactas de las variables escaladas (ground truth)."""
    X = 0.5 * (H0 * h * Pi) ** 2
    u = 2.0 * X / LAMBD ** 4
    V = rho_c0 * np.exp(-LAM * Phi)
    rp, pp = rho_phi_p_phi(Phi, Pi, h)
    rho_tot_n = m + r + rp / rho_c0
    p_tot_n = (pp + r * rho_c0 / 3.0) / rho_c0
    hpH = -1.5 * (rho_tot_n + p_tot_n) / h ** 2          # h'/h (Friedmann)
    Pi_p = -hpH * Pi - 3.0 * (1.0 + u) * Pi / (1.0 + 3.0 * u) + LAM * V / ((1.0 + 3.0 * u) * H0 ** 2 * h ** 2)
    eN = np.exp(N)
    E = h * eN * eN
    S = sqk * Pi * eN * eN
    z = np.exp(-LAM * Phi)
    # identidades exactas
    D = eN ** 4 * (rho_tot_n + p_tot_n)
    E_p = eN * eN * (hpH * h + 2.0 * h)                   # = e^{2N}(h' + 2h)
    S_p = sqk * eN * eN * (Pi_p + 2.0 * Pi)               # = sqrt(k) e^{2N}(Pi' + 2Pi)
    EF2 = eN ** 4 * rho_tot_n
    return u, D, E_p, S_p, EF2, z, E, S

# formulas del codigo v1.5.21
def code_u(N, E, S):
    return E ** 2 * S ** 2 * np.exp(-8.0 * N)
def code_D(N, E, S):
    eN = np.exp(N)
    return (Om_m * eN + (4.0 / 3.0) * Om_r +
            E ** 2 * S ** 2 * np.exp(-4.0 * N) / (3.0 * kappa) +
            E ** 4 * S ** 4 * np.exp(-12.0 * N) / (3.0 * kappa))
def code_EF2(N, E, S, z):
    return (Om_m * np.exp(N) + Om_r +
            S ** 2 * np.exp(-2.0 * N) / (6.0 * kappa) +
            S ** 4 * np.exp(-8.0 * N) / (4.0 * kappa) + z * np.exp(4.0 * N))
def code_dE(N, E, S):
    return 2.0 * E - 1.5 * code_D(N, E, S) / E
def code_dS(N, E, S, z):
    eN = np.exp(N)
    uu = code_u(N, E, S)
    return -((4.0 + 6.0 * uu) * S + 3.0 * LAM * sqk * z * eN * eN) / (1.0 + 3.0 * uu)

rng = np.random.default_rng(20260826)
maxd = {"u": 0.0, "D": 0.0, "E'": 0.0, "S'": 0.0, "EF2": 0.0}
bad = {k: 0 for k in maxd}
Npts = 5000
for _ in range(Npts):
    Nv = rng.uniform(-60.0, 0.0)
    Phiv = rng.uniform(-30.0, 10.0)
    Piv = rng.uniform(-2.0, 2.0)
    mv = Om_m * np.exp(-3.0 * Nv)
    rv = Om_r * np.exp(-4.0 * Nv)
    rp, _ = rho_phi_p_phi(Phiv, Piv, 1.0)
    h2 = mv + rv + rp / rho_c0
    hv = np.sqrt(max(h2, 1e-300))
    ue, De, Ep, Sp, EF2e, zve, Ee, Se = exact_derivs(Nv, Phiv, Piv, hv, mv, rv)
    d = {
        "u": abs(ue - code_u(Nv, Ee, Se)) / (abs(ue) + 1e-300),
        "D": abs(De - code_D(Nv, Ee, Se)) / (abs(De) + 1e-300),
        "E'": abs(Ep - code_dE(Nv, Ee, Se)) / (abs(Ep) + 1e-300),
        "S'": abs(Sp - code_dS(Nv, Ee, Se, zve)) / (abs(Sp) + 1e-300),
        "EF2": abs(EF2e - code_EF2(Nv, Ee, Se, zve)) / (abs(EF2e) + 1e-300),
    }
    for k in maxd:
        maxd[k] = max(maxd[k], d[k])
        if d[k] > 1e-10:
            bad[k] += 1

print("AUDITORIA v1.5.21 (5000 puntos on-shell, N in [-60,0])")
print("=" * 64)
print("identidad |  max rel diff  |  >1e-10  | veredicto")
for k in ["u", "D", "E'", "S'", "EF2"]:
    ok = maxd[k] < 1e-10
    print("  %-6s | %14.3e | %7d | %s" % (k, maxd[k], bad[k], "PASS" if ok else "FALLO"))
print("=" * 64)
print()
print("NOTA KG: la KG correcta es  (1+3u)Pi' + ... + LAM*V/(H0^2 h^2) = 0  con signo +")
print("(V_phi = -LAM V). La v1.5.21 usa  -LAM*V/(H0^2 h^2)  -> signo invertido en el")
print("termino de potencial, tanto en el sistema original como en el fuente de S'.")
print()
print("S' exacta (derivada de la KG correcta):")
print("  S' = [2 + 1.5 D/E^2 - 3(1+u)/(1+3u)] S + 3 L sqrt(k) z e^{6N} / ((1+3u) E^2)")
print("S' v1.5.21:  -(4+6u)S/(1+3u) - 3 L sqrt(k) z e^{2N}/(1+3u)")
print("  -> falta el acoplamiento D/E^2 y el fuente difiere (e^{2N} vs e^{6N}/E^2).")
print()
print("EF2 exacta:")
print("  E^2 = Om_m e^N + Om_r + E^2 S^2 e^{-4N}/(6 k) + E^4 S^4 e^{-12N}/(4 k) + z e^{4N}")
print("EF2 v1.5.21:  ... + S^2 e^{-2N}/(6k) + S^4 e^{-8N}/(4k) + z e^{4N}")
print("  -> faltan los factores E^2/E^4 y las potencias e^{-4N}/e^{-12N}.")
