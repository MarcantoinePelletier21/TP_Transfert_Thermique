import math

def resistance_convection(h, A):
    if h <= 0: raise ValueError("h > 0")
    if A <= 0: raise ValueError("A > 0")
    return 1.0 / (h * A)

def resistance_conduction(L, k, A):
    if L <= 0: raise ValueError("L > 0")
    if k <= 0: raise ValueError("k > 0")
    if A <= 0: raise ValueError("A > 0")
    return L / (k * A)

def resistance_serie(*resistances):
    for R in resistances:
        if R <= 0: raise ValueError(f"R > 0, got {R}")
    return sum(resistances)

def resistance_vers_exterieur(h_int, h_ext, L_plaque, k_plaque,
                              L_asphalte, k_asphalte, A):
    return resistance_serie(
        resistance_convection(h_int, A),
        resistance_conduction(L_plaque, k_plaque, A),
        resistance_conduction(L_asphalte, k_asphalte, A),
        resistance_convection(h_ext, A)
    )

def resistance_vers_sol(h_int, L_ciment, k_ciment, L_isolant, k_isolant, A):
    return resistance_serie(
        resistance_convection(h_int, A),
        resistance_conduction(L_ciment, k_ciment, A),
        resistance_conduction(L_isolant, k_isolant, A)
    )

def flux_massique(m_dot, cp, T_up, T_down):
    if cp <= 0: raise ValueError("cp > 0")
    if m_dot == 0: return 0.0
    return m_dot * cp * (T_up - T_down)

def temperature_harmonique(t, T_mean, A, t0, phi=0.0):
    return T_mean + A * math.cos(2 * math.pi * (t - phi) / t0)
