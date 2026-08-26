# FALSACIÓN SISTEMÁTICA DEL RÉGIMEN DM-LIKE EN TCCU COSMIC ATTRACTOR v4.1

**Autor:** Jairo Omar González Navia — Quindío, Colombia, zona postal 632007
**Ejecución computacional:** AutoClaw (organismo distribuido AGI Jairo)
**Fecha:** 25-08-2026 · **Versión:** v0.3 (auditoría/reproducibilidad)
**Nivel de evidencia:** S1 (analítico) + S2 (numérico reproducible). NO es evidencia observacional.

---

## Resumen

La hipótesis Cosmic Attractor DM-like queda **falsada dentro del espacio de
modelos y condiciones iniciales explorado**. **850 configuraciones evaluadas
bajo el conjunto de protocolos M3b–M6-IC** (criterio F2 invariante: |w|<0.05 y
|dlnρ_Φ/dln a+3|<0.05 durante ΔN≥4 en la era de materia) produjeron **0 con F2
sostenido** (within the explored model and initial-condition domain). El
análisis de la dinámica transitoria muestra que la trayectoria **alcanza** la
región dust-like (w=0.0084; distancia a la curva de polvo 0.017) pero **no
permanece** (residencia máxima ΔN=0.04; |dw/dN|≈1 por e-folding).

> **The failure is not an inability to reach the dust-like manifold, but the
> absence of dynamical trapping on it.**

$$
\boxed{\text{alcanzabilidad} \neq \text{estabilidad} \neq \text{atracción}}
$$

## 1. Marco y protocolo (resumen de v0.2)

- Acción S = ∫d⁴x√−g[M_P²/2 F(Φ)R + X + X²/Λ⁴ − V(Φ)]; parámetros bloqueados
  ξ=0, λ=5, Λ=0.15, V₀=1 (`PARAMETERS_LOCKED.json`).
- Condición de polvo: w=0 ⟺ V = X + X²/Λ⁴ (ρ_Φ = 2X + 4X²/Λ⁴).
- F2 invariante; regla de no-ajuste; jerarquía M1–M6 (detalle en
  `theory/protocolo_falsacion.md`).

## 2. Resultados

| Fase | Dominio | Configs | F2 sostenido |
|---|---|---|---|
| M3b | exponencial | 442 | 0 |
| M3c | inverso-potencia | 168 | 0 |
| M4 | ξ≠0 | 108 | 0 |
| M3d | meseta/doble-exp | 24 | 0 |
| M6-IC | condiciones iniciales | 72 | 0 |
| α×IC | rincón α>2 × ICs | 36 | 0 |
| **Total** | | **850** | **0** |

- 55/72 = 76.4% alcanzan w≈0 transitoriamente; ΔN_max = 0.04 (factor 100 <
  requisito 4); w_best = 0.0084; d = 0.017; |dw/dN| ≈ 1 (Fig. 1).
- **Figura 1** (`figures/figura_q2.png`): A) w(N) transitorias · B) residencia
  ΔN_F2 (max 0.04 vs 4.0) · C) diagrama de fase con la curva de polvo ·
  D) |dw/dN| en los cruces.

## 3. Reproducibilidad computacional

Fichas por campaña con RUN_ID **reales** (SHA-256 de script + parámetros +
versiones + resumen del resultado), en `reproducibility/`:

| Campaña | RUN_ID | Configs | F2 | SHA-256(resultado) |
|---|---|---|---|---|
| M3B | `5196de8f11efca10` | 442 | 0 | ver `reproducibility/hashes.sha256` |
| M3C | `fb7e294f73f6107e` | 168 | 0 | ídem |
| M3D | `ba0c262fb67ec629` | 24 | 0 | ídem |
| M4 | `ab519556e8cdf363` | 108 | 0 | ídem |
| M6IC | `53d2b1ddc51f6bfb` | 72 | 0 | ídem |
| ALPHAIC | `7e53c9915d4a69bf` | 36 | 0 | ídem |

