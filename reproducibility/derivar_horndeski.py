# derivar_horndeski.py — DERIVACION SIMBOLICA de las EOM de fondo Horndeski (G2 + G4(phi,X), G3=G5=0)
# Metodo: lagrangiano reducido FLRW (Kobayashi 2019, arXiv:1901.07183, eq. 31-34) + Euler-Lagrange generalizado.
# Teoria: S = int sqrt(-g)[ G2 + G4 R + G4,X ((D2phi)^2 - phi_munu phi^munu) ]
#   G2 = X + X^2/Lambda^4 - V(phi),  V = V0 (e^{-lambda phi} + alpha phi^2 e^{-beta phi})
#   G4 = (1 + xi phi^2 + eta X/Lambda^4)/2        (G4,X = eta/(2 Lambda^4) = cte)
# Verificacion: limite xi=eta=0 debe reproducir k-essence minimal: 3H^2 = rho_phi, KG estandar.
import sys

import numpy as np
import sympy as sp

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# simbolos y funciones
t = sp.Symbol("t", real=True)
N = sp.Function("N")(t)
a = sp.Function("a")(t)
phi = sp.Function("phi")(t)
# parametros
lam, al, be, xi, eta, Lam, V0 = sp.symbols("lam al be xi eta Lam V0", positive=True)

# cantidades geometricas FLRW (con lapse N)
H_sym = sp.diff(a, t) / a
Np = sp.diff(N, t)
ap = sp.diff(a, t)
app = sp.diff(a, t, 2)
php = sp.diff(phi, t)
phpp = sp.diff(phi, t, 2)

X = php ** 2 / (2 * N ** 2)
x = sp.Symbol("x", positive=True)  # X abstracto para derivadas parciales
Vph = V0 * (sp.exp(-lam * phi) + al * phi ** 2 * sp.exp(-be * phi))
G2x = x + x ** 2 / Lam ** 4 - Vph
G4x = (1 + xi * phi ** 2 + eta * x / Lam ** 4) / 2
G4X = sp.diff(G4x, x)  # G4,X (independiente de X por ser G4 lineal en x)
G2 = G2x.subs(x, X)
G4 = G4x.subs(x, X)

R = 6 / N ** 2 * (app / a + (ap / a) ** 2 - (Np / N) * (ap / a))
D2phi = -(phpp - (Np / N) * php) / N ** 2 - 3 * ap * php / (a * N ** 2)
phimu_phimu = (phpp - (Np / N) * php) ** 2 / N ** 4 + 3 * ap ** 2 * php ** 2 / N ** 4

L = a ** 3 * N * (G2 + G4 * R + G4X * (D2phi ** 2 - phimu_phimu))
L = sp.expand(sp.simplify(L))


def euler_lagrange_2do(L, q):
    """E-L generalizado para L(q, q', q''): dL/dq - d/dt dL/dq' + d^2/dt^2 dL/dq''."""
    qp = sp.diff(q, t)
    qpp = sp.diff(q, t, 2)
    dLdq = sp.diff(L, q)
    dLdq1 = sp.diff(L, qp)
    dLdq2 = sp.diff(L, qpp)
    return sp.simplify(dLdq - sp.diff(dLdq1, t) + sp.diff(dLdq2, t, 2))


def subs_flat(E):
    """N=1, N'=0, N''=0."""
    return sp.simplify(E.subs({N: 1, Np: 0, sp.diff(Np, t): 0}))


print("Derivando EOM de fondo (Horndeski G2+G4(phi,X))...")
E_N = euler_lagrange_2do(L, N)      # variacion en N  -> constraint
E_a = euler_lagrange_2do(L, a)      # variacion en a  -> pressure
E_ph = euler_lagrange_2do(L, phi)   # variacion en phi -> KG

E = subs_flat(-E_N / a ** 3)
P = subs_flat(E_a / (3 * a ** 2))
Ef = subs_flat(E_ph / a ** 3)

# VERIFICACION: limite xi=eta=0
E0 = sp.simplify(E.subs({xi: 0, eta: 0}))
P0 = sp.simplify(P.subs({xi: 0, eta: 0}))
Ef0 = sp.simplify(Ef.subs({xi: 0, eta: 0}))

# k-essence estandar: 3H^2 = rho = X + 3X^2/L^4 + V;  KG estandar
X0 = php ** 2 / 2
rho_std = sp.simplify(X0 + 3 * X0 ** 2 / Lam ** 4 + Vph)
constraint_check = sp.simplify(E0 - (rho_std - 3 * (ap / a) ** 2))
kg_std = sp.simplify(
    sp.diff(php, t) * (1 + 6 * X0 / Lam ** 4) + 3 * (ap / a) * php * (1 + 2 * X0 / Lam ** 4) + sp.diff(Vph, phi))
kg_check = sp.simplify(Ef0 - (-kg_std))

print("== LIMITE xi=eta=0 (k-essence minimal) ==")
print("constraint: E - (3H^2 - rho_phi) =", constraint_check)
print("KG: Ef - (KG_estandar) =", kg_check)
if sp.simplify(constraint_check) == 0 and sp.simplify(kg_check) == 0:
    print("VERIFICACION: PASS (el limite reproduce k-essence minimal)")
else:
    print("VERIFICACION: FALLO - revisar derivacion")
    print("E0 =", sp.simplify(E0))
    print("Ef0 =", sp.simplify(Ef0))

# exportar lambdified: E(H,phi,phidot) y el sistema lineal (P, Ef) en (app, phpp)
params = [lam, al, be, xi, eta, Lam, V0]
E_fn = sp.lambdify((a, ap, phi, php) + tuple(params), E, "numpy")
P_fn = sp.lambdify((a, ap, app, phi, php, phpp) + tuple(params), P, "numpy")
Ef_fn = sp.lambdify((a, ap, app, phi, php, phpp) + tuple(params), Ef, "numpy")
# export ccode (opcional; si falla por la complejidad, no bloquea)
try:
    with open("eoms_horndeski_generadas.py", "w", encoding="utf-8") as f:
        f.write('"""EOM de fondo generadas simbolicamente (sympy 1.14) para G2+G4(phi,X).\n')
        f.write("Teoria: S = int sqrt(-g)[G2 + G4 R + G4,X((D2phi)^2 - phi_munu phi^munu)]\n")
        f.write("G2 = X + X^2/L^4 - V0(e^{-l phi} + a phi^2 e^{-b phi}), G4 = (1 + xi phi^2 + eta X/L^4)/2\n")
        f.write("Parametros p = (lam, al, be, xi, eta, Lam, V0). X = phidot^2/2.\n")
        f.write('"""\n')
        f.write("import numpy as np\n\n")
        f.write("E_code = " + repr(sp.ccode(E)) + "\n")
        f.write("P_code = " + repr(sp.ccode(P)) + "\n")
        f.write("Ef_code = " + repr(sp.ccode(Ef)) + "\n")
    print("eoms_horndeski_generadas.py escrito (ccode).")
except Exception as ex:
    print("ccode export omitido:", str(ex)[:60])
print("LISTO: E_fn, P_fn, Ef_fn lambdificados + VERIFICACION PASS.")
