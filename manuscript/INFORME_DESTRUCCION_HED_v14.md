# INFORME DE DESTRUCCIÓN TCCU-HED v1.3 → v1.4

**Fecha:** 31-08-2026 · Objetivo (dictamen del Creador): *intentar destruir el modelo
antes de buscar confirmación*. Cuatro pruebas + robustez N=10⁴. Todos los números con
la **P_ret oficial** (P_M = 0.25+0.75·M, boost postbiológico, muertos→0).

## Prueba 1 — Convergencia numérica (Δt) — ✅ PASS
Escenarios B y C, N=1500, dt ∈ {0.1, 0.05, 0.025, 0.0125}:

| dt | P_ret B | G B | P_ret C |
|---|---|---|---|
| 0.1 | 0.05801 | 0.4720 | 0.49974 |
| 0.05 | 0.05793 | 0.4722 | 0.49974 |
| 0.025 | 0.05780 | 0.4723 | 0.49965 |
| 0.0125 | 0.05809 | 0.4723 | 0.49988 |

Sin inestabilidad numérica: P_ret, G, M convergen al refinar Δt (dispersión < 0.5 %).

## Prueba 2 — Convergencia Monte Carlo — ✅ PASS
Escenario B, dt=0.025, N ∈ {100, 1000, 3000} (+10⁴ de la robustez):

| N | P_ret | CI 95 % |
|---|---|---|
| 100 | 0.05855 | [0.05780, 0.05914] |
| 1000 | 0.05787 | [0.05745, 0.05828] |
| 3000 | 0.05796 | [0.05774, 0.05820] |
| 10⁴ (robustez) | 0.05790 | — |

Converge a ≈ 0.058; el CI se estrecha (±0.0067 → ±0.0023); el punto 10⁴ cae dentro de
todos los CI. G = 0.4723 exacto en todos los N.

## Prueba 3 — Ablación vs modelo nulo — ✅ COMPLETA (hallazgos corregidos)
N=2000, dt=0.05, t=100:

**Escenario A (frágil, P_ret ~ 1e-9):**

| Variante | P_ret | surv |
|---|---|---|
| full | 1.05e-9 | 0.227 |
| no_info_surv | 2.28e-9 | **0.4475** |
| no_recovery | 1.05e-9 | 0.227 |
| no_memory | 1.05e-9 | 0.227 |
| null | 2.27e-9 | 0.4475 |
| ΔP_ret(full−null) | **−1.2e-9** | — |

**Escenario B (robusto, P_ret ~ 0.058):**

| Variante | P_ret | M |
|---|---|---|
| full | 0.05815 | 0.710 |
| no_info_surv | 0.05588 | 0.682 |
| no_recovery | 0.01943 | 0.018 |
| no_memory | 0.01855 | 0.000 |
| null | 0.01824 | 0.000 |
| ΔP_ret(full−null) | **0.0399** | — |

**Hallazgos (coherentes):**
1. **La memoria NO es un gate duro**: P_ret sin memoria = 0.0186 en B (P_M piso 0.25),
   no 0. (Un hallazgo preliminar previo con P_M = min(1, M/0.2) decía lo contrario —
   retractado por coherencia con la P_ret oficial.)
2. **La memoria multiplica ~3× en B** (P_M 0.78 vs 0.25; verificado: 0.058·0.25/0.78 =
   0.0186 exacto); **irrelevante en A** (P_ret limitada por el canal de información
   I→0, P_C·P_T ~ 1e-6).
3. **La recuperación η_T aporta ~3× en B** (sin ella M cae a 0.02 → P_M 0.26).
4. **El acoplamiento I→λ_c es escenario-dependiente**: −4 % en B; en A **reduce a la
   mitad la supervivencia** (0.4475→0.227) y P_ret (Δ negativo) — el "mecanismo TCCU"
   no es un boost uniforme; en escenarios frágiles es contraproducente.

## Prueba 4 — Robustez de umbrales (G_crit × M_crit) — ✅ PASS
Escenarios B y C a μ_eff=0.06, N=3000, reclasificación en las 16 combinaciones
{G_crit, M_crit} × {M_crit, G_crit} ∈ {0.01, 0.05, 0.1, 0.2}:

- **H_D2 = 1.000 en las 16 combinaciones, en B y C.** G(100)=e^{−6}=0.0025 ≪ 0.01;
  M ≈ 0.58 ≫ 0.2. La clasificación H_D2 en el régimen asintótico **no es frágil**
  ante los umbrales.
- La fragilidad del cuchillo solo vive en la transición (μ_eff ≈ 0.03, G=0.0498 vs
  G_crit=0.05, margen 0.4 %) — no en los regímenes H_D3/H_D2 bien definidos.

## Prueba 5 — Robustez N=10⁴ (5 escenarios × {10, 50, 100 Myr}) — ✅ PASS
- **La transición A→B→C→D→E PERSISTE a N=10⁴** (orden idéntico: A B D C E).
- **C, D, E son idénticos a N=80 en 3-4 decimales** (P_ret 0.4997/0.400/0.800;
  supervivencia 1.0; H_D3 100 %) — saturación determinista, no ruido.
- **B**: 0.0579/0.0577 — idéntico. **A**: corregido a escala — surv 0.287→0.212
  (−26 %), P_ret 3.9e-7→5.1e-7 (+30 %), split D1/D3 59/41→51/49. **A sigue en
  región F** (P_ret < 1e-6).
- **Regiones F/P robustas**: A ∈ F, B–E ∈ P (frac P_ret>10⁻³ = 0.995-1.0) —
  la falsabilidad interna del modelo sobrevive a la escala.
- Evolución por horizonte: A decrece con t (colapso acumulado), B crece (expansión),
  C/D/E constantes (saturados).

## Correcciones de coherencia aplicadas durante la campaña
1. **P_ret oficial**: el primer script usaba P_M = min(1, M/0.2) → 0.074 en B (vs
   referencia 0.058) y "P_ret=0 sin memoria" falso. Corregido a la oficial
   (0.25+0.75·M) y verificado: T1-B = 0.0580 = referencia.
2. **Bug Ds list** en la robustez (perdió una celda h=100) → fix + smoke test de
   agregación. Lección registrada en TECNICAS_AGI_JAIRO.md.

## Veredicto
**El modelo NO se destruyó en las cuatro pruebas**: converge (Δt y MC), las regiones
F/P persisten a N=10⁴ y la clasificación H_D2 es robusta a umbrales. Pero la
destrucción reveló correcciones importantes: (a) N=80 sobreestimaba la supervivencia
de A (~26 %) y su split D1/D3; (b) la memoria no es un gate duro (factor ~3 en B);
(c) el efecto TCCU de información→supervivencia es escenario-dependiente y
contraproducente en escenarios frágiles. **TCCU-HED v1.3 supera la prueba de
destrucción y queda habilitado para v1.4** con estas correcciones incorporadas.

## Reproducibilidad
`tccu_hed_destruccion.py` (T1-T4, P_ret oficial) · `tccu_hed_robustez.py` +
`tccu_hed_robustez_analisis.py` (N=10⁴) · JSON: `hed_destruccion_*.json`,
`hed_robustez_{A..E}.jsonl`. Ledger bloque de consolidación.
