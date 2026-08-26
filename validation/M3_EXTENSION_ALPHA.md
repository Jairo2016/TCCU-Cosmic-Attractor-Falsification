# M3 — Extensión P(X) = X + X^α/Λ^{4(α−1)} (25-08-2026)

**Nivel de evidencia: S2 (numérico) + verificación analítica del límite.**

## Resultado doble

| α | c_s²_min | F2 (DM-like) | w_final |
|---|---|---|---|
| 2.0 (v4.1) | 0.354 | NO (span 0.00) | −0.722 |
| 3.0 | 0.210 | NO | −0.840 |
| 4.0 | 0.149 | NO | −0.872 |
| 5.0 | 0.116 | NO | −0.886 |
| 6.25 | **0.091** | NO | −0.896 |
| 8.0 | 0.069 | NO | −0.903 |
| 10.0 | 0.055 | NO | −0.907 |

## Lectura científica

1. **La extensión SÍ rompe el piso de c_s² = 1/3** (S1): en el régimen dominado
   por X^α, c_s² → 1/(2α−1). α = 6.25 alcanza **c_s² ≈ 0.09**, compatible con el
   benchmark histórico de v4 (0.08) — la parte "velocidad de sonido" del
   programa es realizable en esta familia.
2. **El régimen DM-like sigue sin emerger** (F2 NO para todo α, span 0.00): con
   el potencial exponencial λ = 5 y estas condiciones iniciales, el campo no
   produce w ≈ 0 con ρ_Φ ∝ a⁻³ sostenidos. De hecho, w_final se vuelve MÁS
   negativo (más tipo energía oscura) al crecer α.
3. **Diagnóstico preciso de lo que falta**: el problema no es solo la forma
   cinética — es el acoplamiento potencial-tracking. Para un régimen DM-like
   con k-essence se necesita (a) pendiente λ menor (tracking de materia exige
   λ ≲ √3 ≈ 1.7 en escalar canónico, o la condición análoga del k-essence),
   o (b) un potencial con tramo tipo tracker (no exponencial puro).

## Consecuencia programática

- La familia X^α queda **caracterizada cuantitativamente** (c_s² vs α tabulado).
- El siguiente experimento científico (M3b): barrido conjunto (α, λ) con
  λ ∈ [0.5, 3] buscando la región de tracking donde F2 pase y c_s² < 1/3.

## Archivos

- `numerics/extension_alpha.py` + `data/extension_alpha.json`
- Parámetros de referencia bloqueados: `configs/PARAMETERS_LOCKED.json`
  (SHA256 03157cbd…, ledger af622447…).
