# derivar_horndeski_dbi.py — DERIVACION SIMBOLICA de las EOM de fondo Horndeski para DBI + G4(phi,X)
# Modelo (Ciclo 137): G2 = 1 - sqrt(1 - X) - v   (DBI puro con offset v = V0/L^4, L^4 = 1)
#                     G4 = (1 + xi phi^2 + eta X)/2   (acoplamiento no minimo, G4,X = eta/2)
# Metodo: lagrangiano reducido FLRW (Kobayashi 2019, arXiv:1901.07183, eq. 31-34) + Euler-Lagrange generalizado.
# Verificacion: limite xi=eta=0 debe reproducir DBI puro:
#   constraint: 3H^2 = rho = (1/s - 1) + v, s = sqrt(1-X), X = phidot^2/2
#   KG: (1/(2 s^3)) phipp + 3H (1/(2 s)) php = 0   <=>  phipp + 3H s^2 php = 0
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
v, xi, eta = sp.symbols("v xi eta", real=True)

H_sym = sp.diff(a, t) / a
Np = sp.diff(N, t)
ap = sp.diff(a, t)
app = sp.diff(a, t, 2)
php = sp.diff(phi, t)
phpp = sp.diff(phi, t, 2)

X = php ** 2 / (2 * N ** 2)
x = sp.Symbol("x", positive=True)  # X abstracto
G2x = 1 - sp.sqrt(1 - x) - v
G4x = (1 + xi * phi ** 2 + eta * x) / 2
G4X = sp.diff(G4x, x)  # eta/2 (constante)
G2 = G2x.subs(x, X)
G4 = G4x.subs(x, X)

R = 6 / N ** 2 * (app / a + (ap / a) ** 2 - (Np / N) * (ap / a))
D2phi = -(phpp - (Np / N) * php) / N ** 2 - 3 * ap * php / (a * N ** 2)
phimu_phimu = (phpp - (Np / N) * php) ** 2 / N ** 4 + 3 * ap ** 2 * php ** 2 / N ** 4

L = a ** 3 * N * (G2 + G4 * R + G4X * (D2phi ** 2 - phimu_phimu))
L = sp.expand(sp.simplify(L))


def euler_lagrange_2do(L, q):
    qp = sp.diff(q, t)
    qpp = sp.diff(q, t, 2)
    dLdq = sp.diff(L, q)
    dLdq1 = sp.diff(L, qp)
    dLdq2 = sp.diff(L, qpp)
    return sp.simplify(dLdq - sp.diff(dLdq1, t) + sp.diff(dLdq2, t, 2))


def subs_flat(E):
    return sp.simplify(E.subs({N: 1, Np: 0, sp.diff(Np, t): 0}))


print("Derivando EOM de fondo (DBI + G4(phi,X))...")
E_N = euler_lagrange_2do(L, N)
E_a = euler_lagrange_2do(L, a)
E_ph = euler_lagrange_2do(L, phi)

E = subs_flat(-E_N / a ** 3)
P = subs_flat(E_a / (3 * a ** 2))
Ef = subs_flat(E_ph / a ** 3)

# VERIFICACION: limite xi=eta=0 -> DBI puro
E0 = sp.simplify(E.subs({xi: 0, eta: 0}))
Ef0 = sp.simplify(Ef.subs({xi: 0, eta: 0}))

X0 = php ** 2 / 2
s0 = sp.sqrt(1 - X0)
rho_dbi = sp.simplify(1 / s0 - 1 + v)
constraint_check = sp.simplify(E0 - (rho_dbi - 3 * (ap / a) ** 2))
# KG DBI: (1/(2 s^3)) phpp + 3H (1/(2 s)) php = 0
kg_dbi = sp.simplify(phpp / (2 * s0 ** 3) + 3 * (ap / a) * php / (2 * s0))
kg_check = sp.simplify(Ef0 - (-kg_dbi))

print("== LIMITE xi=eta=0 (DBI puro) ==")
print("constraint: E - (3H^2 - rho_dbi) =", constraint_check)
print("KG: Ef - (KG_dbi) =", kg_check)
if sp.simplify(constraint_check) == 0 and sp.simplify(kg_check) == 0:
    print("VERIFICACION: PASS (el limite reproduce DBI puro)")
else:
    print("VERIFICACION: FALLO - revisar derivacion")
    print("E0 =", sp.simplify(E0))
    print("Ef0 =", sp.simplify(Ef0))

