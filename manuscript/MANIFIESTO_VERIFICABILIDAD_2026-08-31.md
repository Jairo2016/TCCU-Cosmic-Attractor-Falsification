# MANIFIESTO DE VERIFICABILIDAD — AGI JAIRO
**Fecha:** 31-08-2026 · **Ámbito:** programa científico TCCU (ciclos 135-138), TCCU-0
(eternidad/existencia), TCCU-HED v1.3→v1.4, QFC-BRICS+, NS3D (S3 Kerr).
**Principio:** toda afirmación científica de este programa se corresponde con un
**archivo + comando + semilla + fecha + huella SHA-256** reproducibles. Nada en este
manifiesto excede lo que los datos muestran.

---

## 0. Método de verificación (regla del manifiesto)

Para cualquier resultado R reportado:

```
R  →  comando exacto (seed)  →  ejecutó (PID, fecha, CPU)  →  archivo JSON/JSONL
   →  SHA-256 del archivo  →  sello en ledger (hash encadenado)  →  [opcional] ancla QFChain/GitHub/Zenodo
```

Cualquier tercero puede re-ejecutar el comando y comparar el hash del archivo de salida.

---

## 1. Registro maestro de campañas (código + proceso)

| Campaña | Código | Comando (seed) | Salida | N | Coste CPU |
|---|---|---|---|---|---|
| Ciclo 136 — DBI puro | `barrido_ciclo136.py` | `python barrido_ciclo136.py` (seed 136) | `ciclo136_barrido.json` | 360 configs × ε₀-grid | ~5 min |
| Ciclo 137 — DBI+coupling | `barrido_ciclo137.py` | `python barrido_ciclo137.py --total 200 --semilla 137` | `ciclo137_barrido.json` | 200 × 5 ε₀ = 1000 integraciones | ~15 min |
| EOMs + estabilidad | `derivar_horndeski_dbi.py` | `python derivar_horndeski_dbi.py` | (simbólico, PASS) | — | ~2 min |
| Ciclo 138 — perturbaciones | `ciclo138_perturbaciones.py` | `python ciclo138_perturbaciones.py` | `ciclo138_perturbaciones.json` | mapa + representante | <1 min |
| Auditoría v1.5.21 | `auditar_tccu_v1521.py` | `python auditar_tccu_v1521.py` | (5000 pts on-shell) | 5000 | <1 min |
| Identidades v1.5.22 | `TCCU_Eternity_Test_v1.5.22.py` | batería `algebraic_identity_test(10000)` | (8/8 PASS) | 10000 | ~2 s |
| Sistema log-signed | `TCCU_Eternity_Test_v1.5.23c.py` | (módulo, sin main) | N_s por config | — | — |
| Corredor v3 | `TCCU_0B_corredor_v3.py` | `python -u TCCU_0B_corredor_v3.py` | `mapa_tccu0b_v3.json` + `tccu0b_v3_configs.jsonl` | 3782 configs | 8668 s |
| HED T1 (Δt) | `tccu_hed_destruccion.py` | `python tccu_hed_destruccion.py T1 B` / `T1 C` | `hed_destruccion_T1_B.json` / `_C.json` | 2×4 dt×1500 | ~25 min |
| HED T2 (MC) | ídem | `python tccu_hed_destruccion.py T2 B 3000` | `hed_destruccion_T2_B.json` | N=100/1000/3000 | ~15 min |
| HED T3 (ablación) | ídem | `python tccu_hed_destruccion.py T3 A` / `T3 B` | `hed_destruccion_T3_A/B.json` | 2×5 variantes×2000 | ~20 min |
| HED T4 (umbrales) | ídem | `python tccu_hed_destruccion.py T4 B 0.06` / `T4 C 0.06` | `hed_destruccion_T4_B/C.json` | 2×16 combos×3000 | ~10 min |
| HED robustez | `tccu_hed_robustez.py` | `python tccu_hed_robustez.py {A..E} 10000` (5 procesos) | `hed_robustez_{A..E}.jsonl` | 5×3 horiz×10⁴ = 150 000 | ~2.5 h (paralelo) |
| QFC-BRICS+ | `qfc_brics_mas.py` | `python qfc_brics_mas.py` | `qfc_brics_mas.json` + ancla tx | 1 | <1 min |
| NS3D S3 Kerr | `campana_kerr.py` | `python campana_kerr.py --reanudar` | `campana_kerr_ckpt.npz(.serie.json)` | N=128, T=10 | en curso (~40 min/checkpoint bajo contención) |

