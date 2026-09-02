# PROTOCOLO DE VALIDACIÓN DEL CORREDOR TCCU-0 (P1-P10) — v2
**Fecha:** 01-09-2026 · **Fijado por el Creador** como prioridad #2 (tras S3 Kerr).
**Correcciones del Creador aplicadas (v2):**
1. **P1/P2**: la evidencia primaria de convergencia son **integradores de orden
   superior** (BDF, DOP853) sobre el sistema log-signed; Euler es **control auxiliar**
   (P1e). El objetivo es demostrar que el corredor no es un artefacto numérico.
2. **P9**: separar **"supervivencia numérica hasta N=−250/−500"** de
   **"extendibilidad física"**: las integrales τ = ∫dN/h y ℓ = ∫e^N dN/h se evalúan
   e informan **independientemente** (finitud = extendibilidad física).
3. **P10**: reproducción realmente trazable (código + configuración + entorno +
   semilla → resultado → SHA-256), no solo hash del archivo de referencia.
4. **Veredicto**: ningún PASS individual valida. **GLOBAL = VALIDATED / REFUTED /
   INCONCLUSIVE**, exigiéndose el conjunto crítico P1–P4, P7–P9.

## Regla de asimetría (inalterable)
- Corredor sobrevive al refinamiento → **resultado positivo acotado**
  (λ ∈ [λ₋, λ₊] con N_past ≥ 250 y errores de resolución).
- Corredor no sobrevive → **falsación numérica del corredor preliminar**.
- Nunca: "N_past ≥ 250" → "universo eterno". Es una afirmación numérica de
  extendibilidad pasada dentro del modelo.

## Afirmación bajo test
En TCCU-0 (P = X + X²/Λ⁴ − ρ_c0 e^{−λΦ}, M_P=1, Λ=0.15, Ω_m=0.315, Ω_r=9e-5),
signo=+, el fondo se extiende ≥ 250 e-folds hacia el pasado en la banda
λ ∈ [1.66, 1.98] × w0 ∈ [−0.32, +0.20] (barrido fino v3, dn=0.005, detector α>0.95),
con giro del campo (Π cruza 0) y congelación (dominio de radiación).

## Batería congelada

| P | Prueba | Método | Criterio de supervivencia |
|---|---|---|---|
| P1 | Δt ×1/2 (0.0025) | Euler log-signed | α_max(250 e-folds) < 0.95; N_s idéntico |
| P2 | Δt ×1/4 (0.00125) | Euler log-signed | converge con P1 |
| P3 | tolerancias ×10 más estrictas | BDF original, rtol 1e-11 | giro Π→0 reproducido |
| P4 | segundo método (hacia atrás) | sistema ORIGINAL BDF/Radau a N=−80 | α<0.95 y Π cruza 0 (independiente) |
| P5 | borde fino de λ | Δλ=0.0025 en [1.60,1.68] y [1.94,2.02] | localiza λ₋ y λ₊ con incertidumbre |
| P6 | CI perturbadas | Φ₀,Π₀ × {1±1e-6, 1±1e-3} | corredor robusto a perturbaciones pequeñas |
| P7 | invariantes | residuo de Friedmann | |A−A_cuadrática|/A < 1e-8 a lo largo |
| P8 | detección independiente | discriminante b²−4ac vs α>0.95 | N_s coincide (ambos criterios) |
| P9 | extensión >250 | N → −500/−1000 (log-signed, dn=0.01) | α_max < 0.95; integrales τ/ℓ finitas |
| P10 | reproducción limpia | re-ejecutar v3 (muestra) | N_s idéntico (hash) |

## Bordes con incertidumbre
λ₋ = último λ (ascendiendo) con extensión ≥250 · λ₊ = primer λ con ruptura.
Incertidumbre de resolución: ±Δλ/2 en λ y ±dn/2 en N_s.
Resultado esperado de la publicación:
**λ ∈ [λ₋ ± Δλ/2, λ₊ ± Δλ/2] con N_past ≥ 250 ± dn/2 (y errores de los métodos P1-P4).**

## Configuraciones de referencia
- Corredor: (1.66, −0.20, +1) λ⋆ · (1.68, 0.00, +1) · (1.84, 0.00, +1)
- Borde bajo (rompe): (1.64, 0.00, +1) · Borde alto (rompe a −15): (2.00, 0.00, +1)

## Salida
`validacion_corredor.json` (resultados por P) + este documento actualizado con los
veredictos PASS/FAIL/INCONCLUSIVE por prueba. La reproducción (P10) se ancla con las
huellas de `mapa_tccu0b_v3.json` (SHA-256 0562C31F…).

---

## ⚠️ RESULTADO FINAL (2026-09-01): FALSACIÓN NUMÉRICA DEL CORREDOR

La batería P1–P10 v2, ejecutada con las correcciones del Creador, **REFUTA el corredor
preliminar**. Veredicto global: **GLOBAL: REFUTED** (ver
`INFORME_FALSACION_CORREDOR_2026-09-01.md`).

### Causa raíz
`solve_logA` de `TCCU_Eternity_Test_v1.5.23c.py` resuelve la restricción
A = c + αA + βA² por iteración de punto fijo con tasa de contracción ≈α; cuando α→0.93+ se
necesitan >200–500 iteraciones para converger, pero el módulo ejecuta solo 6. El A
resultante es incorrecto por factores 2–100 (residuo hasta 0.14), lo que frena Π y fija
α≈0.94–0.95 → el mapa v3 registró "limite_pasos/extiende" donde no hay extensión.

### Hechos
1. Con la raíz analítica correcta A₋=2c/(s+√(s²+4βc)) (o el sistema original
   Friedmann+KG, verificado con BDF/DOP853/LSODA/Radau, residuo ≤1e-11):
   **α cruza 0.95 a N≈−2..−4.4 para TODOS los configs de la banda**, incluido
   λ⋆=(1.66,−0.20) → N_s=−2.26. α_max→1.0 (borde cinético, X→ρ_tot).
2. El mapa v3 (432 configs "limite_pasos" con α_s≈0.94–0.95 y N_s=−250) era un artefacto
   del solver no convergente.
3. El sistema original confirma: α_max=1.0 a N≈−2.3 (λ=1.66,−0.20), giro Π→0 y
   congelación a N≈−45 (P3 reproducido), pero **el criterio α<0.95 se viola a N≈−2**.

### Veredicto por prueba
P1 FAIL · P2 FAIL · P3 PASS (pero confirma borde, no extensión) · P4 PASS ·
P5 INCONCLUSIVE (bordes λ₋/λ₊ pierden sentido) · P6 INCONCLUSIVE · P7 PASS ·
P8 FAIL · P9 FAIL · P10 PASS → **GLOBAL: REFUTED (falsación numérica del corredor
preliminar)**. Ningún PASS individual valida; la regla del protocolo se cumple:
*si el corredor no sobrevive al refinamiento, se publica igualmente como falsación*.

