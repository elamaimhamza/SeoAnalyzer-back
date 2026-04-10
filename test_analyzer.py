import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from seo.analyzer import analyser

try:
    resultat = analyser("https://www.feen.be/")
    print(" Score global  :", resultat["score_global"])
    print(" Grade         :", resultat["grade"])
    print(" Temps réponse :", resultat["temps_reponse_ms"], "ms")
    print(" HTTPS         :", resultat["est_https"])
    print()
    print(" Critères :")
    for critere in resultat["criteres"]:
        print(f"   {critere['code']} - {critere['nom']} : {critere['score']}/{critere['score_max']} - {critere['statut']}")
    print()
    print(" Recommandations :")
    for reco in resultat["toutes_recommandations"]:
        print(f"   → {reco['critere']} : {reco['message']}")
    print("\n✅ Recommandations IA :")
    print(resultat["recommandations_ia"])
except Exception as e:
    print(" Erreur :", str(e))
    