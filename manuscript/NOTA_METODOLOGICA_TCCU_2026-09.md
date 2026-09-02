# NOTA METODOLÓGICA TCCU — Lecciones de un programa de falsación computacional (2026)

**Versión:** 1.5 (documento metodológico del repositorio TCCU-Cosmic-Attractor-Falsification)
**Fecha:** 2026-09-02
**Ámbito:** destilación pública de las lecciones operativas del programa TCCU
(26-08 → 01-09-2026), incluyendo las cuatro autocorrecciones documentadas.

---

## 1. Resumen

Este documento convierte en lecciones científicas reutilizables lo que el programa
TCCU aprendió operativamente durante sus campañas: cómo someter hipótesis
cosmológicas y físico-matemáticas a simulación, auditoría y falsación reproducible,
y cómo detectar y retirar resultados propios incorrectos sin disfrazarlos.

La lección central es una distinción que, ignorada, produjo el error más costoso
del programa:

> **Consistencia interna de un módulo computacional ≠ validez frente al sistema
> físico que pretende representar.**

Un módulo puede satisfacer todas sus propias identidades (batería 8/8 PASS) y, aún
así, producir un resultado físicamente falso si una pieza interna (un solver de
restricción, un signo, una raíz) resuelve mal la ecuación que se le supone.

---

## 2. El ciclo de campaña (pre-registrado y auditable)

El programa consolidó un ciclo de trabajo que debe repetirse en cada hipótesis:

```
hipótesis → implementación → batería de identidades → simulación →
auditoría → resultado → verificación independiente → publicación o falsación
```

Reglas operativas del ciclo:

1. **Pre-registro antes de ejecutar**: criterios de éxito/fallo, umbrales, semillas
   y pasos definidos *a priori*; el veredicto se aplica después sin renegociar.
2. **Batería de identidades antes de integrar**: ningún código numerico entra en
   campaña sin verificación algebraica automática (derivación on-shell contra un
   ground truth, tolerancia < 1e-8).
3. **Doble formulación**: cuando existe un sistema reducido (con proyección de
   restricción) y un sistema original (sin proyección), ambos deben coincidir;
   si discrepan, el sistema original manda.
4. **Verificación independiente de los resultados clave** con un segundo método o
   integrador, y reproducción desde artefactos (hashes).
5. **Resultados negativos se publican igualmente**, con su causa raíz, sin
   maquillaje; los artefactos erróneos se retiran pero se conservan con su cadena
   de reconstrucción.

---

## 3. La distinción que todo lo gobierna

### 3.1 Consistencia interna vs. validación física

Un módulo reducido (p. ej., sistema log-signed con restricción proyectada) puede:

- satisfacer todas sus identidades internas (las ecuaciones que él mismo define);
- preservar sus propios residuos a precisión de máquina;
- y aun así NO representar el sistema físico original si resuelve mal una ecuación
  intermedia (p. ej., una restricción algebraica con un punto fijo mal convergido).

**Regla:** la validación contra el sistema físico original (Friedmann+KG sin
proyección, en el caso cosmológico) es la piedra de toque. La consistencia interna
es necesaria pero no suficiente.

### 3.2 Estudio de caso: el corredor TCCU-0 (falsación del 01-09-2026)

La búsqueda de "eternidad pasada" en TCCU-0 encontró un corredor aparente:
λ∈[1.66,1.98], con extensiones de cientos de e-folds hacia el pasado, y produjo un
mapa (v3) con 432/3782 configuraciones "extendibles" (N_past ≥ 250, α<0.95).

La verificación posterior mostró que `solve_logA` — el solver de la restricción
algebraica A = c + αA + βA² del módulo reducido — usaba una iteración de punto fijo
con tasa de contracción ≈ α y solo **6 iteraciones**:

| α | iteraciones necesarias para 1e-14 | A_módulo / A_exacta |
|---|---|---|
| 0.27 | 25 | 1.000 |
| 0.90 | 285 | 0.522 |
| 0.93 | 408 | 0.398 |
| 0.95 | 571 | 0.302 |
| 0.999 | >2000 | 0.007 |

El A incorrecto (factor 2–100) frenaba artificialmente Π justo bajo el detector
α>0.95, produciendo el falso corredor. Al sustituir el solver por la **raíz
analítica** A₋ = 2c/(s+√(s²−4βc)) y verificar contra el **sistema original
Friedmann+KG** (4 integradores independientes: BDF, DOP853, LSODA, Radau), el
corredor desapareció:

```
Punto representativo (λ,w₀) = (1.66, −0.20):
  mapa v3        : N_s = −250   (extiende, α_max ≈ 0.95)
  raíz analítica : N_s = −2.26  (α_max ≈ 0.999976)
  sistema original: N_s = −2.3  (α_max = 1.000000)
```

**Conclusión:** la afirmación del corredor (N_past ≥ 250) queda **refutada**. No
porque "cambiara el resultado", sino porque se identificó la causa matemática
concreta del falso resultado: un solver de restricción insuficientemente convergido.