Entorno: Python {python}, numpy {numpy}, scipy {scipy}, matplotlib
{matplotlib}; solver scipy solve_ivp (RK45, dense output); sin RNG (barridos
deterministas); semilla n/a. Archivos: `reproducibility/RUNS.md`,
`environment.yml`, `requirements-lock.txt`, `<CAMPANA>/{RUN_ID.txt,
parameters.json, result.json}`.

## 4. Qué queda falsado / qué queda abierto

| Hipótesis | Estado |
|---|---|
| Exponencial TCCU DM-like | ❌ Falsada en dominio explorado |
| Inverso-potencia TCCU DM-like | ❌ Falsada en dominio explorado |
| Meseta/doble-exp TCCU | ❌ Falsada en dominio explorado |
| Rama ξ≠0 explorada | ❌ Falsada en dominio explorado |
| IC fuera de la cuenca | ❌ No resuelve F2 |
| k-essence en general | 🟡 No falsada |
| Tracking k-essence en general | 🟡 No falsado |
| P(X) puramente cinético | 🟡 No estudiado |
| Otras acciones TCCU | 🟡 Abiertas |
| M7 (P(X,Φ)→P(X)) | 🔒 Congelado |

## 5. Discusión (comparación con la literatura)

- Steinhardt–Wang–Zlatev (1999): condiciones tracker en quintessence —
  contraste teórico, no evidencia a favor de TCCU.
- Chiba (2002): tracking k-essence — el tracking existe en k-essence; la
  estructura específica investigada no lo produce.
- Scherrer (2004): k-essence puramente cinético P=P(X) puede dar
  ρ(a)=ρ₀+ρ₁a⁻³ — la dependencia explícita en Φ (potencial) es la diferencia
  estructural que motiva M7 (congelado).
- Uzan (1999, PRD 59, 123510): soluciones de escala para campos no
  mínimamente acoplados con exponenciales e inverso-potencia — la ausencia de
  F2 en M4 no es una imposibilidad general; es específica de la acción,
  parametrización y dominio explorados.
- Modelos unificados k-inflación+DM+DE (PRD 80, 103508): nuestro resultado es
  una restricción sobre esta estructura concreta, no sobre todo el espacio
  k-essence.

## 6. Conclusiones

1. La hipótesis Cosmic Attractor DM-like queda falsada dentro del espacio de
   modelos y condiciones iniciales explorado (850 configuraciones, 0 F2).
2. La estructura k-essence específica investigada no produjo tracking DM-like
   sostenido (no: "k-essence no puede hacer tracking").
3. Alcanzabilidad (76.4%) ≠ permanencia (ΔN_max 0.04): ausencia de
   atrapamiento dinámico, no de acceso.
4. Resultado negativo auditable: RUN_IDs, hashes, entorno y protocolo
   reproducibles.
5. M7 permanece congelado hasta completar el depósito.

## 7. Referencias

1. Steinhardt, Wang & Zlatev (1999). PRD 59, 123504.
2. Zlatev, Wang & Steinhardt (1999). PRL 82, 896.
3. Zlatev & Steinhardt (1999). Phys. Lett. B 459, 570.
4. Chiba (2002). PRD 66, 063514.
5. Scherrer (2004). PRL 93, 011301.
6. Uzan (1999). PRD 59, 123510 (soluciones de escala no mínimamente acopladas).
7. (2000). Tracking Extended Quintessence. PRD 62, 123510.
8. (2009). Unified model of k-inflation, dark matter and dark energy. PRD 80, 103508.
9. Garriga & Mukhanov (1999). Phys. Lett. B 458, 219.
10. Armendáriz-Picón, Mukhanov & Steinhardt (2001). PRD 63, 103510.
11. De Felice & Tsujikawa (2010). Living Rev. Rel. 13, 3.
12. Planck Collaboration (2020). A&A 641, A6.
13. González Navia (2026). TCCU Cosmic Attractor v4.1 (+ trun.txt §§23–65).

---

**Autores:** Jairo Omar González Navia (conceptual) · AutoClaw (ejecución
computacional, verificación, auditoría). Quindío, Colombia — zona postal
632007. 25 de agosto de 2026.
