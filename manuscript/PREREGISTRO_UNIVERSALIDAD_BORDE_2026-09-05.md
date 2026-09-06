# PRE-REGISTRO: UNIVERSALIDAD DEL BORDE CINÉTICO (TCCU-0 corregido) — 2026-09-05

**Predicción cuantitativa falsable** (formulada tras la falsación del corredor v3).
**Método:** sistema ORIGINAL Friedmann+KG (piedra de toque), NO el módulo reducido.
**Estado:** pre-registro firmado antes de ejecutar.

---

## 1. La predicción

Para la familia k-essence TCCU-0 corregida

    P = X + X²/Λ⁴ − ρ_c0 e^{−λΦ},  M_P=1, Λ=0.15, Ω_m=0.315, Ω_r=9e-5, signo=+,

integrada con el sistema original Friedmann+KG, se predice:

> **P1 — Universalidad de ruptura.** Todo config (λ, w0) en el dominio
> λ ∈ [0.5, 6.0], w0 ∈ [−0.5, +0.5] alcanza el borde cinético α→1⁻ (X→ρ_tot),
> detectado por α > 0.95, en un tiempo pasado **finito y corto**:
> N_s ∈ [−0.5, −6.0].
>
> **P2 — Monotonía en λ.** A w0 fijo, N_s(λ, w0) es **creciente monótona** en λ
> (a mayor λ, mayor número de e-folds hasta la ruptura), sin bandas ni regiones
> extendibles interrumpidas.
>
> **P3 — No existencia de corredor.** No existe ningún config en el dominio con
> N_s < −10 (extensión ≥ 10 e-folds con α < 0.95 sostenido).

**Contraste con lo falsado:** el corredor v3 afirmaba una banda λ∈[1.66,1.98] con
extensión ≥250 e-folds (falso, artefacto de solve_logA). Esta predicción afirma lo
contrario: ruptura universal, corta y monótona en λ.

## 2. Prueba que la destruye (criterios de REFUTACIÓN)

La predicción queda **REFUTADA** si el barrido encuentra al menos uno de:

- (R1) un config con N_s < −10 (extensión larga real, α<0.95 sostenido),
- (R2) no-monotonía de N_s(λ) a w0 fijo (estructura de bandas: una meseta o
  un descenso local > 1 e-fold entre λ vecinos),
- (R3) un config donde α_max < 0.95 en todo el recorrido hasta N = −50
  (sin ruptura en la ventana).

Si no ocurre R1–R3 en el dominio barrido → la predicción **sobrevive acotada**
(no es "verdad física", es: la familia corregida no tiene corredor en este dominio,
con esta resolución y estos integradores).

## 3. Método (pre-registrado)

- Sistema original: Friedmann + KG (derivs_orig), sin proyección de restricción.
- Integradores: BDF primario; DOP853 como control en subconjunto (10 % de configs).
- Precisión: rtol=1e-11, atol=1e-14, max_step=0.05, t_eval denso (resolución 0.05).
- Dominio: λ ∈ {0.5, 0.75, 1.0, 1.25, 1.5, 1.66, 1.75, 1.84, 2.0, 2.25, 2.5,
  3.0, 4.0, 5.0, 6.0} × w0 ∈ {−0.5, −0.3, −0.2, 0.0, +0.2, +0.3, +0.5} = 105 configs
  (signo=+). Subconjunto DOP853: 11 configs (cada ~10º).
- Detector de ruptura: α = Π²/6 > 0.95 (borde cinético) O fallo del integrador
  (NaN/inf en la RHS = región de inviabilidad).
- Límite de extensión: si un config llega a N=−50 sin α>0.95 → se marca
  "sin_ruptura_50" y se reporta como candidato a refutar P1/P3.
- Salida por config inmediata (checkpoint JSONL + flush), reanudable.
- Veredicto: PASS/FAIL/INCONCLUSIVE por config + GLOBAL al final.

## 4. Semilla / entorno

- Determinista (ICs cerradas por fórmula, sin RNG).
- Python 3.10, numpy, scipy (solve_ivp BDF/DOP853).
- Hash del script y del resultado al final (P10).

## 5. Honestidad

- Esta campaña NO demuestra física nueva; acota la familia corregida.
- Si aparece R1/R2/R3 → se publica la refutación de la predicción (resultado
  negativo válido), igual que se publicó la falsación del corredor.
- El corredor v3 queda refutado independientemente de esta campaña; esto es una
  verificación de cobertura, no un rescate.

Firmado: Jairo / AGI (sesión 2026-09-05).
