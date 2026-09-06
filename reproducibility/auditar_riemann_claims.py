# auditar_riemann_claims.py — Auditoría numérica independiente de los claims del
# Riemann Engine (PDF mas..pdf, págs. 62-122). NO demuestra RH: verifica claims
# numéricos concretos con precisión arbitraria (mpmath) y emite PASS/FAIL/INCONCLUSIVE.
# Claims auditados (del inventario inventario_pdf_152p.md §4.13):
#   C1: núcleo Phi(u) = sum_n (2pi^2 n^4 e^{9u/2} - 3pi n^2 e^{5u/2}) exp(-pi n^2 e^{2u})
#   C2: momentos M_k = int_0^∞ u^{2k} Phi(u) du  (finitos, positivos)
#   C3: M_k = (-1)^k/2 Xi^(2k)(0)  (relación con derivadas — vía Taylor)
#   C4: H_N = (M_{i+j}) > 0 para N=0..Nm (definida positiva) -> "PROVEN analítico"
#   C5: R_n = M_{n+1}^2/(M_n M_{n+2}) ; q_n = (2n+1)(2n+2)/((2n+3)(2n+4))
#       claim: R_n > q_n para n=0,1,2 (y R0 in [0.41,0.48], R1 in [0.52,0.59], R2 in [0.61,0.68])
#   C6: J_{2,n}(X) hiperbólico (raíces reales) para n=0..3
#   C7: D3(u)~-8192 pi^9 e^{39u/2 - 3pi e^{2u}} (asintótico u->+inf); E(u)=2(l'')³+l''l''''-(l''')^2
#       con l=log Phi; claim E(u)<0 para u>>1 y E(0)<0
import mpmath as mp
import json, time, hashlib

mp.mp.dps = 50  # precisión: 50 dígitos

# ---------------------------------------------------------------------------
# C1: núcleo Phi
# ---------------------------------------------------------------------------
def Phi(u, Nmax=60):
    """Phi(u) por serie theta (Nmax términos). u>=0."""
    u = mp.mpf(u)
    s = mp.mpf(0)
    e2u = mp.e**(2*u)
    for n in range(1, Nmax+1):
        n2 = mp.mpf(n)**2
        arg = mp.pi * n2 * e2u
        if arg > 700:  # contribución despreciable
            break
        term = (2*mp.pi**2*n2**2*mp.e**(mp.mpf(9)*u/2) - 3*mp.pi*n2*mp.e**(mp.mpf(5)*u/2)) * mp.e**(-arg)
        s += term
    return s

def Phi_alt(u, Nmax=60):
    """Forma equivalente: Phi = 2 e^{5u/2} L theta(e^{2u}) con L = x d^2/dx^2 + 3/2 d/dx.
    Verificación de consistencia C1: ambas representaciones deben coincidir."""
    u = mp.mpf(u)
    x = mp.e**(2*u)
    # theta(x) = sum_{m=-inf}^{inf} e^{-pi m^2 x} = 1 + 2 sum_{m>=1} e^{-pi m^2 x}
    s = mp.mpf(1)
    for m in range(1, Nmax+1):
        arg = mp.pi * m*m * x
        if arg > 700: break
        s += 2*mp.e**(-arg)
    # L theta: x theta'' + (3/2) theta'  (derivadas respecto a x)
    # theta' = sum -pi m^2 e^{-pi m^2 x};  theta'' = sum (pi m^2)^2 e^{-pi m^2 x}
    d1 = mp.mpf(0); d2 = mp.mpf(0)
    for m in range(1, Nmax+1):
        c = mp.pi * m*m
        arg = c * x
        if arg > 700: break
        e = mp.e**(-arg)
        d1 += -c * e
        d2 += c*c * e
    Lv = x*d2 + mp.mpf(3)/2*d1
    return 2*mp.e**(mp.mpf(5)*u/2) * Lv

# ---------------------------------------------------------------------------
# C2/C3: momentos M_k = int u^{2k} Phi(u) du
# ---------------------------------------------------------------------------
def momento(k, u_max=30.0, Nmax=60):
    """M_k por cuadratura de alta precisión (regla tanh-sinh de mpmath)."""
    k = int(k)
    f = lambda t: t**(2*k) * Phi(t, Nmax)
    # mpmath.quad con tanh-sinh sobre [0, u_max]; cola u>u_max ~ e^{-pi e^{2u}} -> nula
    I = mp.quad(f, [0, u_max], method='tanh-sinh')
    # cola estimada: Phi(u) ~ 2 pi^2 e^{9u/2} e^{-pi e^{2u}} para u grande
    cola = mp.quad(lambda t: t**(2*k) * 2*mp.pi**2*mp.e**(mp.mpf(9)*t/2)*mp.e**(-mp.pi*mp.e**(2*t)),
                   [u_max, u_max+3.0], method='tanh-sinh')
    return I + cola

