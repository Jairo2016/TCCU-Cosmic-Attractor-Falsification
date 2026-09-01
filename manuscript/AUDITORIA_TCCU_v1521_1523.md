# Auditoría TCCU-0 v1.5.21 → v1.5.23c — hallazgo físico definitivo

**Fecha:** 26-08-2026 · Modelo: k-essence P = X + X²/Λ⁴ − ρ_c0 e^{−λΦ}, λ=5, Λ=0.15, Ω_m=0.315, Ω_r=9e-5
**Criterio:** NO-GO/eternidad del fondo hacia N→−∞ (prueba de equivalencia + batería algebraica + campaña).

---

## 1. Auditoría de v1.5.21 (5000 puntos on-shell, N ∈ [−60, 0])

| Identidad | max rel diff | Veredicto |
|---|---|---|
| u = E²S²e^{−8N} | 1.6e-15 | ✅ PASS (corregida) |
| D | 7.4e-11 | ✅ PASS |
| E' = 2E − 1.5D/E | 4.5e-10 | ⚠️ fórmula correcta, precisión |
| **S'** | **6.6e+67** | 🔴 FALLO TOTAL |
| **EF2** | **0.40** | 🔴 FALLO |

Errores estructurales confirmados (además de los 3 del Creador):
1. **S' errónea**: la implementada `−(4+6u)S/(1+3u) − 3λ√κ z e^{2N}/(1+3u)` no es el
   transformado de la KG. La exacta: **S' = [2 + 1.5D/E² − 3(1+u)/(1+3u)]S + 3λ√κ z e^{6N}/((1+3u)E²)**
   (incluye acoplamiento D/E²; fuente e^{6N}/E², no e^{2N}).
2. **EF2 errónea**: falta E²/E⁴ y potencias e^{−4N}/e^{−12N}.
   Exacta: E² = Ω_m e^N + Ω_r + E²S²e^{−4N}/(6κ) + E⁴S⁴e^{−12N}/(4κ) + z e^{4N}.
3. **KG con signo erróneo** (hallazgo nuevo): la v1.5.20/21 usa −λV/((1+3u)H0²h²);
   la correcta es **+λV/((1+3u)H0²h²)** (V_φ = −λV). El signo se propaga al fuente de S'.

## 2. v1.5.22 — identidades corregidas: 8/8 PASS

Batería algebraica automática (10000 puntos on-shell): u, D, E', S', EF2, Z', τ', ℓ'
todos < 1e-8 (mayoría ~1e-13). El transformado S,E,Z queda **certificado**.
La integración S,E,Z sigue siendo frágil en el régimen explosivo (E colapsa: E' = 2E − 1.5D/E).

## 3. v1.5.23c — integración robusta (restricción exacta + log-signed)

Sistema reducido: A = h² resuelto por punto fijo en log; A' = −3(A+P/ρ_c0) (continuidad);
KG con signo correcto; m, r, z en log. Llega a N = −1000 sin overflow numérico.
**K analítico simplificado: K = 12 h²[(h′+h)² + h²]** (los e^{−8N} se cancelan; sin cancelación catastrófica).

## 4. 🔴 Hallazgo físico definitivo

**El signo erróneo de la KG era load-bearing.** Con el signo erróneo (v1.5.20/21), el campo
*escala* el potencial (Π→0) y el fondo se extiende limpiamente a N = −60…−1000: el
"pasado profundo" de las versiones previas es un **artefacto del error de signo**.

Con la KG correcta, el campo *rueda* por el exponencial (λ=5 es steep-roll, no slow-roll):
Π acelera y alcanza el **borde cinético Π² = 6** (X/ρ_c0 = (Π²/6)h²·… ≤ ρ_tot ⟹ Π ≤ √6),
donde la restricción de Friedmann deja de tener solución real → **el fondo se rompe a N finito**:

| w0 | sign=+1 | sign=−1 |
|---|---|---|
| −0.30 | N_s = −0.406 | N_s = −0.100 |
| −0.10 | −0.452 | −0.088 |
| 0.00 | −0.474 | −0.082 |
| +0.10 | −0.500 | −0.076 |

**Conclusión honesta:**
- TCCU-0 con λ=5 e IC del barrido **no tiene pasado extendible**: el fondo deja de existir
  a N_s ∈ [−0.08, −0.50] e-folds hacia atrás (y ~0.16 hacia delante). Es un **breakdown
  finito** — más fuerte que la "incompletitud asintótica" que la v1.5.20/21 afirmaba con K→∞.
- El NO-GO queda establecido con la física correcta, **pero por un mecanismo distinto**:
  no hay singularidad geométrica lejana; hay un **límite de existencia del modelo** (la
  velocidad del campo supera el máximo permitido por la restricción).
- La campaña "54 configuraciones hasta N=−1000" **no es el test adecuado**: la física
  correcta rompe el fondo en < 0.5 e-folds; integrar a −1000 es imposible/no significativo.
- El lenguaje NO-GO preciso: "el modelo TCCU-0, bajo sus hipótesis y con λ=5, no admite
  extensión de su fondo hacia el pasado más allá de N_s ≈ −0.5 (ruptura de la restricción
  de Friedmann en el borde cinético Π²=6)". No implica nada sobre el universo real.

## 5. Reproducibilidad
- `auditar_tccu_v1521.py` (auditoría 5000 puntos) · `TCCU_Eternity_Test_v1.5.22.py`
  (identidades 8/8, batería automática) · `TCCU_Eternity_Test_v1.5.23c.py` (sistema
  log-signed con restricción exacta + medidor de N_s).
