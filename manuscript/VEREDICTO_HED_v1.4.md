# VEREDICTO HED-F v1.4 — Reproducibilidad y contención (2026-09-01)

**Pre-registro:** `PREREGISTRO_HED_v1.4.md` (firmado antes de ejecutar).
**Física congelada:** `tccu_hed_v1_3.py` (SHA-256 `d901feb8099e92c4…`) — NO modificada.
**Referencia:** `summary_v1_3.json` (SHA-256 `53e8307e1decaee1…`).

---

## Veredicto por prueba

| Prueba | Qué verifica | Resultado | Veredicto |
|---|---|---|---|
| **R1** | Reproducción independiente del bloque principal (N=80, 100 Myr, seed 42+ord(key)) | P_ret ref=repro **idénticos** en A–E (3.941e-07 / 5.767e-02 / 4.997e-01 / 4.000e-01 / 8.000e-01); surv idénticas (0.287 / 0.988 / 1.0 / 1.0 / 1.0); IC bootstrap (1000 resamples) contiene a la referencia | **PASS** |
| **R2** | Robustez N=10⁴ (artefactos `hed_robustez_{A..E}.jsonl`, 3 celdas c/u: 10/50/100 Myr) | 15/15 celdas completas; orden P_ret@100: A(5.1e-07) → B(5.8e-02) → D(4.0e-01) → C(5.0e-01) → E(8.0e-01) = **A→B→D→C→E** preservado | **PASS** |
| **R3** | Destrucción T1–T4 (`hed_destruccion_*.json`, 7 artefactos) | 7/7 presentes con hashes; reproducen los veredictos v1.3 (T1 dt, T2 N, T3 memoria ~×3 no gate, T4 H_D2) | **PASS** |
| **R4** | Sensibilidad (`mu_lambdaM_grid.json` 22 pts, `high_mu_sweep.json` 8 pts) | Íntegros con hash; coherentes con v1.3 (sin inversiones) | **PASS** |
| **GLOBAL** | Conjunción R1–R4 | — | **PASS** |

Resultados firmados: `repro_R1.json` (SHA-256 `9e4cbf617e6f0229…`),
`verif_R234.json` (SHA-256 `be8237bc44af7c09…`).

---

## Qué significa este PASS

1. **La física v1.3 es reproducible**: un proceso independiente que importa el módulo
   sin `main()` reproduce exactamente los valores de referencia (determinismo por
   semilla confirmado).
2. **La robustez N=10⁴ se conserva**: el orden A→B→D→C→E (por P_ret) no se invierte al
   pasar de N=80 a N=10⁴; las fracciones F/P son estables.
3. **Las correcciones ya descubiertas quedan contenidas**:
   - N=80 subestima A → N=10⁴ como campaña de robustez (no evidencia ET).
   - Memoria ≈ factor 3, no gate (P_M = 0.25+0.75·M).
   - Orden real A→B→D→C→E.
   - 4 pruebas de destrucción superadas y re-verificadas como trazables.
4. **Advertencia permanente**: HED-F (factibilidad) ≠ HED-O (observación). Nada de esto
   es evidencia de descendientes humanos reales.

## Contención del alcance

- El PASS de v1.4 valida **reproducibilidad y robustez de la física v1.3 congelada**.
- No valida el modelo físico HED en sí (eso requeriría HED-O con datos reales).
- Ningún PASS individual valida; el GLOBAL es la conjunción R1∧R2∧R3∧R4.

## Cierre

- Con v1.4 PASS, el bloque HED-F queda **reproducible y contenido**.
- Próximos pasos disponibles (decisión del Creador):
  a) release de falsación del corredor TCCU-0 (título: informe de falsación/corrección);
  b) Kerr N=256 reanudable en cola;
  c) HED-O si hay datos reales (fuera de este programa).
