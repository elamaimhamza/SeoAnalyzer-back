from .base import VerificateurDeBase
from seo.regles import appliquer_regles

class VerificateurH1(VerificateurDeBase):
    code      = "C3"
    nom       = "Balise H1 unique"
    poids     = 10
    score_max = 10

    def verifier(self) -> dict:
        balises_h1 = self.soup.find_all("h1")
        nombre_h1  = len(balises_h1)
        texte_h1   = balises_h1[0].get_text(strip=True) if nombre_h1 > 0 else ""

        regles = [
            {
                "verifie": nombre_h1 > 0,
                "points":  4,
                "message": "Ajouter une balise H1 sur la page"
            },
            {
                "verifie": nombre_h1 == 1,
                "points":  4,
                "message": f"{nombre_h1} balises H1 trouvées — il ne doit y en avoir qu'une seule"
            },
            {
                "verifie": len(texte_h1) > 0,
                "points":  2,
                "message": "Le H1 est vide — ajouter un contenu significatif"
            },
        ]

        score, recommandations = appliquer_regles(regles)

        return {
            "score":           score,
            "score_max":       self.score_max,
            "statut":          self.get_statut(score),
            "details":         {"nombre_h1": nombre_h1, "texte_h1": texte_h1},
            "recommandations": recommandations
        }