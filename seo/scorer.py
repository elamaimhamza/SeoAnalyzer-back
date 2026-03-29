def calculer_score(resultats: list) -> tuple:
    """
    Calcule le score global sur 100 et attribue un grade.

    Paramètre :
        resultats : liste des résultats de chaque checker
        [
            {"code": "C1", "score": 12, "score_max": 15, ...},
            {"code": "C2", "score":  8, "score_max": 10, ...},
            ...
        ]

    Retourne :
        score_global : int : score total sur 100
        grade        : str : grade A+, A, B, C, D ou F
    """

    score_global = 0

    for resultat in resultats:
        score_max = resultat["score_max"]
        score     = resultat["score"]
        poids     = resultat["poids"]

        # Calcul du score pondéré
        # ex: C1 → 12/15 × 15 = 12 points sur 15
        if score_max > 0:
            score_global += (score / score_max) * poids

    score_global = round(score_global)

    # Attribution du grade
    if score_global >= 90:
        grade = "A+"
    elif score_global >= 80:
        grade = "A"
    elif score_global >= 70:
        grade = "B"
    elif score_global >= 60:
        grade = "C"
    elif score_global >= 50:
        grade = "D"
    else:
        grade = "F"

    return score_global, grade

"""
C1 → 12/15 * 15 = 12.0
C2 →  8/10 * 10 =  8.0
C3 →  6/10 * 10 =  6.0
C4 →  6/8  *  8 =  6.0
C5 →  4/8  *  8 =  4.0
C6 →  8/10 * 10 =  8.0
C7 →  8/12 * 12 =  8.0
C8 → 10/10 * 10 = 10.0
C9 →  5/7  *  7 =  5.0
C10→  7/10 * 10 =  7.0
─────────────────────────
Total = 74 → grade B

"""
