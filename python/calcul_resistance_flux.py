"""
Module: calcul_resistance_flux
Fonctions pour le calcul des résistances thermiques (conduction, convection)
et des flux (conductif, massique). Compatible avec un modèle en couche
et un modèle nodal multi-zones.
"""
import math


# ============================================================
# 1) RÉSISTANCES THERMIQUES
# ============================================================

def resistance_convection(h, A):
    """
    Résistance thermique par convection :
        R = 1 / (h * A)
    """
    if h <= 0:
        raise ValueError("Le coefficient de convection h doit être > 0.")
    if A <= 0:
        raise ValueError("L'aire A doit être > 0.")

    return 1.0 / (h * A)


def resistance_conduction(L, k, A):
    """
    Résistance thermique par conduction :
        R = L / (k * A)
    """
    if L <= 0:
        raise ValueError("L'épaisseur L doit être > 0.")
    if k <= 0:
        raise ValueError("La conductivité k doit être > 0.")
    if A <= 0:
        raise ValueError("L'aire A doit être > 0.")

    return L / (k * A)


def resistance_serie(*resistances):
    """
    Somme des résistances thermiques en série.
    """
    for R in resistances:
        if R <= 0:
            raise ValueError(f"Chaque résistance doit être > 0. Valeur donnée : {R}")

    return sum(resistances)


# ============================================================
# 2) RÉSISTANCES COMPLÈTES SELON LE CHEMIN
# ============================================================

def resistance_vers_exterieur(h_int, h_ext,
                              L_plaque, k_plaque,
                              L_asphalte, k_asphalte,
                              A):
    """
    Résistance totale pour le flux vers l'extérieur :
    R = R_conv_int + R_plaque + R_asphalte + R_conv_ext
    """
    R_conv_int = resistance_convection(h_int, A)
    R_plaque   = resistance_conduction(L_plaque, k_plaque, A)
    R_asph     = resistance_conduction(L_asphalte, k_asphalte, A)
    R_conv_ext = resistance_convection(h_ext, A)

    return resistance_serie(R_conv_int, R_plaque, R_asph, R_conv_ext)


def resistance_vers_sol(h_int,
                        L_ciment, k_ciment,
                        L_isolant, k_isolant,
                        A):
    """
    Résistance totale pour le flux vers le sol :
    R = R_conv_int + R_ciment + R_isolant

    (Ne passe PAS par la plaque ni l'asphalte.)
    """
    R_conv_int = resistance_convection(h_int, A)
    R_ciment   = resistance_conduction(L_ciment, k_ciment, A)
    R_isolant  = resistance_conduction(L_isolant, k_isolant, A)

    return resistance_serie(R_conv_int, R_ciment, R_isolant)


# ============================================================
# 3) FLUX THERMIQUES
# ============================================================


def flux_massique(m_dot, cp, T_upstream, T_downstream):
    """
    Flux thermique dû au transport massique :
        q = m_dot * cp * (T_upstream - T_downstream)
    """
    if cp <= 0:
        raise ValueError("cp doit être > 0.")
    if m_dot == 0:
        return 0.0

    return m_dot * cp * (T_upstream - T_downstream)


def temperature_harmonique(t, T_mean, A, t0, phi=0.0):
    """
    Modèle harmonique général :
        T(t) = T_mean + A * cos( 2π (t - phi) / t0 )

    Paramètres
    ----------
    t : float
        Temps (même unité que t0)
    T_mean : float
        Température moyenne (°C)
    A : float
        Amplitude (°C)
    t0 : float
        Période complète (ex.: 24 h ou 24*3600 s)
    phi : float
        Phase (heure du maximum)

    Retour
    ------
    float
        Température au temps t
    """

    return T_mean + A * math.cos(2 * math.pi * (t - phi) / t0)


