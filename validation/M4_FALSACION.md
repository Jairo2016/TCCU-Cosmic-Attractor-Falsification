# M4 — Falsación del acoplamiento no mínimo (ξ ≠ 0, λ = 5, α = 2)

**Fecha:** 25-08-2026 · **Nivel de evidencia:** S2 (108 puntos).

## Resultado

| Filtro | Resultado |
|---|---|
| F1 — fondo converge | **108/108** ✓ |
| F2 — no-ghost / gradiente (Q_s>0, c_s²_full∈(0,1]) | **108/108** ✓ |
| F3 — G_eff/G_N ∈ [0.5, 2] y Ġ/G < 1e-12/yr | **0/108** (G_eff se desvía >1%: sin screening en esta rama) |
| F4 — F2 (DM-like, ΔN≥4) | **0/108** (w_final −0.86…−0.96, campo congelado tipo DE) |
| **Veredicto** | **0/108 PASS** |

## Lectura científica

1. El sistema acoplado (Φ̈, Ḣ) con el signo correcto de la Raychaudhuri es
   numéricamente sano (F1 108/108).
2. La estabilidad escalar-tensor (M4-2) se cumple en todo el dominio: sin
   fantasmas ni inestabilidades de gradiente.
3. **El acoplamiento no mínimo NO crea el atractor DM-like**: con λ=5, α=2, el
   campo permanece dominado por el potencial (w→−0.9) — la dinámica no alcanza
   la condición de polvo, igual que en M3b/M3c.
4. La gravedad efectiva varía (F3): 1/F se aleja >1% de G_N durante la
   evolución — sin mecanismo de screening (chameleon) en esta rama, las
   restricciones solares/BBN serían severas (§40–41).

## Benchmark conservado

$$
\boxed{
M3b:\ 442\to0 \qquad M3c:\ 168\to0 \qquad M4:\ 108\to0
}
$$

Tres familias independientes (exponencial, inverso-potencia, acoplamiento no
mínimo) fallan sistemáticamente el criterio F2 en los dominios explorados.

## Hallazgo metodológico — M5 propuesto duplicaría M3b

El protocolo `theory/decision_m4.md` (Escenario B) proponía M5 = barrido
(α ∈ {2..8} × λ ∈ {0.5..3}, ξ=0, exponencial). **Ese subespacio ya fue
barrido por M3b** (α∈[2,10] × λ∈[0.5,3], 442 puntos, 0 F2). Ejecutarlo de nuevo
no respondería una pregunta nueva.

**Direcciones genuinamente nuevas:**
- **(a) M3d — potencial meseta/tracker** (familia de potencial aún no probada).
- **(b) Revisión de condiciones iniciales de tracking** (protocolo nuevo con
  ICs libres — el tracking k-essence de la literatura puede requerir ICs de
  seguimiento, no la congelación Φ₀=1, π₀=0).

## Archivos

- `numerics/barrido_m4.py` · `data/barrido_m4.json` · `figures/heatmap_m4.png`
- `analisis_m4.py` · `data/M4_RESULTS.csv` · `figures/heatmap_m4_filtros.png`
- Protocolo: `theory/protocolo_falsacion.md`, `theory/decision_m4.md`