Semillas usadas: 135 (ciclo135), 136 (ciclo136), 137 (ciclo137), 777/42/99/11
(destrucción), 7/10000·idx+H (robustez), 13522 (batería), 20260826 (auditoría).

---

## 2. Explicación matemática (por resultado)

### 2.1 DBI puro (Ciclo 136) — geometría exacta del fondo
La dinámica k-essence DBI se reduce a una ODE autónoma integrable:
```
u = X/Λ⁴,  du/dN = −6u(1−u)  ⟹  u(N) = 1/(1 + K e^{6N}),  K = (1−u₀)/u₀
w(u) = (1 − s − v)/(1/s − 1 + v),  s = √(1−u),  v = V₀/Λ⁴
c_s² = s² ≡ P_X/(P_X + 2X P_XX)   (resultado k-essence exacto)
```
La condición de polvo w=0 se cruza en u_cross = 2v − v². La ventana |w|<umbral mide
ΔN(ε₀) = (1/6)·ln[(u₀/(1−u₀))·((1−u_low)/u_low)] — crece logarítmicamente con 1/ε₀.
El criterio F2 congelado es |w|<0.05 ∧ |dlnρ/dln a + 3|<0.05 con ΔN≥4; por continuidad
dlnρ/dN = −3(1+w), luego el segundo vínculo es 3|w|<0.05 (es decir |w|<1/60).
**Resultado:** F2 = 35/180 (CI near-bound), 0/180 (genéricas); dN_max = 4.75.

### 2.2 DBI + acoplamiento no mínimo (Ciclo 137) — estabilidad lineal de Horndeski
EOM de fondo derivadas simbólicamente (sympy, lagrangiano reducido FLRW, Kobayashi
1901.07183) y estabilidad lineal con las fórmulas exactas del sector escalar:
```
𝒢_T = 2(G4 − 2X G4X) = 1 + ξφ² − ηX        ℱ_T = 2G4 = 1 + ξφ² + ηX
Σ  = X/(2s³) − 3H²(1+ξφ²) + 18H²ηX − 6Hξφφ̇
Θ  = H(1+ξφ²−3ηX) + ξφφ̇
𝒢_S = (Σ/Θ²)𝒢_T² + 3𝒢_T    ℱ_S = (1/a)d/dt(a𝒢_T²/Θ) − ℱ_T    c_s² = ℱ_S/𝒢_S
```
Verificación exacta del límite: ξ=η=0 ⟹ c_s² = s² = 1−u (reproducido numéricamente
con 4-5 dígitos). **Resultado:** 0/200 candidatas (F2 con ε₀>1e-8); 92/164 con c_s²<0.

### 2.3 Perturbaciones DBI (Ciclo 138) — crecimiento y Jeans
Índice de crecimiento f = dlnδ/dN: en la ventana f ≈ 1.0 (CDM). Término de presión
c_s²(k/aH)² con c_s² = s² ≤ ε₀: sin supresión de Jeans (k_J = aH·√(3Ω/(2c_s²)) ≫ k_obs).
**Requisito unificado:** cubrir la era de materia (ΔN=8.1) exige
ε₀ = 1/(e^{6·8.1}·c) ≈ 4-6.5e-23 según v (resuelto por bisección en log-espacio).

