from .base import VerificateurDeBase
from seo.regles import appliquer_regles


class VerificateurViewport(VerificateurDeBase):
    code      = "C10"
    nom       = "Meta Viewport"
    poids     = 10
    score_max = 10

    def verifier(self) -> dict:
        viewport = self.soup.find("meta", attrs={"name": "viewport"})
        contenu  = ""

        if viewport:
            contenu = viewport.get("content", "").strip()

        regles = [
            {
                "verifie": viewport is not None,
                "points":  4,
                "message": "Ajouter une balise <meta name='viewport'>"
            },
            {
                "verifie": len(contenu) > 0,
                "points":  3,
                "message": "La balise viewport est présente mais l'attribut content est vide"
            },
            {
                "verifie": "width=device-width" in contenu,
                "points":  2,
                "message": "Ajouter 'width=device-width' dans le contenu de la balise viewport"
            },
            {
                "verifie": "initial-scale=1" in contenu,
                "points":  1,
                "message": "Ajouter 'initial-scale=1' dans le contenu de la balise viewport"
            },
        ]

        score, recommandations = appliquer_regles(regles)

        details = {
            "viewport_present": viewport is not None,
            "contenu":          contenu
        }

        return {
            "score":           score,
            "score_max":       self.score_max,
            "statut":          self.get_statut(score),
            "details":         details,
            "recommandations": recommandations
        }