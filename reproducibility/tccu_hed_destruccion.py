# tccu_hed_destruccion.py — PRUEBAS DE DESTRUCCIÓN DE TCCU-HED v1.3 (auditoría v1.4)
# Copia fiel de step_civilization con compuertas de ablacion (no modifica la fisica original).
# Pruebas:
#  T1 convergencia en dt (0.1, 0.05, 0.025, 0.0125) -> P_ret, G, M
#  T2 convergencia MC (N = 1e2, 1e3, ...) con IC bootstrap
#  T3 ablacion: full / no_info_surv / no_recovery / no_memory / null -> Delta P_ret
#  T4 robustez de umbrales: G_crit x M_crit in {0.01,0.05,0.1,0.2} (reclasificacion)
# Uso: python tccu_hed_destruccion.py <T1|T2|T3|T4> [ESC] [N_EXTRA]
import numpy as np, sys, os, json, time
sys.path.insert(0, r"C:\Users\Jairo Omar\AGI_Workspace")
os.chdir(r"C:\Users\Jairo Omar\AGI_Workspace")
from tccu_hed_v1_3 import ScenarioParams, CivilizationState, SCENARIOS, compute_return_probability
# NOTA (31-08): se usa la P_ret OFICIAL del modelo (P_M = 0.25 + 0.75*M, boost
# postbiologico, muertos -> 0). Una version propia con P_M = min(1, M/0.2) produjo
# numeros incoherentes con la referencia (robustez/N=80) y un "P_ret=0 sin memoria"
# falso: con la oficial queda P_M=0.25 -> P_ret ~ 0.0075 (B). T4 (umbrales) no
# depende de P_ret (solo G, M) y queda valido.


def step_abl(state, params, dt, rng, abl):
    """Copia fiel de step_civilization con compuertas de ablacion."""
    new = CivilizationState(N=state.N, R=state.R, M=state.M,
                            A=state.A, I=state.I, E=state.E, B=state.B,
                            tau=state.tau, alive=state.alive,
                            postbiological=state.postbiological,
                            D_genetic=state.D_genetic, G_ancestry=state.G_ancestry)
    # --- Expansion ---
    new.E = state.E + params.v_e * dt
    growth = 0.08 * (1.0 - state.N / max(1, params.max_colonies)) * params.resilience
    birth = rng.poisson(max(0.0, growth * state.N * dt * 8))
    death_p = min(1.0, params.lambda_c0 * (1.0 - 0.5 * params.resilience) * dt)
    death = rng.binomial(state.N, death_p) if state.N > 0 else 0
    new.N = max(0, state.N + birth - death)
    if new.N == 0:
        new.alive = False
        return new
    # --- Distancia genetica ---
    mu_eff = params.mu * params.tech_mod
    new.D_genetic = state.D_genetic + mu_eff * dt
    new.G_ancestry = float(np.exp(-new.D_genetic))
    # --- Informacion ---
    gen = params.alpha_info * (1.0 + 0.4 * params.resilience)
    loss = params.beta_loss * (1.0 - 0.3 * params.resilience)
    trans = params.gamma_trans * params.resilience
    new.I = max(0.01, state.I + (gen - loss + trans) * dt)
    if new.I > 6.0 and params.resilience > 0.9 and not state.postbiological:
        if rng.random() < 0.08 * dt:
            new.postbiological = True
            new.B = 0.1
            new.I *= 1.4
    # --- Memoria ancestral (con compuertas) ---
    if abl == "no_memory" or abl == "null":
        new.M = 0.0
    else:
        if abl == "no_recovery":
            eta_eff = 0.0
        else:
            eta_eff = params.eta_T0 * min(2.0, new.I / 1.5) * (1.0 + 0.1 * np.log1p(new.N))
            eta_eff *= (0.7 + 0.3 * new.G_ancestry)
        dM = (-params.lambda_M * state.M + eta_eff) * dt
        new.M = float(np.clip(state.M + dM, 0.0, 1.0))
    # --- Mapa de la Tierra ---
    decay_R = 0.008 * (1.0 - params.resilience) * dt
    maintain = (0.04 * params.resilience + 0.03 * new.M) * dt if new.I > 0.8 else 0.0
    new.R = float(np.clip(state.R - decay_R + maintain, 0.0, 1.0))
    if new.E < 15.0:
        new.R = max(new.R, 0.75)
    new.A = state.A + 0.008 * new.N * dt
    new.tau = state.tau + dt
    # --- Colapso parcial (con compuerta no_info_surv) ---
    lambda_eff = params.lambda_c0 * (1.0 - 0.65 * params.resilience)
    if abl != "no_info_surv" and abl != "null":
        if new.I < 0.4:
            lambda_eff *= 2.5
        elif new.I > 3.5:
            lambda_eff *= 0.35
    if rng.random() < 1.0 - np.exp(-lambda_eff * dt):
        new.N = max(0, int(new.N * rng.uniform(0.15, 0.55)))
        new.I *= rng.uniform(0.35, 0.75)
        new.M *= rng.uniform(0.4, 0.85)
        if new.N == 0:
            new.alive = False
    return new


