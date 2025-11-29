import json

def load_parameters(path="JSON/donnees_simulation.json"):
    """load les paramètres du JSON"""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

if __name__ == "__main__":
    params = load_parameters()
    p = params["geometrie"]
    prop = params["proprietes"]

    A1 = (
        (2 * p["p1_x"] * p["scale_x"] * p["pi_z"])
        + (p["pi_y"] * p["scale_y"] * p["pi_z"])
        + (p["p1_x"] * p["pi_y"] * p["scale_x"] * p["scale_y"])
    )

    A2 = (
        (2 * p["p2_x"] * p["scale_x"] * p["pi_z"])
        + (p["p2_x"] * p["pi_y"] * p["scale_x"] * p["scale_y"])
    )

    A3 = (
        (2 * p["p3_x"] * p["scale_x"] * p["pi_z"])
        + (p["p3_x"] * p["pi_y"] * p["scale_x"] * p["scale_y"])
    )

    A4 = (
        (2 * p["p4_x"] * p["scale_x"] * p["pi_z"])
        + (p["p4_x"] * p["pi_y"] * p["scale_x"] * p["scale_y"])
    )

    A5 = (
        (2 * p["p5_x"] * p["scale_x"] * p["pi_z"])
        + (p["p5_x"] * p["pi_y"] * p["scale_x"] * p["scale_y"])
    )

    A6 = (
        (2 * p["p6_x"] * p["scale_x"] * p["pi_z"])
        + (p["pi_y"] * p["scale_y"] * p["pi_z"])
        + (p["p6_x"] * p["pi_y"] * p["scale_x"] * p["scale_y"])
    )

    A7 = (
    (p["p1_x"] * p["pi_y"] * p["scale_x"] * p["scale_y"])
    )

    A8 = (
    (p["p2_x"] * p["pi_y"] * p["scale_x"] * p["scale_y"])
    )

    A9 = (
    (p["p3_x"] * p["pi_y"] * p["scale_x"] * p["scale_y"])
    )

    A10 = (
    (p["p4_x"] * p["pi_y"] * p["scale_x"] * p["scale_y"])
    )

    A11 = (
    (p["p5_x"] * p["pi_y"] * p["scale_x"] * p["scale_y"])
    )

    A12 = (
    (p["p6_x"] * p["pi_y"] * p["scale_x"] * p["scale_y"])
    )


    rho_air = prop["rho_air"]           # kg/m3
    cp_air  = prop["cp_air"]

    # dimensions verticales et largeur (communes)
    H = p["pi_z"]                  # hauteur en m
    W = p["pi_y"] * p["scale_y"]   # largeur en m

    # LONGUEURS DES 6 PLATEAUX (en m)
    L1 = p["p1_x"] * p["scale_x"]
    L2 = p["p2_x"] * p["scale_x"]
    L3 = p["p3_x"] * p["scale_x"]
    L4 = p["p4_x"] * p["scale_x"]
    L5 = p["p5_x"] * p["scale_x"]
    L6 = p["p6_x"] * p["scale_x"]

    # VOLUMES
    V1 = L1 * W * H
    V2 = L2 * W * H
    V3 = L3 * W * H
    V4 = L4 * W * H
    V5 = L5 * W * H
    V6 = L6 * W * H

    # MASS AIR
    m1 = rho_air * V1
    m2 = rho_air * V2
    m3 = rho_air * V3
    m4 = rho_air * V4
    m5 = rho_air * V5
    m6 = rho_air * V6

    # CAPACITANCE THERMIQUE = m * cp   (J/K)
    C1 = m1 * cp_air
    C2 = m2 * cp_air
    C3 = m3 * cp_air
    C4 = m4 * cp_air
    C5 = m5 * cp_air
    C6 = m6 * cp_air

    print("\n--- Capacitances thermiques (C1 à C6, en J/K) ---")
    print("C1 =", C1)
    print("C2 =", C2)
    print("C3 =", C3)
    print("C4 =", C4)
    print("C5 =", C5)
    print("C6 =", C6)
