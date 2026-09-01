# mapa_existencia_tccu0.py v2 — MAPA DE EXISTENCIA (lambda, w0, signo)
# Detector de ruptura CORRECTO: alpha = (Pi^2/6) -> 1 es el borde real (X/rho_tot = alpha < 1).
# El modelo rompe cuando alpha supera 0.95 (borde cinetico); |Pi|->sqrt(6) asintotico no
# basta (rama degenerada con A divergente). Se re-mide toda la grilla.
import json, importlib.util, numpy as np, time

spec = importlib.util.spec_from_file_location("t1523c", "TCCU_Eternity_Test_v1.5.23c.py")
t = importlib.util.module_from_spec(spec)
spec.loader.exec_module(t)

ALPHA_CRIT = 0.95
DN = -0.005
N_LIMIT = -150.0

def n_ruptura(LAM_val, w0, sg):
    t.LAM = LAM_val
    init = t.compute_initial_quantities(w0, sg)
    if init is None:
        return None, "IC_invalida"
    Phi0, Pi0 = init
    y = np.array([Phi0, Pi0, np.log(t.Omega_m0), np.log(t.Omega_r0), 0.0, 0.0])
    N = 0.0
    for _ in range(int(abs(N_LIMIT) / abs(DN))):
        f = t.derivatives(N, y)
        if not np.all(np.isfinite(f)):
            return N, "rhs_no_finito"
        y = y + DN * f
        N += DN
        alpha = y[1] ** 2 / 6.0
        if alpha > ALPHA_CRIT:
            return N, "borde_cinetico"
        if not np.isfinite(alpha):
            return N, "alpha_no_finito"
        if N < N_LIMIT:
            return N, "extiende"
    return N, "limite_pasos"

def main():
    lam_grid = [0.1, 0.3, 0.5, 1.0, 2.0, 3.0, 5.0, 8.0, 12.0]
    w0_grid = [-0.4, -0.3, -0.2, -0.1, 0.0, 0.1, 0.2]
    signs = [1, -1]
    t0 = time.time()
    out = {"modelo": "TCCU-0: P = X + X^2/L^4 - rho_c0 e^{-LAM Phi}",
           "detector": "alpha = Pi^2/6 > 0.95 (borde cinetico)", "configs": []}
    for lam in lam_grid:
        for w0 in w0_grid:
            for sg in signs:
                Ns, razon = n_ruptura(lam, w0, sg)
                out["configs"].append({"lambda": lam, "w0": w0, "signo": sg,
                                       "N_s": (round(Ns, 3) if Ns is not None else None),
                                       "razon": razon})
    with open(r"C:\Users\Jairo Omar\AGI_Workspace\mapa_existencia_tccu0.json", "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("MAPA DE EXISTENCIA TCCU-0 v2 (N_s; 'ext' = extiende >= 150 e-folds)")
    print("lambda | signo=+1 (w0: -0.4 -0.3 -0.2 -0.1 0.0 0.1 0.2) | signo=-1 (idem)")
    for lam in lam_grid:
        fp = []; fn = []
        for w0 in w0_grid:
            for sg in signs:
                c = next(x for x in out["configs"] if x["lambda"] == lam and x["w0"] == w0 and x["signo"] == sg)
                s = ("ext" if c["razon"] == "extiende" else ("%.2f" % c["N_s"]) if c["N_s"] is not None else "?")
                (fp if sg == 1 else fn).append(s)
        print(" %5.2f | %s | %s" % (lam, " ".join("%5s" % s for s in fp), " ".join("%5s" % s for s in fn)))
    n_ext = sum(1 for c in out["configs"] if c["razon"] in ("extiende", "limite_pasos"))
    n_rot = sum(1 for c in out["configs"] if c["razon"] == "borde_cinetico")
    print("\nextienden: %d/%d | borde cinetico: %d | (%.1f s)" % (n_ext, len(out["configs"]), n_rot, time.time() - t0))

if __name__ == "__main__":
    main()
