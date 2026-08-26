# BARRIDO DE PARAMETROS (lambda, Lambda, V0) — 25-08-2026

**Nivel de evidencia: S1 (analítico) + S2 (numérico).**

## Resultado principal: la firma de v4 es IMPOSIBLE en esta forma k-essence

El barrido (168 puntos: λ∈{2..10}, Λ∈{0.05..1}, V₀∈{0.01..10}) encuentra
**0 candidatos** con c_s² < 0.3. La c_s² mínima observada es **0.334** — y eso
es inevitable:

$$
c_s^2 = \frac{1 + 2r}{1 + 6r} \in \left[\tfrac{1}{3}, 1\right], \qquad r = \frac{X}{\Lambda^4} \ge 0.
$$

**El benchmark de v4 (c_s² = 0.08, supresión en k ≳ 0.1) es matemáticamente
imposible** en el modelo P(X) = X + X²/Λ⁴ − V: la velocidad de sonido tiene un
piso 1/3 (límite dominado por X²). Para obtener c_s² < 1/3 se necesitaría otra
forma funcional de P(X) (cambio de modelo, no de parámetros).

## Mejores candidatos (piso 1/3)

| λ | Λ | V₀ | c_s²_min | r_max (invertido) |
|---|---|---|---|---|
| 10 | 0.05 | 10 | 0.3341 | ≈ 166 |
| 8 | 0.05 | 10 | 0.3343 | ≈ 166 |
| 6 | 0.05 | 10 | 0.3344 | ≈ 166 |

Incluso en el piso, c_s² = 1/3 daría k_J ≈ 0.08·√(0.01/(1/3)) ≈ 0.0139 h/Mpc:
una supresión **débil y en escalas muy grandes** (no la firma de v4).

## Consecuencia programática (trun.txt §50)

- Resultado de **restricción/refutación parcial**: con P(X)=X+X²/Λ⁴−V y
  potencial exponencial, la firma Δ_P(k) fuerte de v4 no emerge en ninguna
  combinación de (λ, Λ, V₀).
- Próximas direcciones: (a) otra forma de P(X) con c_s² < 1/3 (p. ej.
  P ∝ X^α con α > 1), (b) rama ξ ≠ 0 (M4) que modifica el sector cinético.

## Archivos

- `numerics/barrido_parametros.py` + `data/barrido_parametros.json`
