# M6-IC — Barrido de condiciones iniciales (protocolo nuevo, decisivo)

**Fecha:** 25-08-2026 · **Nivel de evidencia:** S2 (72 puntos + cuenca).
**Protocolo:** nuevo, fuera de M1–M4 (9 reglas del Creador). Congelado:
potencial exponencial λ=5, Λ=0.15, α=2, ξ=0, criterios F2 idénticos.

## Resultado

| Categoría | N | Significado |
|---|---|---|
| A — sin F2 | 17 | FAIL dinámico |
| B — F2 transitorio (ΔN<4) | **55** | w≈0 aparece transitoriamente, nunca se sostiene |
| C — F2 sostenido (ΔN≥4) | 0 | — |
| D — ATTRACTOR (F2 + cuenca convergente) | **0** | — |
| Control (Φ₀=1, u₀=0) | ΔN_F2 = 0.00 | **reproduce el histórico** ✓ |

## Lectura científica

1. **El mecanismo "toca" el comportamiento de materia pero no puede sostenerlo**:
   55 de 72 trayectorias cruzan la condición w≈0 de forma transitoria (ΔN<4) —
   el campo pasa por la curva de polvo pero la abandona. Nunca 4 e-foldings.
2. **No existe región finita de ICs (ℬ_F2 = ∅)** con F2 sostenido en la rejilla:
   la cuenca de atracción DM-like no aparece en el dominio explorado.
3. **Control válido**: la IC histórica reproduce el resultado previo → el
   protocolo es consistente.

## Conclusión (redacción precisa, regla 9 del Creador)

> Las cuatro familias de potencial, la rama ξ≠0 **y un barrido de 72
> condiciones iniciales** (Φ₀ ∈ [0.3, 3], u₀ ∈ [−2, 5]) no producen un régimen
> DM-like sostenido bajo los criterios F2 predefinidos.

**Decisión: se congela la expansión del espacio de búsqueda → preparar el
artículo de falsación** (la objeción de revisor sobre la cuenca queda
respondida con evidencia).

## Benchmark acumulado (resultados negativos independientes)

$$
442\to0 \quad 168\to0 \quad 108\to0 \quad 24\to0 \quad 72\to0\ (\mathrm{F2\ sostenido})
$$

## Archivos

- `numerics/barrido_m6ic.py` · `data/barrido_m6ic.json`
- Informe del programa: `theory/protocolo_falsacion.md`
