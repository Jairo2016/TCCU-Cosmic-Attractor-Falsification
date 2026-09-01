# CIERRE FORMAL DE TCCU-0 (hallazgo v1.5.23c)

**Fecha:** 26-08-2026 · **Estado: CERRADO** · Sustituye cualquier lenguaje anterior de
"incompletitud asintótica hacia N→−∞" en el programa TCCU-0.

---

## 1. Declaración definitiva

Bajo las hipótesis del modelo (k-essence P = X + X²/Λ⁴ − ρ_c0 e^{−λΦ}, λ=5, Λ=0.15 M_P,
Ω_m0 = 0.315, Ω_r0 = 9×10⁻⁵) y con la **ecuación de Klein–Gordon corregida**
(signo correcto del término de potencial: +λV/((1+3u)H0²h²), ya que V_φ = −λV):

> **El fondo TCCU-0, con las condiciones iniciales del barrido
> (w0 ∈ [−0.3, 0.1], signo de la velocidad ±), no admite extensión hacia el pasado
> más allá de N_s ∈ [−0.08, −0.50] e-foldings: la restricción de Friedmann pierde
> solución real cuando la velocidad del campo alcanza el borde cinético Π² = 6
> (X/ρ_c0 = (Π²/6)·h² ≤ ρ_tot/ρ_c0 ⟹ Π² ≤ 6).**

## 2. Lenguaje sustituido

Quedan **retirados y sustituidos** los siguientes enunciados de versiones anteriores
(v1.5.20/v1.5.21):

- ~~"PASADO INCOMPLETO (K→∞, integrales finitas)"~~ — el criterio K→∞ con pendiente
  8/ln10 y las integrales de horizonte evaluadas a N = −1000 eran el resultado de un
  **artefacto del signo invertido de V_φ** en la KG: con ese signo el campo *escala* el
  potencial (Π → 0) y el fondo se extiende artificialmente al pasado profundo.
- ~~"El modelo TCCU-0 resulta geodésicamente/integralmente incompleto hacia N → −∞"~~
  (formulación asintótica) — reemplazada por la formulación de **ruptura finita**:
- **Nueva formulación:** "El modelo TCCU-0, bajo sus hipótesis y en el dominio
  (λ=5, w0 ∈ [−0.3, 0.1], signo ±), termina en una **ruptura de la restricción de
  Friedmann** en el borde cinético Π² = 6 a N_s finito. El fondo no existe más allá
  de N_s; no se trata de una singularidad geométrica lejana sino de un **límite de
  existencia del propio modelo**. Sin implicaciones sobre el universo real."

## 3. Cadena de verificación que sustenta el cierre

1. **Auditoría v1.5.21** (5000 puntos on-shell): S' errónea (6.6×10⁶⁷), EF2 errónea
   (0.40), u correcta; **KG con signo invertido** (hallazgo nuevo).
2. **v1.5.22**: identidades corregidas — batería algebraica automática **8/8 PASS**
   (~10⁻¹³). El transformado S,E,Z queda certificado.
3. **v1.5.23c**: sistema reducido con restricción exacta (A = h² por punto fijo en log;
   A′ = −3(A + P/ρ_c0) por continuidad) y aritmética log-signed (m, r, z sin overflow
   a N = −1000). K analítico simplificado K = 12h²[(h′+h)² + h²] (sin cancelación).
4. **Comparación signo erróneo vs correcto (Euler manual + BDF)**: signo erróneo →
   N = −60 limpio (artefacto); signo correcto → ruptura en el borde cinético.
5. **N_s medido en 8/8 configuraciones**: −0.08 … −0.50 (tabla en
   `AUDITORIA_TCCU_v1521_1523.md`).

## 4. Consecuencias

- La campaña "54 configuraciones × 7 extensiones hasta N = −1000" **queda obsoleta**
  por la física: con la KG correcta el fondo se rompe en < 0.5 e-folds; integrar a
  −1000 no es posible ni significativo.
- El criterio observable del programa (F2, ciclos 135–138) no se ve afectado: era
  independiente de esta línea de "eternidad".
- **Pendiente (autorizado por el Creador):** mapa de existencia del fondo en el
  espacio (λ, w0, signo) — ver `MAPA_EXISTENCIA_TCCU0.md` (Paso 2). El cierre aquí
  es para λ = 5; el mapa delimitará la frontera del dominio donde el modelo existe
  (posible extensión a λ pequeño).

## 5. Referencias de archivo
- `auditar_tccu_v1521.py` (auditoría) · `TCCU_Eternity_Test_v1.5.22.py` (identidades
  certificadas; campaña profunda **SUPERSEDED**) · `TCCU_Eternity_Test_v1.5.23c.py`
  (sistema definitivo + medidor de N_s) · `AUDITORIA_TCCU_v1521_1523.md`.
- Ledger bloque 40 (auditoría) y bloque 41 (cierre).