def simul_abl(params, t_max, dt, rng, abl):
    state = CivilizationState(N=params.seed_colonies, R=1.0, M=1.0)
    n_steps = int(t_max / dt)
    for _ in range(n_steps + 1):
        if not state.alive:
            break
        state = step_abl(state, params, dt, rng, abl)
    return state


def base_params(esc, mu_eff=None, tech_mod=1.0):
    b = SCENARIOS[esc]
    return ScenarioParams(name=esc, description="", v_e=b.v_e, lambda_c0=b.lambda_c0,
        mu=(mu_eff if mu_eff is not None else b.mu), alpha_info=b.alpha_info,
        beta_loss=b.beta_loss, gamma_trans=b.gamma_trans, resilience=b.resilience,
        tech_mod=(b.tech_mod if mu_eff is None else tech_mod),
        P_return_intent=b.P_return_intent, lambda_M=b.lambda_M, eta_T0=b.eta_T0,
        seed_colonies=b.seed_colonies, max_colonies=b.max_colonies)


def run_batch(params, t_max, dt, n, seed, abl="full"):
    rng = np.random.default_rng(seed)
    Prets, Gs, Ms, surv = [], [], [], []
    for _ in range(n):
        st = simul_abl(params, t_max, dt, rng, abl)
        Prets.append(compute_return_probability(st, params))   # P_ret OFICIAL
        Gs.append(st.G_ancestry); Ms.append(st.M); surv.append(int(st.alive))
    return np.array(Prets), np.array(Gs), np.array(Ms), np.array(surv)


def boot_ci(v, n_boot=1000, seed=3):
    rng = np.random.default_rng(seed)
    m = rng.choice(v, size=(n_boot, len(v)), replace=True).mean(axis=1)
    return float(np.percentile(m, 2.5)), float(np.percentile(m, 97.5))


def T1_dt(esc):
    print("== T1 convergencia dt | escenario %s ==" % esc, flush=True)
    out = []
    for dt in [0.1, 0.05, 0.025, 0.0125]:
        P, G, M, S = run_batch(base_params(esc), 100.0, dt, 1500, seed=int(1000 + dt * 100000))
        out.append({"dt": dt, "P_ret": float(P.mean()), "G": float(G[S == 1].mean()) if S.any() else None,
                    "M": float(M.mean()), "surv": float(S.mean())})
        print("  dt=%.4f -> P_ret=%.4e G=%.4f M=%.4f surv=%.4f" % tuple(
            [out[-1]["dt"], out[-1]["P_ret"], out[-1]["G"] or -1, out[-1]["M"], out[-1]["surv"]]), flush=True)
    with open(r"C:\Users\Jairo Omar\AGI_Workspace\hed_destruccion_T1_%s.json" % esc, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=1, ensure_ascii=False)
    print("  -> T1 %s guardado" % esc, flush=True)


