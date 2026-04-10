from bs4 import BeautifulSoup
from seo.fetcher import fetch_url
from seo.scorer import calculer_score
from seo.checkers.c1_title import VerificateurTitre
from seo.checkers.c2_meta_description import VerificateurMetaDescription
from seo.checkers.c3_h1 import VerificateurH1
from seo.checkers.c4_headings import VerificateurStructureTitres
from seo.checkers.c5_canonical import VerificateurCanonical
from seo.checkers.c6_alt_images import VerificateurAltImages
from seo.checkers.c7_response_time import VerificateurTempsReponse
from seo.checkers.c8_https import VerificateurHTTPS
from seo.checkers.c9_url_structure import VerificateurStructureURL
from seo.checkers.c10_viewport import VerificateurViewport
from seo.ai_recommandations import generer_recommandations_ia

#Liste de tous les vérificateurs :
VERIFICATEURS = [

    VerificateurTitre,
    VerificateurMetaDescription,
    VerificateurH1,
    VerificateurStructureTitres,
    VerificateurCanonical,
    VerificateurAltImages,
    VerificateurTempsReponse,
    VerificateurHTTPS,
    VerificateurStructureURL,
    VerificateurViewport,
]

def analyser(url: str) -> dict:
    """
    Orchestre toute l'analyse SEO d'une URL.

    Étapes :
        1. Récupère le HTML de l'URL
        2. Parse le HTML avec BeautifulSoup
        3. Lance les 10 vérificateurs
        4. Calcule le score global et le grade
        5. Regroupe toutes les recommandations
        6. Retourne le rapport complet
    """

    #Étape1 : Récupérer le HTML
    recupere = fetch_url(url)

    #Étape2 : Parser le HTML
    soup = BeautifulSoup(recupere["html"], "lxml")

    #Étape3 : Lancer les 10 vérificateurs
    resultats = []
    for ClasseVerificateur in VERIFICATEURS:
        verificateur = ClasseVerificateur(
            soup             = soup,
            url              = recupere["final_url"],
            temps_reponse_ms = recupere["response_time_ms"]
        )
        resultat          = verificateur.verifier()
        resultat["code"]  = verificateur.code
        resultat["nom"]   = verificateur.nom
        resultat["poids"] = verificateur.poids
        resultats.append(resultat)

    #Étape 4 : Calculer le score global et le grade
    score_global, grade = calculer_score(resultats)

    #Étape 5 : Regrouper toutes les recommandations
    toutes_recommandations = []
    for resultat in resultats:
        for recommandation in resultat["recommandations"]:
            toutes_recommandations.append({
                "critere": resultat["nom"],
                "message": recommandation
            })
            
    # Étape 6 — Générer les recommandations IA
    recommandations_ia = generer_recommandations_ia({
    "url_finale":       recupere["final_url"],
    "score_global":     score_global,
    "grade":            grade,
    "temps_reponse_ms": recupere["response_time_ms"],
    "est_https":        recupere["is_https"],
    "criteres":         resultats
})

    #Étape 7 : Retourner le rapport complet
    return {
        "url":                    url,
        "url_finale":             recupere["final_url"],
        "score_global":           score_global,
        "grade":                  grade,
        "temps_reponse_ms":       recupere["response_time_ms"],
        "est_https":              recupere["is_https"],
        "statut_http":            recupere["status_code"],
        "criteres":               resultats,
        "toutes_recommandations": toutes_recommandations,
        "recommandations_ia":     recommandations_ia 
    }
