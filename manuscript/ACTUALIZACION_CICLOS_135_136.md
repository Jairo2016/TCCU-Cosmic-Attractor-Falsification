# Actualizacion 26-08-2026 — Ciclos 135 y 136 del programa de falsacion TCCU

Estado del arte: el paquete v1.0 falsa sistematicamente el espacio polinomico
P(X,phi)=X+X^2/L^4-V (850 configuraciones -> 0 con F2 sostenido). Esta
actualizacion extiende el programa en dos direcciones autorizadas por el autor.

## Ciclo 135 — expansion parametrica (potencial hibrido + acoplamiento no minimo)

- Ansatz: V = V0(e^{-l phi} + a phi^2 e^{-b phi}), G4 = (1 + xi phi^2 + eta X/L^4)/2.
- EOM de fondo derivadas SIMBOLICAMENTE (lagrangiano reducido FLRW, Kobayashi
  2019, arXiv:1901.07183, eq. 31-34) y verificadas: el limite xi=eta=0 reproduce
  k-essence minimal exactamente (PASS).
- Barrido: 200 configuraciones (LHS + surrogate GP), reproducible (seed 135).
- Resultado: F2a = 0 (nueva falsacion acotada del espacio expandido), F2b = 9
  (orbitas recurrentes), dN_max = 0.36 e-foldings (vs 0.04 del modelo original,
  9x mejor, aun 11x corto del requisito DeltaN>=4).

## Ciclo 136 — DBI / cinetica pura: primer DeltaN>=4 del programa

- Modelo: G2 = L^4(1 - sqrt(1 - X/L^4)) - V0 (DBI + offset constante), G4 = 1/2,
  sin potencial dependiente del campo (mecanismo de estructura cinetica, linea
  de Scherrer 2004, astro-ph/0402316).
- Analitico: la dinamica de fondo se reduce a du/dN = -6u(1-u) (autonoma,
  integrable), w = (1-s-v)/(1/s-1+v), s = sqrt(1-u); w=0 se cruza en
  u_cross = 2v-v^2. Prediccion: ventana DeltaN ~ (1/6) ln((1-eps0)/eps0) + O(1),
  con eps0 = 1-u0 la distancia de la condicion inicial al limite DBI.
- Resultado (360 configuraciones, seed 136, verificacion RK4 vs forma cerrada
  1.3e-9):
  * CI near-bound (eps0 log-uniforme en [1e-14,1e-2]): F2 = 35/180 (19%),
    F2a = 103/180 (57%), dN_max(F2) = 4.75, dN_max(|w|<0.05) = 4.91.
  * CI genericas (u0 uniforme en (0,0.999]): F2 = 0/180, dN_max = 0.56.
  * Umbral: eps0 <= 6e-13 (v en 0.95-0.99) para DeltaN>=4.
- Mecanismo: cruce lento de la superficie de polvo (P_X -> inf cerca del limite
  DBI), NO un atractor. La familia polinomica tiene un tope duro estructural
  (~0.1 e-foldings); la estructura cinetica no polinomial lo supera.
- Leccion tecnica: integrar en u cerca de u=1 pierde precision float64
  (decrementos < ULP); integrar eps = 1-u evita la cancelacion catastrifica.

## Reproducibilidad

- reproducibility/barrido_ciclo135.py, reproducibility/barrido_ciclo136.py,
  reproducibility/derivar_horndeski.py
- data/ciclo135_barrido.json, data/ciclo136_barrido.json

## Interpretacion honesta

1. El espacio polinomico congelado (v1.0) queda falsado estructuralmente:
   la residencia w=0 >= 4 e-foldings es imposible por la curvatura finita de P.
2. La familia DBI + offset logra DeltaN>=4 por primera vez en el programa, con
   parametro de modelo O(1) (sin fine-tuning de modelo), a cambio de condiciones
   iniciales a ~1e-12 del limite DBI (fisicamente motivadas por la salida de
   inflacion DBI) y crecimiento solo logaritmico de la ventana con 1/eps0.
3. Pendientes: acoplamiento G4(phi,X) sobre DBI para relajar eps0; busqueda de
   P(X) con atraccion genuina a w=0; validacion de perturbaciones (F2 valida
   solo el fondo homogeneo).
