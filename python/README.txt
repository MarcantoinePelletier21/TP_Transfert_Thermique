Ce dossier contient plusieurs scripts pour charger, transformer et visualiser les données
 de température des 29 stations (Low / Mid / Top) à partir du fichier DataSet.npz.

 Pour générer le fichier DataSet.npz il faut exécuter data_analyzer.py après avoir downloader
 les fichiers de données dans un dossier nommé dataverse_files dans le root tu projet. 
 (voir chemin du fichier dans le code si jamais).


1- data_analyzer.py:

Rôle :
-Charger le fichier brut DataSet.csv
Extraire :
-time (vecteur datetime)
-T_out (température extérieure)
-RH_out (humidité extérieure)
-low, mid, top : matrices (nb_points, 29) pour les capteurs

Sauvegarder tout ça dans un fichier binaire compressé DataSet.npz.


2- data_graph.py: 

Rôle :
-Petite interface Tkinter pour visualiser les températures en fonction du temps.
Permet de :
-cocher les hauteurs : Low, Mid, Top
-sélectionner une ou plusieurs stations S1 à S29
-définir un intervalle de temps [Start, End] en texte
-tracer les courbes directement dans la fenêtre
-sauvegarder la figure (Save figure) en PNG/PDF/etc.



3- Stratification.py:

Rôle :
-Calculer la température moyenne pour chaque hauteur (Low, Mid, Top) :
moyenne sur les 29 stations à chaque instant en ignorant les NaN (capteurs en panne)
-Option de faire un moyennage temporel (heure, jour, semaine, etc.) 
-Tracer 3 courbes pour les 29 stations:
Moyenne Low
Moyenne Mid
Moyenne Top
-Variable importante AVG_WINDOW = "1D". Elle peut être ajuster
AVG_WINDOW = 0 : aucun moyennage temporel
→ courbes très bruitées (un point par mesure)
AVG_WINDOW = "1H" : moyenne horaire
AVG_WINDOW = "1D" : moyenne journalière
AVG_WINDOW = "7D" : moyenne hebdomadaire


4- Plateau.py:

Rôle :
-Calculer, pour chaque station Si (i = 1..29), la moyenne verticale :
on prend les 3 capteurs de la station : Low-Si, Mid-Si, Top-Si
on fait la moyenne verticale en ignorant les NaN.

Si GROUPS = [] (liste vide) :
→ le script trace les 29 stations individuellement.
Si tu définis des groupes, par exemple :
GROUPS = [
    [1, 2, 3],   # Groupe 1 = S1, S2, S3
    [4, 5, 6],   # Groupe 2 = S4, S5, S6
    [7, 10, 29]  # Groupe 3 = S7, S10, S29
]
Alors le script :
calcule la moyenne de S1,S2,S3 → courbe “Groupe 1”
calcule la moyenne de S4,S5,S6 → courbe “Groupe 2”
etc.
Tu obtiens UNE courbe par groupe, à la résolution temporelle définie par AVG_WINDOW.


Yo
