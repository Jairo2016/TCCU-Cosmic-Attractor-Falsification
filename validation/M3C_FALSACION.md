# M3C — Falsación del inverso-potencia como tracker DM-like

**Fecha:** 25-08-2026 · **Nivel de evidencia:** S2 (168 puntos numéricos) + test
fuerte de polvo (análisis del Creador).

## Resultado

| Métrica | Valor |
|---|---|
| Puntos barridos (n × Λ) | 168 (n∈[0.25,10] log; Λ∈{0.05…1.0}) |
| Puntos con ventana F2 (ΔN≥4) | **0** |
| Residuo de polvo \|u−r−r²\|/(u+r+r²) en materia | **1.0000 en todos los puntos** |
| c_s²_min global | 0.336 (piso 1/3, cinética v4.1 intacta) |

## Diagnóstico del test fuerte (polvo)

La condición de polvo w=0 ⟺ V = X + X²/Λ⁴ **nunca se aproxima**:

- n pequeño (0.25–2): campo **congelado** (V-dominante, w_fin ≈ −0.99) — el
  inverso-potencia poco empinado se comporta como energía oscura, no materia.
- n grande (10): campo rueda pero sin equilibrar cinética con potencial
  (w_fin ≈ −0.40; nunca w≈0 sostenido con ρ_Φ ∝ a⁻³).

## Conclusión programática (árbol de decisión del Creador)

$$
\boxed{
\text{M3b (exponencial, 442}\to 0\text{)} + \text{M3c (inverso-potencia, 168}\to 0\text{)}
\Rightarrow \text{el fracaso del mecanismo DM-like NO es exclusivo de la exponencial}
}
$$

- **El mecanismo k-essence X + X²/Λ⁴ con estas condiciones iniciales no puede
  sostener la condición de polvo** con ninguno de los dos potenciales.
- **Justifica M4 (ξ ≠ 0) con más fuerza**, como anticipó el Creador.
- Salvedad abierta (no ejecutada, protocolo nuevo requeriría cambiarla): las
  ICs (Φ₀=1, π₀=0) quedaron congeladas; la literatura de tracking k-essence a
  veces exige ICs específicas de seguimiento. Es una vía alternativa
  independiente del cambio de potencial.

## Archivos

- `numerics/barrido_m3c.py` · `data/barrido_m3c.json` · `figures/heatmap_m3c.png`
- Protocolo y jerarquía: `theory/protocolo_falsacion.md`
- Benchmark negativo conservado (no se reemplaza ni se oculta).

## Estado de la jerarquía

M1 ✅ · M2 ✅ · M3a ✅ · **M3b ❌ FALSADO** · **M3c ❌ FALSADO** · M3d (meseta) pendiente · **M4 (ξ≠0) JUSTIFICADO**.
