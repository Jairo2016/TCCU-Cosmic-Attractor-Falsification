# CIERRE CAMPAÑA KERR NS3D — S3/S4/S5/S6 (2026-09-01)

**Sistema:** NS3D pseudospectral (Fourier-Galerkin, Gottlieb-Orszag, dealiasing 2/3,
RK4 adaptativo) · `simulador_ns3d.py` + `campana_kerr.py` · N=128, ν=1e-3, T=10.0,
dt_base=0.002 · vórtices antiparalelos (Kerr) · semilla fija (determinista).

**Estado:** campaña COMPLETADA (exit 0, 25 checkpoints, 5000 pasos, ~1266 min de CPU).
Checkpoint final: `campana_kerr_ckpt.npz` (+ `.serie.json`).

---

## S3 — Ejecución completa y verificación de invariantes

| Métrica | t=0 | t=10 (final) | tendencia |
|---|---|---|---|
| E (energía) | 3.7357 | 3.3246 | ↓ 11.0 % (disipación) |
| enstrofia | 54.67 | 34.28 | ↓ |
| ‖u‖_L3 (norma crítica) | 1.4520 | 1.3239 | ↓ 8.8 % |
| ‖u‖_∞ | 1.0000 | 0.5986 | ↓ |
| ‖ω‖_∞ (wmax) | 8.638 | 7.336 | ↓ (pico 8.39 en t≈4.4) |
| ‖∇u‖_∞ | 6.665 | 5.189 | ↓ |

**Verificación de invariantes desde el checkpoint final (independiente):**
- 6/6 métricas (E, enst, L3, Linf, wmax, gradinf) reproducidas EXACTAMENTE (rel < 1e-15)
  al recalcular el campo espectral guardado con la convención del simulador → el
  checkpoint es íntegro y reproducible.
- Divergencia espectral: max|k·û| = 2.9e-10 (absoluto), **2.7e-15 relativo a |k||û|**
  → campo incompresible a precisión de máquina (proyección Gottlieb-Orszag mantenida
  durante 5000 pasos).
- Deriva de E entre checkpoints: máx 1.01e-2 (escalón inicial), luego monótona
  decreciente — disipación viscosa esperada, sin ganancia de energía.

**S3: PASS** (t=10 completo, invariantes ok, campo reproducible desde checkpoint).

## S4 — Análisis de convergencia (comparación de resoluciones)

El protocolo pre-registra la tipología:
1. L3/‖ω‖∞ **decrecen** → no se observa mecanismo singular.
2. **crecen** sin converger con N → probable under-resolution.
3. **crecen y convergen** con N → evidencia numérica seria (pendiente S6).
4. crecimiento aparente que **desaparece al refinar** → artefacto.

**Estado: no existen series a N=256 ni N=512** (solo N=128). La comparación a tiempos
físicos idénticos (`analisis_convergencia.py`) no puede ejecutarse.

**S4: INCONCLUSIVE** — sin datos de resolución superior no es posible clasificar la
tipología 1-4. (El comportamiento observado a N=128 es compatible con 1, pero la
clasificación formal requiere el barrido en N.)

## S5 — Norma crítica y tasas (trayectoria única, N=128)

- ‖u‖_L3: 1.4196 → 1.3239 entre t=2 y t=10 (sin contar el transitorio inicial):
  **decrece** — sin crecimiento de la norma crítica.
- dL3/dt máximo: **−1.00e-02** (negativo; nunca positivo sostenido).
- ‖ω‖_∞ máximo en la ventana: 8.39 (t≈4.4), luego decae → sin acumulación.
- ‖∇u‖_∞ máximo: 5.93 (t≈4.4), luego decae.

**S5: PASS (acotado)** — en esta trayectoria y resolución (N=128, ν=1e-3, T=10) no se
observa crecimiento de la norma crítica ni de la vorticidad.

## S6 — Veredicto

**S6: INCONCLUSIVE (resultado negativo acotado, NO confirmación física).**

- La hipótesis H0 ("posible singularidad de tipo Kerr en este régimen") **NO es
  falsada** en sentido estricto: S4 no se pudo ejecutar (sin N=256/512).
- Pero el resultado es un **negativo acotado valioso**: a N=128, ν=1e-3, T=10, las
  normas críticas **decrecen** — no hay indicio numérico de blow-up en la trayectoria
  explorada.
- **NO se convierte este resultado numérico en confirmación física** (regla del
  protocolo): sería necesaria la serie N=256/512 para S4/S6 formal.

## Archivos
- `campana_kerr_ckpt.npz` (campo final, 100 MB) + `campana_kerr_ckpt.npz.serie.json` (25 pts)
- `campana_kerr_reanudada.log` (registro completo de la campaña)
- `auditoria_kerr.json` (invariantes + metadatos + hashes)
- Hashes: simulador_ns3d.py `c49e4faa73ba…` · campana_kerr.py `df51c9644965…` ·
  npz `fcf39f2f6f37…`

## Siguiente paso
Barrido en N (N=256, y si el presupuesto lo permite N=512) a tiempos físicos idénticos
para ejecutar S4 y clasificar la tipología; con ello S6 pasa de INCONCLUSIVE a un
veredicto formal. Decisión del Creador sobre el costo CPU (N=256 ≈ 8× el costo de N=128;
N=512 ≈ 64×).
