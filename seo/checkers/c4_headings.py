from .base import VerificateurDeBase
from seo.regles import appliquer_regles

class VerificateurStructureTitres(VerificateurDeBase):
    code      = "C4"
    nom       = "Structure Headings"
    poids     = 8
    score_max = 8

    def verifier(self) -> dict:
        titres    = self.soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"])
        niveaux   = [int(h.name[1]) for h in titres]
        saut_detecte = False

        # Vérifier s'il y a un saut de niveau
        for i in range(1, len(niveaux)):
            if niveaux[i] - niveaux[i - 1] > 1:
                saut_detecte = True
                break

        regles = [
            {
                "verifie": len(titres) > 0,
                "points":  3,
                "message": "Aucun titre trouvé — ajouter des balises H2, H3 pour structurer la page"
            },
            {
                "verifie": not saut_detecte,
                "points":  3,
                "message": "La hiérarchie des titres présente des sauts de niveaux ex: H1 → H3 sans H2"
            },
            {
                "verifie": len(titres) >= 2,
                "points":  2,
                "message": "Ajouter au moins un H2 pour structurer le contenu"
            },
        ]

        score, recommandations = appliquer_regles(regles)

        details = {
            "nombre_titres": len(titres),
            "titres": [
                {"balise": h.name, "texte": h.get_text(strip=True)[:60]}
                for h in titres
            ]
        }

        return {
            "score":           score,
            "score_max":       self.score_max,
            "statut":          self.get_statut(score),
            "details":         details,
            "recommandations": recommandations
        }