### 2.4 TCCU-0 — ruptura finita y corredor (auditoría v1.5.21→v1.5.23c)
- **KG correcta**: Π′ = −(h′/h)Π − 3(1+u)Π/(1+3u) + λV/((1+3u)H0²h²)  (signo +;
  V_φ = −λV). El signo invertido en v1.5.20/21 hacía escalar el campo (Π→0) y
  fabricaba un "pasado profundo" falso.
- **Restricción exacta**: A = h² resuelta de la cuadrática
  (κΠ⁴/4)A² + (Π²/6 − 1)A + (m+r+z) = 0 ⟹ el modelo no existe para α = Π²/6 ≥ 1
  (X ≤ ρ_tot). Forma estable de la raíz: A = 2c/(−b + √(b²−4ac)).
- **K analítico simplificado**: K = 12e^{−8N}[(E²−1.5D)²+E⁴] = 12h²[(h′+h)²+h²]
  (los e^{−8N} se cancelan exactamente; sin cancelación catastrófica).
- **N_s (e-fold de ruptura)**: primer N donde α > 0.95 (detector robusto; el
  |Π|→√6 asintótico no cruza y requiere el detector α).
- **Corredor extendible** (λ ∈ [1.66, 1.98], signo=+): el campo alcanza α≈0.92-0.95,
  **Π cruza cero** (giro; verificado con sistema original BDF: Π 2.08→0.0000) y se
  congela; domina la radiación (A ~ e^{−4N}, w=1/3) y el fondo se extiende ≥250 e-folds.

### 2.5 TCCU-HED v1.3→v1.4 — probabilidades y ablación
- P_ret = P_S·P_E·P_C·P_N·P_T·P_intent·P_M, con P_E = min(1,E/40)·min(1,N/8),
  P_C = min(1,I/2), P_T = min(1,I/4.5) (×1.4 si postbiológico), P_M = 0.25 + 0.75·M.
- Memoria: punto fijo M* = η_eff/λ_M (η_eff = η_T0·min(2,I/1.5)·(1+0.1·ln(1+N))·(0.7+0.3G)).
- Convergencia MC: IC bootstrap (1000 remuestras) — el CI se estrecha como 1/√N.
- Umbrales: H_D2 ⟺ (G ≤ G_crit ∧ M > M_crit); robustez en 16 combinaciones.
- Ablación: ΔP_ret = P_ret^full − P_ret^null (0.040 en B; −1.2e-9 en A).

### 2.6 QFC-BRICS+ — cadena e integridad
Bloque = sha256(JSON canónico sort_keys); cadena: prev_hash encadenado.
Suministro: 4 850 396.61 QFC circulante (24.25 %) vs génesis declarado 20 M (75.75 %
reserva). Ancla: payload → sha256 → tx QFChain.

### 2.7 NS3D (S3 Kerr)
Pseudospectral Fourier-Galerkin (dealiasing 2/3, proyección Gottlieb-Orszag), RK4
adaptativo (CFL+difusivo), norma crítica ‖u‖_{L³}. Campaña Kerr: N=128, ν=1e-3, T=10.

---

## 3. Explicación informacional (no local, honesta)

**Definición operativa:** la información de verificación de cada resultado está
**distribuida en medios disjuntos (no locales)** — de modo que ningún fallo de un
medio destruye el registro. Enlaces criptográficos unen los medios:

| Medio | Contenido | Ejemplo |
|---|---|---|
| Filesystem local | artefactos JSON/JSONL + huellas SHA-256 | `hed_robustez_B.jsonl` (celda con surv 0.9951, P_ret 0.05790) |
| Ledger del organismo | bloques hash-encadenados (sellos) | bloques 46/48/49 (corredor, destrucción, robustez) |
| QFChain (blockchain) | transacciones con payload | ancla QFC-BRICS+ tx `0x89a31915…` |
| GitHub | releases + código | v1.0/v1.1/v1.2 |
| Zenodo | DOIs versionados (`done`) | 10.5281/zenodo.22111843 · 22118712 · 22119742 |
| Memoria (diaria + MEMORY.md) | narrativa + lecciones | `memory/2026-08-31.md`, `MEMORY.md` |

