#!/usr/bin/env python3
"""
generar_run_ids.py — Infraestructura de reproducibilidad (v0.3, auditoria)
==========================================================================
Extrae RUN_IDs REALES de las campanas ejecutadas (no inventados):
  RUN_ID = SHA256(script + parametros + versiones + resumen del resultado)[:16]
Genera:
  reproducibility/
    environment.yml, requirements-lock.txt, RUNS.md, hashes.sha256
    <CAMPAÑA>/RUN_ID.txt, parameters.json, result.json
Uso: python generar_run_ids.py
"""

import hashlib
import json
import os
import platform
import sys
import datetime

import numpy
import scipy
import matplotlib

try:
    from importlib.metadata import version as _v
    VER = {p: _v(p) for p in ["numpy", "scipy", "matplotlib"]}
except Exception:
    VER = {"numpy": numpy.__version__, "scipy": scipy.__version__,
           "matplotlib": matplotlib.__version__}

AQUI = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(AQUI)
DATA = os.path.join(REPO, "data")
REPRO = os.path.join(REPO, "reproducibility")

CAMPAÑAS = {
    "M3B": {
        "script": "numerics/barrido_m3b.py",
        "resultado": "data/barrido_m3b.json",
        "params": {
            "modelo": "TCCU-Cosmic-Attractor", "version": "v4.1",
            "potencial": "exponencial V0 e^{-lambda phi}", "xi": 0.0,
            "Lambda": 0.15, "V0": 1.0,
            "rejilla": {"alpha": "[2,10] paso 0.5 (17)", "lambda": "[0.5,3] paso 0.1 (26)"},
            "F2": {"eps_w": 0.05, "eps_rho": 0.05, "DeltaN_min": 4.0, "a<1": True},
            "n_configuraciones": 442,
        }},
    "M3C": {
        "script": "numerics/barrido_m3c.py",
        "resultado": "data/barrido_m3c.json",
        "params": {
            "modelo": "TCCU-Cosmic-Attractor", "version": "v4.1",
            "potencial": "inverso-potencia V0 Phi^{-n}", "xi": 0.0,
            "rejilla": {"n": "logspace[0.25,10] (28)", "Lambda": "[0.05..1.0] (6)"},
            "F2": {"eps_w": 0.05, "eps_rho": 0.05, "DeltaN_min": 4.0, "a<1": True},
            "n_configuraciones": 168,
        }},
    "M3D": {
        "script": "numerics/barrido_m3d.py",
        "resultado": "data/barrido_m3d.json",
        "params": {
            "modelo": "TCCU-Cosmic-Attractor", "version": "v4.1",
            "potencial": "meseta + doble-exponencial", "xi": 0.0,
            "rejilla": {"meseta_lam": "[1,2,3,5,8]", "doble_exp": "3x3",
                        "Lambda": "[0.15,0.3,0.5]"},
            "F2": {"eps_w": 0.05, "eps_rho": 0.05, "DeltaN_min": 4.0, "a<1": True},
            "n_configuraciones": 24,
        }},
    "M4": {
        "script": "numerics/barrido_m4.py",
        "resultado": "data/barrido_m4.json",
        "params": {
            "modelo": "TCCU-Cosmic-Attractor", "version": "v4.1",
            "potencial": "exponencial lam=5 (congelado)", "xi": "12 valores",
            "rejilla": {"xi": "[-0.20..0.20] (12)", "Lambda": "[0.05..1.0] (9)"},
            "F2": {"eps_w": 0.05, "eps_rho": 0.05, "DeltaN_min": 4.0, "a<1": True},
            "filtros": {"M4-1": "F>0, A>0", "M4-2": "Q_s>0, c_s2_full in (0,1]",
                        "M4-3": "G_eff y Gdot_G"},
            "n_configuraciones": 108,
        }},
    "M6IC": {
        "script": "numerics/barrido_m6ic.py",
        "resultado": "data/barrido_m6ic.json",
        "params": {
            "modelo": "TCCU-Cosmic-Attractor", "version": "v4.1",
            "potencial": "exponencial lam=5", "xi": 0.0, "Lambda": 0.15,
            "rejilla": {"Phi_0": "[0.3..3.0] (8)", "u_0": "[-2..5] (9)"},
            "F2": {"eps_w": 0.05, "eps_rho": 0.05, "DeltaN_min": 4.0, "a<1": True},
            "n_configuraciones": 72,
        }},
    "ALPHAIC": {
        "script": "numerics/barrido_alpha_ic.py",
        "resultado": "data/barrido_alpha_ic.json",
        "params": {
            "modelo": "TCCU-Cosmic-Attractor", "version": "v4.1",
            "potencial": "exponencial lam=5", "xi": 0.0, "Lambda": 0.15,
            "rejilla": {"alpha": "[3,5,6.25]", "IC": "3x4"},
            "F2": {"eps_w": 0.05, "eps_rho": 0.05, "DeltaN_min": 4.0, "a<1": True},
            "n_configuraciones": 36,
        }},
}


