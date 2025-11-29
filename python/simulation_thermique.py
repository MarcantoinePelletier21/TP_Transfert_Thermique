import json
import numpy as np

from calcul_resistance_flux import (
    resistance_convection,
    resistance_conduction,
    temperature_harmonique,
)


# ============================================================
# 1) LOAD PARAMETERS FROM JSON
# ============================================================

def load_parameters(path="JSON/donnees_simulation.json"):
    """load les paramètres du JSON"""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

# ============================================================
# 2) TEMPERATURE LAWS FOR EXT AND SOIL
# ============================================================

def TempExt(t, params):
    """calcul temp extérieure"""
    p = params["temperature_exterieure"]
    return temperature_harmonique(t, p["T_mean"], p["A"], p["t0"], p["phi"])


def TempSol(t, params):
    """calcul temp sol"""
    p = params["temperature_sol"]
    return temperature_harmonique(t, p["T_mean"], p["A"], p["t0"], p["phi"])


# ============================================================
# 3) COMPUTATION OF R_ext AND R_sol FOR EACH PLATEAU
# ============================================================

def compute_resistances(params):
    """Compute R_ext[i] and R_sol[i] for plateaus 1..6 using JSON areas."""
    
    prop = params["proprietes"]
    geom = params["geometrie"]

    # --- Extract thicknesses ---
    L_plaque   = geom["epaisseur_plaque"]
    L_asphalte = geom["epaisseur_asphalte"]
    L_ciment   = geom["epaisseur_ciment"]
    L_isolant  = geom["epaisseur_isolant"]

    # --- convection coefficients ---
    h_int = prop["h_int"]
    h_ext = prop["h_ext"]

    # --- Prepare arrays output ---
    R_ext = np.zeros(6)
    R_sol = np.zeros(6)

    for i in range(6):
        p = i + 1  # plateau number (1..6)

        # Plateau-specific areas
        A_plaque = geom[f"A_plaque_p{p}"]
        A_ciment = geom[f"A_ciment_p{p}"]

        # 1) Internal convection surface = plaque area
        R_conv_int_plaque = resistance_convection(h_int, A_plaque)
        R_conv_int_ciment = resistance_convection(h_int, A_ciment)


        # 2) Toward exterior
        R_ext[i] = (
            R_conv_int_plaque
            + resistance_conduction(L_plaque,   prop["k_acier"],    A_plaque)
            + resistance_conduction(L_asphalte, prop["k_asphalte"], A_plaque)
            + resistance_convection(h_ext, A_plaque)
        )

        # 3) Toward ground
        R_sol[i] = (
            R_conv_int_ciment
            + resistance_conduction(L_ciment,  prop["k_ciment"],  A_ciment)
            + resistance_conduction(L_isolant, prop["k_isolant"], A_ciment)
        )

    return R_ext, R_sol


# ============================================================
# 5) Q aerotherme
# ============================================================
def compute_Q_aerotherme(i, T, T_ext, heaters, heater_timers, params, dt):
    """
    i : index plateau (0..5)
    T : temperatures array T[n-1]
    T_ext : current exterior temperature
    heaters : array of heater ON/OFF states (0 or 1)
    heater_timers : array of delay timers (in hours)
    dt : timestep in hours
    """

    # update timers
    if heater_timers[i] > 0:
        heater_timers[i] = max(0, heater_timers[i] - dt)

    T_moy = 0.5 * (T[0] + T[5])   # moyenne des plateaux 1 et 6
    P_i = params["chauffage"][f"p{i+1}"]

    # --- Conditions d'arrêt ---
    if T_ext > -1 or T_moy > 38.75:
        # turn OFF
        if heaters[i] == 1:
            heaters[i] = 0
            heater_timers[i] = 10/60      # 10 min = 0.166 h
        return 0.0

    # --- Conditions pour ON ---
    if T_ext < -1:

        # timer active → impossible de rallumer
        if heater_timers[i] > 0:
            return 0.0

        # sinon → ON
        heaters[i] = 1
        return P_i

    # fallback
    return 0.0

# ============================================================
# 5) Q infiltration
# ============================================================
def compute_Q_infiltration(i, T, T_ext, params):
    """
    i : plateau index (0..5)
    T : array of plateau temperatures [T1..T6]
    T_ext : exterior temperature
    Retourne Q_inf_i (W), signé:
        Q > 0 : chauffe le plateau
        Q < 0 : refroidit le plateau
    """
    infil = params["infiltration"]
    cp = params["proprietes"]["cp_air"]

    # --- 1) Débit de masse effectif pour le plateau i ---
    if i == 0:   # plateau 1
        mdot_i = 0.5 * infil["gap_1"] + infil["gap_front"]

    elif i == 1: # plateau 2
        mdot_i = 0.5 * infil["gap_1"] + 0.5 * infil["gap_2"]

    elif i == 2: # plateau 3
        mdot_i = 0.5 * infil["gap_2"] + 0.5 * infil["gap_3"]

    elif i == 3: # plateau 4
        mdot_i = 0.5 * infil["gap_3"] + 0.5 * infil["gap_4"]

    elif i == 4: # plateau 5
        mdot_i = 0.5 * infil["gap_4"] + 0.5 * infil["gap_5"]

    elif i == 5: # plateau 6
        mdot_i = 0.5 * infil["gap_5"] + infil["gap_back"]

    else:
        mdot_i = 0.0

    # --- 2) Effet thermique ---
    # On utilise la valeur absolue : peu importe le sens, on échange avec T_ext.
    mdot_eff = abs(mdot_i)

    # ΔT = T_ext - T_i :
    #  - si T_ext < T_i → ΔT < 0 → Q_inf < 0 → refroidissement
    #  - si T_ext > T_i → ΔT > 0 → Q_inf > 0 → chauffage
    dT = T_ext - T[i]

    Q_inf = mdot_eff * cp * dT

    return Q_inf


