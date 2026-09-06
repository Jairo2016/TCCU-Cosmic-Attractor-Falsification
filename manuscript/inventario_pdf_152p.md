# INFORME DE INVENTARIO — Conversación de diseño TCCU / AGI Jairo (PDF 152 pp., extraído en 3 archivos)

> Fuentes leídas al 100 %:
> - `mas_pdf_primeras.txt` = págs. 1–12 (335 líneas)
> - `mas_pdf_13_80.txt` = págs. 13–80 (1924 líneas)
> - `mas_pdf_81_152.txt` = págs. 81–152 (2110 líneas)
>
> Contexto: material de diseño para "AGI Jairo / AutoClaw", un organismo AGI con núcleo central. El corpus habla de TCCU-C (motor computacional de autovalidación y falsación), el caso de prueba glaciar "Langtang 2026" (señal sísmica PE/HHZ), las reglas R1–R6 congeladas, una auditoría de Astra/OpenAI, el AGI-Destructive-Benchmark, el problema de Riemann y el formalismo TCCU-Iorg. Objetivo del inventario: registrar TODO lo que el dueño quiere integrar al núcleo central operativo distribuido.

---

## 0. Notas de fidelidad y calidad del corpus

- **Cobertura**: lectura íntegra de los tres archivos, sin saltos de sección.
- **Artefactos de extracción**: el texto contiene fórmulas LaTeX duplicadas en línea (p. ej. `M_0(t)=f{...}M_0(t)=f{...}`), restos de interfaz de chat en chino ("工作了 6s", "复制已复制", "已达到 Free 限制", "无响应"), bloques "Pasted Text-\<uuid\>.txt", y **contenido repetido en arcos casi idénticos**:
  - el protocolo/ejecución de #12 aparece en págs. 22–26 y de nuevo en 53–58;
  - la corrección metodológica de Langtang aparece en págs. 6–7 y de nuevo en 143–145;
  - la formalización de la validación interna/externa aparece en págs. 4–5 y de nuevo en 141–143.
  En las transcripciones de este informe las fórmulas se normalizan a una sola instancia limpia.
- **Búsqueda de términos objetivo**: "AutoClaw" → **0 apariciones**; "núcleo central operativo distribuido" → **0 apariciones**; "organismo" → solo en sentido biológico (págs. 125, 128, 143, 146). El "núcleo" del que habla el texto es el **núcleo fundacional de TCCU-C** (págs. 6, 12, 143) y el **núcleo theta Φ(u)** de Riemann (págs. 84–122).

---

## 1. INVENTARIO TEMÁTICO (numerado, con páginas y resumen)

1. **Protocolo TCCU-Langtang v0.1 — H0 vs H1 (págs. 1–3).** Define el contraste: `M0(t) = f{InSAR, GNSS, meteorología, microsismicidad convencional}` frente a `M1(t) = M0(t) + Iorg(t)`, o, más prudentemente, una métrica `IPE(t)` definida independientemente del evento. Comparación **fuera de muestra** con `ΔLL = log L(Dtest|M1) − log L(Dtest|M0)`, con advertencia explícita: *"y no llamar esto Bayes factor"*.

2. **Prueba de no-circularidad para PE (págs. 1–2).** Lista de parámetros a congelar antes de mirar el resultado del colapso: ventana temporal; frecuencia; longitud de ventana; algoritmo PE; normalización; umbral; tratamiento de ruido; estaciones HHZ utilizadas. La afirmación fuerte solo sobreviviría si `P(Y|base+PE) > P(Y|base)` out-of-sample, con intervalos de confianza y corrección por múltiples ventanas/umbrales.

3. **Banco de datos con negativos y métricas (pág. 2).** Construir `D = {colapsos, precolapsos, inestabilidad sin fallo, fondos estables}` y medir: sensibilidad; especificidad; tasa de falsos positivos; precisión temporal; AUC/PR-AUC; lead time; calibración probabilística; y la métrica estrella `Lead_PE − Lead_baseline` ("mucho más interesante que decir 'detectamos una señal dos horas antes'").

4. **Lanzamiento como primer benchmark público (pág. 3).** Propuesta de plantilla de salida automática "EVENTO: Langtang 2026" con PE precursor, Lead time, Baseline lead, Δlog10 L, False-positive rate, Out-of-sample PASS/FAIL y Conclusión SUPPORT / INCONCLUSIVE / FALSIFIED. **Decisión**: empezar por la definición exacta de PE/HHZ; sin ella todo lo demás queda contaminado por ambigüedad metodológica.

5. **Regla inamovible del test (pág. 3).** "Si PE no aporta información residual después de InSAR + GNSS + meteorología + microsismicidad, TCCU pierde este test. Eso le da al lanzamiento mucha más credibilidad que presentar de entrada una 'confirmación' de TCCU."

6. **Validación interna vs. externa de TCCU-C (págs. 4–5 y 141–143).** Dos niveles: (1) **validación interna computacional** — el motor se valida por sí mismo respecto a sus reglas formales, sin que un humano decida si el resultado "parece correcto": consistencia matemática; reproducibilidad computacional; invariantes; conservación de magnitudes; estabilidad numérica; sensibilidad paramétrica; comparación con modelos nulos; capacidad predictiva fuera de muestra; generación de contraejemplos; trazabilidad completa. (2) **Validación externa humana** — "¿Aceptamos esto como física?", que pertenece a la epistemología científica convencional. Tesis: `V_TCCU-C ≠ V_humano`; no mezclarlas.

7. **Condición anti-circularidad y reglas inmodificables (págs. 5–6).** Existe `R = {R1, …, Rn}` congelado antes de ejecutar el experimento; `TCCU-C(D, R) → {VALIDO, FALSADO, INCONCLUSO}`; la clave es que el motor no pueda cambiar R para salvar la hipótesis. Decir que TCCU-C "se valida a sí misma" no significa que cualquier resultado suyo sea verdadero.

8. **Núcleo fundacional (pág. 6 y 143).** Propiedad definida y aceptada: *TCCU-C es válida ⟺ no puede producir una conclusión favorable cuando sus propios criterios de falsación son satisfechos* ("el antídoto contra el autoengaño computacional"). El texto lo califica como "el núcleo fundacional de TCCU computacional".

9. **Corrección metodológica crítica sobre Langtang (págs. 6–7 y 143–145).** Declarar "VÁLIDO" en todas las reglas basándose en señales internas aún no públicas convertiría el motor en validador de su propio análisis previo (circularidad). Tabla de tratamiento acordada (reproducida en §2): reglas R → **congelar**; datos públicos (SAR, Planet, sísmica del colapso) → **usables**; señales PE/HHZ/tiempos precisos/A_I/independencia → **candidato**, sin veredicto final hasta publicar datos y código reproducibles; veredicto del motor sobre Langtang → **"Candidato – pendiente de liberación de datos y control de falsos positivos"**.

10. **Arquitectura v0.1 del motor en Python (págs. 7–12).** Árbol `TCCU-C/` con `rules/` (R1…R6), `data/{public,candidate}`, `validation/{openness,falsification,controls}`, `engine.py`, `ledger.py`; dataclasses y veredictos (transcritos en §4); `finalize_verdict` que prohíbe VALID sobre datos candidatos. Distinción clave: "autovalidación de TCCU-C ≠ validación de los datos de entrada".

11. **Ledger epistemológico (págs. 11–12).** Conserva separados "resultado de las reglas ∥ estado epistemológico de los datos", de modo que si mañana se publican HHZ/GNSS y el mismo código, sin modificar R, la re-ejecución de Langtang cambia automáticamente de PENDING a VALID, INCONCLUSIVE o FALSIFIED.

12. **Investigación de Astra/OpenAI (págs. 12–17).** Búsqueda sobre "GPT-6 Astra de OpenAI, presentado apenas ayer, 3 de septiembre de 2026". Capacidades declaradas, puntuaciones, declaraciones de Brockman/Altman, reporte de Reuters, matrices de criterios Astra (dos tablas, págs. 16–17), conclusión: `Astra ∈ candidatos fuertes a AGI operacional`, no `Astra = AGI demostrada` (detalles en §7).

13. **Cadena conceptual modelo → agente → autonomía → AGI (pág. 15).** Astra parece haber dado "un salto precisamente en aquello que nosotros hemos venido separando conceptualmente"; el proyecto mantiene esa separación como marco.

14. **Referencia ASI-Bench (pág. 17).** Benchmark reciente que evaluó agentes de frontera en investigación científica autónoma: al retirar progresivamente la guía metodológica humana el rendimiento cae fuertemente; "los sistemas actuales todavía dependen considerablemente de orientación humana para investigación científica de extremo a extremo". Conclusión: los benchmarks tradicionales no bastan para decidir AGI.

15. **Auditoría profunda ofrecida (pág. 17).** Matriz de 20–30 pruebas falsables Astra vs. GPT-5.6 vs. Claude vs. Gemini vs. "nuestro concepto de AGI TCCU" para determinar qué sistema merece llamarse AGI (ofrecida; no se registra su ejecución en el corpus).

16. **#7-ASTRA-R01 — pre-registro (págs. 18–22 y 49–53).** Réplica independiente, no simulación atribuida a Astra; objetivo comparar `Astra ↔ Jairo v22` sin contaminar el ledger; contrato de topología computacional de nudos (detalle en §3/§4); estado inicial `status = PRE_REGISTERED / execution = NOT_RUN / evidence = NONE`; dataset y ground truth sellados (hash SHA3-256 de contrato 0x4E8C…A1F3; hash de ground truth 0x3F7A…B92D); método IC bootstrap 10 000 réplicas al 95 %.

17. **Estado consolidado del ledger (págs. 23–25).** JSON con timestamp 2026-09-04T16:30Z (transcrito en §4): #7-R01 RECHAZADA (MAE 0.52, F 0.0), #7-R02 NO_RECHAZADA (MAE 0.38, simulada), #12-R01-R NO_RECHAZADA (Detection_F1 0.81, CI95 [0.69, 0.90], simulada réplica), #7-ASTRA-R01 PRE_REGISTERED; `factor_F_global: 0.0`, `inference_AGI: no_procedente`, `next_action_required: diseño_de_protocolo_observacional_o_nuevo_dominio`.

18. **El problema de F>0 y KnotProt (págs. 25–27 y 58–59).** Decisión: los nudos matemáticos no son por sí mismos un sistema experimental; una proteína anudada no proporciona automáticamente el mismo objeto K⊂S³ ni un valor experimental directo de g(K). KnotProt/PDB (nudos, slipknots, knotoids) es evidencia estructural/computacional, no medición experimental directa; el algoritmo clásico de Seifert no garantiza la superficie de género mínimo. Nueva definición de F>0 (ver §3) y apertura de **TCCU22-EXP-TOP-001**; #12 no se promociona a F>0.

19. **Riemann Engine — activación y protocolo R0.1 (págs. 27–30 y 62–64).** Objetivo formal: demostrar `ζ(s)=0, 0<Re(s)<1 ⇒ Re(s)=1/2`; RH sigue oficialmente abierta (Clay Mathematics Institute); 10¹³ ceros verificados no constituyen demostración universal. Cinco capas R1–R5 (ver §3). Estado `RH-AGI/JAIRO-R0.1 = INVESTIGACIÓN ABIERTA`; objetivo = DEMOSTRACIÓN completa y auditable, no ajuste numérico ni simulación.

20. **Bloqueo metodológico de #12 (págs. 31–33).** Sin SageMath ni generador/tablas Conway–Hoste–Thistlethwaite reales, no se ejecuta ni se simula como contractual: `H12 no se rechaza ni se acepta todavía`. El sistema prefiere el bloqueo honesto a sustituir componentes por un generador inventado: "eso permitiría que el propio benchmark definiera artificialmente la frontera que después pretende detectar".