def sha256_text(t):
    return hashlib.sha256(t.encode("utf-8")).hexdigest()


def main():
    os.makedirs(REPRO, exist_ok=True)
    env = {
        "python": sys.version.split()[0],
        "numpy": VER["numpy"], "scipy": VER["scipy"],
        "matplotlib": VER["matplotlib"],
        "os": platform.system() + " " + platform.release(),
        "solver": "scipy.integrate.solve_ivp (RK45, dense output)",
        "rtol": "1e-8/1e-9 segun campana", "atol": "1e-10/1e-11/1e-12",
        "semilla": "determinista (sin RNG en los barridos)",
        "fecha_generacion": datetime.datetime.now().astimezone().isoformat(),
    }

    filas = []
    for camp in CAMPAÑAS:
        info = CAMPAÑAS[camp]
        src = open(os.path.join(REPO, info["script"]), "r", encoding="utf-8").read()
        res = json.load(open(os.path.join(REPO, info["resultado"]), "r",
                             encoding="utf-8"))
        # resumen estructural del resultado (sin dependencia de orden interno)
        n_total = len(res.get("puntos", []))
        resumen = json.dumps({
            "campana": camp, "n_total": n_total,
            "n_exitos": res.get("n_exitos", 0),
            "mejor": res.get("mejor"),
        }, sort_keys=True)
        run_id = sha256_text(src + "|" + json.dumps(info["params"], sort_keys=True)
                             + "|" + resumen + "|" + VER["numpy"] + VER["scipy"])[:16]

        carpeta = os.path.join(REPRO, camp)
        os.makedirs(carpeta, exist_ok=True)
        with open(os.path.join(carpeta, "RUN_ID.txt"), "w") as f:
            f.write(run_id + "\n")
        with open(os.path.join(carpeta, "parameters.json"), "w",
                  encoding="utf-8") as f:
            json.dump(info["params"], f, ensure_ascii=False, indent=2)
        with open(os.path.join(carpeta, "result.json"), "w", encoding="utf-8") as f:
            json.dump(res, f, ensure_ascii=False, indent=2)

        # hash del resultado completo
        h = hashlib.sha256(open(os.path.join(carpeta, "result.json"), "rb").read()).hexdigest()
        filas.append({"campana": camp, "RUN_ID": run_id,
                      "n_configuraciones": info["params"]["n_configuraciones"],
                      "F2_sostenido": res.get("n_exitos", 0),
                      "sha256_resultado": h})

    # hashes.sha256
    with open(os.path.join(REPRO, "hashes.sha256"), "w") as f:
        for r in filas:
            f.write(f"{r['sha256_resultado']}  {r['campana']}/result.json\n")

    # environment.yml + requirements-lock.txt
    with open(os.path.join(REPRO, "environment.yml"), "w") as f:
        f.write(f"name: tccu-falsacion\nchannels: [conda-forge]\ndependencies:\n"
                f"  - python={env['python']}\n  - numpy={env['numpy']}\n"
                f"  - scipy={env['scipy']}\n  - matplotlib={env['matplotlib']}\n")
    with open(os.path.join(REPRO, "requirements-lock.txt"), "w") as f:
        for p in ["numpy", "scipy", "matplotlib"]:
            f.write(f"{p}=={VER[p]}\n")

    # RUNS.md
    with open(os.path.join(REPRO, "RUNS.md"), "w", encoding="utf-8") as f:
        f.write("# RUNS — campañas de falsación (auditoría v0.3)\n\n")
        f.write(f"Entorno: python {env['python']} | numpy {env['numpy']} | "
                f"scipy {env['scipy']} | matplotlib {env['matplotlib']} | "
                f"{env['os']}\n")
        f.write(f"Solver: {env['solver']}\n\n")
        f.write("| Campaña | RUN_ID | Configs | F2 sostenido | SHA-256(resultado) |\n")
        f.write("|---|---|---|---|---|\n")
        for r in filas:
            f.write(f"| {r['campana']} | {r['RUN_ID']} | {r['n_configuraciones']} "
                    f"| {r['F2_sostenido']} | {r['sha256_resultado'][:16]}… |\n")
        total = sum(r["n_configuraciones"] for r in filas)
        f2 = sum(r["F2_sostenido"] for r in filas)
        f.write(f"\n**Total: {total} configuraciones evaluadas bajo el conjunto de "
                f"protocolos M3b–M6-IC; {f2} F2 sostenido (within the explored "
                f"model and initial-condition domain).**\n")

    print(f"[OK] reproducibility/ generada: {len(filas)} campanas, "
          f"{sum(r['n_configuraciones'] for r in filas)} configuraciones.")
    for r in filas:
        print(f"  {r['campana']:<8} {r['RUN_ID']}  configs={r['n_configuraciones']} "
              f"F2={r['F2_sostenido']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
