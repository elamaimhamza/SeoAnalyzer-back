from .base import VérificateurDeBase
from seo.regles import appliquer_regles


class VérificateurMetaDescription(VérificateurDeBase):
    code      = "C2"
    nom       = "Meta Description"
    poids     = 10
    score_max = 10

    def verifier(self) -> dict:
        meta        = self.soup.find("meta", attrs={"name": "description"})
        description = meta.get("content", "").strip() if meta else ""
        longueur    = len(description)

        regles = [
            {
                "vérifié": meta is not None,
                "points":  4,
                "message": "Ajouter une balise <meta name='description'>"
            },
            {
                "vérifié": longueur > 0,
                "points":  3,
                "message": "La meta description ne doit pas être vide"
            },
            {
                "vérifié": 150 <= longueur <= 160,
                "points":  3,
                "message": f"Longueur {longueur} car. — viser entre 150 et 160 caractères"
            },
        ]

        score, recommandations = appliquer_regles(regles)

        return {
            "score":           score,
            "score_max":       self.score_max,
            "statut":          self.get_statut(score),
            "details":         {"description": description, "longueur": longueur},
            "recommandations": recommandations
        }