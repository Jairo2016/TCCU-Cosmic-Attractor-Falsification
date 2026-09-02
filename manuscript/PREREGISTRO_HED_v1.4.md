# PRE-REGISTRO HED-F v1.4 — Reproducibilidad y congelación de v1.3

**Fecha:** 2026-09-01
**Estado:** PRE-REGISTRO (antes de cualquier ejecución nueva)
**Física congelada:** `tccu_hed_v1_3.py` (NO se modifica — la física es la de v1.3).
**Código de referencia (hash):** `tccu_hed_v1_3.py` → SHA-256 `d901feb8099e92c4…`
**Resultado de referencia:** `summary_v1_3.json` → SHA-256 `53e8307e1decaee1…`

---

## 1. Objetivo de v1.4

v1.4 NO cambia la física. Es una **campaña de reproducibilidad y contención**:

1. Congelar ecuaciones y parámetros de v1.3 (sin cambios).
2. Congelar criterios F/P y H_D2 (sin cambios).
3. Pre-registrar TODOS los pasos y criterios de veredicto ANTES de ejecutar.
4. Reproducción independiente (nuevo proceso, semillas explícitas, hash de salida).
5. Campaña N=10⁴ como **robustez numérica** — NO como evidencia de ET humanos.
6. Análisis de sensibilidad congelado (µ×λ_M y µ alto ya existentes).
7. Veredicto final: PASS / FAIL / INCONCLUSIVE por prueba y GLOBAL.

---

## 2. Física congelada (v1.3, sin cambios)

Modelo HED-F: civilización humana exoplanetaria como proceso estocástico con
`CivilizationState` (D_genetic, G_ancestry=exp(−D), I, A, E, B, R, M, tau, N, alive,
postbiological) y `step_civilization` con:

- Expansión: `E += v_e·dt`; nacimiento Poisson; muerte binomial; colapso parcial.
- Genética: `D += μ_eff·dt`, `μ_eff = μ·tech_mod`; `G = exp(−D)` (índice auxiliar, NO filogenia).
- Información: `I` con generación/pérdida/transmisión; transición postbiológica.
- Memoria: `dM/dt = −λ_M·M + η_T(I,N,G)` con recuperación arqueológica; `M∈[0,1]`.
- Mapa R, actividad A, tiempo tau.
- `P_ret = P_S·P_E·P_C·P_N·P_T·P_intent·P_M` con **P_M = 0.25 + 0.75·M** (oficial).
- Clasificación ternaria: H_D3 (G>G_crit ∧ M>M_crit), H_D1 (solo G), H_D2 (solo M),
  H_none.

Parámetros: escenarios A–E tal como en v1.3 (v_e, λ_c0, μ, α_info, β_loss, γ_trans,
resilience, tech_mod, P_intent, λ_M, η_T0, seed_colonies, max_colonies).

**Regla de congelación:** ninguna ejecución de v1.4 modifica `tccu_hed_v1_3.py`.
Cualquier cambio de física → sería v1.5 con su propio pre-registro.

---

## 3. Criterios congelados (v1.3)

| Criterio | Valor | Uso |
|---|---|---|
| P_ret interesante | 1e-6 | umbral bajo |
| P_ret plausible | 1e-3 | frontera de plausibilidad (región P) |
| G_crit | 0.05 | continuidad biológica detectable |
| M_crit | 0.05 | memoria ancestral no extinguida |
| D_genetic detectable | 3.0 | −ln(G)>3 ⇔ G<0.05 |
| Falsabilidad | región F (P_ret≈0) y región P (P_ret>1e-3) | ambas deben existir |
| Frontera de fase | P_ret=1e-3 ∧ M>M_crit | barrido (v_e,λ_c,λ_M) |

---

## 4. Correcciones ya descubiertas que v1.4 CONSERVA explícitamente

Estas correcciones están incorporadas en el análisis (no en la física):

1. **N=80 subestima A** (actividad acumulada) — la campaña de robustez usa N=10⁴.
2. **Memoria ≈ factor 3, NO gate**: P_M = 0.25+0.75·M (M=0 → P_M=0.25, no 0);
   eliminar memoria ~×3 el P_ret, no lo anula (T3-B: Δ=0.040).