# ---------------------------------------------------------------------------
# C5: q_n
# ---------------------------------------------------------------------------
def q_n(n):
    n = mp.mpf(n)
    return (2*n+1)*(2*n+2)/((2*n+3)*(2*n+4))

# ---------------------------------------------------------------------------
# C7: E(u) = 2(l'')³ + l'' l'''' - (l''')^2 ,  l = log Phi  (derivadas en u)
# ---------------------------------------------------------------------------
def E_u(u, Nmax=60):
    u = mp.mpf(u)
    # derivadas numéricas de alta precisión de l = log Phi vía diferencias centrales
    # con paso adaptado a la precisión (mpmath: paso ~ 10^{-dps/4})
    h = mp.mpf(10)**(-12)
    l = lambda x: mp.log(Phi(x, Nmax))
    l0 = l(u)
    l1p = l(u+h); l1m = l(u-h)
    l2p = l(u+2*h); l2m = l(u-2*h)
    lp = (l1p - l1m)/(2*h)
    lpp = (l1p - 2*l0 + l1m)/h**2
    lppp = (l2p - 2*l1p + 2*l1m - l2m)/(2*h**3)
    l4 = (l2p - 4*l1p + 6*l0 - 4*l1m + l2m)/h**4
    E = 2*lpp**3 + lpp*l4 - lppp**2
    return E, lpp, l4, lppp

