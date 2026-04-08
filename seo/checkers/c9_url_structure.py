from .base import VerificateurDeBase
from seo.regles import appliquer_regles
from urllib.parse import urlparse, parse_qs



class VerificateurStructureURL(VerificateurDeBase):
    code      = "C9"
    nom       = "Structure URL"
    poids     = 7
    score_max = 7

    def verifier(self) -> dict:
        url             = self.url
        analyse         = urlparse(url)
        chemin          = analyse.path
        parametres      = parse_qs(analyse.query)
        longueur        = len(url)

        regles = [
            {
                "verifie": longueur <= 100,
                "points":  2,
                "message": f"URL trop longue ({longueur} Je vous conseille de viser moins de 100 caractères"
            },
            {
                "verifie": len(parametres) <= 2,
                "points":  2,
                "message": f"{len(parametres)} paramètres dans l'URL — simplifier la structure"
            },
            {
                "verifie": "_" not in chemin,
                "points":  1,
                "message": "Utiliser des tirets (-) plutôt que des underscores (_) dans l'URL"
            },
            {
                "verifie": "%20" not in url and " " not in url,
                "points":  1,
                "message": "L'URL contient des espaces — les remplacer par des tirets (-)"
            },
            {
                "verifie": url == url.lower(),
                "points":  1,
                "message": "L'URL contient des majuscules — utiliser uniquement des minuscules"
            },
        ]

        score, recommandations = appliquer_regles(regles)

        details = {
            "url":              url,
            "longueur":         longueur,
            "nombre_parametres": len(parametres),
            "chemin":           chemin
        }

        return {
            "score":           score,
            "score_max":       self.score_max,
            "statut":          self.get_statut(score),
            "details":         details,
            "recommandations": recommandations
        }