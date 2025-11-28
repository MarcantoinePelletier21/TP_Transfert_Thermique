import json
import numpy as np

from calcul_resistance_flux import (
    resistance_convection,
    resistance_conduction,
    temperature_harmonique,
    flux_massique
)


# ============================================================
# 1) LOAD PARAMETERS FROM JSON
# ============================================================

def load_parameters(path="JSON/donnees_simulation.json"):
    """load les paramètres du JSON"""
    with open(path, "r") as f:
        return json.load(f)


# ============================================================
# 2) TEMPERATURE LAWS FOR EXT AND SOIL
# ============================================================

def T_ext(t, params):
    """calcul temp extérieure"""
    p = params["temperature_exterieure"]
    return temperature_harmonique(t, p["T_mean"], p["A"], p["t0"], p["phi"])


def T_sol(t, params):
    """calcul temp sol"""
    p = params["temperature_sol"]
    return temperature_harmonique(t, p["T_mean"], p["A"], p["t0"], p["phi"])


# ============================================================
# 3) COMPUTATION OF R_ext AND R_sol FOR EACH PLATEAU
# ============================================================

def compute_resistances(params, Aire):
    """calcul résistances"""
    prop = params["propritetes"]
    geom = params["geometrie"]

    # Internal convection
    R_conv_int = resistance_convection(h=prop["h_int"], A=Aire)

    # Toward exterior: conv_int + cond_plaque + cond_asphalte + conv_ext
    R_ext = (
        R_conv_int
        + resistance_conduction(L=geom["epaisseur_plaque"], k=prop["k_acier"], A=Aire)
        + resistance_conduction(L=geom["epaisseur_asphalte"], k=prop["k_asphalte"], A=Aire)
        + resistance_convection(h=prop["h_ext"], A=Aire)
    )

    # Toward ground: conv_int + cond_ciment + cond_isolant
    R_sol = (
        R_conv_int
        + resistance_conduction(L=geom["epaisseur_ciment"], k=prop["k_ciment"], A=Aire)
        + resistance_conduction(L=geom["epaisseur_isolant"], k=prop["k_isolant"], A=Aire)
    )

    return R_ext, R_sol


# ============================================================
# 4) COMPUTE TOTAL AIR MASS FLOW Q_air FOR EACH PLATEAU
# ============================================================

def compute_Q_air(i, T, params):
    """
    i : plateau index (1..6)
    T : array of current temperatures [T1..T6]
    params : JSON dict

    Includes: infiltration + exchange with neighbours.
    """
    infil = params["infiltration"]
    flowON = params["flow_heaterON"]

    cp = params["propritetes"]["cp_air"]

    # --- 1) infiltration (mass flows) ---
    # example split rule you described:
    if i == 1:
        mdot_inf = infil["gap_1"] * 0.5 + infil["gap_front"]
    elif i == 2:
        mdot_inf = infil["gap_1"] * 0.5 + infil["gap_2"] * 0.5
    # [...]
    else:
        mdot_inf = 0.0

    Q_inf = mdot_inf * cp * (T[i-1] - T_ext_current)   # sign depends on model choice

    # --- 2) exchange between plateaus ---
    # example: i=1 connected to 2, i=2 connected to 1&3, ... 
    # Using T[i] - T[j]
    Q_ex = 0.0

    # Example 1→2
    if i == 1:
        Q_ex += flowON["f12"] * cp * (T[1] - T[0])

    # (complete with your real logic)
    # ...

    return Q_inf + Q_ex


# ============================================================
# 5) MAIN SIMULATION LOOP
# ============================================================

def simulate(params, dt=1.0, t_end=24.0):
    """
    dt in hours.
    Returns arrays: time, temperatures[6]
    """
    n_steps = int(t_end / dt) + 1
    time = np.linspace(0, t_end, n_steps)

    # 6 plateau temperatures (initial guess)
    T = np.zeros((n_steps, 6))
    T[0, :] = np.full(6, 10.0)   # initial guess 10°C

    # compute A (plateau area)
    Aire = params["geometrie"]["scale_x"] * params["geometrie"]["scale_y"]

    # precompute R_ext and R_sol
    R_ext, R_sol = compute_resistances(params, Aire)

    # time loop
    for n in range(1, n_steps):
        t = time[n]

        global T_ext_current, T_sol_current
        T_ext_current = T_ext(t, params)
        T_sol_current = T_sol(t, params)

        for i in range(6):
            Ti = T[n-1, i]

            # Total Q_air (infiltration + neighbour flows)
            Q_air_i = compute_Q_air(i+1, T[n-1], params)

            # ODE → algebraic steady-step
            T[n, i] = q_to_Tnew(
                Ti=Ti,
                T_ext=T_ext_current,
                T_sol=T_sol_current,
                Q_air=Q_air_i,
                dt=dt,
                R_ext=R_ext,
                R_sol=R_sol
            )

    return time, T


# ============================================================
# 6) RUN EXAMPLE
# ============================================================

if __name__ == "__main__":
    params = load_parameters()
    time, T = simulate(params, dt=0.1, t_end=48)

    # Example print
    print("Final temperatures:", T[-1])
