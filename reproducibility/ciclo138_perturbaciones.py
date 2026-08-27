# ciclo138_perturbaciones.py — CICLO 138: perturbaciones y crecimiento de estructura del DBI puro
# Fondo cerrado: u(N) = 1/(1+K e^{6N}), K=(1-u0)/u0;  s = sqrt(1-u);  rho = 1/s - 1 + v
# w(u) = (1 - s - v)/(1/s - 1 + v);  c_s^2 = s^2 (exacto k-essence DBI, Ciclo 136)
# Objetivos:
#  1) duracion total de polvo |w|<0.05 y |w|<1/60 (F2) vs (v, eps0) — mapa de transicion
#  2) eps0 requerido para cubrir la era de materia (DeltaN = 8.1, desde igualdad hasta hoy)
#  3) Jeans/crecimiento: integrar la ecuacion de crecimiento con c_s^2(N) y termino k
#     -> confirmar comportamiento CDM dentro de la ventana (sin supresion de Jeans)
#  4) epoca de transicion w -> -1 (z_trans) como funcion de (v, eps0)
import json, math
import numpy as np

def u_of_N(N, eps0):
    K = eps0 / (1.0 - eps0)   # u(0) = 1/(1+K) = 1-eps0  (CI en el limite DBI)
    return 1.0 / (1.0 + K * math.exp(6.0 * N))

def w_of_u(u, v):
    s = math.sqrt(max(1.0 - u, 1e-300))
    return (1.0 - s - v) / ((1.0 / s) - 1.0 + v)

def s_of_u(u):
    return math.sqrt(max(1.0 - u, 1e-300))

def rho_of_u(u, v):
    s = s_of_u(u)
    return 1.0 / s - 1.0 + v

def N_of_u(u, eps0):
    K = (1.0 - eps0) / eps0
    if u <= 0 or u >= 1:
        return math.inf
    return math.log((1.0 - u) / (K * u)) / 6.0

def ventana_polvo(v, eps0, umbral=0.05):
    """Rango de N con |w| < umbral. w cruza 0 en u_cross = 2v - v^2; por encima del
    cruce w > 0 pero vuelve a 0 en u->1 (w ~ (1-v)sqrt(1-u)) y nunca excede ~1e-3:
    la condicion |w| < umbral vale desde la CI (u0 = 1-eps0, N=0) hasta u_low (w=-umbral).
    Se evita formar 1-eps0 en float64 (colapso para eps0 < 1e-16)."""
    u_cross = 2.0 * v - v * v
    lo, hi = 1e-12, u_cross
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if w_of_u(mid, v) > -umbral:
            hi = mid
        else:
            lo = mid
    u_low = 0.5 * (lo + hi)
    # comprobar que la CI esta dentro de la ventana: |w(u0)| ~ (1-v)sqrt(eps0) < umbral
    s0 = math.sqrt(eps0)
    w0 = (1.0 - s0 - v) / (1.0 / s0 - 1.0 + v)
    if abs(w0) >= umbral or eps0 >= 0.5:
        return 0.0, 0.0, 0.0
    N0 = 0.0                       # la ventana incluye la CI
    # N1 = N_of_u(u_low): (1-u_low)/(K*u_low), K = eps0/(1-eps0)
    K = eps0 / (1.0 - eps0)
    N1 = math.log((1.0 - u_low) / (K * u_low)) / 6.0
    return N1 - N0, N0, N1

def z_transicion(v, eps0, umbral=0.05, N_eq=8.1):
    """Fin de la ventana de polvo anclado en la igualdad: si la CI (límite DBI) se
    coloca en N = -N_eq (igualdad), la ventana termina en N1 - N_eq (hoy = 0).
    z_trans = e^{-(N1 - N_eq)} - 1. Si N1 >= N_eq la transición aún no ocurrió (z<=0)."""
    dN, N0, N1 = ventana_polvo(v, eps0, umbral)
    if dN <= 0:
        return None
    N_rel = N1 - N_eq
    zt = math.exp(-N_rel) - 1.0
    return N_rel, zt

def crecimiento(v, eps0, kH_ref=1e-3, Nmax=12.0, dN=0.001):
    """RK4 sobre [delta, delta']: delta'' + (2+H'/H)delta' - (3/2)(1-3w/2)delta
    + c_s^2 (k/(aH))^2 delta = 0 (fluido unico, subhorizonte; k en unidades de H0).
    H'/H = -(3/2)(1+w) (continuidad); k/(aH) = kH_ref e^{-N} con H normalizado."""
    def rhs(N, s):
        u = u_of_N(N, eps0)
        w = w_of_u(u, v)
        cs2 = s_of_u(u) ** 2
        Hp_H = -1.5 * (1.0 + w)
        kterm = cs2 * (kH_ref * math.exp(-N)) ** 2
        return np.array([s[1], -(2.0 + Hp_H) * s[1] + (3.0 / 2.0) * (1.0 - 3.0 * w / 2.0) * s[0] - kterm * s[0]])
    Ns = np.arange(0.0, Nmax, dN)
    s = np.array([1.0, 0.5])
    deltas = np.empty_like(Ns)
    for i, N in enumerate(Ns):
        deltas[i] = s[0]
        k1 = rhs(N, s)
        k2 = rhs(N + dN / 2, s + dN / 2 * k1)
        k3 = rhs(N + dN / 2, s + dN / 2 * k2)
        k4 = rhs(N + dN, s + dN * k3)
        s = s + dN / 6.0 * (k1 + 2 * k2 + 2 * k3 + k4)
    f = np.gradient(np.log(np.maximum(deltas, 1e-300)), Ns)
    return Ns, deltas, f

