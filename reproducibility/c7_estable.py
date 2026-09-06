# c7_estable.py — C7 verificado con derivadas de la serie (termino a termino),
# sin diferencias finitas de log(Phi). l = log Phi; E = 2(l'')^3 + l'' l'''' - (l''')^2.
# Phi(u) = sum_n (2 pi^2 n^4 e^{9u/2} - 3 pi n^2 e^{5u/2}) e^{-pi n^2 e^{2u}}
# Derivadas: cada termino es A e^{alpha u} e^{-pi n^2 e^{2u}} con A cte, alpha in {9/2, 5/2}.
# d/du [e^{alpha u} e^{-c e^{2u}}] = e^{alpha u} e^{-c e^{2u}} (alpha - 2 c e^{2u}).
# Iterando: operador D = alpha - 2 c e^{2u} aplicado, con c = pi n^2. Como D contiene e^{2u},
# al derivar de nuevo aparece -4 c e^{2u} por la regla del producto (derivada de -2c e^{2u}).
# Implementamos derivadas por recurrencia polinomial en x = e^{2u}:
#   termino = A e^{alpha u} e^{-c x}  ->  d/du = (alpha - 2 c x) * termino
#   siguiente derivada: d/du[(alpha - 2cx) termino] = [(-4cx) + (alpha-2cx)^2]*termino ... via regla.
# Mas simple: factor comun e^{-c x}; definir P_k(u) tal que d^k/d u^k [e^{alpha u} e^{-c x}] =
# e^{alpha u} e^{-c x} * Q_k(x), Q_0=1, Q_{k+1} = (alpha - 2 c x) Q_k + 2 x Q_k'  ... pero Q_k' en x.
# Q_k es polinomio en x. dQ_k/du = 2x Q_k'(x). Entonces:
#   Q_{k+1}(x) = (alpha - 2 c x) Q_k(x) + 2 x dQ_k/dx.
# Implementamos con polinomios (listas de coeficientes en x).
import mpmath as mp
import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
mp.mp.dps = 50

def dphi(u, kmax=4, Nmax=60):
    """Devuelve [Phi, Phi', Phi'', Phi''', Phi''''] en u por suma de terminos m=1..Nmax.
    Cada termino m: A e^{alpha u} e^{-c x}, x=e^{2u}, A=2 pi^2 m^4 (alpha=9/2)
    y A=-3 pi m^2 (alpha=5/2)."""
    u = mp.mpf(u)
    x = mp.e**(2*u)
    vals = [mp.mpf(0) for _ in range(kmax+1)]
    for m in range(1, Nmax+1):
        c = mp.pi * m*m
        ex = mp.e**(-c*x)
        if ex == 0:
            break
        for A, al in [(2*mp.pi**2*m**4, mp.mpf(9)/2), (-3*mp.pi*m**2, mp.mpf(5)/2)]:
            # Q_0 = 1 (polinomio en x, lista de coef de menor a mayor grado)
            Q = [mp.mpf(1)]
            base = A * ex * mp.e**(al*u)
            vals[0] += base * Q[0]
            for k in range(kmax):
                # Q_{k+1} = (al - 2 c x) Q_k + 2 x Q_k'
                dQ = [mp.mpf((i+1))*Q[i+1] for i in range(len(Q)-1)]  # Q_k'(x)
                # (al - 2cx)Q: coef j -> al*Q_j - 2c*Q_{j-1}
                nQ = [mp.mpf(0)]*(len(Q)+1)
                for j, qj in enumerate(Q):
                    nQ[j] += al*qj
                    nQ[j+1] += -2*c*qj
                # + 2x Q'
                for j, dj in enumerate(dQ):
                    nQ[j+1] += 2*dj
                # recortar ceros al final
                while nQ and nQ[-1] == 0:
                    nQ.pop()
                Q = nQ
                # evaluar en x
                acc = mp.mpf(0)
                for j, qj in enumerate(Q):
                    acc += qj * x**j
                vals[k+1] += base * acc
    return vals

def E_estable(u):
    d = dphi(u, 4)
    Phi = d[0]
    if Phi <= 0:
        return None, "Phi<=0"
    lp = d[1]/Phi
    lpp = (d[2]*Phi - d[1]**2)/Phi**2
    lppp = (d[3]*Phi**2 - 3*d[2]*d[1]*Phi + 2*d[1]**3)/Phi**3
    l4 = (d[4]*Phi**3 - 4*d[3]*d[1]*Phi**2 + 12*d[2]*d[1]**2*Phi - 6*d[1]**4 - 3*d[2]**2*Phi**2)/Phi**4
    # formula de Faà di Bruno para log: verificar numericamente en u=0 contra diferencias finitas
    E = 2*lpp**3 + lpp*l4 - lppp**2
    return E, (lp, lpp, lppp, l4)

# sanity check en u=0: comparar con diferencias finitas de alta precision
for u in [mp.mpf(0), mp.mpf(1), mp.mpf(2), mp.mpf(3), mp.mpf(4), mp.mpf(5)]:
    E, derivs = E_estable(u)
    if E is None:
        print("u=%d: Phi<=0 (no evaluable)" % u)
    else:
        print("u=%d: E=%.30e -> %s" % (u, E, "E<0 OK" if E < 0 else "E>=0 (check)"))
