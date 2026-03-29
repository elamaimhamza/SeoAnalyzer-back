from .base import VerificateurDeBase
from seo.regles import appliquer_regles


class VerificateurTitre(VerificateurDeBase):
    code      = "C1"
    nom       = "Balise Title"
    poids     = 15
    score_max = 15

    def verifier(self) -> dict:
        balise_title = self.soup.find("title")
        titre        = balise_title.get_text(strip=True) if balise_title else ""
        longueur     = len(titre)

        regles = [
            {
                "vérifié": balise_title is not None,
                "points":  5,
                "message": "Ajouter une balise <title>"
            },
            {
                "vérifié": longueur > 0,
                "points":  4,
                "message": "La balise <title> ne doit pas être vide"
            },
            {
                "vérifié": 50 <= longueur <= 60,
                "points":  6,
                "message": f"Longueur {longueur} car. — viser entre 50 et 60 caractères"
            },
        ]

        score, recommandations = appliquer_regles(regles)

        return {
            "score":           score,
            "score_max":       self.score_max,
            "statut":          self.get_statut(score),
            "details":         {"titre": titre, "longueur": longueur},
            "recommandations": recommandations
        }