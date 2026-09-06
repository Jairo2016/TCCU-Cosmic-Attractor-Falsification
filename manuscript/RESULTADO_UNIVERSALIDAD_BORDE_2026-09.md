# RESULTADO: CAMPAÑA UNIVERSALIDAD DEL BORDE CINÉTICO (TCCU-0 corregido) — 2026-09-05/06

**Pre-registro:** `PREREGISTRO_UNIVERSALIDAD_BORDE_2026-09-05.md`
**Método:** sistema ORIGINAL Friedmann+KG (BDF primario + DOP853 control), rtol=1e-11
(diagnóstico de overflow con rtol=1e-10/DOP853), 105 configs
(λ∈{0.5…6.0}×w0∈{−0.5…+0.5}, signo=+), checkpoint por config (reanudable).
**Datos:** `universalidad_borde.jsonl` (105 filas) · `universalidad_borde_resumen.json`
**Scripts:** `universalidad_borde.py` · `diagnosticar_errores_universalidad.py` ·
`completar_universalidad.py`

---

## Veredicto por predicción

| Predicción | Veredicto | Evidencia |
|---|---|---|
| **P1 — ruptura universal** (todo config rompe en N_s finito y corto) | **PASS (acotado)** | 105/105 configs integrados: 101 rupturas explícitas + 4 fallos de integrador con α>0.95 ya detectado. Ninguno llega a N=−50 con α<0.95. Rango N_s ∈ [−6.81, −0.90]. |
| **P2 — monotonía global** (N_s creciente en λ a w0 fijo) | **REFUTADA** | La estructura tiene un **pico de extendibilidad finita** alrededor de λ≈1.75–2.25; N_s crece hasta el pico y luego decrece. Ningún w0 es monótono creciente en todo el rango. |
| **P3 — no existencia de corredor** (ningún N_s < −10) | **PASS** | N_s mínimo observado: −6.81 (λ=2.25, w0=+0.5). Nada se acerca a −10. |

**Veredicto final: PARCIAL — P1 y P3 consistentes (acotados), P2 refutada.**
La predicción compuesta no se sostiene en su forma monótona; la universalidad de
*ruptura corta* sí se sostiene en el dominio barrido.

---

## El hallazgo de estructura (pico de extendibilidad finita)

N_s(λ) a w0 fijo NO es monótona: crece hasta un máximo y luego decrece.

| w0 | λ del pico | N_s en el pico |
|---|---|---|
| −0.5 | 1.75 | −6.16 |
| −0.3 | 2.00 | −5.71 |
| −0.2 | 2.00 | −3.90 |
| 0.0 | 2.00 | −4.45 |
| +0.2 | 2.25 | −4.00 |
| +0.3 | 2.25 | −3.85 |
| +0.5 | 2.25 | **−6.81** |

Interpretación: la región λ≈1.75–2.25 (que el mapa v3 exageró como corredor de 250
e-folds) aparece aquí como un **máximo finito de extendibilidad** (~4–7 e-folds),
consistente con la falsación del corredor pero señalando que esa zona no es
paramétricamente neutra: el campo escala más antes de romper. La ruptura es
**inevitable** (P1/P3), pero su escala temporal tiene estructura (P2 falsa).

## Nota numérica honesta

- Los configs marcados "error" en la campaña inicial (λ≥2.25 con ciertos w0) eran
  overflow de `exp(−λΦ)` en float64 del sistema ORIGINAL; re-integrados con
  rtol=1e-10 o DOP853 todos rompen en N_s corto (ver `diagnosticar_errores…`).
- El máximo N_s = −6.81 (λ=2.25, w0=+0.5) fue verificado con BDF y el pico
  λ=1.75/w0=−0.5 (−6.14) con DOP853 (−6.135) — estructura robusta al integrador.
- 4 configs de λ alta terminan con "Required step size < spacing" tras α>0.95
  (región de inviabilidad post-ruptura); N_s queda registrado por el detector previo.

## Comparación con el corredor v3 (falsado)

- v3 afirmaba: banda λ∈[1.66,1.98], N_past ≥ 250, α<0.95 sostenido → **falso**.
- Esta campaña: en esa banda todo rompe; N_s típico ≈ −2..−6 (máx −6.8).
- La zona del "corredor" es un máximo FINITO de N_s, no una extensión larga.

## Consecuencia

- La familia corregida TCCU-0 no tiene pasado extendible ≥10 e-folds en
  λ∈[0.5,6]×w0∈[−0.5,0.5] (P3, sistema original, esta resolución).
- La predicción P2 (monotonía) queda descartada y documentada como resultado
  negativo parcial — igual de publicable que un PASS.
- Siguiente natural: extender el dominio (λ<0.5, w0 fuera de [−0.5,0.5], signo=−)
  si se quiere cobertura total; o cerrar TCCU-0 como familia sin pasado extendible
  en el dominio estudiado.