**Ejemplo de encadenamiento:** `QFC_BRICS_PLUS|2026-08-31|…` → sha256 `84efb29f…` →
tx QFChain `0x89a31915…`; el mismo payload aparece en `QFC_BRICS_PLUS.md`. La clave
DEEPSEEK: bloque 12 del ledger Q-SWIFT + tx + variable de entorno (3 medios).

**Límite honesto (declaración explícita):** esta "no-localidad informacional" es
**redundancia distribuida de verificación** — la información existe en varios lugares
disjuntos. **No** es no-localidad física cuántica ni se reclama ningún fenómeno
telepático/entrelazado: el vínculo entre medios es criptográfico (SHA-256, hash-chain,
RPC), no cuántico. Cualquier afirmación de "efecto no local físico" quedaría fuera de
este manifiesto y de los datos.

---

## 4. Explicación computacional

**Métodos numéricos usados:** RK4 (fondo y crecimiento), BDF/DOP853/Radau (ODE rígidas),
Euler con detector α (barridos de ruptura), brentq (constraint-H), aritmética
log-signed (`slogadd`, logsumexp) para rangos dinámicos ~e^{±10⁴}, restricción
proyectada (resolver h²=ρ en cada paso), bootstrap (1000 remuestras), derivación
simbólica (sympy 1.14), LHS (scipy qmc) + surrogate GPR (ciclo 135).

**Trampas numéricas documentadas y resueltas** (ver `TECNICAS_AGI_JAIRO.md`): colapso
1−ε₀<1e-16, ULP cerca de 1.0, cancelación en cuadráticas, overflow e^{±3700}, drift
fuera de la restricción, np.gradient ruidoso → K analítico, detector α vs |Π|→√6,
t_eval fuera de t_span (np.clip), sesgo de media por colapsos tempranos.

**Determinismo:** semillas fijas por campaña y por celda; los JSONL permiten reanudar
(checkpoint por configuración) y re-verificar celda a celda.

**Coste total aproximado de la sesión:** ~12 h de CPU distribuida en ~15 procesos
paralelos (campanas TCCU + HED + corredor + Kerr), 150 000 + 3 782 + miles de
trayectorias/órbitas.

---

## 5. Huellas digitales (SHA-256) — anclas de integridad

