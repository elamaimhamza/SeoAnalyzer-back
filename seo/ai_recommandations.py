import os
import anthropic
from dotenv import load_dotenv

load_dotenv()

def generer_recommandations_ia(resultat: dict) -> str:
    """
    Envoie les résultats de l'analyse SEO à Claude
    et retourne des recommandations personnalisées
    """

    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    # Prépare les critères échoués et en avertissement
    criteres_echoues = [
        f"{c['nom']} ({c['score']}/{c['score_max']} pts)"
        for c in resultat["criteres"]
        if c["statut"] == "échoué"
    ]

    criteres_avertissement = [
        f"{c['nom']} ({c['score']}/{c['score_max']} pts)"
        for c in resultat["criteres"]
        if c["statut"] == "avertissement"
    ]

    criteres_reussis = [
        c["nom"]
        for c in resultat["criteres"]
        if c["statut"] == "réussi"
    ]

    prompt = f"""
Tu es un expert SEO senior. Voici les résultats d'une analyse SEO pour le site : {resultat['url_finale']}

SCORE GLOBAL : {resultat['score_global']}/100 — Grade : {resultat['grade']}
TEMPS DE RÉPONSE : {resultat['temps_reponse_ms']} ms
HTTPS : {'Oui' if resultat['est_https'] else 'Non'}

CRITÈRES ÉCHOUÉS :
{chr(10).join(f'- {c}' for c in criteres_echoues) if criteres_echoues else '- Aucun'}

CRITÈRES EN AVERTISSEMENT :
{chr(10).join(f'- {c}' for c in criteres_avertissement) if criteres_avertissement else '- Aucun'}

CRITÈRES RÉUSSIS :
{chr(10).join(f'- {c}' for c in criteres_reussis) if criteres_reussis else '- Aucun'}

En te basant sur ces résultats, génère un rapport de recommandations SEO personnalisées en français.
Le rapport doit contenir :
1. Un résumé rapide de l'état du site en 2-3 phrases
2. Les 3 actions prioritaires à faire en premier avec des explications concrètes
3. Les améliorations secondaires à faire ensuite
4. Un conseil final encourageant

Sois concret, précis et adapte tes conseils au contexte de ce site spécifique.
    """

    reponse = client.messages.create(
        model      = "claude-opus-4-5",
        max_tokens = 2048,
        messages   = [{"role": "user", "content": prompt}]
    )

    return reponse.content[0].text