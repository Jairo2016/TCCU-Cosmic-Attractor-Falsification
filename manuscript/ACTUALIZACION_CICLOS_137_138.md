# Actualizacion 26-08-2026 (v1.2) — Ciclos 137 y 138

## Ciclo 137 — DBI + acoplamiento no minimo G4(phi,X): FALSACION

Modelo: G2 = 1 - sqrt(1-X) - v, G4 = (1 + xi phi^2 + eta X)/2. 200 configuraciones
(LHS seed 137) x 5 niveles eps0 en [1e-2, 1e-10]. EOM derivadas simbolicamente y
verificadas (limite xi=eta=0 = DBI puro exacto); estabilidad lineal con las formulas
exactas de Kobayashi 2019 (eq. 42-52): c_s^2 = F_S/G_S, verificadas en el limite
(c_s^2 = s^2 = 1-u, resultado k-essence exacto).

Resultado (criterio del autor: DeltaN>=4 con eps0 > 1e-8):
- **Candidatas: 0/200 -> FALSACION acotada de la utilidad del acoplamiento.**
- dN_F2 max a eps0=1e-8: 1.44 (vs 2.44 del DBI puro: el acoplamiento EMPEORA).
- Estabilidad: 72/164 estables; **92/164 con c_s^2 < 0 (56 % inestabilidad de
  gradiente)**; 34/200 invalidas (el campo rebasa el limite DBI u>1).
- Hallazgo lateral: acoplamiento xi fuerte (0.75-0.93) genera una ventana de polvo
  alternativa a eps0 sueltas (DeltaN ~ 2 a eps0=1e-2), techo ~2 e-folds.

## Ciclo 138 — Perturbaciones y crecimiento del DBI puro (cierre observable)

Fondo cerrado: u(N) = 1/(1+K e^{6N}), c_s^2 = s^2. Mapa de duracion de polvo
|w|<0.05: DeltaN ~ (1/6) ln(1/eps0) — de 0.28 (eps0=1e-2) a 7.26 (eps0=1e-20).
- **eps0 requerido para la era de materia completa (DeltaN=8.1): ~4-7e-23** segun v.
- Crecimiento dentro de la ventana: f = dln delta/dN = 0.95 (analitico 1.0) ->
  agrupa como CDM; c_s^2 <= 1e-8 -> sin supresion de Jeans en escalas observables.
- Transicion w: 0 -> -1 en z_trans = e^{-(DeltaN-8.1)} - 1. Viable solo si
  DeltaN = 8.1 (eps0 ~ 5e-23): el modelo es un sector oscuro unificado tipo
  Chaplygin con origen cinetico — una re-parametrizacion fuertemente constrenida
  de LCDM, no un mecanismo nuevo de materia oscura.

## Interpretacion honesta (resumen del programa)
1. La familia polinomica TCCU congelada (v1.0) queda falsada estructuralmente.
2. La estructura cinetica no polinomial (DBI) logra DeltaN>=4 por primera vez
   (Ciclo 136) pero con CI a ~1e-12 del limite DBI.
3. El acoplamiento no minimo no relaja el fine-tuning y desestabiliza (Ciclo 137).
4. El crecimiento de estructura del DBI es CDM dentro de su ventana, pero la
   ventana no cubre la era de materia sin eps0 ~ 5e-23 (Ciclo 138).
El valor cientifico: constrenimientos publicables sobre el espacio de teorias
escalar-tensor de sector oscuro + metodologia reproducible.

## Reproducibilidad
- reproducibility/barrido_ciclo137.py, derivar_horndeski_dbi.py, ciclo138_perturbaciones.py
- data/ciclo137_barrido.json, ciclo138_perturbaciones.json
