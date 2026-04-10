from pydantic import BaseModel, HttpUrl
from typing import List

#Ce que le frontend envoie 
class AnalyseRequete(BaseModel):
    url: HttpUrl

#La forme d'un critère dans la réponse 
class ResultatCritere(BaseModel):
    code:            str
    nom:             str
    score:           int
    score_max:       int
    poids:           int
    statut:          str
    details:         dict
    recommandations: List[str]

#La forme d'une recommandation
class Recommandation(BaseModel):
    critere: str
    message: str

#e que le backend retourne au frontend
class AnalyseReponse(BaseModel):
    url:                    str
    url_finale:             str
    score_global:           int
    grade:                  str
    temps_reponse_ms:       int
    est_https:              bool
    statut_http:            int
    criteres:               List[ResultatCritere]
    toutes_recommandations: List[Recommandation]
    recommandations_ia:     str