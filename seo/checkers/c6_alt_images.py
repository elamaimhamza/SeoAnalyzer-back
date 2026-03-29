from .base import VerificateurDeBase
from seo.regles import appliquer_regles

class VerificateurAltImages(VerificateurDeBase):
    code      = "C6"
    nom       = "Attributs Alt Images"
    poids     = 10
    score_max = 10

    def verifier(self) -> dict:
        images          = self.soup.find_all("img")
        total           = len(images)
        sans_alt        = sum(1 for img in images if not img.get("alt", "").strip())
        avec_alt        = total - sans_alt

        regles = [
            {
                "verifie": total > 0,
                "points":  2,
                "message": "Aucune image trouvée sur la page"
            },
            {
                "verifie": sans_alt == 0,
                "points":  4,
                "message": f"{sans_alt} image(s) sans attribut alt — ajouter une description pour chaque image"
            },
            {
                "verifie": total > 0 and avec_alt == total,
                "points":  4,
                "message": "Toutes les images doivent avoir un attribut alt non vide"
            },
        ]

        score, recommandations = appliquer_regles(regles)

        details = {
            "total_images": total,
            "avec_alt":     avec_alt,
            "sans_alt":     sans_alt
        }

        return {
            "score":           score,
            "score_max":       self.score_max,
            "statut":          self.get_statut(score),
            "details":         details,
            "recommandations": recommandations
        }