**Consecuencia metodológica:** la batería de identidades 8/8 del módulo reducido
validaba el módulo contra sí mismo, no contra el sistema físico. El estatus de esos
artefactos queda recalificado de "validados" a "consistentes internamente,
pendientes de verificación contra el sistema original".

---

## 4. Trampas numéricas cazadas en campañas reales

| Trampa | Síntoma | Solución |
|---|---|---|
| 1−ε₀ colapsa para ε₀<1e-16 | N₀=+inf → ΔN=−inf | integrar en ε₀ o en log |
| Decrementos < ULP cerca de 1.0 | RK4 "estable" pero falso | cambiar variable (ε=1−u) |
| Cancelación en cuadráticas con a→0 | raíz gigante espuria | forma estable 2c/(−b+√disc) |
| exp() de magnitudes ~e³⁷⁰⁰ | overflow → NaN | aritmética log-signed (slogadd) |
| Estado que crece doble-exponencial | E colapsa | integrar logE |
| Drift fuera de la restricción | h→0 violando Friedmann | constraint proyectada (resolver h²=ρ) |
| Punto fijo con contracción lenta (tasa ≈α→1) | A erróneo por factor 2–100 | raíz analítica o segundo método |
| Derivada numérica de K | ruido | K analítico simplificado |
| Asintótico \|Π\|→√6 sin cruzar | detector ciego | detector α=Π²/6 > 0.95 |
| t_eval fuera de t_span (logspace) | ValueError | np.clip(t_eval, t_min, 0) |
| Media sesgada por colapsos tempranos | curva teórica ≠ datos | separar supervivientes |
| Integración "hacia adelante" en campaña del pasado | ruptura falsa a N≈210 (futuro) | dn<0 (hacia el pasado) |

---

## 5. Patrones de campaña robusta

1. **Checkpoint por configuración** (JSONL + append + flush): sobrevive reinicios;
   escribir la celda inmediatamente tras el bucle y *después* agregar (el crash en
   la agregación post-cómputo perdió una celda de 10⁴ realizaciones).
2. **Costo por realización medido antes** de lanzar campañas grandes; paralelizar
   por celda; gestionar el límite de jobs.
3. **Monitoreo por archivo de progreso** (no por pipe que retiene la salida);
   verificar procesos por CPU acumulada y edad.
4. **Pre-registro de veredictos**: P1..Pn con PASS/FAIL/INCONCLUSIVE + GLOBAL;
   ningún PASS individual valida; el GLOBAL es la conjunción.

---

## 6. Honestidad (reglas no negociables)

1. No rescatar un resultado fallido: si la física correcta rompe el modelo, se
   reporta la ruptura, no se busca un "arreglo".
2. Reportar los errores propios (signo invertido, raíz equivocada, sesgo de media,
   solver mal convergido) con la misma claridad que los ajenos.
3. Toda afirmación "el modelo hace X" debe poder reproducirse con el comando
   exacto y el seed.
4. Separar siempre: simulación ≠ evidencia · probabilidad del modelo ≠
   probabilidad de la hipótesis · región F (inviabilidad interna) ≠ falsación
   empírica · ruptura finita de la restricción ≠ singularidad real.
5. Cuando un mapa grueso y uno fino discrepan, el fino manda; cuando el sistema
   reducido y el original discrepan, el original manda. Ambas reglas se aplicaron
   y ambas revocaron resultados previos favorables.

---

## 7. Lenguaje preciso (NO-GO)

- "Región F del modelo" → **región de inviabilidad interna** (no "falsación empírica").
- "Ruptura finita de la restricción" → así, sin escalar a "singularidad del universo".
- P_ret (probabilidad interna del modelo) ≠ P(H_D|E) (inferencia sobre el universo).
- "H_D rechazada" → "H_D rechazada bajo el conjunto de supuestos y el modelo causal
  especificado".
- "N_past ≥ 250" → afirmación numérica de extendibilidad pasada dentro del modelo;
  nunca "universo eterno".

---

## 8. Estado del programa (referencia para el ciclo siguiente)

| Línea | Estado |
|---|---|
| TCCU-0 (DM unificada) | falsado bajo la formulación estudiada |
| Corredor de pasado | refutado (falsación publicada en v1.4) |
| HED-F | v1.3 destrucción superada; v1.4 preregistro+reproducción GLOBAL PASS (física congelada) |
| Kerr NS3D | S3 PASS; S4/S6 INCONCLUSIVE (falta N=256) |
| Infraestructura | 5 releases, 5 DOIs, hashes, ledger, reproducibilidad |

---

## 9. Conclusión

El valor científico del programa TCCU a septiembre de 2026 no reside en una teoría
demostrada — ninguna lo está — sino en un sistema capaz de:

- convertir hipótesis especulativas en hipótesis computables;
- someterlas a simulación, identidades, auditoría y falsación;
- detectar errores graves en sus propias implementaciones;
- retractar resultados que inicialmente parecían favorables;
- conservar únicamente aquello que sobrevive a pruebas cada vez más estrictas.

La regla más transferible es la que abre este documento: **la consistencia interna
no valida un sistema físico; solo la verificación contra el sistema original lo
hace.** Quien la aplique ahorrará la clase de falsación costosa — pero instructiva —
que este programa ya ha pagado.
