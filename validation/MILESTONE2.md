# MILESTONE 2 — Perturbaciones covariantes completas (25-08-2026)

**Nivel de evidencia: S2 (numérico reproducible).** No es evidencia observacional.

## Pregunta del hito

¿La inestabilidad escalar sub-Hubble del milestone 1 (δ_φ ×9.2e7) es física
real del k-essence o un artefacto de la aproximación cuasiestática (Φ· = 0)?

## Resultados (sistema covariante completo, gauge Newtoniano, sin cuasiestática)

| Cantidad | M1 (cuasiestático) | M2 (covariante completo) |
|---|---|---|
| Crecimiento de δ_φ vs modo grande | ×9.2e7 | **×23** |
| Inestabilidad escalar | **SÍ** | **NO** |
| Δ_P(k) en k ∈ [0.05, 0.3] | **−0.997** | **≤ +0.026** |
| σ8 ratio (vs c_s²=1) | 0.058 | **1.00006** |

## Lectura científica

1. **La inestabilidad del M1 era un artefacto de la cuasiestática**: al incluir
   la evolución de Φ (constraint de momento) y el acoplamiento δ−Φ·, el sector
   escalar es estable en las escalas consideradas. Queda verificada la
   advertencia del documento (§8: "debe comprobarse la estabilidad completa de
   las perturbaciones").
2. **Sin supresión**: con la trayectoria de referencia (c_s² ≈ 0.98), la
   potencia de materia es prácticamente ΛCDM (Δ_P ≈ 0). El benchmark de v4
   (c_s² = 0.08 → supresión en k ≳ 0.1) queda definitivamente descalificado a
   nivel de fondo (§7), de HMF/lentes (M1) y de perturbaciones (M2).
3. **Resultado del programa (trun.txt §50)**: con ξ=0, λ=5, Λ=0.15 el modelo es
   estable pero **no produce su firma observacional** (Δ_P ≠ 0). Esto constituye
   una **restricción del espacio de parámetros** — uno de los tres resultados
   científicamente útiles del programa (confirmación / refutación / restricción).

## Pendientes

- M3: normalización absoluta As→P(k) y σ8 real (ICs exactas en radiación).
- Barrido de sensibilidad (§23.9): λ, Λ, V_0 (y ξ≠0 en M4) para buscar
  trayectorias con c_s² ≪ 1 donde la firma Δ_P emerja.
- f = 5.03 (borde del gradiente): revisar la definición de f en a=1.

## Archivos

- `numerics/perturbations_full.py` + `data/perturbaciones_m2.json`
- Teoría: `theory/perturbation_equations.md` (sistema completo documentado)
