# M3b — Falsación del k-essence X^α + exponencial como tracker DM-like

**Fecha:** 25-08-2026 · **Nivel de evidencia:** S2 (442 puntos numéricos).

## Resultado

| Métrica | Valor |
|---|---|
| Puntos barridos (α × λ) | 442 (α∈[2,10] paso 0.5; λ∈[0.5,3] paso 0.1) |
| Puntos con ventana F2 (ΔN≥4) | **0** |
| Puntos con al menos 1 e-folding de F2 | **0** (span=0.00 en todos) |
| c_s²_min global | min **0.056**, mediana **0.104** (requisito de sonido bien cubierto) |

## Conclusión científica

La familia `P(X) = X + X^α/Λ^{4(α−1)} − V₀ e^{−λφ}` **no produce el régimen
DM-like** (|w|<0.05 y ρ_Φ∝a⁻³ simultáneos) en ninguna combinación de
α ∈ [2,10], λ ∈ [0.5,3]. El fallo es **total y sistemático**: la condición
simultánea nunca se satisface ni siquiera momentáneamente.

- La **velocidad de sonido deja de ser el problema**: c_s² < 0.2 es alcanzable
  (α ≥ 5), el requisito cinético está resuelto.
- El **potencial exponencial es el obstáculo**: con V = V₀ e^{−λφ} el campo o
  bien congela (V-dominante, w→−1) o bien rueda sin equilibrar cinética con
  potencial en el régimen w≈0 sostenido.

## Decisión programática (trun.txt §50: resultado de refutación parcial)

1. **La subclase exponencial queda falsada como tracker DM-like** en esta
   rejilla. El benchmark v4 (c_s²≈0.08 + supresión) era doblemente
   inalcanzable: imposible en v4.1 (piso 1/3, S1) y sin régimen DM-like en la
   extensión X^α (S2).
2. **Dos direcciones abiertas** (modificación más profunda, como anticipó el
   Creador):
   - **(a) Potencial con tramo tracker**: p. ej. V ∝ Φ^{−n} (inverso-potencia)
     o potenciales con meseta que permitan w≈0 sostenido durante la era de
     materia.
   - **(b) Acoplamiento no mínimo (M4, ξ≠0)**: F(Φ)=1+ξΦ² modifica el sector
     cinético y la gravedad efectiva, abriendo otro régimen.

## Archivos

- `numerics/barrido_m3b.py` + `data/barrido_m3b.json`
- `figures/heatmap_m3b.png` (mapa de calor α×λ con c_s²_min; sin estrellas F2)
- Base bloqueada: `configs/PARAMETERS_LOCKED.json` (v4.1, sometida a falsación)
