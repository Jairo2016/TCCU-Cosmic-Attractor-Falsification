# TCCU-0B corredor lambda~2 v3
# Misma física que v2; checkpoint por configuración y reanudación.
import json, importlib.util, numpy as np, time, os, signal, sys

BASE = r"C:\Users\Jairo Omar\AGI_Workspace"
TARGET = os.path.join(BASE, "TCCU_Eternity_Test_v1.5.23c.py")
PROGRESS = os.path.join(BASE, "tccu0b_v3_progreso.json")
RESULTS = os.path.join(BASE, "tccu0b_v3_configs.jsonl")
FINAL = os.path.join(BASE, "mapa_tccu0b_v3.json")

spec = importlib.util.spec_from_file_location("t1523c", TARGET)
t = importlib.util.module_from_spec(spec)
spec.loader.exec_module(t)

ALPHA_CRIT = 0.95
DN = -0.005
N_LIMIT = -250.0

def n_ruptura(LAM_val, w0, sg):
    t.LAM = LAM_val
    init = t.compute_initial_quantities(w0, sg)

    if init is None:
        return None, "IC_invalida", None, None, 0

    Phi0, Pi0 = init
    y = np.array([
        Phi0, Pi0,
        np.log(t.Omega_m0),
        np.log(t.Omega_r0),
        0.0, 0.0
    ], dtype=float)

    N = 0.0
    alpha_max = 0.0
    max_steps = int(abs(N_LIMIT) / abs(DN))

    for step in range(1, max_steps + 1):
        f = t.derivatives(N, y)

        if not np.all(np.isfinite(f)):
            return N, "rhs_no_finito", alpha_max, y[0], step

        y = y + DN * f
        N += DN

        alpha = y[1] ** 2 / 6.0
        alpha_max = max(alpha_max, alpha)

        if alpha > ALPHA_CRIT:
            return N, "borde_cinetico", alpha, y[0], step

        if N < N_LIMIT:
            return N, "extiende", alpha_max, y[0], step

    return N, "limite_pasos", alpha_max, y[0], max_steps


def cargar_hechos():
    hechos = {}
    if not os.path.exists(RESULTS):
        return hechos

    with open(RESULTS, "r", encoding="utf-8") as f:
        for line in f:
            try:
                c = json.loads(line)
                key = (c["lambda"], c["w0"], c["signo"])
                hechos[key] = c
            except Exception:
                pass

    return hechos


def guardar_progreso(done, total, lam, w0, sg, elapsed):
    tmp = PROGRESS + ".tmp"

    data = {
        "version": "TCCU-0B-v3",
        "done": done,
        "total": total,
        "lambda_actual": lam,
        "w0_actual": w0,
        "signo_actual": sg,
        "porcentaje": round(100.0 * done / total, 3),
        "segundos": round(elapsed, 3),
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }

    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)

    os.replace(tmp, PROGRESS)


def main():
    lam_vals = np.round(np.arange(1.4, 2.601, 0.02), 4)
    w0_vals = np.round(np.arange(-0.4, 0.201, 0.02), 4)
    signos = [1, -1]

    total = len(lam_vals) * len(w0_vals) * len(signos)

    hechos = cargar_hechos()
    done = len(hechos)

    print("=" * 70)
    print("TCCU-0B v3 — CORREDOR LAMBDA ~ 2")
    print("Física: TCCU_Eternity_Test_v1.5.23c.py")
    print(f"Configuraciones totales: {total}")
    print(f"Ya completadas: {done}")
    print(f"Pendientes: {total - done}")
    print("=" * 70, flush=True)

    t0 = time.time()

    try:
        for lam in lam_vals:
            for w0 in w0_vals:
                for sg in signos:

                    key = (float(lam), float(w0), int(sg))

                    if key in hechos:
                        continue

                    inicio = time.time()

                    Ns, razon, alpha_s, Phi_s, steps = n_ruptura(
                        lam, w0, sg
                    )

                    dt = time.time() - inicio

                    c = {
                        "lambda": float(lam),
                        "w0": float(w0),
                        "signo": int(sg),
                        "N_s": round(Ns, 3) if Ns is not None else None,
                        "razon": razon,
                        "alpha_s": round(alpha_s, 6) if alpha_s is not None else None,
                        "Phi_s": round(Phi_s, 6) if Phi_s is not None else None,
                        "steps": int(steps),
                        "segundos_config": round(dt, 3)
                    }

                    with open(RESULTS, "a", encoding="utf-8") as f:
                        f.write(json.dumps(c, ensure_ascii=False) + "\n")
                        f.flush()

                    hechos[key] = c
                    done += 1

                    guardar_progreso(
                        done, total, lam, w0, sg,
                        time.time() - t0
                    )

                    print(
                        f"[{done:4d}/{total}] "
                        f"lambda={lam:.2f} "
                        f"w0={w0:.2f} "
                        f"sg={sg:+d} "
                        f"N_s={Ns if Ns is not None else 'None'} "
                        f"razon={razon} "
                        f"steps={steps} "
                        f"dt={dt:.2f}s",
                        flush=True
                    )

    except KeyboardInterrupt:
        print("\nINTERRUPCIÓN MANUAL.")
        print("El checkpoint queda guardado.")
        print("Puede reanudarse ejecutando nuevamente este programa.")
        return

    configs = list(hechos.values())

    validos = [c for c in configs if c["N_s"] is not None]
    rot = [c for c in configs if c["razon"] == "borde_cinetico"]
    ext = [c for c in configs if c["razon"] in ("extiende", "limite_pasos")]
    profundos = [c for c in validos if c["N_s"] < -60]

    if validos:
        best = max(validos, key=lambda c: -c["N_s"])
    else:
        best = None

    out = {
        "campana": "TCCU-0B corredor lambda~2 v3",
        "n_configs": len(configs),
        "n_borde": len(rot),
        "n_extiende": len(ext),
        "n_profundos_gt60": len(profundos),
        "lambda_star": best,
        "profundos": profundos,
        "configs": configs
    }

    with open(FINAL, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)

    print("=" * 70)
    print("CAMPAÑA COMPLETADA")
    print(f"configs = {len(configs)}")
    print(f"borde = {len(rot)}")
    print(f"extiende/limite = {len(ext)}")
    print(f"profundos (>60) = {len(profundos)}")

    if best:
        print(
            "LAMBDA_STAR: "
            f"lambda={best['lambda']:.3f} "
            f"w0={best['w0']:.3f} "
            f"signo={best['signo']:+d} "
            f"N_s={best['N_s']}"
        )

    print(f"Tiempo total: {time.time() - t0:.1f} s")
    print("=" * 70)


if __name__ == "__main__":
    main()