3. **Orden real de escenarios**: A → B → D → C → E (por P_ret medio/plausibilidad).
4. **Cuatro pruebas de destrucción superadas** (T1 dt, T2 N, T3 ablación I/λ_c,
   T4 umbrales H_D2) — v1.4 las re-verifica como reproducibilidad.
5. **N=10⁴ = robustez numérica, NO evidencia de ET humanos** (advertencia permanente).
6. **P_ret oficial** = P_S·P_E·P_C·P_N·P_T·P_intent·P_M con P_M=0.25+0.75·M
   (una versión preliminar con P_M=min(1,M/0.2) quedó retractada por incoherencia).

---

## 5. Plan de ejecución pre-registrado (v1.4)

| Paso | Acción | Entrada | Salida | Criterio |
|---|---|---|---|---|
| R1 | Reproducción independiente del bloque principal | tccu_hed_v1_3.py (import, sin main), N=80, t=100 Myr, seed 42+ord(key) | repro_R1.json | P_ret por escenario ≈ referencia (dentro de ruido MC esperado) |
| R2 | Reproducción de la campaña de robustez N=10⁴ | tccu_hed_robustez.py A–E (checkpoint por celda) | hed_robustez_v14_*.jsonl | orden A→B→D→C→E; fracciones F/P estables; N=80 vs 10⁴ convergen |
| R3 | Re-verificación de destrucción T1–T4 | tccu_hed_destruccion.py | hed_destruccion_v14_*.json | T1: P_ret estable con dt; T2: convergencia con N; T3: memoria ~×3; T4: H_D2 robusto a umbrales |
| R4 | Sensibilidad congelada | mu_lambdaM_grid.json + high_mu_sweep.json (reproducidos) | sens_v14.json | mapa μ×λ_M coherente; sin inversiones de orden |
| R5 | Veredicto por prueba + GLOBAL | resumen de R1–R4 | VEREDICTO_HED_v1.4.md | PASS/FAIL/INCONCLUSIVE; ningún PASS individual valida |

**Semillas:** R1 usa seed=42+ord(key) (igual que v1.3); R2/R3 usan las semillas de
los scripts existentes (checkpoint por celda, reanudable); R4 semilla fija del barrido.

**Entorno:** Python 3.10, numpy, scipy; ventanas; sin GPUs. Registro de hashes de
entrada/salida en cada paso (P10-style).

---

## 6. Criterios de veredicto (pre-registrados)

| Prueba | PASS si | FAIL si | INCONCLUSIVE si |
|---|---|---|---|
| R1 (reproducción) | P_ret de cada escenario dentro de ±2σ MC del valor v1.3 (σ estimado por bootstrap de la propia muestra) | desviación sistemática >2σ en ≥2 escenarios | ruido MC no estimable o ejecución incompleta |
| R2 (robustez 10⁴) | orden A→B→D→C→E preservado; fracciones F/P sin cambios de región | orden invertido o fronteras movidas >10% | celdas incompletas (>10% perdidas) |
| R3 (destrucción) | T1–T4 reproducen los veredictos de v1.3 | algún T1–T4 cambia de PASS a FAIL | celda perdida sin checkpoint |
| R4 (sensibilidad) | mapa μ×λ_M coherente con v1.3 (sin inversiones) | inversión de orden inducida por µ | grid incompleto |
| **GLOBAL** | R1–R4 PASS | algún FAIL crítico | ≥1 INCONCLUSIVE sin resolución |

**Regla global:** ningún PASS individual valida v1.4; el GLOBAL es la conjunción.
Y la advertencia permanente: todo esto es HED-F (factibilidad), nunca evidencia
observacional de descendientes humanos reales.

---

## 7. Contención del alcance

- Este pre-registro NO promete confirmación de ET humanos ni de H_D2 real.
- El producto es: **la física v1.3 es reproducible, robusta a N=10⁴ y a las pruebas
  de destrucción, con sensibilidad mapeada** — o no lo es, y se declara.
- Si R1–R4 fallan → se investiga y se documenta; v1.4 puede terminar en INCONCLUSIVE
  con causa raíz identificada (igual que el corredor TCCU-0: el refinamiento manda).

---

## 8. Firma de congelación

- `tccu_hed_v1_3.py` SHA-256: `d901feb8099e92c4…` (congelado)
- `summary_v1_3.json` SHA-256: `53e8307e1decaee1…` (referencia)
- Este pre-registro: firmado por su contenido; cualquier ejecución v1.4 lo referencia.
