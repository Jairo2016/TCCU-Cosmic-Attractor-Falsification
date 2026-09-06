# AUDITORÍA NUMÉRICA INDEPENDIENTE — CLAIMS DEL RIEMANN ENGINE
**Fecha:** 2026-09-06 · **Precisión:** 50 dígitos (mpmath) · **Método:** cuadratura de alta
precisión + derivadas término a término de la serie theta + autovalores de Hankel.
**Scripts:** `nucleo_tccu_c/riemann/auditar_riemann_claims.py`, `c7_estable.py`.
**ADVERTENCIA PERMANENTE:** verificación numérica ≠ demostración. RH sigue OPEN.
Ningún PASS aquí acerca la demostración; solo comprueba que los claims numéricos
concretos del corpus se sostienen (o no) bajo cálculo independiente.

---

## Resumen de veredictos

| Claim | Qué verifica | Veredicto | Detalle |
|---|---|---|---|
| C1 | Φ serie == forma theta (2e^{5u/2}Lϑ) | ✅ **PASS** | rel < 1e-51 en u=0,1,2 |
| C2 | M_k = ∫u^{2k}Φ du finitos positivos (k=0..10) | ✅ **PASS** | M₀=0.12428…, M₁=5.743e-3, …, M₁₀=3.42e-7 |
| C3 | M_k = (−1)^k/2·Ξ^(2k)(0) (Taylor) | ✅ **PASS** | Ξ(0.5) numérico == Taylor(6) a rel 2.1e-17 |
| C4 | H_N = (M_{i+j}) ≻ 0 para N=0..5 | ✅ **PASS** | autovalores todos > 0 (H₅ mín 2.3e-10) |
| C5-core | R_n > q_n (n=0..4) | ✅ **PASS** | R₀=0.358>0.167, R₁=0.638>0.400, R₂=0.753>0.536, R₃, R₄ ✓ |
| C5-ref | R₀∈[0.41,0.48], R₁∈[0.52,0.59], R₂∈[0.61,0.68] | ❌ **DISCREPANCIA** | mis valores: R₀=0.358, R₁=0.638, R₂=0.753 — **fuera de todas las bandas** |
| C6 | J_{2,n} hiperbólico (n=0..3) | ✅ **PASS** | discriminantes > 0 (decrecientes: 7.1e-5 → 3.8e-18) |
| C7 | E(u)<0 para u=0..5 (E=2(ℓ″)³+ℓ″ℓ⁗−(ℓ‴)²) | ✅ **PASS** | E<0 en u=0..5 con derivadas término a término (−1.0e4 → −4.2e16) |

**Resultado: 6/7 claims sostenidos + 1 discrepancia numérica real en C5-ref.**

---

## La discrepancia C5-ref (hallazgo principal)

El corpus afirma (inventario §4.13): "R₀ ∈ [0.41, 0.48], R₁ ∈ [0.52, 0.59],
R₂ ∈ [0.61, 0.68] — todos R_n⁻ > q_n → VERIFICADO".

Mi cálculo independiente (dos métodos de cuadratura coincidiendo a 30 dígitos,
verificación cruzada M₁ = −Ξ″(0)/2 consistente) da:

| n | R_n (auditoría) | Banda del corpus | q_n (fórmula) |
|---|---|---|---|
| 0 | **0.3583** | [0.41, 0.48] | 0.1667 |
| 1 | **0.6376** | [0.52, 0.59] | 0.4000 |
| 2 | **0.7531** | [0.61, 0.68] | 0.5357 |

Además, **inconsistencia interna del corpus**: su q₁ reportado = 0.3 (=3/10), pero su
propia fórmula q_n=(2n+1)(2n+2)/((2n+3)(2n+4)) da q₁ = 12/30 = **0.4**. El valor 0.3 no
sale de esa fórmula.

**Interpretaciones posibles (no resueltas aquí):**
1. El corpus usa una **normalización de momentos distinta** a M_k=∫u^{2k}Φ du (p. ej.
   momentos sobre los coeficientes γ_k=2M_k/(2k)! con otra convención, o la secuencia b_n
   de ξ estándar). Probé R_n sobre γ_k → da 2.15/1.59/1.41, que tampoco cae en las bandas.
2. Los valores del corpus provienen de un cálculo con otra definición de Φ o de Ξ.
3. Error numérico en el corpus.

**Consecuencia honesta:** la afirmación "R₀∈[0.41,0.48] etc." **no se reproduce** con la
normalización canónica que el propio corpus define (M_k=∫u^{2k}Φ, γ_k=2M_k/(2k)!).
La desigualdad estructural R_n>q_n (que es lo que implica J₂ₙ hiperbólico vía Turán) **sí
se cumple** con mis valores. El claim de hiperbolicidad d=2 sobrevive; las bandas
numéricas concretas del corpus quedan **en discrepancia no resuelta**.

### Resolución adicional (2026-09-06): inconsistencia interna confirmada en q₁

Auditoría dirigida de la fórmula q_n del corpus:

