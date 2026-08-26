# Falsación Sistemática del Atractor Cósmico TCCU como Mecanismo de Sector Oscuro Unificado

**Subtítulo:** Un Estudio Computacional Reproducible de Tracking Tipo Polvo, Atrapamiento Dinámico y Dependencia de las Condiciones Iniciales

---

*English:*
# Systematic Falsification of the TCCU Cosmic Attractor as a Unified Dark-Sector Mechanism
**Subtitle:** A Reproducible Computational Study of Dust-Like Tracking, Dynamical Trapping and Initial-Condition Dependence

---

**Autor:** Jairo Omar González Navia — Quindío, Colombia, zona postal 632007
**Ejecución computacional:** AutoClaw (organismo distribuido AGI Jairo)
**Fecha:** 25-08-2026 · **Versión:** v1.0 (paquete de depósito)
**Nivel de evidencia:** S1 (analítico) + S2 (numérico reproducible)

> ## Declaración de alcance
>
> **El presente trabajo constituye una falsación dentro de un espacio de
> modelos computacionalmente explorado, no una falsación observacional de
> TCCU.**
>
> *This is a model-space falsification, not an observational falsification.*

---

## Resumen

Presentamos un estudio computacional sistemático de falsación del Atractor
Cósmico TCCU, una hipótesis escalar k-essence propuesta para generar un sector
oscuro efectivo unificado. El modelo se sometió a un criterio tipo polvo
predefinido que exige simultáneamente |w_Φ|<0.05, dilución tipo materia y un
tiempo mínimo de residencia de cuatro e-foldings. Seis campañas computacionales
exploraron configuraciones exponenciales, inverso-potencia,
meseta/doble-exponencial, no mínimamente acopladas y de condiciones iniciales
variadas. **En 850 configuraciones evaluadas, ninguna trayectoria satisfizo el
criterio F2 sostenido dentro del dominio de modelos y condiciones iniciales
explorado.** En la campaña de condiciones iniciales, 55 de 72 trayectorias
atravesaron transitoriamente la región tipo polvo, pero el tiempo máximo de
residencia fue de solo 0.04 e-foldings, **cien veces más corto** que el
intervalo requerido. La trayectoria más cercana alcanzó w_Φ = 0.0084, mientras
que el flujo transversal medido cerca del cruce fue |dw_Φ/dN| ≈ 1. Estos
resultados indican que el principal obstáculo **no es la accesibilidad del
régimen tipo polvo, sino la ausencia de atrapamiento dinámico sobre él**. El
estudio no falsa al k-essence, a la materia oscura escalar ni a TCCU en
general; falsa el mecanismo DM-like del Atractor Cósmico dentro del dominio de
modelos y condiciones iniciales explícitamente explorado. Todas las
ejecuciones, parámetros, entornos de software, hashes y salidas numéricas
quedan archivados para reproducibilidad.

*Abstract (English):* We present a systematic computational falsification study
of the TCCU Cosmic Attractor, a scalar k-essence hypothesis proposed to
generate an effective unified dark sector. The model was tested under a
predefined dust-like criterion requiring simultaneously |w_Φ|<0.05, matter-like
dilution, and a minimum residence time of four e-foldings. Six computational
campaigns explored exponential, inverse-power, plateau/double-exponential,
non-minimally coupled, and varied-initial-condition configurations. Across 850
evaluated configurations, no trajectory satisfied the sustained F2 criterion
within the explored model and initial-condition domain. In the initial-condition
campaign, 55 of 72 trajectories crossed the dust-like region transiently, but
the maximum residence time was only 0.04 e-foldings, one hundred times shorter
than the required interval. The closest trajectory reached w_Φ=0.0084, while
the measured transverse flow near the crossing was approximately |dw_Φ/dN|≃1.
These results indicate that the principal obstruction is not accessibility of
the dust-like regime, but its lack of dynamical trapping. The study does not
falsify k-essence, scalar-field dark matter, or TCCU in general; it falsifies
the Cosmic Attractor DM-like mechanism within the explicitly explored model and
initial-condition domain. All runs, parameters, software environments, hashes
and numerical outputs are archived for reproducibility.

---

## Resultado central

$$
\boxed{
\begin{array}{rcl}
M3B&:&442\rightarrow0\\
M3C&:&168\rightarrow0\\
M3D&:&24\rightarrow0\\
M4&:&108\rightarrow0\\
M6IC&:&72\rightarrow0\\
ALPHAIC&:&36\rightarrow0
\end{array}}
\qquad
\boxed{\mathbf{850\ configuraciones\ evaluadas,\quad 0\ F2\ sostenido}}
$$

$$
\boxed{\text{alcanzabilidad} \neq \text{estabilidad} \neq \text{atracción}}
$$

## Secciones completas

Marco, protocolo M1–M6, resultados, reproducibilidad (RUN_IDs y hashes),
discusión con la literatura (Steinhardt–Wang–Zlatev, Chiba, Scherrer, Uzan,
extended quintessence, modelos unificados), conclusiones y referencias:
ver `manuscript/borrador_falsacion_v03.md` (versión de auditoría v0.3, idéntica
en contenido científico) y `reproducibility/RUNS.md`.

## Paquete de depósito

```
TCCU-Cosmic-Attractor-Falsification-v1.0/
├── README.md
├── LICENSE
├── CITATION.cff
├── paper/          manuscrito v1.0 (este archivo)
├── manuscript/     borrador_falsacion_v03.md (auditoría)
├── reproducibility/ RUN_IDs, entorno, hashes, RUNS.md
├── validation/     informes de falsación por campaña
├── data/           barrido_*.json (resultados completos)
└── figures/        figura_q2.png
```

---

**Autores:** Jairo Omar González Navia (conceptual, teoría TCCU, protocolo) ·
AutoClaw (ejecución computacional, verificación numérica, auditoría).
Quindío, Colombia — zona postal 632007. 25 de agosto de 2026.
