# INSTRUCCIONES DE PUBLICACIÓN — GitHub + DOI (Zenodo)

**Ejecutor:** Jairo Omar González Navia (manos del organismo) · **Preparado por:** AutoClaw
**Repo local:** `TCCU-Cosmic-Attractor-Falsification-v1.0/` (commit inicial listo)

---

## 1. Crear el repositorio en GitHub (web)

1. https://github.com → **New repository**
2. Nombre: `TCCU-Cosmic-Attractor-Falsification`
3. **Public** · NO crear README / .gitignore / LICENSE (ya vienen en el commit)

## 2. Subir (PowerShell)

```powershell
cd "C:\Users\Jairo Omar\AGI_Workspace\TCCU-Cosmic-Attractor-Falsification-v1.0"
git remote add origin https://github.com/TU_USUARIO/TCCU-Cosmic-Attractor-Falsification.git
git push -u origin main
```

*Reemplaza `TU_USUARIO`. El primer push abre el navegador (Git Credential Manager) para iniciar sesión en GitHub.*

## 3. DOI automático (Zenodo ↔ GitHub)

1. https://zenodo.org → **Log in** → **GitHub** (misma cuenta) → autorizar
2. Zenodo → **Settings → GitHub** → activar `TCCU-Cosmic-Attractor-Falsification`
3. GitHub → repo → **Releases → Create a new release**:
   - Tag: `v1.0` · Título: `v1.0` · Notas: resumen de depósito (ver `METADATOS_ZENODO.md`)
4. Zenodo crea el registro y asigna el **DOI** (`10.5281/zenodo.…`)

## 4. Después del DOI

Pegar el DOI a AutoClaw → actualiza `CITATION.cff`, memoria y ancla en QFChain.
