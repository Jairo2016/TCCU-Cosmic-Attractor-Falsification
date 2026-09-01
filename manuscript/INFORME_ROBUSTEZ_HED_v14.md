# INFORME DE ROBUSTEZ TCCU-HED v1.3 → v1.4 — N = 10⁴

**Fecha:** 31-08-2026 · 150,000 trayectorias (5 escenarios × 3 horizontes × 10⁴ realizaciones),
dt=0.025, seeds fijos por celda, checkpoint JSONL (reanudable). Comparación contra la
referencia N=80 (`summary_v1_3.json`).

## 1. Persistencia de la transición A→B→C→D→E (horizonte 100 Myr)

| Esc | Surv 10⁴ | Surv 80 | P_ret 10⁴ | P_ret 80 | frac>10⁻³ | Clases 10⁴ |
|---|---|---|---|---|---|---|
| A | 0.2120 | 0.2875 | 5.14e-07 | 3.94e-07 | 0.000 | D1 0.51 / D3 0.49 |
| B | 0.9951 | 0.9875 | 5.79e-02 | 5.77e-02 | 0.995 | D3 1.00 |
| C | 1.0000 | 1.0000 | 4.997e-01 | 4.997e-01 | 1.000 | D3 1.00 |
| D | 1.0000 | 1.0000 | 4.000e-01 | 4.000e-01 | 1.000 | D3 1.00 |
| E | 1.0000 | 1.0000 | 8.000e-01 | 8.000e-01 | 1.000 | D3 1.00 |

- **Ordenamiento A→B→D→C→E: idéntico entre N=80 y N=10⁴** (C=0.50 > D=0.40 — la
  narrativa "A→B→C→D→E" no es monótona en P_ret; el orden real es A B D C E).
- **C, D, E son idénticos a N=80 en 3-4 decimales** (0.4997 / 0.400 / 0.800): son
  puntos de saturación determinista (supervivencia 1.0, factores P_* saturados), no
  ruido MC.
- **B**: 0.0579 vs 0.0577 — idéntico dentro del error.
- **A es el único corregido a escala**: supervivencia 0.2875 → **0.2120** (−26 %),
  P_ret 3.94e-7 → **5.14e-7** (+30 %), split D1/D3 0.59/0.41 → **0.51/0.49**. El
  bloque N=80 subestimaba los errores MC de A (baja supervivencia → alta varianza).

## 2. Regiones F / P (falsabilidad interna a escala) — ROBUSTAS

- **A ∈ F**: P_ret = 5.14e-7 < 10⁻⁶, frac>10⁻³ = 0.000.
- **B–E ∈ P**: frac P_ret>10⁻³ = 0.995–1.000.
- La separación F/P (criterio de éxito a priori) sobrevive a la escala.

## 3. Evolución con el horizonte (10 → 50 → 100 Myr) — COMPLETA

| Esc | Surv 10/50/100 | P_ret 10/50/100 |
|---|---|---|
| A | 0.61 / 0.37 / 0.21 | 3.2e-6 / 6.6e-7 / 5.1e-7 |
| B | 0.99 / 1.00 / 1.00 | 1.8e-3 / 2.6e-2 / 5.8e-2 |
| C | 1.00 / 1.00 / 1.00 | 7.4e-2 / 0.50 / 0.50 |
| D | 1.00 / 1.00 / 1.00 | 0.20 / 0.40 / 0.40 |
| E | 1.00 / 1.00 / 1.00 | 0.40 / 0.80 / 0.80 |

- **A**: P_ret DECRECE con t (colapso acumulado: supervivencia 0.61→0.21).
- **B**: P_ret CRECE con t (la expansión E y N se acumulan; a 10 Myr aún no se satura).
- **C/D/E**: saturan a 50 Myr (P_ret constante después).
- Clases: **H_D3 100% en todos los horizontes** a μ base (consistente: G sigue sobre
  G_crit con μ_eff de las bases).

## 4. Lecciones de la campaña
1. El bloque N=80 era suficiente para tendencias (orden, F/P) pero NO para magnitudes
   de escenarios frágiles (A: surv con 26% de error).
2. La saturación determinista de C/D/E explica por qué P_ret allí es exacta — no es
   un artefacto sino el límite del modelo (P_* → 1).
3. El orden real (A B D C E) debe corregirse en la narrativa del documento (no es
   monótono A<B<C<D<E en P_ret).

## 5. Reproducibilidad
- `tccu_hed_robustez.py` (5 procesos paralelos, checkpoint por celda) → `hed_robustez_{A..E}.jsonl`
- `tccu_hed_robustez_analisis.py` → tablas. Se corrigió un bug de agregación (Ds list)
  que perdió una celda; la campaña se relanzó con fix y se completó.
