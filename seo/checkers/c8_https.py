from .base import VerificateurDeBase
from seo.regles import appliquer_regles

class VerificateurHTTPS(VerificateurDeBase):
    code      = "C8"
    nom       = "HTTPS / Sécurité"
    poids     = 10
    score_max = 10

    def verifier(self) -> dict:
        url             = self.url
        est_https       = url.startswith("https")
        pas_http        = not url.startswith("http://")

        regles = [
            {
                "verifie": est_https,
                "points":  6,
                "message": "Le site n'utilise pas HTTPS — installer un certificat SSL"
            },
            {
                "verifie": pas_http,
                "points":  2,
                "message": "Le site utilise HTTP non sécurisé — migrer vers HTTPS"
            },
            {
                "verifie": not url.startswith("http://www"),
                "points":  2,
                "message": "Rediriger http://www vers https:// pour éviter le contenu dupliqué"
            },
        ]

        score, recommandations = appliquer_regles(regles)

        details = {
            "url":       url,
            "est_https": est_https
        }

        return {
            "score":           score,
            "score_max":       self.score_max,
            "statut":          self.get_statut(score),
            "details":         details,
            "recommandations": recommandations
        }