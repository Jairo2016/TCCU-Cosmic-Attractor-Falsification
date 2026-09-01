# CORREDOR DE PASADO EXTENDIBLE EN TCCU-0 — consolidación del barrido fino v3

**Fecha:** 31-08-2026 · Barrido fino completo: 3782 configuraciones
(λ ∈ [1.40, 2.60] Δλ=0.02 × w0 ∈ [−0.40, 0.20] Δw0=0.02 × signo ±), dn=0.005,
detector α = Π²/6 > 0.95 (borde cinético real), verificación BDF.

## ⚠️ REVOCACIÓN del mapa grueso (§21 del maestro)

El mapa grueso (paso Δλ=0.1) concluyó "126/126 rompen en el borde cinético". **Queda
REVOCADO**: el barrido fino encuentra una **banda de pasado extendible** que el paso
grueso perdió entre λ=1.6 y 2.0. Regla confirmada: cuando un mapa grueso y uno fino
discrepan, el fino manda.

## Resultado del barrido fino v3

- **Borde cinético: 3350/3782 (88.6 %)** — rompen a N_s finito.
- **Extendibles: 432/3782 (11.4 %)** — alcanzan N = −250 sin romper (α < 0.95 en
  todo el recorrido; el campo gira, Π cruza 0 y se congela; domina la radiación).
- **λ⋆ = 1.66, w0 = −0.20, signo=+1** (α_s = 0.9497 al final del recorrido).

### Región extendible (signo = +1)

| λ | rango w0 extendible | n configs |
|---|---|---|
| 1.66 | [−0.20, +0.20] | 21 |
| 1.68 | [−0.26, +0.20] | 24 |
| 1.70 | [−0.30, +0.20] | 26 |
| 1.72–1.84 | [−0.32, +0.20] | 27 |
| 1.86–1.88 | [−0.30, +0.20] | 26 |
| 1.90 | [−0.28, +0.20] | 25 |
| 1.92–1.94 | [−0.26..−0.28, +0.20] | 24-25 |
| 1.96–1.98 | [−0.24, +0.20] | 23 |

**Banda completa: λ ∈ [1.66, 1.98] × w0 ∈ [−0.32, +0.20]** (simétrica en el tope
w0=+0.20, asimétrica hacia w0<0). Dentro de la banda, α se estabiliza en 0.82–0.95
(escalada cuasi-crítica seguida de congelación).

### Fuera de la banda (signo = +1)
- λ = 2.00: rompe a N_s = −18.49 (w0=−0.2) y −15.08 (w0=0) — la banda se cierra
  abruptamente (coincide con el mapa grueso).
- λ ≥ 2.02: N_s cae monótonamente a −0.80 (λ=2.60).
- λ ≤ 1.64: N_s ≈ −1.2..−2.1.
- **signo = −1: SIEMPRE rompe rápido** (N_s ∈ [−0.06, −0.17]) en todo el grid.

## Mecanismo físico (verificado con sistema original independiente, BDF)
En la banda, el campo escala el potencial (Φ → −160), Π alcanza ~92-95 % del borde
cinético, **cruza cero (giro)** y se congela; con Π≈0 domina la radiación y el fondo
se extiende como FLRW estándar (A ~ e^{−4N}, w=1/3). No es una rama degenerada:
el giro se reproduce con el sistema original (BDF: Π 2.08 → 0.0000).

## Implicación para el cierre
- El **CIERRE_TCCU0 (§20)** sigue válido **para λ=5** (rompe a N_s ≈ −0.4..−0.5).
- Pero la afirmación de dominio "no hay pasado eterno en el dominio explorado" queda
  **corregida**: existe la banda extendible λ≈1.66-1.98 (signo=+) donde el pasado del
  modelo se extiende al menos 250 e-folds (posiblemente indefinidamente — el estado
  congelado+radiación es asintóticamente extensible). TCCU-0 tiene **regiones con
  pasado extendible** y **regiones con ruptura finita**, separadas por la banda.

## Reproducibilidad
- `TCCU_0B_corredor_v3.py` (checkpoint JSONL, reanudable) → `mapa_tccu0b_v3.json`,
  `tccu0b_v3_configs.jsonl`. Ledger: bloque de consolidación.