| n | q_n fórmula (2n+1)(2n+2)/((2n+3)(2n+4)) | q_n reportado en corpus | ¿Coincide? |
|---|---|---|---|
| 0 | 1/6 = 0.1667 | 1/6 = 0.1667 | ✅ |
| 1 | **12/30 = 0.4000** | **3/10 = 0.3000** | ❌ **NO** |
| 2 | 15/28 = 0.5357 | 15/28 = 0.5357 | ✅ |
| 3 | 28/45 = 0.6222 | 28/45 = 0.6222 | ✅ |
| 4 | 45/66 = 0.6818 | 45/66 = 0.6818 | ✅ |

El valor q₁=3/10 **no sale de la fórmula que el propio corpus declara** (que da 0.4).
La inconsistencia es **aislada en n=1** — los demás q_n son consistentes con la fórmula.

Además, la desigualdad estructural de Turán relevante para J₂ₙ hiperbólico
(R_n > (2n+1)/(2n+3), Csordas–Norfolk–Varga) **se cumple con los valores auditados**:

| n | R_n (auditoría) | (2n+1)/(2n+3) | ¿R_n > umbral? |
|---|---|---|---|
| 0 | 0.3583 | 0.3333 | ✅ |
| 1 | 0.6376 | 0.6000 | ✅ |
| 2 | 0.7531 | 0.7143 | ✅ |

**Conclusión de la resolución:** la discrepancia C5-ref apunta a un **error local de
transcripción o normalización en la tabla numérica del corpus** (bandas de R_n y q₁),
no a un fallo de la matemática estructural: la hiperbolicidad de J₂ₙ (claim C6) se
sostiene con la normalización canónica y el umbral de Turán correcto. Para que el corpus
sea citable, deben corregirse q₁ (0.3 → 0.4) y las bandas de R_n, o documentarse la
normalización alternativa que las produce.

### Resolución DEFINITIVA (2026-09-06): la definición del corpus coincide con la mía → el error está en sus momentos

Verificación contra el texto original del corpus (pág. 96 del PDF), que define
explícitamente:

```
R_n = M_{n+1}² / (M_n M_{n+2})   ≥   q_n = (2n+1)(2n+2) / ((2n+3)(2n+4))
```

**Esta es exactamente la normalización canónica que usé.** No hay normalización
alternativa que explique la discrepancia: el propio corpus declara la misma definición.

Cálculo inverso: ¿qué M₂ produciría R₀ ∈ [0.41, 0.48]?

| R₀ objetivo | M₂ requerido | M₂ auditado (50 dígitos) | Razón |
|---|---|---|---|
| 0.41 | 6.473e-4 | 7.407e-4 | 1.144 |
| 0.45 | 5.897e-4 | 7.407e-4 | **1.256** |
| 0.48 | 5.529e-4 | 7.407e-4 | 1.340 |

Los momentos del corpus que producirían sus bandas son ~15-34% menores que los
calculados independientemente. Dado que:
1. la definición de R_n es idéntica (pág. 96),
2. la integración independiente a 50 dígitos es robusta (dos métodos, verificación
   cruzada con Ξ″(0) consistente),
3. la discrepancia es sistemática y grande (no redondeo ni truncación de serie),

**la conclusión es que los momentos M₂..M₄ (o la construcción de los "intervalos
rigurosos") del corpus contienen un error numérico**, o sus intervalos no se derivan de
la definición declarada. Las bandas R₀∈[0.41,0.48], R₁∈[0.52,0.59], R₂∈[0.61,0.68]
**no son reproducibles** y no deben citarse sin corrección.

**Lo que SÍ se sostiene** (independiente del error): R_n > (2n+1)/(2n+3) con valores
auditados (0.358>0.333, 0.638>0.600, 0.753>0.714) ⇒ J₂ₙ hiperbólico vía Turán (claim C6
PASS), y la positividad H_N≻0 (C4 PASS).

---

## Cómo se corrigió C7 (transparencia de método)

- Primera versión: diferencias finitas de log Φ con paso fijo → NaN en u=3,4 (Φ≈e⁻¹⁴⁰,
  e⁻⁵⁰⁰; cancelación catastrófica).
- Versión estable: derivadas de Φ por **derivación término a término de la serie theta**
  (recurrencia polinómica en x=e^{2u}, análoga al bloque m=1 exacto que el corpus usa).
  Resultado: E(u)<0 en u=0..5, coincidiendo en u=0 con el método anterior (−1.04567e4).

## Nota metodológica (regla del programa)

- 6 PASS numéricos **no** convierten el Riemann Engine en una demostración: el propio
  corpus mantiene RH=OPEN, F=0, SOLVED=NO, y bloquea R4 el puente "Hankel/Jensen finito ⇒
  RH". Esta auditoría confirma que las piezas numéricas básicas (núcleo, momentos,
  positividad de Hankel hasta N=5, hiperbolicidad J₂ hasta n=3, E<0 en u=0..5) son
  **consistentes con el cálculo independiente** — nada más.
- La discrepancia C5-ref es **el resultado científicamente útil** de esta auditoría:
  marca un punto concreto donde el corpus debe ser revisado o su normalización
  documentada explícitamente antes de que sus tablas numéricas sean citables.

## Archivos
- `nucleo_tccu_c/riemann/auditar_riemann_claims.py` (auditoría C1-C7)
- `nucleo_tccu_c/riemann/c7_estable.py` (E(u) por derivadas término a término)
- `auditoria_riemann_claims.json` (resultados)