def T2_mc(esc, extra_N):
    print("== T2 convergencia MC | escenario %s ==" % esc, flush=True)
    out = []
    for N in [100, 1000, extra_N]:
        P, G, M, S = run_batch(base_params(esc), 100.0, 0.025, N, seed=777)
        lo, hi = boot_ci(P)
        out.append({"N": N, "P_ret": float(P.mean()), "CI95": [lo, hi], "G": float(G[S == 1].mean()) if S.any() else None})
        print("  N=%5d -> P_ret=%.4e CI95=[%.3e, %.3e] G=%.4f" % (N, P.mean(), lo, hi, out[-1]["G"] or -1), flush=True)
    with open(r"C:\Users\Jairo Omar\AGI_Workspace\hed_destruccion_T2_%s.json" % esc, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=1, ensure_ascii=False)
    print("  -> T2 %s guardado" % esc, flush=True)


def T3_abl(esc):
    print("== T3 ablacion | escenario %s ==" % esc, flush=True)
    out = {}
    for abl in ["full", "no_info_surv", "no_recovery", "no_memory", "null"]:
        P, G, M, S = run_batch(base_params(esc), 100.0, 0.05, 2000, seed=42, abl=abl)
        out[abl] = {"P_ret": float(P.mean()), "surv": float(S.mean()),
                    "G": float(G[S == 1].mean()) if S.any() else None, "M": float(M.mean())}
        print("  %-14s -> P_ret=%.4e surv=%.4f G=%.4f M=%.4f" % (abl, out[abl]["P_ret"], out[abl]["surv"],
              out[abl]["G"] or -1, out[abl]["M"]), flush=True)
    out["Delta_P_ret_full_null"] = out["full"]["P_ret"] - out["null"]["P_ret"]
    print("  Delta_P_ret (full - null) = %.3e" % out["Delta_P_ret_full_null"], flush=True)
    with open(r"C:\Users\Jairo Omar\AGI_Workspace\hed_destruccion_T3_%s.json" % esc, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=1, ensure_ascii=False)
    print("  -> T3 %s guardado" % esc, flush=True)


def T4_thr(esc, mu_eff, n=3000):
    print("== T4 umbrales | escenario %s mu_eff=%.3f ==" % (esc, mu_eff), flush=True)
    P, G, M, S = run_batch(base_params(esc, mu_eff=mu_eff), 100.0, 0.05, n, seed=99)
    Gs, Ms = G[S == 1], M[S == 1] if S.any() else (G, M)
    out = {"esc": esc, "mu_eff": mu_eff, "n": int(n), "n_surv": int(S.sum()), "matriz": {}}
    print("  G_crit\\M_crit | " + " ".join("%8s" % m for m in [0.01, 0.05, 0.10, 0.20]))
    for gc in [0.01, 0.05, 0.10, 0.20]:
        row = []
        for mc in [0.01, 0.05, 0.10, 0.20]:
            d2 = float(np.mean((Gs <= gc) & (Ms > mc)))
            out["matriz"]["g%s_m%s" % (gc, mc)] = {"H_D2": d2,
                "H_D3": float(np.mean((Gs > gc) & (Ms > mc))),
                "H_D1": float(np.mean((Gs > gc) & (Ms <= mc))),
                "none": float(np.mean((Gs <= gc) & (Ms <= mc)))}
            row.append("%8.3f" % d2)
        print("  %7.2f   | %s" % (gc, " ".join(row)), flush=True)
    with open(r"C:\Users\Jairo Omar\AGI_Workspace\hed_destruccion_T4_%s.json" % esc, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=1, ensure_ascii=False)
    print("  -> T4 %s guardado (matriz de fraccion H_D2)" % esc, flush=True)


if __name__ == "__main__":
    test = sys.argv[1].upper()
    esc = sys.argv[2].upper() if len(sys.argv) > 2 else "B"
    if test == "T1":
        T1_dt(esc)
    elif test == "T2":
        extra = int(sys.argv[3]) if len(sys.argv) > 3 else 10000
        T2_mc(esc, extra)
    elif test == "T3":
        T3_abl(esc)
    elif test == "T4":
        mue = float(sys.argv[3]) if len(sys.argv) > 3 else 0.06
        T4_thr(esc, mue)
    else:
        print("uso: T1|T2|T3|T4 [ESC] [param]")