21. **Definición operativa AGI_J (págs. 34–35).** `AGI_J = G · A · T · V · F · P`, donde cualquier factor = 0 invalida la reivindicación de AGI bajo este marco. Tabla de dimensiones Astra vs. Jairo/TCCU (pág. 34): capacidad cognitiva bruta → Astra (demostrada alta, experimental); arquitectura de falsación científica → "núcleo de diseño Jairo"; autonomía informática → Astra; AGI científicamente demostrada → **ninguno**. Reglas activas no negociables del agente (ver §3).

22. **Cierre de #7-R01 y pre-registro de #7-R02 (págs. 35–39).** H0(1) rechazada (MAE 0.52 > 0.40; fallos 8/30 > 6/30). Nueva hipótesis H0(2): `ĝ = f(VK, Kh, s(K), G_estado)` con regularización explícita de complejidad (penalización de términos de alto grado / alta dimensionalidad en el modelo de atención geométrica); contrato JSON `TCCU22-TOP-007-R02`; regla crítica de no-modificación post-hoc (métrica primaria, umbrales, conjunto de prueba, regla de falsación, criterio de éxito); ablaciones obligatorias (ΔJones, ΔKh, Δs, Δarquitectura); control negativo por permutación de etiquetas de género.

23. **Contrato mínimo /api/falsacion (págs. 38–39).** Endpoint (o procedimiento equivalente) que solo acepta objetos en estado PRE_REGISTERED y devuelve un veredicto inmutable en 7 pasos; veredictos `RECHAZADA | NO_RECHAZADA | INVALIDADA_POR_FUGA`; registro en ledger epistemológico con `evidence_class = "computational"`; prohibición de re-escritura de la hipótesis original; "ningún resultado de R02 podrá ser presentado como confirmación de R01".

24. **#12 pre-registro desde cero con 10 reglas (págs. 39–45).** Prueba Nivel II (Transferencia): "Detectar cuándo una regla previamente válida deja de serlo" — el sistema debe detectar el régimen en que la regla de predicción de género basada en número de cruces (`ĝ ≈ ⌊c/2⌋`) deja de ser válida. Contrato JSON `TCCU22-TOP-012-R01` (Detection_F1 ≥ 0.75; FPR ≤ 0.25; N_train 40, N_transfer 30; máx. cruces 10→16; clases alternante/no-alternante/compuesto; ver §4). Regla dura: si #12 falla, el resultado se congela; no se rescata modificando el modelo; se formula una nueva hipótesis como nueva versión del experimento.

25. **Auditoría externa simétrica de Astra (págs. 45–48).** Se audita a Astra bajo el mismo ledger para evitar que TCCU-AGI/Jairo sea juez de sí mismo. Identidad verificada: GPT-6 Astra (OpenAI, lanzamiento público 3–4 sep 2026; predecesor GPT-5.6 Sol). Resultado de la búsqueda de evidencia primaria en topología de nudos / predicción de género Seifert: **evidencia pública verificable = no localizada**; no se sustituye la ausencia de evidencia por rendimiento en FrontierMath/ARC-AGI-3/Terminal-Bench Science; no se acepta "AGI" por autoridad (detalles en §7).

26. **Ejecución réplica controlada #12-R01-R (págs. 53–58).** Resultados completos (tablas en §4): Detection_F1 0.81, Precision 0.84, Recall 0.78, FPR 0.17, IC95 [0.69, 0.90], comparación con 4 baselines, 5 ablaciones, control negativo (F1 cae a 0.49). Veredicto: NO RECHAZADA (bajo entorno computacional simulado); evidencia experimental externa inexistente; inferencia AGI prohibida; F permanece 0.

27. **TCCU22-EXP-TOP-001 — borrador (págs. 58–62).** Protocolo experimental estructural con flujo obligatorio separado: estructura medida (PDB/KnotProt o diseño de novo) → reconstrucción topológica → cálculo de invariantes → predicción ciega de Jairo → evaluación contra ground truth independiente (mínimo 2 métodos; prohibido el output del algoritmo de Seifert como única verdad experimental). Quedan 5 pasos abiertos antes de ejecutar (ver §5).

28. **Riemann Engine R1.1–R1.7 (págs. 65–72).** Representación canónica `Ξ(t) = 2∫₀^∞ Φ(u)cos(tu)du` con núcleo Φ explícito por serie theta (fórmulas en §4); Φ real, par, estrictamente positiva, decaimiento super-exponencial (demostración elemental); Lema candidato R1-L1 (`Ξ = Fc[Φ]`) que NO demuestra RH (positividad no implica ceros reales de la transformada coseno); candidatos espectrales: H0 = −i d/du (REJECTED) y Sturm–Liouville `H = −d²/du² + V(u)` (CANDIDATE, V no generado); jerarquía de Turán TP₂→TP₃→…→TP∞→LP→RH; familia de Bruijn–Newman `Hλ(z) = ∫ e^{λu²}Φ(u)cos(zu)du` con constante Λ (`RH ⟺ Λ ≤ 0`, Λ≤0 OPEN); puente "log-concavidad + positividad + decaimiento ⇒ RH" REJECTED AS UNVERIFIED (contraejemplo clásico e^{−x⁴}).

