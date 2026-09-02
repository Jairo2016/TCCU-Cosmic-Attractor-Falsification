# INFORME DE FALSACIÓN NUMÉRICA DEL CORREDOR TCCU-0 (v3)

**Fecha:** 2026-09-01
**Autor:** Jairo / AGI (sesión DSH)
**Estado:** DEFINITIVO — el corredor preliminar λ∈[1.66,1.98]×w0∈[−0.32,+0.20] con N_past≥250 **NO sobrevive al refinamiento numérico**.

---

## 1. Resumen ejecutivo

La batería de validación P1–P10 (v2, corrección del Creador del 01-09) al ejecutarse sobre
`TCCU_Eternity_Test_v1.5.23c.py` + `validar_corredor.py` reveló una **discrepancia
irreconciliable entre dos formulaciones del mismo modelo**:

| Formulación | α_max (λ=1.66, w0=−0.2) | N_s (α>0.95) |
|---|---|---|
| Módulo log-signed v1.5.23c (solve_logA con iteración de punto fijo, 6 pasos) | 0.9495 | −250 (sobrevive) |
| Sistema ORIGINAL Friedmann+KG (BDF/DOP853/LSODA/Radau, residuo ≤1e-11) | **1.000000** | **−2.3** |
| Sistema reducido con raíz analítica CORRECTA de la restricción | **0.999976** | **−2.26** |

**La causa raíz es un error de convergencia en `solve_logA`**: la iteración de punto fijo
`A ← c + αA + βA²` tiene tasa de contracción ~α; cuando α→0.93+ se necesitan **>200–500
iteraciones** para converger a 1e-14, pero el módulo ejecuta solo **6**. El A resultante es
incorrecto por factores 2–100 (residuo hasta 0.14), lo que frena artificialmente Π y fija
α≈0.94–0.95 durante 250 e-folds. Con la restricción resuelta correctamente, **el campo
escala hasta el borde cinético α=1 (X=ρ_tot) en ~2–4 e-folds** para TODOS los configs de la
banda del mapa v3, incluido λ_star=(1.66,−0.20).

**Veredicto conforme al protocolo:** corredor preliminar **REFUTADO** → se publica como
*falsación numérica del corredor preliminar*. NO se publica como resultado positivo.

---

## 2. Afirmación bajo test (protocolo v2)

> En TCCU-0 (P = X + X²/Λ⁴ − ρ_c0 e^{−λΦ}, M_P=1, Λ=0.15, Ω_m=0.315, Ω_r=9e-5), signo=+,
> el fondo se extiende ≥250 e-folds hacia el pasado en la banda λ∈[1.66,1.98] ×
> w0∈[−0.32,+0.20], con giro del campo (Π cruza 0) y congelación (dominio de radiación).

Fuente: mapa v3 (`mapa_tccu0b_v3.json`: 432/3782 configs "limite_pasos", α_s<0.95 a N=−250).

---

## 3. Cadena de evidencia

### 3.1 Bug 1 — `run_orden_superior` no fija `t.LAM` (P1/P2 inválidos como estaban escritos)

En `validar_corredor.py` v2, `run_orden_superior` llamaba `t.derivatives(N,y)` sin
`t.LAM = lam`, por lo que P1/P2 (BDF/DOP853) integraron con el **default del módulo
LAM=5.0** (que se sabe rompe a N≈−0.4). Las 18 corridas fallaron. **Corregido** en el
diagnóstico: fijar `t.LAM = lam`.

### 3.2 Bug 2 — `run_euler_aux` integra hacia ADELANTE (P1e/P5/P6/P8 inválidos)

`run_euler_aux` hacía `y += dn*f` con dn=+0.0025 → N va de 0 a **+250** (futuro). El
"rhs_no_finito a N≈210" era la singularidad cinética del FUTURO, no del pasado. El mapa v3
usa `DN = −0.005` (hacia atrás). Con la corrección de signo, el Euler hacia atrás llega a
N=−250 sin problema (α_max=0.9495), **coincidiendo con el mapa v3**.

### 3.3 Bug 3 (RAÍZ) — `solve_logA` no converge cerca del borde cinético

La restricción es `A = c + αA + βA²` con c=m+r+z, α=Π²/6, β=κΠ⁴/4. Su solución física
(raíz pequeña) es

    A₋ = 2c / (s + √(s² + 4βc)),   s = 1−α

El módulo itera `logA ← logadd(logc, logalpha+logA, logbeta+2logA)` (6 pasos, tolerancia
1e-14). Medición directa:

| α | iteraciones para 1e-14 | A_módulo/A_exacta | residuo del módulo |
|---|---|---|---|
| 0.27 | 25 | 1.000 | 0.000 |
| 0.50 | 46 | 0.992 | 0.004 |
| 0.90 | 285 | 0.522 | 0.092 |
| 0.93 | 408 | 0.398 | 0.106 |
| 0.95 | 571 | 0.302 | 0.116 |
| 0.999 | >2000 | 0.007 | 0.142 |