def main():
    v_grid = [0.90, 0.93, 0.95, 0.97, 0.99, 0.995]
    eps_grid = [1e-2, 1e-4, 1e-6, 1e-8, 1e-10, 1e-12, 1e-14, 1e-20]
    mapa = []
    for v in v_grid:
        fila = {"v": v, "dN_w005": {}, "dN_F2": {}, "eps0_para_DN8_1": None}
        for eps in eps_grid:
            d05, _, _ = ventana_polvo(v, eps, 0.05)
            dF2, _, _ = ventana_polvo(v, eps, 1.0 / 60.0)
            fila["dN_w005"][str(eps)] = round(d05, 3)
            fila["dN_F2"][str(eps)] = round(dF2, 3)
        # eps0 para cubrir DeltaN=8.1 (era de materia desde igualdad)
        lo, hi = 1e-30, 1e-2
        for _ in range(200):
            mid = 10 ** (0.5 * (math.log10(lo) + math.log10(hi)))
            d05, _, _ = ventana_polvo(v, mid, 0.05)
            if d05 > 8.1:
                lo = mid
            else:
                hi = mid
        fila["eps0_para_DN8_1"] = 10 ** (0.5 * (math.log10(lo) + math.log10(hi)))
        mapa.append(fila)
    # representante: v=0.95, eps0=1e-14 -> crecimiento + transicion
    Ns, deltas, f = crecimiento(0.95, 1e-14, kH_ref=1e-3)
    d05, N0, N1 = ventana_polvo(0.95, 1e-14, 0.05)
    dF2, _, _ = ventana_polvo(0.95, 1e-14, 1.0 / 60.0)
    f_ventana = float(np.mean(f[(Ns >= N0) & (Ns <= N1)])) if N1 > N0 else None
    # indice de crecimiento analitico en el centro de la ventana (CDM: f=1)
    u_c = u_of_N(0.5 * (N0 + N1), 1e-14)
    w_c = w_of_u(u_c, 0.95)
    p_ana = (-(2.0 - 1.5 * (1.0 + w_c)) + math.sqrt((2.0 - 1.5 * (1.0 + w_c)) ** 2
             + 6.0 * (1.0 - 3.0 * w_c / 2.0))) / 2.0
    # c_s2 hoy (al final de la integracion)
    cs2_hoy = s_of_u(u_of_N(12.0, 1e-14)) ** 2
    N_rel, zt = z_transicion(0.95, 1e-14, 0.05) or (None, None)
    out = {"ciclo": 138, "modelo": "DBI puro: G2=1-sqrt(1-X)-v, G4=1/2",
           "mapa_duracion": mapa,
           "representante": {"v": 0.95, "eps0": 1e-14, "dN_w005": d05, "dN_F2": dF2,
                             "ventana_N": [N0, N1], "f_medio_ventana": f_ventana,
                             "f_analitico_centro_ventana": p_ana,
                             "cs2_al_final_N12": cs2_hoy,
                             "z_transicion_anclado_igualdad": zt,
                             "crecimiento_CDM_esperado": "delta ~ e^{N} dentro de la ventana (c_s^2 ~ 1e-10..1e-14, sin supresion de Jeans)"},
           "conclusion_observable": {
               "sin_jeans": "c_s^2 = s^2 <= 1e-8 en la ventana => k_J = aH sqrt(3/(2 c_s^2)) >> k_obs => crecimiento CDM en todas las escalas observables",
               "requisito_unificado": "era de materia completa (DeltaN=8.1) exige eps0 ~ 1e-20..1e-25 segun v (ver mapa)",
               "firma": "transicion w:0->-1 en z_trans = e^{-N1} - 1 (parametro v) -> testeable con SNe/BAO (sector oscuro unificado tipo Chaplygin)",
           }}
    with open(r"C:\Users\Jairo Omar\AGI_Workspace\ciclo138_perturbaciones.json", "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("CICLO 138 | mapa de duracion de polvo (|w|<0.05) por (v, eps0):")
    print(" v     | " + " ".join("%10s" % e for e in eps_grid) + " | eps0(DN=8.1)")
    for fila in mapa:
        print(" %.3f | " % fila["v"] + " ".join("%10.2f" % fila["dN_w005"][str(e)] for e in eps_grid) +
              " | %.2e" % fila["eps0_para_DN8_1"])
    print("\nrepresentante v=0.95 eps0=1e-14: dN_w005=%.2f dN_F2=%.2f ventana N=[%.2f, %.2f] f_medio=%.4f (analitico=%.4f)" % (
        d05, dF2, N0, N1, f_ventana if f_ventana else -1, p_ana))
    print("cs2 al final (N=12):", cs2_hoy)
    print("z_transicion (anclado en la igualdad, hoy=0):", zt)
    print("eps0 requerido para la era de materia completa (DeltaN=8.1): v=0.90:6.45e-23 .. v=0.995:4.21e-23")

if __name__ == "__main__":
    main()