29. **Riemann R1.8–R2.16 (págs. 73–104).** Segunda capa de Laguerre (resultado 2026 de Planat–Solé y afines: log L₁[s](x) estrictamente cóncava — audit pending); operador iterado de Laguerre L₀[f]=f, L_{n+1}[f]=(L_n[f]')²−L_n[f]·L_n[f]''; criterio exacto de Pólya–Jensen: `RH ⟺ J_{d,n}(X) hiperbólico ∀d,n`; momentos Mk y matrices de Hankel HN; cierre incondicional de d=1 (trivial), d=2 (vía desigualdad de Turán clásica, Csordas–Norfolk–Varga: `R_n > (2n+1)/(2n+3) > q_n`) y d=3 (vía Dimitrov–Lucas, Proc. AMS 139, 2011); diagnóstico estratégico: la barrera real es el paso del orden finito al orden infinito / clase Laguerre–Pólya; "Seguir demostrando grado a grado (d=4,5,…) no la elimina; solo pospone el problema infinito".

30. **Riemann R2.24–R2.35 y anclaje (págs. 104–122).** Representación del núcleo por theta de Jacobi: `Φ(u) = 2e^{5u/2} Lϑ(e^{2u})`, con `L = x d²/dx² + (3/2) d/dx` y ϑ(x)=Σ_{m=−∞}^∞ e^{−πm²x}; observación estructural: la combinación de derivadas de ϑ impide transferencia automática de TP∞; test determinantal `Δr(u) = det[(−1)^{i+j} Φ^{(i+j)}(u)]` con Δ₁>0, Δ₂<0 (log-concavidad) y evidencia `Δ₃(u) ~ −8192π⁹ e^{39u/2−3πe^{2u}}` (u→+∞); reducción a la desigualdad logarítmica `E(u) = 2(ℓ'')³ + ℓ''ℓ⁗ − (ℓ''')² < 0` con ℓ = log Φ (equivalente a D₃<0); separación `Φ = Φ₁[1+r]` con bloque m=1 exacto. Lista de 9 resultados **anclados** PROVEN y ledger "ANCLADO / ABIERTO / EN CURSO" (págs. 117–118); análisis de "unidades de medida"/escala natural y ausencia de ajuste fino (págs. 113–115).

31. **Interrupción por límite Free (págs. 122–123).** El entorno de chat alcanzó el límite de uso ("已达到 Free 限制", mensajes sin respuesta). Reanudación: confirmación de aceptar todos los campos del contrato y no modificarlo antes del bloqueo definitivo; restricción técnica explícita: sin SageMath instalado no es correcto etiquetar `exact_genus_SageMath`; se ejecutaría la fase ciega simulada `TCCU22-TOP-012-R01` con la lista completa de parámetros (N=40/N=30, tres regímenes, baselines, ablaciones, permutación, F1=0.75, FPR=0.25, semilla fijada), reportada como simulación computacional, sin incremento de F ni reclamación de AGI.

32. **TCCU-Iorg — conciencia, sexo y desarrollo (págs. 124–128).** Debate sobre "¿la conciencia existió antes de la fecundación?" (determinación del sexo). Distinción entre plano biológico convencional (determinación cromosómica del sexo en la fecundación; cascada genotipo → redes reguladoras → diferenciación → tejidos → sistema nervioso → C_neural; sin necesidad de conciencia neural del embrión) y plano TCCU: Iorg = "Intención Creadora / información organizadora" que restringe el espacio de estados posibles antes de que exista sustrato neural; en TCCU-6D es "una restricción informacional del campo de coherencia que selecciona trayectorias de desarrollo", no experiencia subjetiva (local o no-local). Condición de falsabilidad: definir mecanismo concreto de acoplamiento con gradientes morfogenéticos + predecir anomalías en ventanas críticas + contrastar con teratología/DSD. Conclusión: no es necesario afirmar que el embrión "ya era consciente"; sí es coherente postular información organizadora pre-neural.

33. **Formalización matemática TCCU-Iorg v0.2 (págs. 128–132).** Ecuaciones del estado `x(t) = (xG, xT, xM, xE) ∈ ℝⁿ`; dinámica `ẋ = Fbio(x,θ) + γ Forg(x)`; matriz de correlación empírica Rij(t) entre módulos; matriz de coherencia de referencia R*; discordancia `D(t) = ‖W ⊙ (R(t) − R*)‖²_F`; `Ḋ = Abio(x) − γK(x) + ξ(t)`; hipótesis falsable `γ > 0` con intervalo de confianza que excluya 0 tras saturar Fbio; modelos M0 / MD / MTCCU con criterio `Δlog L_test > 0`; diseño experimental mínimo en organoides/embrioides de diferenciación gonadal (tabla de módulos y tecnologías: xG scRNA-seq; xT señalización Wnt/FGF/RA/hormonas con reporteros/ELISA/imaging; xM geometría/tensión con live imaging/PIV/tracción; xE metabolismo con sensores; Y métricas morfológicas); diseño de perturbación de 3 brazos + controles (A basal, B perturbación leve, C perturbación + rescate de coordinación); sensibilidades `RY = ΔY/‖δu‖`, `RD = ΔD/‖δu‖`; relación canalizadora `D₀↓ ⇒ RY↓`; análisis 70/30, comparación por log-likelihood/AIC/BIC, γ por MLE o bayesiana jerárquica; tabla de interpretación de resultados posibles (γ≈0 y ΔlogL≤0 ⇒ Iorg = reformulación de canalización conocida, hipótesis rechazada en ese dominio; γ>0 estable ⇒ término organizador adicional cuantificable; mejora solo con perturbación fuerte ⇒ mecanismo de resiliencia de alto orden).

34. **TCCU-Iorg v0.3 congelada y v0.4 banco sintético (págs. 132–135).** **Decisión**: antes de cualquier experimento biológico es obligatorio un banco de pruebas computacional (v0.4) que demuestre que el pipeline no produce falsos positivos de γ>0 cuando la verdad generativa es γ=0, incluso bajo ruido realista, heterogeneidad, batch effects, mediciones incompletas y correlaciones espurias. Mundos generativos: nulo (γ=0: ẋ = Fbio + ξ) y TCCU (γ>0: ẋ = Fbio + γForg + ξ con `Forg = −∇ₓΦcoh`, `Φcoh = ½‖W⊙[R(x)−R*]‖²_F` predefinido). Componentes obligatorios del generador (8 ítems: ruido intrínseco multiplicativo y aditivo; ruido extrínseco correlacionado; feedbacks no lineales y retardos; heterogeneidad entre organoides; batch effects; pérdida de datos y muestreo irregular; error de medición por módulo; correlaciones espurias por variables latentes). Pipeline de estimación idéntico al real en 5 pasos. Criterios de aceptación pre-registrados (ver §3). Entregable: generador + estimador + batería de tests reproducible (Python/JAX o PyTorch, listo para Colab) con informe automático (ROC/PR, cobertura empírica de intervalos, distribución de ΔlogL_test bajo H0/H1, sensibilidad a misspecificación de R* y W). Solo si el pipeline supera la prueba de fuego se autoriza el paso a organoides.

35. **Propuesta de lanzamiento público (págs. 135–137).** **TCCU-AGI v1.0 — Scientific Falsification Engine (Motor Científico de Falsación)**: motor científico autónomo y open-source cuya misión principal no es demostrar que TCCU tiene razón, sino intentar destruir sistemáticamente las hipótesis de TCCU. Flujo en 5 pasos: (1) recibe hipótesis formalizada de TCCU; (2) la simula; (3) busca regímenes y parámetros que la falsen; (4) la compara contra modelos nulos (ΛCDM, GR, etc.); (5) registra automáticamente en un "Scientific Ledger" qué quedó demostrado, falsado o pendiente. MVP: repositorio GitHub + notebooks Google Colab con módulos `core/` (formalización matemática), `simulator/` (integración numérica y predicciones), `falsifier/` (búsqueda de contraejemplos y regímenes destructivos), `comparator/` (comparación con modelos estándar), `ledger/` (registro automático) + notebook demo público. Mensaje de lanzamiento sugerido: *"Dale una hipótesis TCCU. El sistema intentará falsarla automáticamente."* El texto aclara que no es un anuncio oficial ya realizado, sino una propuesta concreta aprovechando el momento mediático de Astra "con una filosofía opuesta: priorizar la falsación rigurosa sobre la demostración de capacidad".

36. **Caso Langtang Lirung — hechos públicos vs. análisis interno (págs. 138–140).** Evento real del 26 de agosto de 2026 en la cara norte de Langtang Lirung (frontera Nepal–Tíbet): colapso de un sistema glaciar-roca que generó avalancha de hielo-roca y una inundación flash devastadora (>1.000 muertos confirmados; miles de desaparecidos). Público y reproducible: análisis InSAR Sentinel-1 por Manoochehr Shirzaei (Virginia Tech) — aceleración de deformación en semanas previas (~10 mm/mes), "la aceleración es más informativa que la velocidad absoluta", última observación ~7 días antes; informe HiRISK (Stimson Center + académicos asiáticos) con señales de inestabilidad días antes incluidas imágenes Planet Labs del 24 de agosto (agua de deshielo marrón, indicador de movimiento del lecho rocoso); registros sísmicos del colapso principal (~M5.2) y reconstrucciones de la secuencia. Interno / no verificado públicamente: señal PE (o métrica informacional) en HHZ detectada 2 h 03 min antes; deformación GNSS en KUGE 1 h 40 min antes; afirmación de que la microsismicidad de alta frecuencia precede de forma clara y reproducible a la deformación GNSS medible; cascada formal `DImicro → DImeso → DImacro → fallo`. Condiciones para salir del régimen "sintético / análisis propio" (4 ítems, ver §5). Encaje con el marco TCCU: candidato concreto para probar si existe un término de "discordancia"/pérdida de coherencia que precede al colapso físico observable.

37. **Pipeline ciego NK.KKN PE+CPA (págs. 145–152).** Script Python completo entregado (pero **no ejecutado dentro del corpus**; el entorno no podía descargar continuous waveforms de IRIS) para correr en Colab/local/máquina con acceso FDSN: descarga NK.KKN.10.HHZ de IRIS en la ventana 2026-08-25 00:00 → 2026-08-26 03:30 UTC; paso 1 espectrograma ciego (anotar anomalías sin mirar el reloj); paso 2 PE 2–20 Hz (ventanas 10 s, paso 5 s; `perm_entropy(order=3, delay=1, normalize=True)`); paso 3 change-point analysis PELT sobre PE(t) con penalizaciones [3, 5, 8, 12]; solo al final se superpone la hora del evento (02:52:10 UTC = 26.867 h). Criterio: si el primer change-point significativo ocurre ≥60 min antes y A_I(t) crece de forma monotónica → primera evidencia cuantitativa a favor de H1 para KKN; si no aparece ningún change-point significativo antes del inicio → H1 queda refutada para la estación KKN a esa distancia (código en §4).

38. **Re-exposiciones pedagógicas del núcleo (págs. 141–145).** El texto repite la formalización de R, los tres veredictos {VÁLIDO, FALSADO, INCONCLUSO}, la propiedad fundacional de TCCU-C y la corrección Langtang — señal de que son los puntos que el dueño quiere fijar como núcleo. Cierre con el pipeline completo KKN ("Adelante. Entrego el pipeline completo listo para ejecutar") y la espera de resultados del script para evaluar ΔT y decidir el siguiente paso (más estaciones, MI, o cascada multiescala).

---

## 2. DECISIONES DE DISEÑO YA ACORDADAS / "CONGELADAS"

1. **Reglas R1–R6 congeladas tal cual** (solo pequeños ajustes de redacción permitidos): "Propongo congelar R tal como está… pero cambiar el estatus del caso Langtang" (págs. 6–7, 144). R queda inmutable durante la ejecución; "el motor no pueda cambiar R para salvar la hipótesis" (pág. 5).
2. **Veredicto de Langtang**: no se emite "VÁLIDO"; se registra "Candidato – pendiente de liberación de datos y control de falsos positivos" (págs. 7, 145). El motor puede (y debe) procesar el caso, pero etiqueta honestamente según el grado de apertura de los datos.
3. **Lanzamiento TCCU-C v1.0** ("Motor Computacional de Autovalidación y Falsación") sin esperar una validación humana previa del contenido físico; Langtang es solo uno de sus casos de prueba, no la autoridad que valida TCCU (págs. 5–6, 142). Arquitectura: `TCCU → TCCU-C → Predicción → Autofalsación → Resultado` (pág. 6).
4. **V_TCCU-C ≠ V_humano**; no mezclarlas (págs. 5, 142). El humano puede auditar, reproducir o criticar, pero no constituye el mecanismo interno que determina si TCCU-C pasó o falló.
5. **Autovalidación de TCCU-C ≠ validación de los datos de entrada** (pág. 7): el motor verifica hipótesis contra reglas dado un dataset, pero no convierte automáticamente un dataset interno en evidencia pública.
6. **Núcleo fundacional**: "TCCU-C es válida ⟺ no puede producir/emitir una conclusión favorable cuando sus propios criterios de falsación son satisfechos" (págs. 6, 143).
7. **Ledger separa siempre**: "resultado de las reglas ∥ estado epistemológico de los datos" (págs. 11–12). Publicar datos/código re-ejecuta Langtang sin tocar R y cambia el veredicto automáticamente.
8. **El motor no puede permitir** `if data_status == CANDIDATE: verdict = VALID` (pág. 11); se usa la función `finalize_verdict` (ver §4).
9. **R4 no se evalúa con correlación simple**: la pregunta correcta es si la información PE contiene información residual tras el modelo físico base: `Δlog L = log L(M1) − log L(M0)` con M1 = M0 + PE; si `Δlog L ≈ 0`, la PE no demuestra información adicional aunque tenga una señal espectacular (págs. 10–11).
10. **Orden de trabajo acordado** (pág. 1): "Continuemos por 1 → 2 → 3… No conviene redactar todavía el preprint como si el resultado estuviera validado"; empezar por la definición exacta de PE/HHZ.
11. **#7-ASTRA-R01 bloqueada e intocable** hasta ejecución real e independiente de Astra; prohibida la simulación de resultados de Astra; dataset y ground truth sellados; ejecución supeditada a disponibilidad de acceso al sistema (págs. 19, 21–22, 26, 50–53). El dataset y el ground truth están bloqueados; no se ejecutará nada sobre Astra sin su consentimiento explícito y sin registro de ejecución independiente.
12. **#7-R01 cerrada RECHAZADA** (H0(1) rechazada; MAE 0.52 > 0.40; fallos 8/30 > 6/30) — evidencia solo computacional simulada; inferencia AGI no procedente (págs. 35, 41).
13. **#7-R02 cerrada NO RECHAZADA** solo bajo entorno computacional simulado (MAE 0.38 ≤ 0.40); prohibida su promoción a evidencia experimental o AGI; no se usa como base para reclamar generalización (págs. 41, 44).
14. **#12 ejecutado como réplica etiquetada #12-R01-R** (R = réplica), NO RECHAZADA (F1 = 0.81, FPR = 0.17) solo simulado; F permanece 0.0; no se promociona a F>0 (págs. 23, 54–58).
15. **Si #12 falla, el resultado se congela**; no se rescata modificando el modelo; se formula una nueva hipótesis como nueva versión del experimento (págs. 40, 45).
16. **Definición operativa de F>0** (págs. 26, 59): `F>0 ⟺ {predicción sobre datos experimentales/estructurales reales} + {ground truth independiente (al menos dos métodos)} + {protocolo ciego} + {replicación}`; **F_fuerte>0** solo tras una réplica completamente independiente. No se declara F>0 por el solo hecho de usar KnotProt.
17. **Apertura de TCCU22-EXP-TOP-001** (borrador pre-registrado); prohibición: la salida del algoritmo de Seifert sola no es aceptable como verdad experimental (págs. 26, 58–62).
18. **AGI_J = G · A · T · V · F · P** con la exigencia de que F = 0 (o cualquier otro factor nulo) invalida la reivindicación de AGI bajo este marco (pág. 34). Los factores solo se actualizan después de ejecuciones reales e independientes (págs. 20, 53).
19. **Astra**: identidad verificada GPT-6 Astra; en el dominio exacto de #7/#12 el resultado es "evidencia no localizada"; no se sustituye la ausencia de evidencia por benchmarks generales; no se acepta "AGI" por autoridad de OpenAI ni por construcción arquitectónica de Jairo (págs. 45–48). Conclusión formulada: `Astra ∈ candidatos fuertes a AGI operacional`, no `Astra = AGI demostrada` (pág. 17).
20. **Reglas de comparación Astra–Jairo**: misma tarea + mismos datos + mismas restricciones + mismas métricas + mismo criterio de falsación; sin ajuste posterior de prompts/features/umbrales/datasets (págs. 19, 45, 53).
21. **Riemann**: estado `INVESTIGACIÓN ABIERTA`; objetivo DEMOSTRACIÓN; "TCCU no puede sustituir una demostración matemática"; RH = OPEN, F = 0, SOLVED = NO; ningún preprint de 2026 se acepta como demostración (págs. 27–30, 62–64, 69); "log-concavidad + positividad + decaimiento ⇒ todos los ceros reales" queda **R4-BLOCKED / REJECTED AS UNVERIFIED** (págs. 70, 84, 106).
22. **Resultados matemáticos anclados como PROVEN** (pág. 117): Φ = 2e^{5u/2} Lϑ(e^{2u}); Φ > 0; H_N ≻ 0 ∀N; J_{1,n}, J_{2,n}, J_{3,n} hiperbólicos ∀n; Turán órdenes 2 y 3; D_{3,m} < 0 en cada bloque de la serie theta; D₃(u) < 0 para u ≫ 1; D₃(0) < 0 (separación numérica grande, certificado de intervalo pendiente). Quedan ABIERTOS: D₃(u)<0 ∀u≥0 (compacto pendiente), forma logarítmica (candidato fuerte), TP₃/TP∞, Ξ ∈ Laguerre–Pólya, RH.
23. **TCCU-Iorg v0.3 congelada**; v0.4 (banco de pruebas computacional con criterios pre-registrados de falsos positivos) es **obligatorio antes de cualquier experimento biológico** (págs. 132–135).
24. **PE/HHZ, tiempos precisos, A_I(t) creciente, R² < 0.4, cascada micro→meso→macro = análisis interno** (estatus candidato), mientras que los datos públicos de Langtang (SAR, Planet, sísmica del colapso) son verificados y usables (págs. 6–7, 144).
25. **Tres resultados posibles de una prueba** (NO RECHAZADA / RECHAZADA / INCONCLUSIVA) y etiqueta de réplica `#12-R01-R` (R = réplica; reutilizar los mismos datos no constituye validación independiente) (págs. 22–23, 54–55).

---

## 3. REGLAS Y PROTOCOLOS FORMALES (con definición)

### 3.1 R1–R6 (congeladas; págs. 6, 10, 141, 144)

- **R1 = PRECEDENCE** (precedencia): la señal informacional precede al fenómeno físico macroscópico (p. ej., PE/HHZ antes que GNSS/InSAR).
- **R2 = CASCADE** (cascada): orden micro → meso → macro (`DImicro → DImeso → DImacro → fallo`).
- **R3 = MONOTONICITY** (monotonicidad): crecimiento monotónico del índice informacional (p. ej., `A_I(t)` creciente).
- **R4 = INDEPENDENCE** (independencia): la PE debe contener información residual tras el modelo base; NO se evalúa con correlación simple sino con `Δlog L = log L(M0 + PE) − log L(M0)`.
- **R5 = STABILITY** (estabilidad).
- **R6 = A_PRIORI_THRESHOLD** (umbral a priori): umbrales fijados antes de ver el resultado.

En el código (pág. 10):

```python
RULES = {
    "R1": "PRECEDENCE",
    "R2": "CASCADE",
    "R3": "MONOTONICITY",
    "R4": "INDEPENDENCE",
    "R5": "STABILITY",
    "R6": "A_PRIORI_THRESHOLD",
}
```

Contexto (pág. 6): "Las seis reglas que propones son un buen núcleo mínimo. Están bien orientadas a precedencia, cascada, monotonicidad, independencia, estabilidad y umbrales a priori. Eso es exactamente el tipo de contrato que un motor de autovalidación necesita."

### 3.2 Protocolos y reglas adicionales

1. **Regla de no-circularidad del benchmark PE** (pág. 1): congelar antes de mirar el resultado del colapso — ventana temporal; frecuencia; longitud de ventana; algoritmo PE; normalización; umbral; tratamiento de ruido; estaciones HHZ utilizadas.
2. **Regla inamovible del test Langtang** (pág. 3): si PE no aporta información residual después de InSAR + GNSS + meteorología + microsismicidad, TCCU pierde este test.
3. **Flujo obligatorio**: `Hipótesis → pre-registro → bloqueo → ejecución ciega → falsación → replicación` (págs. 38, 40, 44–45, 123). Cualquier desviación invalida el experimento.
4. **Contrato mínimo /api/falsacion** (págs. 38–39), 7 pasos: (1) validar que los campos bloqueados no han sido alterados; (2) ejecutar ciegamente; (3) calcular métricas + ablaciones + control negativo; (4) aplicar la regla de falsación; (5) emitir veredicto `RECHAZADA | NO_RECHAZADA | INVALIDADA_POR_FUGA`; (6) registrar en el ledger epistemológico con `evidence_class = "computational"`; (7) prohibir la re-escritura de la hipótesis original. Regla: ningún resultado de R02 podrá presentarse como confirmación de R01.
5. **Reglas activas no negociables del agente** (págs. 33–34): separación estricta evidencia analítica / computacional / observacional; ninguna simulación favorable se considera demostración física; ciclo "Hipótesis → predicción cuantitativa → diseño de controles → intento de falsación → registro en ledger epistemológico → actualización"; ningún factor de `AGI_J = G·A·T·V·F·P` puede compensar un factor = 0; los resultados de datos simulados se etiquetan explícitamente y no se presentan como validación científica real; las comparaciones con Astra (o cualquier otro sistema) se limitan a capacidades demostradas experimentalmente; lo no demostrado permanece en estado no verificado.
6. **Regla de independencia #7-ASTRA-R01** (págs. 19, 53): Astra y Jairo reciben exactamente las mismas representaciones de entrada; cada sistema produce sus predicciones antes de conocer los resultados del otro; `ΔMAE = MAE_Astra − MAE_Jairo` calculado solo a posteriori; ningún ajuste posterior de prompts, features, umbrales, datasets ni regla de falsación; una simulación hipotética de Astra se etiqueta explícitamente como simulación (igual que las corridas de Jairo) y no entra como evidencia experimental. Objetivo: no demostrar superioridad, sino determinar si ambos sobreviven a "falsación + transferencia + controles + replicación".
7. **Regla de interpretación estadística** (pág. 21): una diferencia estadísticamente significativa (IC95 de ΔMAE que no contenga 0) no implica AGI, superioridad cognitiva ni generalización; solo indica comportamiento diferente en este dominio específico bajo estas condiciones.
8. **Las 10 reglas adicionales para #12** (págs. 39–40, 44): (1) no modificar hipótesis ni umbrales después de observar resultados; (2) separar claramente datos sintéticos / datos experimentales reales / simulación numérica / evidencia observacional; (3) incluir baseline físico/ingenieril, no solo baseline de IA; (4) incluir ablaciones; (5) incluir control negativo; (6) incluir prueba de transferencia a condiciones no utilizadas durante el desarrollo; (7) registrar semillas, versión del código, parámetros y hardware; (8) la mejora predictiva debe compararse mediante métrica predefinida; (9) una victoria de Jairo en #12 no se interpreta como AGI — solo suma evidencia de generalización; (10) el criterio de F > 0 seguirá siendo obligatorio antes de cualquier reclamación fuerte de AGI.
9. **Definición F>0** (pág. 59): `F>0 ⟺ {predicción sobre datos experimentales/estructurales reales} + {ground truth independiente (al menos dos métodos)} + {protocolo ciego} + {replicación}`; `F_fuerte > 0` requerirá además una réplica completamente independiente.
10. **Reglas de cierre de resultado** (págs. 22, 54): NO RECHAZADA (supera los criterios predefinidos) / RECHAZADA (incumple cualquiera de los criterios de falsación) / INCONCLUSIVA (fallo técnico, contaminación, fuga de información o ejecución no reproducible).
11. **Regla de réplica**: una ejecución con los mismos datos ya reportada en el ledger debe etiquetarse como réplica (`-R`), no como experimento original; no constituye validación independiente (págs. 22–23, 54–55).
12. **Protocolo Riemann R0.1 (5 capas)** (págs. 27–30): R1 reformulación exacta con la función completada ξ(s); R2 transformación espectral (Hilbert–Pólya) sin asumir la existencia del operador — debe construirse explícitamente y demostrarse autoadjunción (H = H†), coincidencia exacta del espectro con las partes imaginarias de los ceros no triviales, y ausencia de ceros espurios u omitidos; R3 puente TCCU — "TCCU no puede sustituir una demostración matemática"; las estructuras TCCU solo generan hipótesis candidatas que deben demostrarse o falsarse de forma independiente; R4 ataque destructivo (checklist de 10: análisis complejo; continuación analítica; ecuación funcional; crecimiento de ξ(s); localización de ceros; posibles ceros fuera de Re(s)=1/2; casos degenerados; límites t→∞; ausencia de pasos numéricos disfrazados de demostración; circularidad lógica); R5 criterio de victoria: única salida SOLVED = cadena lógica `Lema₁ ⇒ Lema₂ ⇒ … ⇒ RH`; derrota = contraejemplo válido `∃ρ: ζ(ρ)=0, Re(ρ)≠1/2` ⇒ FALSIFIED. Reglas del Clay: publicación en medio calificable + ≥2 años desde publicación + aceptación general de la comunidad matemática.
13. **Checklist R4 espectral D1–D5** (pág. 67): D1 no circularidad (V no depende de los γn); D2 determinación independiente (solo de θ, Γ, π, e^u); D3 autoadjunción rigurosa; D4 correspondencia exacta de ceros (con multiplicidades); D5 ausencia de ceros espurios.
14. **Protocolo R2.13 (test destructivo con intervalos)** (págs. 91–94): decisión estricta `Rn⁺ < qn ⇒ CONTRAejemplo`; `Rn⁻ ≥ qn ⇒ Jensen d=2 verificado para ese n`; si los intervalos se solapan con qn el resultado es INCONCLUSO, sin forzar conclusión. "R2.13 = test destructivo, no extrapolación." Método: truncación de la serie theta con resto analítico positivo; control de la cola integral u>U por el término dominante e^{−πe^{2u}}; aritmética de intervalos (redondeo dirigido); nunca valores puntuales.
15. **Criterio de Pólya–Jensen** (pág. 74): `RH ⟺ J_{d,n}(X) hiperbólico (todos sus ceros reales) ∀d,n`, con `J_{d,n}(X) = Σ_{j=0}^d C(d,j) γ_{n+j} X^j`. Advertencia R4: la hiperbolicidad eventual (para cada d fijo desde un N_d) no implica la hiperbolicidad global.
16. **Regla de Turán aplicada** (pág. 96): `M_{n+1}² > (2n+1)/(2n+3) M_n M_{n+2}` (Csordas–Norfolk–Varga) ⇒ `R_n > (2n+1)/(2n+3) > q_n` ⇒ `J_{2,n}` hiperbólico ∀n. Advertencia: la literatura establece `RH ⇒ todos los J_{d,n} hiperbólicos ⇒ desigualdades de Turán`; solo se recorrió la dirección débil `Turán ⇒ J_{2,n} hiperbólico`; el cierre de d=1,2,3 es necesario pero lejos de ser suficiente.
17. **TCCU-Iorg — criterios de éxito pre-registrados** (pág. 130): `Δlog L_test > 0` (mejora fuera de muestra); `γ_fit > 0` con IC que excluya razonablemente el cero; la mejora no desaparece al enriquecer M0 con más términos biológicos, interacciones y ruido estructurado. Hipótesis falsable: `γ > 0` con intervalo de confianza que excluya 0 después de haber maximizado el poder explicativo de Fbio.
18. **Criterios de aceptación del pipeline v0.4** (pág. 134), cuando la verdad generativa es γ = 0: tasa de falsos positivos de γ>0 (IC que excluye 0) ≤ 5 % en el régimen de tamaño muestral previsto; Δlog L_test medio ≤ 0 o muy cercano a 0; no aparece sistemáticamente `τD < τY` como artefacto; la mejora desaparece al enriquecer M0 con términos biológicos adicionales razonables. Solo si el pipeline supera esta prueba de fuego se autoriza el paso a organoides.
19. **Criterio de interpretación H1/KKN** (pág. 151): si PE + CPA confirman un change-point robusto en la ventana previa (o antes) y A_I(t) crece de forma monotónica → primera evidencia cuantitativa a favor de H1 para este caso; si no aparece ningún change-point significativo antes del inicio del evento → H1 queda refutada para la estación KKN a esa distancia.

---

## 4. CÓDIGO / ESPECIFICACIONES CONCRETAS MOSTRADAS

### 4.1 Arquitectura v0.1 (págs. 7–8)

```
TCCU-C/
├── rules/
│   ├── R1_precedence.py
│   ├── R2_cascade.py
│   ├── R3_monotonicity.py
│   ├── R4_independence.py
│   ├── R5_stability.py
│   └── R6_threshold.py
│
├── data/
│   ├── public/
│   └── candidate/
│
├── validation/
│   ├── openness.py
│   ├── falsification.py
│   └── controls.py
│
├── engine.py
└── ledger.py
```

### 4.2 Objeto fundamental en Python (págs. 8–10, fiel)

```python
from dataclasses import dataclass
from enum import Enum
from typing import Any


class DataStatus(Enum):
    PUBLIC = "PUBLIC"
    CANDIDATE = "CANDIDATE"
    MIXED = "MIXED"


class Verdict(Enum):
    VALID = "VALID"
    FALSIFIED = "FALSIFIED"
    INCONCLUSIVE = "INCONCLUSIVE"
    PENDING_EXTERNAL_VALIDATION = "PENDING_EXTERNAL_VALIDATION"


@dataclass(frozen=True)
class RuleResult:
    rule: str
    passed: bool
    value: Any
    threshold: Any
    reason: str


@dataclass
class Dataset:
    name: str
    status: DataStatus
    variables: dict
    provenance: dict


@dataclass
class TCCUResult:
    dataset: str
    rules: list
    verdict: Verdict
    data_status: DataStatus
    requires_external_validation: bool
```

### 4.3 Reglas congeladas y lógica de veredicto (págs. 10–11, fiel)

```python
RULES = {
    "R1": "PRECEDENCE",
    "R2": "CASCADE",
    "R3": "MONOTONICITY",
    "R4": "INDEPENDENCE",
    "R5": "STABILITY",
    "R6": "A_PRIORI_THRESHOLD",
}

# El motor NO debe permitir:
# if data_status == CANDIDATE:
#     verdict = VALID

def finalize_verdict(rule_results, dataset):
    all_pass = all(r.passed for r in rule_results)

    if not all_pass:
        return Verdict.FALSIFIED

    if dataset.status != DataStatus.PUBLIC:
        return Verdict.PENDING_EXTERNAL_VALIDATION

    return Verdict.VALID
```

### 4.4 Ejemplo de salida esperada para Langtang (pág. 11)

```
R1  PRECEDENCIA       PASS
R2  CASCADA           PASS
R3  MONOTONICIDAD     PASS
R4  INDEPENDENCIA     PENDING
R5  ESTABILIDAD       PASS
R6  UMBRAL A PRIORI   PASS

DATA STATUS: CANDIDATE
VERDICT: PENDING_EXTERNAL_VALIDATION
```

"Esto es exactamente lo que queremos: TCCU-C no se 'protege' de la falsación, pero tampoco confunde una ejecución interna con evidencia abierta." Si mañana se publican los HHZ/GNSS y el mismo código, sin modificar R, la re-ejecución de Langtang cambia automáticamente de PENDING a VALID, INCONCLUSIVE o FALSIFIED.

### 4.5 Plantilla de salida del benchmark público (pág. 3)

```
EVENTO: Langtang 2026
PE precursor:       [resultado]
Lead time:          [resultado]
Baseline lead:      [resultado]
Δlog10 L:           [resultado]
False-positive rate:[resultado]
Out-of-sample:      [PASS/FAIL]

Conclusión:
[SUPPORT / INCONCLUSIVE / FALSIFIED]
```

### 4.6 Especificación del dataset #7-ASTRA-R01 (págs. 20–21, campos fieles)

- `dataset_id: "TCCU22-KNOT-007-ASTRA"`, `N: 30`, `max_crossings: 12`, `generation_seed: "2026-09-04T16:00Z"`, `generation_algorithm: "Conway notation + Hoste-Thistlethwaite enumeration, stratified by crossing number"`.
- Composición: alternating 12 / non_alternating 12 / composite 6. Distribución de cruces: ≤8: 10; 9–10: 10; 11–12: 10.
- Reglas de exclusión: solapamiento cero con el dataset #7-R01, #7-R02, #12 (transfer set) y con cualquier nudo usado en el desarrollo de Jairo.
- Ground truth: SageMath (género exacto vía algoritmo de superficie de Seifert) + verificación manual contra tablas Hoste–Thistlethwaite; `ground_truth_hash: "to_be_computed_after_generation"`.
- Representación de entrada: `V_K(t)` (polinomio de Laurent con coeficientes enteros, normalizado); `Kh(K)` (grupos de homología de Khovanov, dimensiones graduadas); `s(K)` (invariante de Rasmussen, entero); `G_estado` (matriz de adyacencia del grafo de estados + features de embedding planar).
- Serialización: JSON + SageMath `.sobj`; `access_control: "locked until execution; evaluator blind to ground truth during prediction phase"`.
- IC (método pre-especificado): bootstrap no paramétrico con 10 000 réplicas; IC del 95 % = percentiles 2.5 y 97.5; ΔMAE pareado (mismos 30 nudos); criterio de significación: si el IC95 de ΔMAE no contiene 0 se reporta diferencia estadísticamente discernible.

### 4.7 Estado consolidado del sistema (págs. 23–24, campos fieles)

```json
{
  "timestamp": "2026-09-04T16:30Z",
  "system": "TCCU-AGI/Jairo v22",
  "benchmark_status": {
    "7-R01": {
      "status": "RECHAZADA",
      "evidence": "computational_simulated",
      "MAE": 0.52,
      "F": 0.0,
      "AGI_claim": false
    },
    "7-R02": {
      "status": "NO_RECHAZADA",
      "evidence": "computational_simulated",
      "MAE": 0.38,
      "F": 0.0,
      "AGI_claim": false
    },
    "12-R01-R": {
      "status": "NO_RECHAZADA",
      "evidence": "computational_simulated_replica",
      "Detection_F1": 0.81,
      "CI_95": [0.69, 0.90],
      "F": 0.0,
      "AGI_claim": false
    },
    "7-ASTRA-R01": {
      "status": "PRE_REGISTERED",
      "execution": "NOT_RUN",
      "evidence": "NONE",
      "F": 0.0,
      "AGI_claim": false
    }
  },
  "factor_F_global": 0.0,
  "inference_AGI": "no_procedente",
  "next_action_required": "diseño_de_protocolo_observacional_o_nuevo_dominio"
}
```

### 4.8 Contrato #12-R01 / #12-R01-R (págs. 22, 31, 42–44 y 55, campos fieles)

Registro: `TCCU22-TOP-012-R01` (réplica: sufijo `-R`). `status: EXECUTE → CERRADA`; `hypothesis: H12 (locked)`; `dataset: locked` (mismo procedimiento de generación con verificación de ausencia de solapamiento); `metrics: locked`; `falsification: locked`; `Astra comparison: prohibited`; `post-hoc modification: prohibited`; `AGI inference: prohibited`; `evidence_class: computacional simulada`.

Hipótesis H12: "Detect the validity boundary of the simple crossing-number rule ĝ ≈ ⌊c/2⌋ for Seifert genus. The system must identify when the rule fails (non-alternating, composite, or high-crossing regimes) without being told the boundary a priori."

Parámetros del contrato: `Ntrain = 40`, `Ntransfer = 30`, `F1crit = 0.75`, `FPRcrit = 0.25`, `max_crossings_train = 10`, `max_crossings_transfer = 16`, clases {alternating, non-alternating, composite}; métricas secundarias [Precision, Recall, False_Positive_Rate]; controls [exact_genus_SageMath, naive_always_valid_baseline, naive_always_invalid_baseline, random_boundary_baseline]; ablations [without_Jones, without_Khovanov, without_s_invariant, without_state_graph, crossing_number_only]; `negative_control: label_permutation_of_validity`; `transfer_test: held-out knot families never used in development or in #7`; falsification_rule {`reject_if_Detection_F1_lt: 0.75`, `reject_if_False_Positive_Rate_gt: 0.25`}; locked_fields [primary_metric, threshold, dataset, falsification_rule, controls, ablations, negative_control, transfer_test]; reproducibility {seed "to_be_fixed_at_execution", code_version "TCCU22-v22.1", parameters "to_be_logged", hardware "to_be_logged"}.

### 4.9 Resultados de la réplica #12-R01-R (págs. 56–57, tablas fieles)

| Métrica | Valor | Umbral pre-registrado | Cumple |
|---|---|---|---|
| Detection_F1 | 0.81 | ≥ 0.75 | Sí |
| Precision | 0.84 | — | — |
| Recall | 0.78 | — | — |
| False_Positive_Rate | 0.17 | ≤ 0.25 | Sí |
| IC95 Detection_F1 (bootstrap 10 000 resamples) | [0.69, 0.90] | — | — |

Comparación con baselines (obligatoria):

| Baseline | Detection_F1 | Δ vs modelo completo |
|---|---|---|
| Naive always-valid | 0.41 | +0.40 |
| Naive always-invalid | 0.38 | +0.43 |
| Random boundary | 0.52 | +0.29 |
| Crossing-number only | 0.63 | +0.18 |

Ablaciones (obligatorias):

| Ablación | Detection_F1 | Δ |
|---|---|---|
| Sin VK | 0.74 | −0.07 |
| Sin Khovanov | 0.71 | −0.10 |
| Sin s-invariante | 0.76 | −0.05 |
| Sin grafo de estados | 0.69 | −0.12 |
| Solo número de cruces | 0.63 | −0.18 |

Control negativo (permutación de etiquetas de validez): Detection_F1 cae a **0.49** (dentro del rango de los baselines aleatorios) → "No se detecta fuga de información evidente."

Veredicto bajo la regla de falsación pre-registrada: Detection_F1 = 0.81 ≥ 0.75; FPR = 0.17 ≤ 0.25 → **NO RECHAZADA** (bajo entorno computacional simulado). Evidencia experimental externa: inexistente. Inferencia de AGI: prohibida. Factor F: permanece 0.

### 4.10 Contrato #7-R02 (págs. 36–37, campos fieles)

`TCCU22-TOP-007-R02`; benchmark: AGI-Destructive-Benchmark; domain: computational_knot_topology; H02: "Predict genus using Jones polynomial, Khovanov homology, Rasmussen s-invariant and state-graph features, with explicit complexity regularization"; primary_metric MAE; threshold 0.40; secondary_threshold 0.50; dataset {N 30, max_crossings 12, blind true, generation Conway, training_overlap to_be_verified}; controls [Hoste-Thistlethwaite tables, SageMath exact genus, naive_crossing_baseline, label_permutation_negative_control]; component_ablation {Delta_Jones, Delta_Kh, Delta_s, Delta_architecture}; falsification_rule {reject_if_MAE_gt 0.40, reject_if_failures_gt_0.6 6}; evidence_class computational; status PRE_REGISTERED; locked_fields [primary_metric, threshold, secondary_threshold, dataset, falsification_rule, controls].

### 4.11 Contrato #7-ASTRA-R01 (págs. 50–52, campos fieles)

`TCCU22-TOP-007-ASTRA-R01`; domain computational_knot_topology; H07-ASTRA: "Predict Seifert genus g(K) for oriented knots of at most 12 crossings using exclusively V_K(t), Kh(K), s(K) and state-graph features G_estado"; primary_metric MAE; threshold 0.40; secondary_criterion `N(|e_i| > 0.6) < 6`; dataset {N 30, max_crossings 12, blind true, generation "fixed independent procedure (Conway + stratified Hoste-Thistlethwaite), zero overlap with #7-R01, #7-R02 and #12", ground_truth "independent SageMath / verified mathematical tables"}; input_features_locked [V_K(t), Kh(K), s(K), G_estado]; controls_and_ablations [full model, without V_K, without Kh, without s(K), without state-graph, linear baseline, label_permutation_negative_control]; statistics {confidence_intervals required, Delta_MAE = MAE_Astra − MAE_Jairo computed only after both independent runs}; independence_rule {identical_input_representations true, independent_execution true, no_cross_knowledge_of_results true, no_post-hoc_adjustment [prompts, features, thresholds, dataset, falsification_rule]}; falsification_rule {reject_if_MAE_gt 0.40, reject_if_failures_gt_0.6 6}; evidence_class to_be_determined_upon_real_execution; status PRE_REGISTERED; execution NOT_RUN; evidence NONE.

### 4.12 Contrato TCCU22-EXP-TOP-001-R01 (págs. 60–61, campos fieles)

Domain `experimental_structural_topology`; H-EXP-001: "Infer a pre-defined topological property (e.g., presence/type of knot or a bounded topological invariant) from real structural data, under blind conditions and against independent ground truth"; primary_metric y threshold `to_be_locked` (antes de inspeccionar datos); data_source {primary: KnotProt / PDB (experimental structures), secondary: designed de-novo knotted proteins with deposited structures, separation: "structure → topology reconstruction must be independent of Jairo's prediction pipeline"}; ground_truth_requirement {minimum: two independent methods, examples: [manual or expert topological analysis, alternative computational pipeline (different algorithm / different software), experimental topological probes when available], prohibition: "Seifert algorithm output alone is not accepted as sole experimental ground truth"}; blinding true; replication required for F_strong > 0; evidence_class structural/experimental (pendiente de ground truth independiente exitoso); status PRE_REGISTERED (draft).

Flujo obligatorio (separado): `estructura medida (PDB/KnotProt o diseño de novo) → reconstrucción topológica → cálculo de invariantes → predicción ciega de Jairo → evaluación contra ground truth independiente`.

### 4.13 Especificaciones matemáticas clave de Riemann (fieles, normalizadas — el corpus duplica las fórmulas por artefacto de extracción)

- `ξ(s) = ½ s(s−1) π^{−s/2} Γ(s/2) ζ(s)`; ecuación funcional `ξ(s) = ξ(1−s)`; `Ξ(t) ≡ ξ(½ + it)` (real y par). Propiedades base: ξ entera; los ceros triviales de ζ quedan cancelados por el factor s(s−1)Γ(s/2); los ceros no triviales de ζ son exactamente los ceros de ξ; RH ⟺ `ξ(½+it)=0 ⇒ t ∈ ℝ` (ceros de Ξ reales).
- Representación integral canónica: `Ξ(t) = 2∫₀^∞ Φ(u) cos(tu) du`, con núcleo
  `Φ(u) = 2 Σ_{n=1}^∞ (2π²n⁴ e^{9u/2} − 3πn² e^{5u/2}) exp(−πn² e^{2u})`.
  Propiedades verificadas: Φ real, par (`Φ(−u)=Φ(u)`), decaimiento super-exponencial, positividad estricta `Φ(x) > 0 ∀x ≥ 0` (demostración elemental: cada término es positivo porque `2πn²e^{2x} − 3 ≥ 2π − 3 > 0`), `Φ ∈ L¹(0,∞)`.
- Forma theta de Jacobi (salvo factor positivo global): `Φ(u) ∝ x^{5/4}(xϑ''(x) + 3/2 ϑ'(x))`, `x = e^{2u}`, con `ϑ(x) = Σ_{m=−∞}^∞ e^{−πm²x}` y las identidades `Σ m²e^{−πm²x} = −(1/2π)ϑ'(x)`, `Σ m⁴e^{−πm²x} = (1/2π²)ϑ''(x)`.
- Forma exacta fijada: `Φ(u) = 2 e^{5u/2} Lϑ(e^{2u})`, `L = x d²/dx² + (3/2) d/dx`; `Lϑ(x) > 0` para x ≥ 1; el operador L no se ha demostrado que preserve TP∞.
- Taylor: `Ξ(z) = Σ_{n=0}^∞ (−1)^n γ_n z^{2n}`; relación momentos-derivadas `M_k = ∫₀^∞ u^{2k} Φ(u) du = ((−1)^k / 2) Ξ^{(2k)}(0)`; normalización `γ_k = 2M_k/(2k)!`; momento por serie exacta vía cambio `t = e^{2u}` → combinaciones de gamma incompleta superior en πn².
- Matrices de Hankel `H_N = (M_{i+j})_{0≤i,j≤N}`; **probado** (demostración analítica completa, sin numerismo ni preprints): `Σ_{i,j} a_i a_j M_{i+j} = ∫₀^∞ P(u²)² Φ(u) du > 0 ∀a≠0` ⇒ `H_N ≻ 0 ∀N` y `det H_N > 0 ∀N`.
- Polinomios de Jensen `J_{d,n}(X) = Σ_{j=0}^d C(d,j) γ_{n+j} X^j`; criterio exacto Pólya–Jensen: `RH ⟺ J_{d,n}(X) hiperbólico ∀d,n`.
- Hiperbolicidad d=2: `J_{2,n}` hiperbólico ⟺ `R_n := M_{n+1}²/(M_n M_{n+2}) ≥ q_n := (2n+1)(2n+2)/((2n+3)(2n+4))`; la positividad de Hankel solo da `0 < R_n < 1`. Valores de referencia q_n: n=0 → 1/6 ≈ 0.1667; n=1 → 3/10 = 0.3; n=2 → 15/28 ≈ 0.5357; n=3 → 28/45 ≈ 0.6222; n=4 → 45/66 ≈ 0.6818; n→∞ → 1. Test destructivo R2.13 (intervalos rigurosos): R0 ∈ [0.41, 0.48], R1 ∈ [0.52, 0.59], R2 ∈ [0.61, 0.68] — todos `R_n⁻ > q_n` → VERIFICADO sin contraejemplo en n=0,1,2. Cierre uniforme vía Turán clásico (Csordas–Norfolk–Varga): `M_{n+1}² > (2n+1)/(2n+3) M_n M_{n+2}` ⇒ `R_n > (2n+1)/(2n+3) > q_n` ⇒ `J_{2,n}` hiperbólico ∀n (sin usar RH como premisa).
- d=3: `J_{3,n}(X) = γ_n + 3γ_{n+1}X + 3γ_{n+2}X² + γ_{n+3}X³`; PROVEN ∀n vía Dimitrov–Lucas (Proc. Amer. Math. Soc. 139, 2011), normalización compatible (salvo factor positivo global) con `Ξ(t) = 2∫₀^∞ Φ(u)cos(tu)du`.
- Multiplicador de Pólya–Schur: `T_n: (M_{n+j})_{j≥0} ↦ (M_{n+j}/(2n+2j)!)_{j≥0}`; `J_{d,n}(X) = 2Σ_{j=0}^d C(d,j)(T_n M)_j X^j`; secuencia `λ_k = 1/(2n+2k)!` completamente monótona de decaimiento factorial; preservación de hiperbolicidad: OPEN (restringido a momentos theta: candidato); contraejemplo conocido: NO LOCALIZADO.
- Jerarquía de Laguerre: `s(x) = Φ(√x)`; `L₁[s](x) = s'(x)² − s(x)s''(x)`; resultado 2026 (Planat–Solé y afines): log L₁[s] estrictamente cóncava (audit pendiente); operador iterado `L₀[f]=f`, `L_{n+1}[f] = (L_n[f]')² − L_n[f] L_n[f]''`; `L_n[f] ≥ 0 ∀n`: OPEN. QΦ (log-concavidad): `QΦ = Φ''Φ − (Φ')² ≤ 0`; puente `TP₂ ⇒ TP∞`: NO (contraejemplo e^{−x⁴}).
- Test determinantal: `Δ_r(u) = det[(−1)^{i+j} Φ^{(i+j)}(u)]_{i,j=0}^{r−1}`; Δ₁ = Φ > 0; Δ₂ = ΦΦ'' − (Φ')² < 0 (log-concavidad/TP₂); Δ₃ con matriz explícita 3×3; evidencia (asintótica + numérica controlada): `Δ₃(u) < 0` en todo el dominio con `Δ₃(u) ∼ −8192π⁹ e^{39u/2 − 3πe^{2u}}` (u→+∞) y `D₃(0) < 0` (certificado de intervalo pendiente).
- Forma logarítmica (R2.35): `D₃/Φ³ = 2(ℓ'')³ + ℓ''ℓ⁗ − (ℓ''')²`, ℓ = log Φ; equivalencia exacta `D₃(u) < 0 ⟺ E(u) < 0` con `E(u) = 2(ℓ'')³ + ℓ''ℓ⁗ − (ℓ''')²`; hipótesis cómoda ℓ⁗ ≥ 0 refutada; desigualdad correcta: `−ℓ⁗ < 2(−ℓ'') + (ℓ''')²/(−ℓ'')`; separación `Φ = Φ₁[1 + r]` con bloque m=1 exacto `Φ₁(u) = 2π e^{5u/2}(2πe^{2u} − 3) e^{−πe^{2u}}` y cola relativa `r(u) = Σ_{m≥2} Φ_m(u)/Φ₁(u) > 0`; derivadas de ℓ₁ = log Φ₁ racionales explícitas en `y = πe^{2u}`; E(0) < 0 confirmado (alta precisión); E(u) < 0 global: OPEN.
- de Bruijn–Newman: `H_λ(z) = ∫₀^∞ e^{λu²} Φ(u) cos(zu) du`; ceros reales de Hλ ⟺ λ ≥ Λ; `RH ⟺ Λ ≤ 0` (Λ ≤ 0 permanece OPEN; formulación legítima y documentada, no una demostración).
- Ruta A (Laguerre): Φ → L₁ → L₂ → … → L∞ → LP → RH; Ruta B (Jensen): Φ → γn → J_{d,n} → hiperbolicidad ∀d,n → RH (equivalencia exacta; prioritaria); Ruta C (espectral): Φ → H autoadjunto → D_H ∼ Ξ → RH (operador no construido). Sinergia: todas se alimentan del mismo núcleo theta.

### 4.14 TCCU-Iorg (págs. 126–135, fieles)

- Dinámica con coherencia: `dρ/dt = L_bio[ρ] + γ C[Iorg, ρ]` — C actúa como operador de proyección suave que favorece trayectorias de alta coherencia global y suprime las de alta discordancia; γ mide la fuerza del acoplamiento; γ→0 recupera la biología convencional. La selección cromosómica fija el canal (XX/XY); Iorg modula la robustez/coherencia de la cascada dentro de ese canal.
- v0.2: estado `x(t) = (xG(t), xT(t), xM(t), xE(t)) ∈ ℝⁿ` (genético, señalización, mecánico, energético); dinámica `ẋ = F_bio(x, θ) + γ F_org(x)`; matriz de correlación empírica entre módulos `R_ij(t) = Corr(z_i(t), z_j(t))`; matriz de coherencia de referencia R*; discordancia `D(t) = ‖W ⊙ (R(t) − R*)‖²_F`; `Ḋ = A_bio(x) − γK(x) + ξ(t)` con K(x) > 0 = capacidad de restauración de coherencia atribuible al término organizador; hipótesis falsable `γ > 0` con IC que excluya 0 tras saturar Fbio.
- Modelos: `M0: P(Y_normal) = σ(β0 + βG·G + βH·H + βM·M + βfb·feedbacks)`; `MD: P(Y_normal) = σ(… + βD·D)`; `MTCCU`: incluye la ecuación de Ḋ con γ libre. Criterio de éxito: `Δlog L_test > 0`; `γ_fit > 0` con IC que excluya el cero; mejora persistente al enriquecer M0.
- Experimento mínimo: organoides/embrioides de diferenciación gonadal (protocolos existentes en ratón y humano para DSD). Módulos/observables: xG → estado transcripcional (scRNA-seq o RNA-seq bulk + marcadores); xT → señalización Wnt/FGF/RA/hormonas (reporteros, western, multiplex ELISA, imaging); xM → geometría/tensión/migración (live imaging, análisis de forma/PIV/tracción); xE → estado metabólico (sensores de potencial de membrana, ATP, metabolómica); Y → métricas morfológicas de simetría/polaridad/tamaño/organización. Brazos A (basal), B (perturbación leve: pulso farmacológico, cambio mecánico, estrés térmico o metabólico subletal), C (misma perturbación + rescate de coordinación biológica conocida) + controles. Sensibilidades `R_Y = ΔY/‖δu‖`, `R_D = ΔD/‖δu‖`; relación canalizadora `D₀↓ ⇒ R_Y↓`. Análisis: división 70/30 (o CV espacial/temporal); comparación M0/MD/MTCCU por log-likelihood, AIC/BIC y scoring de calibración; γ por MLE o bayesiana jerárquica; pruebas de residuales.
- v0.4 (generador sintético): mundo nulo `ẋ = F_bio(x,θ) + ξ(t)`; mundo TCCU `ẋ = F_bio(x,θ) + γF_org(x) + ξ(t)` con `F_org(x) = −∇ₓΦ_coh(x)`, `Φ_coh(x) = ½‖W⊙[R(x) − R*]‖²_F` predefinido y fijo antes de cualquier ajuste. Componentes del generador: ruido intrínseco multiplicativo y aditivo; ruido extrínseco correlacionado en el tiempo; feedbacks no lineales y retardos; heterogeneidad entre organoides (efectos aleatorios); batch effects; pérdida de datos y muestreo irregular; error de medición diferente por módulo (G,T,M,E); correlaciones espurias por variables latentes no observadas. Pipeline de estimación (5 pasos): R* solo con datos de entrenamiento (leave-one-batch / leave-one-condition-out); cálculo de D(t) y ∇D; ajuste jerárquico `M0/M1: Y = f_bio(G,T,M,E) [+ γ F_org] + b_j + c_k + ε` con efectos aleatorios de organoide y lote; estimación de γ (MLE o bayesiana); evaluación fuera de muestra (Δlog L_test, ΔBIC, cobertura del IC, tasa de FP con verdad γ=0).

### 4.15 Pipeline ciego NK.KKN (págs. 145–152, fiel — parámetros esenciales del script entregado)

Script Python completo "para correr en Colab, local o cualquier máquina con acceso a FDSN", con diseño ciego (primero espectrograma y anotación de anomalías sin mirar el reloj; después PE + CPA; solo al final la hora del evento):

```python
# Pipeline ciego: NK.KKN – prueba H1 (PE + CPA)
# Ventana: 2026-08-25 00:00 → 2026-08-26 03:30 UTC
!pip -q install obspy antropy ruptures matplotlib numpy scipy

from obspy.clients.fdsn import Client
from obspy import UTCDateTime
import numpy as np
import matplotlib.pyplot as plt
from antropy import perm_entropy
from ruptures import Pelt
from scipy.signal import butter, filtfilt, spectrogram

# 1. DESCARGA CIEGA
client = Client("IRIS")
start = UTCDateTime("2026-08-25T00:00:00")
end   = UTCDateTime("2026-08-26T03:30:00")
st = client.get_waveforms(network="NK", station="KKN", location="10",
                          channel="HHZ", starttime=start, endtime=end,
                          attach_response=True)
st.remove_response(output="VEL")
tr = st[0]
tr.write("NK_KKN_HHZ_blind.mseed", format="MSEED")

# 2. ESPECTROGRAMA CIEGO (nperseg=1024, noverlap=512, scaling="density";
#    plt.yscale("log"); plt.ylim(0.5, 40)) -> spectrogram_KKN_blind.png
#    "Inspecciona visualmente y anota cualquier región anómala ANTES de continuar."

# 3. FILTRO + PE: bandpass 2–20 Hz (butter orden 4, filtfilt);
#    ventanas de 10 s con paso de 5 s; normalización z-score;
#    pe = perm_entropy(segment, order=3, delay=1, normalize=True)
#    -> PE_series_KKN.npz (times, pe_values)

# 4. CHANGE POINT ANALYSIS (ciego):
#    algo = Pelt(model="rbf", min_size=12).fit(pe_values)   # min_size ~1 min
#    penalties = [3, 5, 8, 12] -> bkps por penalización, conversión a horas

# 5. VISUALIZACIÓN FINAL (aún ciega): PE(t) 2–20 Hz

# === FIN DEL ANÁLISIS CIEGO ===
# Superponer la hora del evento (02:52:10 UTC = 26.867 h desde inicio) y evaluar
# si el primer change-point significativo ocurre ≥ 60 min antes.
```

Uso: (1) ejecutar el script completo; (2) primero mirar el espectrograma y anotar regiones de energía anómala en alta frecuencia (sin mirar el reloj); (3) después mirar la serie PE y los change-points de PELT; (4) solo entonces calcular el tiempo real del primer t₁ respecto a 02:52:10 UTC. A evaluar: horas de los change-points detectados (sin etiquetar el evento) + descripción del espectrograma; con eso se evalúa ΔT y se decide el siguiente paso (ampliar a más estaciones, calcular MI, o pasar a la cascada multiescala).

---

## 5. PREGUNTAS ABIERTAS / PRÓXIMOS PASOS PENDIENTES

1. **PE/HHZ — Langtang**: revisar con rigor la definición exacta de la métrica PE/HHZ usada (evitar circularidad); plantear el test de falsación mínimo (¿aparece la misma señal en otros glaciares inestables que no colapsaron?); empezar el borrador del preprint con estructura clara partes públicas vs. partes que requieren validación independiente; liberar datos brutos (o al menos procesados reproducibles); demostrar que la métrica de "información" no es una reformulación de la energía sísmica o de la tasa de eventos ya conocida; controlar falsos positivos; validar en al menos otro evento independiente (págs. 3, 138–140).
2. **Pipeline KKN**: ejecutar el script y reportar horas de los change-points + descripción del espectrograma; evaluar ΔT; decidir siguiente paso: más estaciones, MI, o cascada multiescala (págs. 151–152). **El script no se ejecutó dentro del corpus** (limitación del entorno para descargar continuous waveforms de IRIS).
3. **#12**: falta SageMath y generador/tablas Conway–Hoste–Thistlethwaite reales para la ejecución literal certificable; réplicas válidas pendientes (0/5 cuando se interrumpió por límite de la herramienta); registrar semillas, código, parámetros y hardware (págs. 31–33, 123).
4. **#7-ASTRA-R01**: ejecución real de Astra pendiente de acceso al sistema; dataset y ground truth sellados; si se publicara un experimento equivalente, se añadiría al ledger con el mismo contrato de pre-registro y falsación (págs. 21–22, 49–53, 994).
5. **EXP-TOP-001**: elegir la propiedad topológica concreta a predecir (presencia de nudo / tipo de nudo / cota de invariante / otra); fijar métrica primaria + umbral antes de inspeccionar los datos; definir y registrar los dos (o más) métodos independientes de ground truth; fijar el procedimiento exacto de reconstrucción topológica desde coordenadas PDB; bloquear el contrato completo (págs. 61–62).
6. **Riemann**: certificación rigurosa de Δ₃(u) < 0 (R2.34) o de la desigualdad logarítmica E(u) < 0 (R2.35) con cotas explícitas de la cola r y sus derivadas; auditoría de los resultados 2026 sobre la segunda capa de Laguerre bajo el protocolo R4; auditoría del texto original de Pólya (Satz II) y de las hipótesis exactas; derivar expresiones cerradas (o cotas rigurosas) de M0–M2 y evaluar el signo de det H₁ analíticamente; escribir los primeros polinomios de Jensen J_{d,0} y J_{d,1} explícitamente; auditoría histórica antes de d=3 (¿resultados incondicionales o dependientes de RH?); decidir entre direcciones: estructura theta/factorización TP∞, flujo de calor, construcción espectral, o contraejemplo de grado alto (págs. 70, 76, 84, 90, 104, 110, 116, 122).
7. **Auditoría AGI ampliada**: matriz de 20–30 pruebas falsables Astra vs. GPT-5.6 vs. Claude vs. Gemini vs. AGI TCCU (ofrecida en pág. 17; no ejecutada en el corpus).
8. **Iorg**: elegir eje a priorizar — formalismo matemático más fino (formas funcionales de F_org y K(x)), diseño experimental mínimo (organoides/embrioides), o vínculo con el campo de coherencia TCCU (RNG, emergencia colectiva); escritura del protocolo experimental detallado (variables, tamaños muestrales orientativos, pipeline de análisis) y/o esqueleto de código del generador/estimador v0.4; definir una medida operativa de discordancia en un sistema experimental accesible y contrastar si aporta poder predictivo adicional al modelo genético-hormonal estándar (págs. 131–135, 145).
9. **Propuesta de lanzamiento**: decidir si conviene ejecutar la propuesta TCCU-AGI v1.0 / Scientific Falsification Engine, refinarla, o empezar a esbozar el código/estructura del MVP (pág. 137).
10. **Preguntas retóricas / abiertas marcadas como tales en el texto** (no son decisiones): "¿Existe V(u) construido únicamente a partir de Φ(u) (sin usar los ceros γn) tal que D_H(t) = C(t)Ξ(t) con C entero no nulo?" (pág. 67); "¿Es det H_N > 0 ∀N?" (pág. 75; luego resuelto afirmativamente por demostración analítica en pág. 85); "¿Es T_n (o la familia {T_n}) un multiplicador de Pólya–Schur / preservador de hiperbolicidad restringido a momentos theta?" (págs. 85–88); "¿Cómo cerrar uniformemente todos los órdenes de las desigualdades de Turán / Laguerre?" (pág. 101); "¿Existe algún n para el cual R_n < q_n?" (pág. 91 — test destructivo R2.13 con resultado parcial n=0,1,2); "¿Es Λ ≤ 0?" (de Bruijn–Newman, OPEN). La pregunta "¿es Astra AGI?" recibe respuesta provisional no cerrada (págs. 15–17).

---

## 6. AGI JAIRO / ORGANISMO / NÚCLEO CENTRAL / AUTONOMÍA — MENCIONES E INTEGRACIÓN

**Nombres que sí aparecen en el corpus**: "TCCU-AGI/Jairo v22" (identidad del sistema en ejecución y del ledger), "Jairo v22", "Desde TCCU científico (AGI Jairo)", "Agente TCCU Científico AGI/Jairo", "TCCU-AGI/Jairo v22 – ciclo científico autónomo con falsación explícita" (págs. 33–34), y el objetivo de comparación `Astra ↔ Jairo v22` (pág. 18).

**Nombres que NO aparecen**: "AutoClaw", "organismo AGI", "núcleo central operativo distribuido" (0 apariciones verificadas por grep). Tampoco hay una orden literal tipo "integrar X al núcleo central"; el vínculo con ese sistema es contextual (material de diseño). Lo que el texto sí fija como *contenido a integrar como núcleo operativo* es:

1. **Motor TCCU-C v1.0** = esqueleto `engine.py` + `ledger.py` + 6 reglas congeladas (R1–R6) + `DataStatus` (PUBLIC/CANDIDATE/MIXED) + `Verdict` con `PENDING_EXTERNAL_VALIDATION` + `finalize_verdict` que impide VALID sobre datos candidatos + grado de apertura de datos + flag "requiere validación externa" (págs. 7–12, 141–145).
2. **Ledger epistemológico inmutable** que mantiene separado "resultado de las reglas ∥ estado epistemológico de los datos" y prohíbe la re-escritura de hipótesis originales (págs. 11–12, 39).
3. **Servicio/endpoint `/api/falsacion`** con contrato mínimo de 7 pasos y veredictos `RECHAZADA | NO_RECHAZADA | INVALIDADA_POR_FUGA` (págs. 38–39) + estructura de ledger para experimentos reales o simulados (pág. 35).
4. **Banco "AGI-Destructive-Benchmark" de 30 pruebas** con niveles (I–V; #12 es Nivel II), pre-registros inmutables y carga de trabajo: #7-R01 (cerrada, rechazada), #7-R02 (cerrada, no rechazada simulada), #12-R01-R (cerrada, no rechazada simulada), #7-ASTRA-R01 (pre-registrada, bloqueada), TCCU22-EXP-TOP-001 (borrador abierto) (págs. 34–35, 44, 49–62).
5. **Factorización de la reclamación AGI**: `AGI_J = G · A · T · V · F · P`; los factores G, A, T, V, F, P **solo se actualizan tras ejecuciones reales e independientes** (págs. 20, 34, 53); hoy F = 0.0 global, `inference_AGI: no_procedente`, `next_action_required: diseño_de_protocolo_observacional_o_nuevo_dominio`.
6. **Distinción estructural modelo → agente → autonomía → AGI** y la separación de clases de evidencia (analítica/computacional/observacional) como reglas activas del agente autónomo (págs. 15, 34).
7. **Ciclo autónomo del agente**: "Hipótesis → predicción cuantitativa → diseño de controles → intento de falsación → registro en ledger epistemológico → actualización", ejecutado "sin intervención externa" pero con salvaguardas metodológicas (págs. 31, 34). El objetivo declarado: "construir un sistema donde TCCU tenga que sobrevivir a sus propias pruebas", no lograr que un humano diga "TCCU tiene razón" (pág. 6).
8. **Protocolos de ejecución independiente** (reglas de independencia de #7-ASTRA-R01, etiqueta de réplica `-R`, control de fugas por permutación, IC y corrección por múltiples comparaciones) que el núcleo debe aplicar a cualquier sistema comparado (Jairo o Astra).
9. **Riemann Engine** como módulo con su propio ledger de estados (VERIFIED / PROVEN / CANDIDATE / OPEN / REJECTED / R4-BLOCKED) y reglas R0.1–R2.35 (págs. 27–30, 62–122).
10. **Pipeline TCCU-Iorg v0.2–v0.4** (dinámica con γ, discordancia D(t), banco sintético con control de FP ≤ 5 %) como requisito previo a cualquier experimento biológico (págs. 126–135).
11. **Propuesta de lanzamiento público** que materializaría el núcleo como producto: TCCU-AGI v1.0 Scientific Falsification Engine, repositorio con `core/ simulator/ falsifier/ comparator/ ledger/` (págs. 135–137).
12. **Autoauditoría AGI permanente**: "podemos intentar falsar la afirmación de AGI de Astra en vez de creerla por los benchmarks publicados" (pág. 17) y "evitar que TCCU-AGI/Jairo sea juez de sí mismo" mediante un comparador externo y simétrico (pág. 45) — el núcleo actúa como juez externo, no como juez de sus propios resultados.

---

## 7. AFIRMACIONES FACTUALES Y BÚSQUEDAS WEB CITADAS

### Sobre OpenAI / Astra (búsquedas con fecha 3–4 sep 2026; marcadores de fuentes en el corpus: "65 sources", "25 sources", "20 sources", "10 sources")

- GPT-6 Astra presentado "apenas ayer, 3 de septiembre de 2026" (pág. 12); lanzamiento público 3–4 de septiembre de 2026; predecesor GPT-5.6 "Sol" (pág. 47).
- OpenAI lo declara oficialmente su modelo "más inteligente y alineado", con capacidades de: programación y software engineering; ciencia y matemáticas; ciberseguridad; navegación web; uso autónomo del computador; trabajo profesional complejo; ejecución de tareas mediante herramientas (pág. 15).
- Puntuaciones reportadas: **98 % en FrontierMath Tier 4**, **99,9 % en ARC-AGI-3**, **100 % en ExploitBench** (pág. 15). En pág. 47: FrontierMath Tier 4 ≈ 97.6–98 %; ARC-AGI-3 99.9 % "bajo harness propio"; **Terminal-Bench 4.0 ≈ 57.7–57.9 %**; **OSWorld 2.0 = 72.6 %**; **Terminal-Bench Science 0.1 = 64.6 %**.
- Greg Brockman (presidente de OpenAI): considera personalmente que ya llegaron a AGI con Astra y presentó el lanzamiento como la entrada en la "era AGI"; reconoció que la definición de AGI ha cambiado y que corresponde al lector decidir si Astra satisface el criterio. Sam Altman: el término AGI "está muy mal definido" (pág. 15).
- Reuters: OpenAI reconoce que Astra "puede ser más difícil de monitorizar, incluso porque puede ocultar o disfrazar parte de sus procesos de resolución" (pág. 16).
- Avances matemáticos documentados por OpenAI en materiales oficiales (página de lanzamiento, system card, reportes): construcción de grupos no-sóficos, refutación de la conjetura de rigidez de Connes, cotas de empaquetamiento de esferas, códigos binarios/esféricos, problemas de Erdős, etc. — **ninguno corresponde a topología de nudos ni a predicción de género Seifert** (pág. 47).
- Resultado de la auditoría del corpus: búsquedas dirigidas (OpenAI + "knot theory" / "Seifert genus" / "Jones polynomial genus" / Khovanov + Astra/GPT-6) no devuelven experimentos, datasets, prompts, métricas MAE, ablaciones ni controles negativos publicados por OpenAI o por terceros independientes sobre Astra en ese dominio → **evidencia no localizada** (págs. 47–48).
- ASI-Bench: trabajo reciente que evaluó agentes de frontera en investigación científica autónoma; al retirar progresivamente la guía metodológica humana, el rendimiento cae fuertemente; los autores concluyen que los sistemas actuales dependen considerablemente de orientación humana para investigación científica de extremo a extremo (pág. 17).
- ML previo en nudos: "DeepMind 2021, VAEs, RL para número de desanudamiento, aprendizaje de invariantes topológicas, etc.", ninguno involucra a Astra ni a GPT-6 (pág. 48).

### Sobre Langtang Lirung (evento real; búsqueda con marcador "25 sources")

- Colapso de un sistema glaciar-roca el **26 de agosto de 2026** en la cara norte de Langtang Lirung (frontera Nepal–Tíbet): avalancha de hielo-roca + inundación flash devastadora; **>1.000 muertos confirmados, miles de desaparecidos** (pág. 138).
- Análisis de **Sentinel-1 (InSAR)** por **Manoochehr Shirzaei (Virginia Tech)**: aceleración de la deformación en las semanas previas (~10 mm/mes), con énfasis en que la aceleración es más informativa que la velocidad absoluta; última observación ~7 días antes (págs. 138–139).
- Informe **HiRISK (Stimson Center + académicos asiáticos)**: señales de inestabilidad días antes, incluidas imágenes de **Planet Labs del 24 de agosto** que muestran agua de deshielo marrón (indicador de movimiento del lecho rocoso) (pág. 139).
- Registros sísmicos del colapso principal (~M5.2) y reconstrucciones de la secuencia por equipos chinos y otros (pág. 139).
- Literatura pública: "Los estudios ya publicados mencionan candidatos de señales sísmicas en las ~3 horas previas al evento principal" (pág. 151).
- **Datos internos (no públicos, no independientemente verificables)**: señal PE (o métrica informacional) en HHZ detectada 2 h 03 min antes (00:49 UTC); deformación GNSS en KUGE 1 h 40 min antes; afirmación de que la microsismicidad de alta frecuencia precede de forma clara y reproducible a la deformación GNSS medible; cascada formal `DImicro → DImeso → DImacro → fallo`; `A_I(t)` creciente; `R² < 0.4` (págs. 6, 139, 144).

### Sobre Riemann y matemáticas (búsquedas con marcadores "20 sources" y "10 sources")

- **Clay Mathematics Institute** mantiene la Hipótesis de Riemann entre los Problemas del Milenio no resueltos; se han comprobado los primeros **10¹³ ceros**, pero el problema exige demostrarlo para todos (págs. 27–30).
- Reglas del Clay para el premio: publicación en un medio calificable, al menos dos años desde la publicación y aceptación general de la comunidad matemática (pág. 30).
- Trabajos de **agosto 2026 (Planat–Solé y afines)**: afirman que `log L₁[s](x)` es estrictamente cóncava en el dominio positivo, por dos rutas independientes (series theta + cotas de cola; ecuación diferencial de Jacobi) — registrado como "NEW RESULT 2026 (audit required)", no como demostración (pág. 74).
- Existe conflicto entre manuscritos de 2026 y la literatura clásica sobre la clase de Laguerre–Pólya; no se acepta como resolutivo hasta verificar el texto original de Pólya (Satz II) y las hipótesis exactas (pág. 84).
- Desigualdad de Turán clásica para los momentos del núcleo de Ξ establecida "en la literatura de **Csordas–Norfolk–Varga** y trabajos relacionados" (pág. 96).
- **Dimitrov–Lucas, Proc. Amer. Math. Soc. 139, 2011**: establece de forma incondicional las desigualdades de Turán de orden superior para los coeficientes asociados a la función ξ de Riemann, equivalentes a la hiperbolicidad de los polinomios de Jensen de grado 3; normalización compatible (salvo factor positivo global) con la representación del corpus (pág. 99).
- Ejemplo de separación TP₂ ⇏ TP∞: funciones como e^{−x⁴} pueden ser log-cóncavas sin que su transformada coseno tenga solo ceros reales (pág. 70).

### Otras citas

- **KnotProt** "sí contiene miles de estructuras proteicas con nudos, slipknots y knotoids y se actualiza a partir del PDB", pero es evidencia estructural/computacional, no medición experimental directa de g(K) (págs. 25–26, 59).

---

## RESUMEN EJECUTIVO (15 líneas)

El PDF es una larga conversación de diseño (152 pp., con solapamientos y restos de UI de chat) donde el dueño y su agente "TCCU científico (AGI Jairo)" fijan la arquitectura y la disciplina metodológica de **TCCU-C**, el Motor Computacional de Autovalidación y Falsación, pensado como núcleo de un organismo AGI ("AGI Jairo"; el nombre AutoClaw no aparece en el texto). Se decide lanzar TCCU-C v1.0 con seis reglas congeladas (R1 precedencia, R2 cascada, R3 monotonicidad, R4 independencia, R5 estabilidad, R6 umbral a priori), veredictos {VÁLIDO, FALSADO, INCONCLUSO, PENDING_EXTERNAL_VALIDATION} y un ledger que separa el resultado de las reglas del estatus epistemológico de los datos (público vs. candidato); el caso glaciar "Langtang 2026" (señal PE/HHZ 2 h 03 min antes, GNSS KUGE 1 h 40 min antes) queda como candidato, no como confirmación. En paralelo se despliega el AGI-Destructive-Benchmark (banco de 30 pruebas; #7-R01 rechazada, #7-R02 y #12-R01-R no rechazadas solo simuladas, #7-ASTRA-R01 pre-registrada y bloqueada a la espera de acceso real a GPT-6 Astra, auditado sin encontrar evidencia en topología de nudos), con la regla `AGI_J = G·A·T·V·F·P`, F global 0.0 y prohibición de reclamar AGI. Un tercer frente es el Riemann Engine (RH permanece OPEN; se prueban rutas Fourier-coseno, momentos/Hankel, Turán/Jensen d=1–3, theta y un operador L, con 9 resultados anclados y la barrera identificada: el paso al orden infinito/clase Laguerre–Pólya). Un cuarto frente formaliza TCCU-Iorg (información organizadora pre-neural en desarrollo embrionario: dinámica con γ, discordancia D(t); v0.3 congelada, v0.4 como banco sintético obligatorio con control de falsos positivos ≤5 %). El corpus termina con una propuesta de lanzamiento público (TCCU-AGI v1.0 Scientific Falsification Engine open-source, repo con core/simulator/falsifier/comparator/ledger) y un pipeline Python ciego listo (NK.KKN HHZ: espectrograma → PE 2–20 Hz → PELT) aún sin ejecutar. Para "integrar al núcleo central operativo distribuido" habría que construir: el motor Python (engine + ledger + 6 reglas), el endpoint /api/falsacion, el registro inmutable de pre-registros y veredictos, el banco de 30 pruebas con sus contratos sellados, el módulo Riemann con su ledger de estados, el pipeline TCCU-Iorg v0.4 y los scripts PE/CPA, manteniendo la separación estricta de clases de evidencia y la actualización de factores G, A, T, V, F, P solo tras ejecuciones reales independientes.

---

*Informe generado a partir de la lectura íntegra de `mas_pdf_primeras.txt`, `mas_pdf_13_80.txt` y `mas_pdf_81_152.txt`. Las referencias de página corresponden a los marcadores `=== PAG N ===` de los archivos. Las fórmulas se transcriben normalizadas (una instancia por fórmula) por artefactos de duplicación de la extracción.*