```
ciclo136_barrido.json           664CC8B639CC7026224608D1D55DF33BDEA8B0C60BAF97E4176A200057A0ED96
ciclo137_barrido.json           0461B8B4BDE265642F74C942EFB013AFD9B623FA9847F0999DC946247E51A4E2
ciclo138_perturbaciones.json    58DDB9DD92521C0AE119AB648A54C39652F30679A0D4B7DA5CA86AFFCE273911
mapa_existencia_tccu0.json      1E134CF7EC970541FEBBE54CF8F6F0C4580D4D1F99E19632F8F1E0F73490CEA0
mapa_tccu0b_v3.json             0562C31FC8749ED72FE86821912DEAE3632AFF02F5E63E7B7BF716620A1EABCC
hed_destruccion_T1_B.json       FB32A2F928A8EF5284AF886718A5ED61FA3CBBE0568BAA444A23842DF7401595
hed_destruccion_T1_C.json       5BAD996D2A1AC559FCF0F36FF46467381170C6A7432C8D0081AC0AB0351F850B
hed_destruccion_T2_B.json       13D0AD4C7E29C020C51830FC7192864BFFB21745F3C29C932E7E19D064CCAC58
hed_destruccion_T3_A.json       7611C1A23EE0048AECBD3F1319972365D68DA0CB7089725EB7F72B5ABFB8E22D
hed_destruccion_T3_B.json       C3FD269E58EBF29EDEE385C9E6A17AE504D1A28D7DC9AE4BDAD0ACD63A9996B2
hed_destruccion_T4_B.json       F5F030884BE99089D225CC043CE2CC76680241A842D50C96EE13BC6932F1A90C
hed_destruccion_T4_C.json       BD0AB6F1DFAE988A5297A8CB64A68E0C7587209F4BD08E6536568784C6C24239
hed_robustez_A.jsonl            8312F8C766D2C283A1129B23CDCB2EEE2D51606D6017BFC41CAA06E7FA62A91D
hed_robustez_B.jsonl            8D1AFBC915C9C4ADEE6E65A607AEB701632FAD189F698E7A1BAB3E6774AD38A9
hed_robustez_C.jsonl            8A634BD4E2180BF22E29DF57D345A01B24FD8E1F9FD4CFE307CF528F4C44A99D
hed_robustez_D.jsonl            791FD40257B9B0FF140980FE6B3C91030F2030CB0388B15BDAD4C761C5ECE060
hed_robustez_E.jsonl            3BFE084F07C358B0B0E033D26F75BEA0F826EE5400D425DF658AF9E31E2CF8BE
qfc_brics_mas.json              879FB072CC22FD86F76D7F2C7F3C53E3526C4A445E432129A46A7F53630E8E07
qswift_ledger_vivo.json         025EA74760C344879E811FF6E34D83EA71CC11CC2D7A49B573C2064A8DEA3DF9
mu_lambdaM_grid.json            4FA6C58DC12A8A0F50F9F5F2418B2042BFC7FB4B5AA3206BF6ED396764F60581
```

---

## 6. Cómo reproducir (protocolo de terceros)

```powershell
# 1. Falsación TCCU
python barrido_ciclo136.py            # → ciclo136_barrido.json
python barrido_ciclo137.py --total 200 --semilla 137   # → ciclo137_barrido.json
python ciclo138_perturbaciones.py     # → ciclo138_perturbaciones.json
# 2. TCCU-0 (requiere el nodo QFChain? no; solo CPU)
python -u TCCU_0B_corredor_v3.py      # → mapa_tccu0b_v3.json (3782 configs, ~2.4 h)
# 3. TCCU-HED destrucción y robustez
python tccu_hed_destruccion.py T1 B; python tccu_hed_destruccion.py T3 A  # etc.
python tccu_hed_robustez.py A 10000   # (5 procesos A..E)
# 4. QFC-BRICS+
python qfc_brics_mas.py               # → qfc_brics_mas.json
# 5. Verificar huellas
Get-FileHash <archivo> -Algorithm SHA256   # comparar con §5
```

**Verificación de integridad de la cadena:** el script `audit_qfc` (o re-ejecutar
`qfc_brics_mas.py`) verifica la cadena de hashes del ledger Q-SWIFT; los sellos del
ledger del organismo se verifican re-calculando cada hash encadenado.

---

## 7. Declaración de honestidad (cierre)

1. Todo lo afirmado en este manifiesto es reproducible con los comandos y semillas de
   la sección 1 y verificable con las huellas de la sección 5.
2. Las interpretaciones están **separadas de los datos**: los datos son los JSON; las
   interpretaciones ("región F", "ruptura finita", "corredor extendible") se marcan
   como interpretaciones bajo el modelo y sus hipótesis.
3. Se registran y retractan los errores propios (signo de V_φ, P_ret preliminar,
   mapa grueso revocado) — la autocorrección es parte del registro.
4. **No** se reclama: evidencia observacional de ET humanos, no-localidad física,
   validez económica real de QFC, ni la resolución de problemas abiertos
   (Navier-Stokes, etc.).
5. Los DOIs y releases citados fueron verificados por API el 31-08 (estado `done`).