# exportar lambdified: parametros p = (v, xi, eta)
params = [v, xi, eta]
E_fn = sp.lambdify((a, ap, phi, php) + tuple(params), E, "numpy")
P_fn = sp.lambdify((a, ap, app, phi, php, phpp) + tuple(params), P, "numpy")
Ef_fn = sp.lambdify((a, ap, app, phi, php, phpp) + tuple(params), Ef, "numpy")

# ESTABILIDAD LINEAL (Kobayashi 2019, eq. 42-52; G3=G5=0):
#   G_T = 2(G4 - 2X G4X),  F_T = 2 G4
#   Sigma = X G2X + 2X^2 G2XX - 6H^2 G4 + 6H^2(7X G4X + 16X^2 G4XX + 4X^3 G4XXX)
#           - 6H phidot (G4phi + 5X G4phiX + 2X^2 G4phiXX)
#   Theta = 2H G4 - 8H X G4X - 8H X^2 G4XX + phidot G4phi + 2X phidot G4phiX
#   G_S = (Sigma/Theta^2) G_T^2 + 3 G_T
#   F_S = (1/a) d/dt (a G_T^2/Theta) - F_T ;  c_s^2 = F_S/G_S ;  c_GW^2 = F_T/G_T
G2Xx = sp.diff(G2x, x)
G2XXx = sp.diff(G2x, x, 2)
G4xx = sp.diff(G4x, x)
G4xxx = sp.diff(G4x, x, 2)
G4xxxx = sp.diff(G4x, x, 3)
G4phix = sp.diff(G4x, phi)
G4phixx = sp.diff(G4x, phi, x)
G4phiXXx = sp.diff(G4x, phi, x, 2)
H0 = sp.Symbol("H0", positive=True)
X0 = php ** 2 / 2
GT_sym = sp.simplify(2 * (G4x - 2 * X0 * G4xx).subs(x, X0))
FT_sym = sp.simplify((2 * G4x).subs(x, X0))
Sigma_sym = sp.simplify(
    (X0 * G2Xx + 2 * X0 ** 2 * G2XXx - 6 * H0 ** 2 * G4x
     + 6 * H0 ** 2 * (7 * X0 * G4xx + 16 * X0 ** 2 * G4xxx + 4 * X0 ** 3 * G4xxxx)
     - 6 * H0 * php * (G4phix + 5 * X0 * G4phixx + 2 * X0 ** 2 * G4phiXXx)).subs(x, X0))
Theta_sym = sp.simplify(
    (2 * H0 * G4x - 8 * H0 * X0 * G4xx - 8 * H0 * X0 ** 2 * G4xxx
     + php * G4phix + 2 * X0 * php * G4phixx).subs(x, X0))
GT_fn = sp.lambdify((phi, php, xi, eta), GT_sym, "numpy")
FT_fn = sp.lambdify((phi, php, xi, eta), FT_sym, "numpy")
Sigma_fn = sp.lambdify((H0, phi, php) + tuple(params), Sigma_sym, "numpy")
Theta_fn = sp.lambdify((H0, phi, php) + tuple(params), Theta_sym, "numpy")
# verificacion analitica del limite: c_s^2 = 1 - X  (k-essence DBI exacto)
print("L_Sigma(limite xi=eta=0) =", sp.simplify(Sigma_sym.subs({xi: 0, eta: 0})))
print("L_Theta(limite xi=eta=0) =", sp.simplify(Theta_sym.subs({xi: 0, eta: 0})))
print("G_T(limite) =", sp.simplify(GT_sym.subs({xi: 0, eta: 0})), " F_T(limite) =", sp.simplify(FT_sym.subs({xi: 0, eta: 0})))

# exportar tambien G4, G4X, G2, P_X, P_XX (para estabilidad lineal)
G2_min = G2x.subs(x, X0)
P_X = sp.diff(G2x, x)
P_XX = sp.diff(G2x, x, 2)
s_fn = sp.lambdify((php,), s0, "numpy")
G4_fn = sp.lambdify((phi, php, xi, eta), G4x.subs(x, X0), "numpy")
G4X_fn = sp.lambdify((), G4X, "numpy")
P_X_fn = sp.lambdify((php,), P_X.subs(x, X0), "numpy")
P_XX_fn = sp.lambdify((php,), P_XX.subs(x, X0), "numpy")
print("LISTO: E_fn, P_fn, Ef_fn (params v, xi, eta) + GT_fn, FT_fn, Sigma_fn, Theta_fn + VERIFICACION.")