Con A incorrecto (2–3× menor), el término de arrastre de KG (∝1/A) queda distorsionado:
Π se frena justo debajo de √6 (α≈0.94–0.95) y la trayectoria "sobrevive" 250 e-folds.
Es un **artefacto del solver**, no dinámica del modelo.

### 3.4 Verificación con la raíz correcta y con el sistema original (independiente)

Reemplazando `solve_logA` por la raíz analítica exacta A₋ (y sin tocar nada más del
módulo), DOP853 a N=−6 da, para la banda del mapa:

| λ | w0 | N_s (α>0.95) | α_max |
|---|---|---|---|
| 1.66 | −0.20 | −2.26 | 0.999976 |
| 1.66 | 0.00 | −1.90 | 0.999988 |
| 1.68 | 0.00 | −1.93 | 0.999983 |
| 1.70 | 0.00 | −1.99 | 0.999976 |
| 1.80 | 0.00 | −2.32 | 0.999874 |
| 1.84 | 0.00 | −2.50 | 0.999743 |
| 1.90 | 0.00 | −2.92 | 0.999191 |
| 1.98 | +0.20 | −2.86 | 0.998530 |
| 2.00 | 0.00 | −4.43 | 0.990148 |

Fuera de la banda (misma raíz correcta, DOP853): λ=1.0..1.4 → N_s≈−1.2..−1.5
(α_max=1.0, borde rápido); λ=2.2, 2.5, 3.0, 5.0 → la integración **termina antes**
(N_ult=−3.56, −1.35, −0.90, −0.45 respectivamente; success=False por borde cinético en
la raíz), consistente con el mapa v3 que los clasificaba como borde (λ=5 rompe a
N_s≈−0.4..−0.5). Es decir: fuera de la banda tampoco hay supervivencia; el "borde" es
universal, no específico de la banda.

**Nota sobre ramas:** la restricción A=c+αA+βA² tiene dos raíces reales (A₊ grande,
A₋ física=h²). El IC físico (h=1 a N=0) selecciona A₋. La rama A₊ (no física) produce
una trayectoria que no escala y "sobrevive" 250 e-folds (control: α_max=0.274, campo
decae) — esto confirma que solo la rama física importa y que es la que escala al borde.
El sistema ORIGINAL (que no proyecta la restricción) da exactamente la misma física:
α→1 a N≈−2.3, α_max=1.0 (4 integradores, residuo ≤1e-11).

El **sistema original** (Friedmann+KG, sin proyección de restricción; BDF/DOP853/LSODA/
Radau, residuo de Friedmann ≤1e-11, coincidencia total entre métodos) confirma:

| λ | w0 | N_s (α>0.95) | α_max |
|---|---|---|---|
| 1.00 | 0.00 | −1.3 | 1.000000 |
| 1.66 | −0.20 | −2.4 | 1.000000 |
| 2.00 | 0.00 | −4.5 | 1.000000 |
| 5.00 | 0.00 | −1.6 | 1.000000 |

### 3.5 El mapa v3 también es internamente sospechoso

- `n_borde=3350`, `n_extiende=0`, `n_limite_pasos=432` (nunca hubo "extiende" real).
- λ=2.0, w0=0, signo=+1 aparece como borde a N_s=−15.08 con α_s=0.9897 — consistente con
  romper, pero el N_s correcto es −4.4 (la discrepancia es el mismo artefacto).
- λ=5, w0=0, signo=+1: mapa v3 lo da como borde; el sistema original da α_max=1.0 a
  N_s≈−1.6 y la raíz correcta termina a N_ult=−0.45 — confirmando ruptura rápida
  (coincide cualitativamente con lo conocido).
- Los configs "limite_pasos" (432) con α_s≈0.94–0.95 son exactamente los que el solver
  roto frena bajo 0.95. **La banda λ∈[1.66,1.98] como región de extensión ≥250 e-folds
  no existe en la dinámica correcta.**

### 3.6 P3 (sistema original, BDF rtol=1e-11, N=−80) — reproducido

P3 sí funciona y es correcto: α_final=0.00000, Π_final≈1e-15 a N=−80 (el campo gira y se
congela), pero a lo largo del camino **α_max=1.0** (el borde cinético se alcanza a
N≈−2.3). Es decir: P3 confirma la ruptura cinética, no la supervivencia.

---

## 4. Veredicto por prueba (esquema P1..P10 + GLOBAL)

