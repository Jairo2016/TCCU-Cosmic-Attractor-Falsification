# M3D — Falsación de los potenciales meseta y doble-exponencial

**Fecha:** 25-08-2026 · **Nivel de evidencia:** S2 (24 puntos).

## Resultado

| Forma de potencial | Puntos | F2 (ΔN≥4) |
|---|---|---|
| Meseta V = V₀(1 − e^{−λφ}), λ∈{1,2,3,5,8} × Λ∈{0.15,0.3,0.5} | 15 | **0** |
| Doble-exp V = V₀(e^{−λ₁φ}+e^{−λ₂φ}), (λ₁,λ₂)∈{(3,.5),(5,1),(8,1)} | 9 | **0** |
| **Total** | 24 | **0** |

Patrón uniforme: w_final ∈ [−0.87, −1.00] — el campo termina dominado por el
potencial (tipo energía oscura) en todas las configuraciones; la condición de
polvo nunca se aproxima (span = 0.00).

## Conclusión sistemática (redacción precisa, según el Creador)

$$
\boxed{
\begin{array}{ll}
M3b\ \text{exponencial} & 442 \to 0 \\
M3c\ \text{inverso-potencia} & 168 \to 0 \\
M4\ \ \text{no mínimo (ξ≠0)} & 108 \to 0 \\
M3d\ \text{meseta + doble-exp} & 24 \to 0
\end{array}}
$$

**Redacción exacta defendible (protege contra la objeción de revisor
"¿exploraron toda la cuenca de atracción?"):**

> Las cuatro familias de potencial y la rama de acoplamiento no mínimo
> **exploradas** no producen un régimen DM-like sostenido **bajo las condiciones
> iniciales congeladas (Φ₀=1, π₀=0) y los criterios F2 predefinidos**.

NO se puede concluir "el sistema no posee ningún atractor DM-like"; solo
"no se encontró un atractor desde la cuenca de condiciones iniciales utilizada".
Esa cuenca NO fue explorada — es exactamente el objeto de **M6-IC** (protocolo
nuevo, fuera de M1–M4).

## Grado de libertad restante (no explorado)

La **condiciones iniciales de tracking**: la literatura de k-essence/quintessence
tracking suele exigir ICs en el régimen de seguimiento (la solución tracker es
un atractor al que las ICs deben pertenecer a su cuenca). Las ICs congeladas
(Φ₀=1, π₀=0, campo subdominante) pueden estar fuera de la cuenca.

**Propuesta: protocolo M6-IC** — barrido de condiciones iniciales
(Φ₀, π₀) alrededor del punto de tracking esperado, con el mismo criterio F2.
Esto requiere LIBERAR las ICs (cambio deliberado del protocolo, aprobación del
Creador) manteniendo todo lo demás congelado.

## Archivos

- `numerics/barrido_m3d.py` · `data/barrido_m3d.json`
- Protocolo: `theory/protocolo_falsacion.md`
