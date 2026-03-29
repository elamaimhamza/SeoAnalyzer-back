from .base import VerificateurDeBase
from seo.regles import appliquer_regles

class VerificateurTempsReponse(VerificateurDeBase):
    code      = "C7"
    nom       = "Temps de réponse"
    poids     = 12
    score_max = 12

    def verifier(self) -> dict:
        ms = self.temps_reponse_ms

        regles = [
            {
                "verifie": ms > 0,
                "points":  2,
                "message": "Impossible de mesurer le temps de réponse"
            },
            {
                "verifie": ms < 4000,
                "points":  4,
                "message": f"Temps de réponse {ms}ms — site très lent, optimiser le serveur"
            },
            {
                "verifie": ms < 2000,
                "points":  6,
                "message": f"Temps de réponse {ms}ms — viser moins de 2 secondes"
            },
        ]

        score, recommandations = appliquer_regles(regles)

        details = {
            "temps_reponse_ms": ms,
            "evaluation":
                "rapide"    if ms < 2000 else
                "acceptable" if ms < 4000 else
                "lent"
        }

        return {
            "score":           score,
            "score_max":       self.score_max,
            "statut":          self.get_statut(score),
            "details":         details,
            "recommandations": recommandations
        }