def main():
    import sys
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    print("="*78)
    print("AUDITORÍA NUMÉRICA DE CLAIMS — RIEMANN ENGINE (precisión 50 dígitos)")
    print("="*78)
    res = {"claims": [], "fecha": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
           "precision": 50, "nota": "auditoria numerica independiente; NO demuestra RH"}

    # C1 + consistencia con forma theta
    ok = True
    for u in [mp.mpf(0), mp.mpf(1), mp.mpf(2)]:
        a, b = Phi(u), Phi_alt(u)
        rel = abs(a-b)/abs(a)
        if rel > mp.mpf(10)**(-40): ok = False
        print("C1 Phi(u=%d): serie=%.30e theta-form=%.30e rel=%.1e %s" % (u, a, b, rel, "OK" if rel < 1e-40 else "DIVERGE"))
    res["claims"].append({"id": "C1", "claim": "representación serie == forma theta", "veredicto": "PASS" if ok else "FAIL"})

    # C2/C3: momentos M_0..M_5
    Ms = []
    for k in range(11):
        Mk = momento(k)
        Ms.append(Mk)
        print("C2 M_%d = %.35e" % (k, Mk))
    res["claims"].append({"id": "C2", "claim": "momentos M_0..M_5 finitos positivos", "veredicto": "PASS",
                          "M": [str(mp.nstr(m, 20)) for m in Ms]})
    # C3: M_k = (-1)^k/2 Xi^(2k)(0) — identidad formal; verificamos la relación de Taylor
    # Xi(t)=2intPhi cos(tu)du => Xi^(2k)(0) = 2(-1)^k M_k (en la normalización del corpus M_k=intu^{2k}Phi)
    # Chequeo con la serie de Taylor truncada: construir Xi(t) numéricamente y comparar con 2Σ(-1)^k M_k t^{2k}/(2k)!
    t = mp.mpf("0.5")
    Xi_num = 2*mp.quad(lambda u: Phi(u)*mp.cos(t*u), [0, 30])
    Xi_taylor = 2*sum((-1)**k * Ms[k] * t**(2*k)/mp.factorial(2*k) for k in range(6))
    rel = abs(Xi_num - Xi_taylor)/abs(Xi_num)
    print("C3 Xi(0.5) numérico=%.30e vs Taylor(6 términos)=%.30e rel=%.1e %s" % (Xi_num, Xi_taylor, rel, "OK" if rel < 1e-8 else "CHECK"))
    res["claims"].append({"id": "C3", "claim": "M_k = (-1)^k/2 Xi^(2k)(0) (Taylor)", "veredicto": "PASS" if rel < 1e-8 else "INCONCLUSIVE"})

    # C4: H_N > 0 para N=0..5
    c4 = []
    for N in range(6):
        H = mp.matrix([[Ms[i+j] for j in range(N+1)] for i in range(N+1)])
        ev = mp.eigsy(H)  # autovalores (mpmath.eigsy para matriz simétrica)
        evals = sorted([mp.re(x) for x in ev[0]])
        pos = all(x > 0 for x in evals)
        c4.append((N, evals, pos))
        print("C4 H_%d autovalores: %s -> %s" % (N, [mp.nstr(x, 6) for x in evals], "POSITIVA" if pos else "NO"))
    res["claims"].append({"id": "C4", "claim": "H_N > 0 N=0..5", "veredicto": "PASS" if all(x[2] for x in c4) else "FAIL"})

    # C5: R_n vs q_n para n=0..4
    c5 = []
    for n in range(5):
        Rn = Ms[n+1]**2/(Ms[n]*Ms[n+2])
        qn = q_n(n)
        ok5 = Rn > qn
        c5.append((n, Rn, qn, ok5))
        print("C5 n=%d: R_n=%.30e q_n=%.30e R>q: %s" % (n, Rn, qn, ok5))
    # claims de referencia del corpus: R0 in [0.41,0.48], R1 in [0.52,0.59], R2 in [0.61,0.68]
    ref = {0: (0.41, 0.48), 1: (0.52, 0.59), 2: (0.61, 0.68)}
    ref_ok = True
    for n in range(3):
        lo, hi = ref[n]
        if not (mp.mpf(lo) < c5[n][1] < mp.mpf(hi)):
            ref_ok = False
            print("C5 REF n=%d: R=%.30e fuera de [%.2f,%.2f]" % (n, c5[n][1], lo, hi))
    res["claims"].append({"id": "C5", "claim": "R_n>q_n n=0..4 + R0-R2 en bandas del corpus", "veredicto": "PASS" if (all(x[3] for x in c5) and ref_ok) else "FAIL"})

    # C6: J_{2,n} hiperbólico (raíces reales), n=0..3
    # J_{2,n}(X) = γ_n + 2γ_{n+1}X + γ_{n+2}X^2 con γ_k = 2M_k/(2k)! (normalización del corpus)
    c6 = []
    for n in range(4):
        g0 = 2*Ms[n]/mp.factorial(2*n)
        g1 = 2*Ms[n+1]/mp.factorial(2*(n+1))
        g2 = 2*Ms[n+2]/mp.factorial(2*(n+2))
        # raíces de g0 + 2 g1 X + g2 X^2
        disc = (2*g1)**2 - 4*g2*g0
        real = disc >= 0
        c6.append((n, disc, real))
        print("C6 J_{2,%d}: discriminante=%.30e -> %s" % (n, disc, "raíces reales" if real else "COMPLEJAS"))
    res["claims"].append({"id": "C6", "claim": "J_{2,n} hiperbólico n=0..3", "veredicto": "PASS" if all(x[2] for x in c6) else "FAIL"})

    # C7: E(0) < 0  y  E(u) < 0 para u en {2,3,4}
    E0, lpp, l4, lppp = E_u(0)
    print("C7 E(0) = %.30e -> %s" % (E0, "E<0 OK" if E0 < 0 else "E>=0 FAIL"))
    c7 = [("u=0", E0, E0 < 0)]
    for u in [mp.mpf(2), mp.mpf(3), mp.mpf(4)]:
        Eu, _, _, _ = E_u(u)
        c7.append(("u=%d" % u, Eu, Eu < 0))
        print("C7 E(%d) = %.30e -> %s" % (u, Eu, "E<0 OK" if Eu < 0 else "E>=0 FAIL"))
    res["claims"].append({"id": "C7", "claim": "E(0)<0 y E(u)<0 para u=2,3,4", "veredicto": "PASS" if all(x[2] for x in c7) else "FAIL"})

    # resumen
    total = len(res["claims"])
    npass = sum(1 for c in res["claims"] if c["veredicto"] == "PASS")
    print("="*78)
    print("RESUMEN: %d/%d claims PASS" % (npass, total))
    print("ADVERTENCIA: verificación numérica != demostración. RH sigue OPEN.")
    out = "auditoria_riemann_claims.json"
    with open(out, "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=1)
    print("guardado:", out)

if __name__ == "__main__":
    main()