# ============================================================
# 5) Q flow
# ============================================================
def compute_Q_flow(i, T, flow, params):
    """
    i : plateau index (0..5)
    T : array des températures [T1..T6]
    flow : dict = flow_heaterON ou flow_heaterOFF
    Retourne Q_flow_i (W)
    """
    cp = params["proprietes"]["cp_air"]

    if i == 0:
        # Plateau 1, couplé seulement à 2 (f12)
        # P1 perd si T1 > T2
        Q = flow["f12"] * cp * (T[1] - T[0])

    elif i == 1:
        # Plateau 2, couplé à 1 et 3
        # depuis 1 → 2 : f21, T1 - T2
        # vers 3 → 2 perd si T2 > T3 : f23, T3 - T2
        Q = (
            flow["f21"] * cp * (T[0] - T[1]) +
            flow["f23"] * cp * (T[2] - T[1])
        )

    elif i == 2:
        # Plateau 3, couplé à 2 et 4
        Q = (
            flow["f32"] * cp * (T[1] - T[2]) +
            flow["f34"] * cp * (T[3] - T[2])
        )

    elif i == 3:
        # Plateau 4, couplé à 3 et 5
        Q = (
            flow["f43"] * cp * (T[2] - T[3]) +
            flow["f45"] * cp * (T[4] - T[3])
        )

    elif i == 4:
        # Plateau 5, couplé à 4 et 6
        Q = (
            flow["f54"] * cp * (T[3] - T[4]) +
            flow["f56"] * cp * (T[5] - T[4])
        )

    elif i == 5:
        # Plateau 6, couplé seulement à 5
        Q = flow["f65"] * cp * (T[4] - T[5])

    else:
        Q = 0.0

    return Q


def q_to_Tnew(Ti, T_ext, T_sol, Q_air, dt, R_ext, R_sol, C):
    """
    Mise à jour de la température d'un plateau en utilisant
    un modèle thermique RC (Euler explicite).

    Ti : température actuelle du plateau (°C)
    T_ext : température extérieure (°C)
    T_sol : température du sol (°C)
    Q_air : flux d'air total (W)
    dt : pas de temps (heures)
    R_ext, R_sol : résistances thermiques (K/W)
    C : capacité thermique du plateau (J/K)
    """

    dt_s = dt * 3600  # conversion heures → secondes

    # flux conduction
    Q_cond_ext = (T_ext - Ti) / R_ext
    Q_cond_sol = (T_sol - Ti) / R_sol

    # flux total
    Q_total = Q_cond_ext + Q_cond_sol + Q_air

    # intégration dT/dt = Q/C
    T_new = Ti + (dt_s / C) * Q_total

    return T_new




# ============================================================
# 5) MAIN SIMULATION LOOP
# ============================================================

def simulate(params, dt=1/60, t_end=48):
    """
    Simulation thermique du puits.
    dt : en heures (ex: 1/60 h = 1 minute)
    t_end : durée totale en heures
    """

    # ============================================================
    # Charger C depuis le JSON
    # ============================================================
    C_json = params["capacitance_thermique"]
    C = np.array([
        C_json["C1"],
        C_json["C2"],
        C_json["C3"],
        C_json["C4"],
        C_json["C5"],
        C_json["C6"]
    ], dtype=float)

    # ============================================================
    # Time vector et initialisation T
    # ============================================================
    n_steps = int(t_end / dt) + 1
    time = np.linspace(0, t_end, n_steps)

    T = np.zeros((n_steps, 6))
    T[0, :] = np.full(6, 10.0)  # initial plateau temperature

    # ============================================================
    # Résistances plateau-par-plateau
    # ============================================================
    R_ext, R_sol = compute_resistances(params)

    # ============================================================
    # État des aérothermes
    # ============================================================
    heaters = np.zeros(6, dtype=int)       # 0 = OFF, 1 = ON
    heater_timers = np.zeros(6, float)     # cooldown (heures)

    # ============================================================
    # Boucle temporelle
    # ============================================================
    for n in range(1, n_steps):

        t = time[n]

        # Température extérieure / sol au temps t
        T_ext_current = TempExt(t, params)
        T_sol_current = TempSol(t, params)

        # Sélection du bon set de flow ON / OFF
        if np.any(heaters == 1):
            flow = params["flow_heaterON"]
        else:
            flow = params["flow_heaterOFF"]

        # --------------------------------------------------------
        # Boucle plateau
        # --------------------------------------------------------
        for i in range(6):

            Ti = T[n-1, i]

            # Flux aérotherme avec temporisateur
            Q_aero = compute_Q_aerotherme(
                i=i,
                T=T[n-1],
                T_ext=T_ext_current,
                heaters=heaters,
                heater_timers=heater_timers,
                params=params,
                dt=dt
            )

            # Flux d'infiltration
            Q_inf = compute_Q_infiltration(
                i=i,
                T=T[n-1],
                T_ext=T_ext_current,
                params=params
            )

            # Flux d'échange entre plateaux
            Q_flow_i = compute_Q_flow(
                i=i,
                T=T[n-1],
                flow=flow,
                params=params
            )

            # Q total (air)
            Q_total = Q_aero + Q_inf + Q_flow_i

            # --------------------------------------------------------
            # Mise à jour température
            # --------------------------------------------------------
            T[n, i] = q_to_Tnew(
                Ti=Ti,
                T_ext=T_ext_current,
                T_sol=T_sol_current,
                Q_air=Q_total,
                dt=dt,
                R_ext=R_ext[i],
                R_sol=R_sol[i],
                C=C[i]
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
