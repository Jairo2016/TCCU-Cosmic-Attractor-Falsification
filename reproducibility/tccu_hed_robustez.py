# tccu_hed_robustez.py — CAMPAÑA DE ROBUSTEZ TCCU-HED v1.3
# 10^4 realizaciones por (escenario, horizonte) en {10, 50, 100} Myr.
# Objetivo: intentar ROMPER el modelo — ¿persiste la transición A->B->C->D->E
# (en P_ret, supervivencia, clases) al pasar de N=80 a N=10^4?
# Checkpoint por celda (JSONL por escenario), reanudable.
# Uso: python tccu_hed_robustez.py <ESCENARIO> [N_REAL]
import numpy as np, sys, os, json, time
sys.path.insert(0, r"C:\Users\Jairo Omar\AGI_Workspace")
os.chdir(r"C:\Users\Jairo Omar\AGI_Workspace")
from tccu_hed_v1_3 import ScenarioParams, simulate_trajectory, SCENARIOS

ESC = sys.argv[1].upper()
N_REAL = int(sys.argv[2]) if len(sys.argv) > 2 else 10000
DT = 0.025
HORIZONS = [100.0, 50.0, 10.0]
OUT = r"C:\Users\Jairo Omar\AGI_Workspace\hed_robustez_%s.jsonl" % ESC

base = SCENARIOS[ESC]
done = {}
if os.path.exists(OUT):
    with open(OUT, encoding="utf-8") as f:
        for line in f:
            try:
                c = json.loads(line); done[c["horizon"]] = c
            except Exception:
                pass

for H in HORIZONS:
    if H in done:
        print("  [%s] horizonte %.0f ya hecho (%.0f real)" % (ESC, H, done[H]["n_real"]), flush=True)
        continue
    p = ScenarioParams(name=ESC, description="robustez", v_e=base.v_e, lambda_c0=base.lambda_c0,
        mu=base.mu, alpha_info=base.alpha_info, beta_loss=base.beta_loss,
        gamma_trans=base.gamma_trans, resilience=base.resilience, tech_mod=base.tech_mod,
        P_return_intent=base.P_return_intent, lambda_M=base.lambda_M, eta_T0=base.eta_T0,
        seed_colonies=base.seed_colonies, max_colonies=base.max_colonies)
    rng = np.random.default_rng(int(10000 * (ord(ESC) - 64) + H))
    t0 = time.time()
    cnt = {"H_D1": 0, "H_D2": 0, "H_D3": 0, "H_none": 0}
    Gs, Ms, Ds, Prets, surv = [], [], [], [], []
    cps = {str(cp): {"G": [], "M": [], "P_ret": [], "alive": []} for cp in [10.0, 25.0, 50.0, 75.0, 100.0]}
    for i in range(N_REAL):
        traj = simulate_trajectory(p, H, DT, rng, checkpoints=[10.0, 25.0, 50.0, 75.0, 100.0])
        f = traj["final"]
        cnt[f["descent_class"]] = cnt.get(f["descent_class"], 0) + 1
        Gs.append(f["final_G"]); Ms.append(f["final_M"]); Ds.append(f["final_D"])
        Prets.append(f["final_P_ret"]); surv.append(int(f["survived"]))
        for cp, st in traj["checkpoints"].items():
            cps[str(cp)]["G"].append(st["G"]); cps[str(cp)]["M"].append(st["M"])
            cps[str(cp)]["P_ret"].append(st["P_ret"]); cps[str(cp)]["alive"].append(int(st["alive"]))
        if (i + 1) % 2000 == 0:
            print("  [%s] h=%.0f %d/%d (%.0f s)" % (ESC, H, i + 1, N_REAL, time.time() - t0), flush=True)
    n = N_REAL
    Gs = np.array(Gs); Ms = np.array(Ms); Prets = np.array(Prets); surv = np.array(surv)
    Ds = np.array(Ds)   # FIX 31-08: Ds era lista -> crash en la agregacion tras 10^4 realizaciones
    # estadisticas: todas vs supervivientes
    msk = surv == 1
    cell = {
        "escenario": ESC, "horizon": H, "n_real": n, "dt": DT,
        "survival": float(surv.mean()),
        "mean_G_all": float(Gs.mean()), "mean_G_surv": float(Gs[msk].mean()) if msk.any() else None,
        "mean_D_all": float(Ds.mean()), "mean_D_surv": float(np.array(Ds)[msk].mean()) if msk.any() else None,
        "mean_M_all": float(Ms.mean()), "mean_M_surv": float(Ms[msk].mean()) if msk.any() else None,
        "mean_P_ret_all": float(Prets.mean()),
        "mean_P_ret_surv": float(Prets[msk].mean()) if msk.any() else None,
        "frac_P_gt_1e-3": float((Prets > 1e-3).mean()),
        "frac_P_gt_1e-6": float((Prets > 1e-6).mean()),
        "clases": {k: v / n for k, v in cnt.items()},
        "checkpoints": {cp: {"mean_G": float(np.mean(v["G"])), "mean_M": float(np.mean(v["M"])),
                             "mean_P_ret": float(np.mean(v["P_ret"])), "frac_alive": float(np.mean(v["alive"]))}
                        for cp, v in cps.items()},
        "segundos": round(time.time() - t0, 1),
    }
    with open(OUT, "a", encoding="utf-8") as f:
        f.write(json.dumps(cell, ensure_ascii=False) + "\n"); f.flush()
    print("  [%s] h=%.0f COMPLETO: surv=%.4f P_ret=%.3e fracP=%.3f clases=%s (%.0f s)" % (
        ESC, H, cell["survival"], cell["mean_P_ret_all"], cell["frac_P_gt_1e-3"],
        {k: round(v, 3) for k, v in cnt.items()}, time.time() - t0), flush=True)
print("ESCENARIO %s TERMINADO" % ESC, flush=True)
