



def appliquer_regles(regles: list) -> tuple:
    """
    Paramètre :
        regles :
            {
                "verifie" : bool  — la condition est-elle respectée ?
                "points"  : int   — points gagnés si la règle est respectée
                "message" : str   — recommandation affichée si la règle échoue
            }

    Retourne :
        score           : int  — total des points gagnés
        recommandations : list — liste des recommandations pour les règles échouées
    """

    score = 0
    recommandations = []

    for regle in regles:
        if regle["verifie"]:
            
            score += regle["points"]
        else:
            
            recommandations.append(regle["message"])

    return score, recommandations