# MILESTONE 1 — Perturbaciones cuasiestáticas y P(k) (25-08-2026)

**Nivel de evidencia: S2 (numérico) con normalización S3.** No es evidencia observacional.

## Resultados (RUN_ID del fondo: 8f7022e25d654965)

| Cantidad | Valor | Lectura |
|---|---|---|
| c_s² mediana (a<1) | **0.9774** | ≈ 1: la trayectoria no produce c_s² pequeña |
| Inestabilidad escalar sub-Hubble | **SÍ** (δ_φ ×9.2e7) | término −(1−3c_s²)θ_φ anti-amortigua con c_s² > 1/3 |
| f (a=1) | **−0.046** | crecimiento negativo — patológico |
| σ8_TCCU (ratio→Planck) | **0.047** | potencia destruida a k ≳ 0.08 |
| Δ_P(k) (firma §39) | **−0.997 en k ≥ 0.08** | supresión total de P(k) en pequeña escala |

## Lectura científica honesta

1. La "supresión" que v4 atribuía a la escala de Jeans (c_s² = 0.08) **no emana
   de la trayectoria** (c_s² ≈ 1) — consistente con la retractación §7. El
   benchmark de v4 queda descalificado también a nivel de perturbaciones.
2. En su lugar, el sistema perturbativo cuasiestático implementado muestra una
   **inestabilidad escalar sub-Hubble** que destruye la potencia de materia.
   Esto puede ser (a) física real del k-essence con c_s² > 1/3, o (b) un
   artefacto de la aproximación cuasiestática (Φ_N' = 0, sub-Hubble, ICs en
   radiación). **Pendiente crítico del milestone 2**: derivar e integrar el
   sistema covariante completo (gauge invariante, Mukhanov-Sasaki para
   k-essence) para decidir (a) vs (b).
3. F2 (DM-like) ya había fallado en el fondo; ahora el sector perturbativo
   refuerza el veredicto: con estos parámetros el campo no se comporta como
   materia oscura agrupada.

## Archivos

- `numerics/background.py` + `tests/test_background.py` — conservación C1-C3 PASA.
- `numerics/perturbations.py` — sistema cuasiestático + T(k) + Δ_P(k) + fσ8.
- `data/perturbaciones_m1.json`, `data/background_v41.json`.

## Siguientes hitos (proyecto multisesión)

M2: sistema covariante completo de perturbaciones (k-essence, gauge invariante).
M3: ICs adiabáticas exactas en radiación y normalización As→P(k) absoluta.
M4: rama ξ ≠ 0 (estabilidad tensorial/escalar, G_eff, restricciones solares).
M5: pipeline Euclid/LSST con likelihood y covarianzas documentadas.
