# tccu_hed_robustez_analisis.py — Análisis de la campaña de robustez N=10^4
# Lee hed_robustez_{A..E}.jsonl; compara contra summary_v1_3.json (N=80):
#  1) ¿Persiste la transición A->B->C->D->E (P_ret, supervivencia, clases) a N=10^4?
#  2) Regiones F (P_ret<1e-6) y P (P_ret>1e-3) — falsabilidad interna a escala.
#  3) Estabilidad estadística: IC bootstrap de P_ret (1000 remuestras).
#  4) Evolución con el horizonte (10 -> 50 -> 100 Myr): ¿cambia el ordenamiento?
import json, sys, numpy as np, os

BASE = r"C:\Users\Jairo Omar\AGI_Workspace"

def load(esc):
    p = os.path.join(BASE, "hed_robustez_%s.jsonl" % esc)
    out = {}
    if not os.path.exists(p):
        return out
    with open(p, encoding="utf-8") as f:
        for line in f:
            try:
                c = json.loads(line); out[c["horizon"]] = c
            except Exception:
                pass
    return out

def boot_ci(values, n_boot=1000, seed=5):
    v = np.asarray(values)
    rng = np.random.default_rng(seed)
    m = rng.choice(v, size=(n_boot, len(v)), replace=True).mean(axis=1)
    return float(np.percentile(m, 2.5)), float(np.percentile(m, 97.5))

def main():
    escs = "ABCDE"
    data = {e: load(e) for e in escs}
    # referencia N=80
    ref = json.load(open(os.path.join(BASE, "summary_v1_3.json"), encoding="utf-8"))["scenarios"]
    print("=" * 78)
    print("ROBUSTEZ TCCU-HED v1.3 — N=10^4 vs N=80 (horizonte 100 Myr)")
    print("=" * 78)
    print("%-3s | %-10s | %-12s | %-10s | %-24s" % ("Esc", "Surv 1e4/80", "P_ret 1e4/80", "frac>1e-3", "Clases dominantes 1e4"))
    for e in escs:
        c = data[e].get(100.0)
        if not c:
            print("%s | (pendiente)" % e); continue
        r = ref[e]
        cl = sorted(c["clases"].items(), key=lambda kv: -kv[1])[:2]
        print("%-3s | %8.4f/%.4f | %10.3e/%.3e | %9.3f | %s" % (
            e, c["survival"], r["survival_rate"], c["mean_P_ret_all"], r["mean_final_P_ret"],
            c["frac_P_gt_1e-3"], ", ".join("%s %.2f" % (k, v) for k, v in cl)))
    # ordenamiento de P_ret y supervivencia (persistencia de la transicion)
    print("\nORDENAMIENTO A->E por P_ret (100 Myr):")
    orden_ref = sorted(escs, key=lambda e: ref[e]["mean_final_P_ret"])
    orden_n10k = sorted([e for e in escs if 100.0 in data[e]], key=lambda e: data[e][100.0]["mean_P_ret_all"])
    print("  N=80 :", " ".join(orden_ref))
    print("  N=1e4:", " ".join(orden_n10k), "->", "PERSISTE" if orden_ref == orden_n10k else "CAMBIA")
    print("\nREGIONES F/P (N=1e4, 100 Myr):")
    for e in escs:
        c = data[e].get(100.0)
        if c:
            reg = "F (P_ret<1e-6)" if c["mean_P_ret_all"] < 1e-6 else ("P (P_ret>1e-3)" if c["frac_P_gt_1e-3"] > 0.5 else "transicion")
            print("  %s: P_ret=%.2e frac>1e-3=%.3f -> %s" % (e, c["mean_P_ret_all"], c["frac_P_gt_1e-3"], reg))
    # evolucion con horizonte
    print("\nEVOLUCION CON HORIZONTE (surv | P_ret):")
    for e in escs:
        row = []
        for H in [10.0, 50.0, 100.0]:
            c = data[e].get(H)
            row.append("%s:%.2f/%.1e" % ("h%d" % H, c["survival"], c["mean_P_ret_all"]) if c else "h%d:--" % H)
        print("  %s: %s" % (e, " | ".join(row)))
    print("\nNOTA: la campana aun puede estar en curso; las celdas ausentes apareceran al completarse.")

if __name__ == "__main__":
    main()
