from abc import ABC, abstractmethod
from bs4 import BeautifulSoup



class VérificateurDeBase(ABC):
    
    code       = ""
    nom        = ""
    poids      = 0
    score_max  = 0
    

    def __init__(self, soup: BeautifulSoup, url: str = "", temps_reponse_ms: int = 0):
        self.soup = soup
        self.url = url
        self.temps_reponse_ms = temps_reponse_ms

    #cette fonction doit retourner un dictionnaire 
    @abstractmethod
    def verifier(self) -> dict:  
        """Chaque critère DOIT implémenter cette méthode"""
        pass

    def get_statut(self, score: int) -> str:
        ratio = score / self.score_max if self.score_max > 0 else 0
        #ça veut dire que le score de chaque critère si dépasse 80% de son score max 
        # ex: C1 :12/15 = 80% donc la fonction va retourner (réussi) 
        if ratio >= 0.8: 
            return "réussi"
        elif ratio >= 0.5:#50%
            return "avertissement"
        return "échoué"