| P | Prueba | Veredicto | Justificación |
|---|---|---|---|
| P1 | DOP853/Radau rtol {1e-8,1e-10,1e-12}, N=−250 | **FAIL** | Con raíz correcta el integrador no alcanza N=−250: α→1 a N≈−2.3 (borde). El α_max<0.95 del mapa no se reproduce. |
| P2 | BDF original a N=−80 (segundo método) | **FAIL** | Reproduce giro Π→0, pero α_max=1.0 (borde) a N≈−2.3. |
| P3 | tolerancias ×10 (original, rtol 1e-11) | **PASS (pero contraproducente)** | Integra bien; confirma borde cinético, no extensión. |
| P4 | segundo método (Radau original) | **PASS** | Radau concuerda con BDF/DOP853/LSODA (α_max=1.0). |
| P5 | bordes finos de λ | **INCONCLUSIVE** | El concepto de borde λ₋/λ₊ de la banda pierde sentido: TODOS los configs de la banda rompen a N≈−2..−4. |
| P6 | CI perturbadas ±1e-6/±1e-3 | **INCONCLUSIVE** | No se evalúa: la trayectoria muere antes por borde cinético. |
| P7 | invariantes (residuo de Friedmann) | **PASS** | Residuo ≤1e-11 en el sistema original (los métodos concuerdan). |
| P8 | detector independiente (discriminante) | **FAIL** | El discriminante s²−4βc→0 en el borde cinético; el detector α>0.95 salta a N≈−2.3, no a −250. |
| P9 | extensión N=−500 + integrales τ/ℓ | **FAIL** | La afirmación bajo test es "α<0.95 a N=−250"; con la raíz correcta α→1 a N≈−2..−4. La extensión numérica a N=−500 de la trayectoria física no es alcanzable con la raíz correcta (borde cinético); el sistema original llega a N≈−80 (límite float64 de ρ_r), donde α ya retornó a 0 tras el giro en N≈−45 — pero el criterio α<0.95 se viola a N≈−2. τ/ℓ no son evaluables como "extendibilidad ≥250 con α<0.95" porque el criterio muere primero. |
| P10 | reproducibilidad (hash) | **PASS** | Cadena trazable (ver §6); reproduce el hallazgo con hash fijo. |
| **GLOBAL** | — | **REFUTED** | Corredor preliminar falsado numéricamente. |

---

## 5. Falsación del mapa v3 y de λ_star

- `lambda_star` (1.66,−0.20): el mapa v3 daba α_s=0.949658 (sobrevive). Con la raíz
  correcta: N_s=−2.26, α_max=0.999976. **λ_star deja de existir como punto de extensión.**
- La afirmación "432/3782 configs extienden ≥250 e-folds" se **retira**: es un artefacto
  del solver de restricción no convergente.
- La afirmación "el fondo se extiende ≥250 e-folds en λ∈[1.66,1.98]" se **refuta**.

**Lo que SÍ queda en pie (resultado acotado):** en la dinámica correcta del sistema
original, el campo escala a α→1 (X→ρ_tot) y el borde cinético se alcanza en ~1–5 e-folds
hacia el pasado para la mayoría de configs; la extensión pasada ≥250 e-folds con α<0.95
**no ocurre en ningún config de la banda testeada**.

---

## 6. Trazabilidad (P10)

- Código evaluado: `TCCU_Eternity_Test_v1.5.23c.py` (sin modificar, módulo original);
  `validar_corredor.py` v2 (batería, con los bugs 1-2 documentados).
- Verificación raíz correcta: reemplazo local de `solve_logA` por A₋ analítico (fórmula en
  §3.3), sin tocar `derivatives` ni el resto del módulo.
- Sistema original: `derivs_orig` (Friedmann+KG) con BDF/DOP853/LSODA/Radau,
  rtol=1e-11..1e-12, atol=1e-14..1e-15, max_step=0.05..0.1, t_eval linspace(0,−80,250..400).
- Entorno: Python 3.10, numpy, scipy (solve_ivp). Semilla: ICs deterministas por config.
- Hash del módulo y del mapa v3: ver `validacion_corredor.json` (P10) al ejecutarse la
  batería corregida; el hallazgo es independiente del hash porque se reprodujo con dos
  formulaciones y 4 integradores.

---

## 7. Lección de método (para TECNICAS_AGI_JAIRO.md)

1. **Un solver de restricción con punto fijo de contracción lenta (tasa ~α) no es
   confiable cerca del borde del dominio (α→1)**: verificar siempre contra la raíz
   analítica o un segundo método (sistema original sin proyección).
2. **La "identidad" de un sistema reducido contra sí mismo no valida física**: el
   residuo de Friedmann del módulo reducido es pequeño porque usa el MISMO A incorrecto
   para integrar y para verificar. El residuo verdadero (contra el sistema original) era
   el que importaba y no se había medido hasta hoy.
3. **P3 (sistema original) es la piedra de toque**: si el sistema reducido y el original
   discrepan, el original manda (preserva la restricción a 1e-11 con 4 integradores).
4. Publicar el corredor como **falsación numérica del corredor preliminar** (regla del
   protocolo: si desaparece bajo refinamiento, se publica igualmente como falsación).

---

## 8. Archivos afectados

- `mapa_tccu0b_v3.json` — resultado de corredor **RETIRADO** (sustituido por este informe).
- `CORREDOR_PASADO_EXTENDIBLE.md` — ver nota de retractación anexa.
- `MASTER_SCIENTIFIC_STATUS_2026-08-26.md` §21–§22 — ver nota de retractación anexa.
- `TCCU_Eternity_Test_v1.5.23c.py` — NO se modifica (el bug se documenta; la corrección
  local queda descrita en este informe para reproducibilidad).
