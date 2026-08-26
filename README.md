# TCCU-Cosmic-Attractor-Falsification v1.0

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.22111843.svg)](https://doi.org/10.5281/zenodo.22111843)

**Falsación Sistemática del Atractor Cósmico TCCU como Mecanismo de Sector
Oscuro Unificado** — Un Estudio Computacional Reproducible de Tracking Tipo
Polvo, Atrapamiento Dinámico y Dependencia de las Condiciones Iniciales.

**Autor:** Jairo Omar González Navia (Quindío, Colombia — zona postal 632007)
**Ejecución computacional:** AutoClaw (organismo distribuido AGI Jairo)
**Fecha:** 25-08-2026 · **Licencia:** CC BY 4.0

> **Declaración de alcance:** falsación dentro de un espacio de modelos
> computacionalmente explorado, **no** una falsación observacional de TCCU.

## Contenido

- `paper/` — manuscrito v1.0 (español + inglés)
- `manuscript/` — versión de auditoría v0.3 (contenido científico idéntico)
- `reproducibility/` — RUN_IDs, entorno, hashes, RUNS.md (auditable)
- `validation/` — informes de falsación por campaña (M3B–M6IC, ALPHAIC)
- `data/` — resultados numéricos completos (barrido_*.json)
- `figures/` — figura central Q2 (cruce transitorio)

## Resultado central

**850 configuraciones evaluadas bajo el conjunto de protocolos M3b–M6-IC;
0 F2 sostenido** (within the explored model and initial-condition domain).
Alcanzabilidad ≠ estabilidad ≠ atracción.

## Reproducir

```powershell
# entorno
conda env create -f reproducibility/environment.yml
# verificar hashes
certutil -hashfile reproducibility/hashes.sha256 SHA256
# auditoria de integridad
python TCCU-Cosmic-Attractor/auditoria_integridad.py
```

## Citar

Ver `CITATION.cff` o: González Navia, J. O. & AutoClaw (2026). *Falsación
Sistemática del Atractor Cósmico TCCU como Mecanismo de Sector Oscuro
Unificado* (v1.0). DOI: [10.5281/zenodo.22111843](https://doi.org/10.5281/zenodo.22111843)


## Actualizacion 2026-08-26 (ciclos 135-136)

Ver `manuscript/ACTUALIZACION_CICLOS_135_136.md`: expansion parametrica (200 configs, 0 F2a, dN_max 0.36) y DBI/cinetica pura con el primer DeltaN>=4 del programa (F2 35/180 con CI near-bound, dN_max 4.75; 0/180 con CI genericas).