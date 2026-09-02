# repro_hed_v1_4.py — R1 del pre-registro HED-F v1.4
# Reproduccion INDEPENDIENTE del bloque principal de v1.3 (fisica congelada, sin main()).
# Importa tccu_hed_v1_3.py como modulo (no modifica nada), ejecuta run_monte_carlo
# A-E con N=80, t=100 Myr, dt=0.025, seed=42+ord(key), y compara contra summary_v1_3.json
# con estimacion de ruido MC por bootstrap (intervalo ~2sigma de la propia muestra).
# Salida: repro_R1.json (resultados + comparacion + veredicto R1)
import json, sys, os, hashlib, importlib.util
import numpy as np

BASE = r"C:\Users\Jairo Omar\AGI_Workspace"
sys.path.insert(0, BASE)

# --- cargar modulo v1.3 SIN ejecutar su main ---
spec = importlib.util.spec_from_file_location("hed13", os.path.join(BASE, "tccu_hed_v1_3.py"))
hed = importlib.util.module_from_spec(spec)
spec.loader.exec_module(hed)

REF = json.load(open(os.path.join(BASE, "summary_v1_3.json"), encoding="utf-8"))
REF_SC = REF["scenarios"]

def sha256f(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for ch in iter(lambda: f.read(65536), b""):
            h.update(ch)
    return h.hexdigest()

def bootstrap_ci(x, n_resamples=1000, q=0.95):
    """IC bootstrap (percentil) de la media; z=2 sigma si la distribucion es normal."""
    x = np.asarray(x, dtype=float)
    rng = np.random.default_rng(1234)
    means = np.array([rng.choice(x, size=len(x), replace=True).mean() for _ in range(n_resamples)])
    lo, hi = np.percentile(means, 100*(1-q)/2), np.percentile(means, 100*(1+q)/2)
    return float(lo), float(hi)

out = {"paso": "R1", "pre_registro": "PREREGISTRO_HED_v1.4.md", "fecha": "2026-09-01"}
out["hashes"] = {
    "tccu_hed_v1_3.py": sha256f(os.path.join(BASE, "tccu_hed_v1_3.py")),
    "summary_v1_3.json": sha256f(os.path.join(BASE, "summary_v1_3.json")),
}
out["config"] = {"N": 80, "t_max_myr": 100.0, "dt_myr": 0.025, "checkpoints": [10,25,50,75,100]}

checkpoints = [10.0, 25.0, 50.0, 75.0, 100.0]
resultados = {}
comparacion = {}
veredictos = {}

for key in ["A", "B", "C", "D", "E"]:
    res = hed.run_monte_carlo(key, n_realizations=80, t_max_myr=100.0, dt_myr=0.025,
                              seed=42 + ord(key), checkpoints=checkpoints)
    s = res["summary"]
    resultados[key] = s
    ref = REF_SC[key]
    # bootstrap sobre las realizaciones (finals) para P_ret final
    P_final = np.asarray(res["finals"]["final_P_ret"], dtype=float)
    lo, hi = bootstrap_ci(P_final)
    # P_ret medio de la referencia (final) — el summary guarda mean_final_P_ret
    ref_P = ref["mean_final_P_ret"]
    dentro = (lo <= ref_P <= hi) or abs(s["mean_final_P_ret"] - ref_P) <= max(1e-12, 0.1*abs(ref_P))
    # supervivencia
    surv_ok = abs(s["survival_rate"] - ref["survival_rate"]) < 0.05
    comparacion[key] = {
        "P_ret_ref": ref_P, "P_ret_repro": s["mean_final_P_ret"],
        "P_ret_IC95": [lo, hi], "P_ret_dentro_IC": bool(dentro),
        "surv_ref": ref["survival_rate"], "surv_repro": s["survival_rate"], "surv_ok": bool(surv_ok),
        "clases_ref": ref["descent_fractions"], "clases_repro": s["descent_fractions"],
    }
    veredictos[key] = "PASS" if (dentro and surv_ok) else ("FAIL" if (not dentro and not surv_ok) else "INCONCLUSIVE")
    print("%s: P_ret ref=%.3e repro=%.3e IC95=[%.1e,%.1e] dentro=%s | surv %.3f->%.3f | %s" % (
        key, ref_P, s["mean_final_P_ret"], lo, hi, dentro, ref["survival_rate"], s["survival_rate"], veredictos[key]))

n_pass = sum(1 for v in veredictos.values() if v == "PASS")
out["resultados"] = resultados
out["comparacion"] = comparacion
out["veredictos_por_escenario"] = veredictos
out["veredicto_R1"] = ("PASS" if n_pass == 5 else ("FAIL" if n_pass <= 2 else "INCONCLUSIVE"))
out["nota"] = "Ningun PASS individual valida; R1 es reproducibilidad del bloque v1.3."

with open(os.path.join(BASE, "repro_R1.json"), "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
out["repro_R1_sha256"] = sha256f(os.path.join(BASE, "repro_R1.json"))
with open(os.path.join(BASE, "repro_R1.json"), "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("R1 veredicto:", out["veredicto_R1"], "| sha256:", out["repro_R1_sha256"][:16])
