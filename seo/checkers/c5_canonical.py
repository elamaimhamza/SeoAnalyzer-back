from .base import VerificateurDeBase
from seo.regles import appliquer_regles

class VerificateurCanonical(VerificateurDeBase):
    code      = "C5"
    nom       = "Balise Canonical"
    poids     = 8
    score_max = 8

    def verifier(self) -> dict:
        canonical    = self.soup.find("link", rel="canonical")
        url_canonical = ""

        if canonical:
            url_canonical = canonical.get("href", "").strip()

        regles = [
            {
                "verifie": canonical is not None,
                "points":  4,
                "message": "Ajouter une balise <link rel='canonical' href='...'>"
            },
            {
                "verifie": len(url_canonical) > 0,
                "points":  2,
                "message": "La balise canonical est présente mais l'attribut href est vide"
            },
            {
                "verifie": url_canonical.startswith("https"),
                "points":  2,
                "message": "L'URL canonical doit commencer par https"
            },
        ]

        score, recommandations = appliquer_regles(regles)

        details = {
            "canonical_present": canonical is not None,
            "url_canonical":     url_canonical
        }

        return {
            "score":           score,
            "score_max":       self.score_max,
            "statut":          self.get_statut(score),
            "details":         details,
            "recommandations": recommandations
        }