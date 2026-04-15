import asyncio
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__)))

from db.database import engine, Base, AsyncSessionLocal
from db.models import CriteresSEO

criteres = [
    {"code": "C1",  "nom": "Balise Title",        "poids": 15, "score_max": 15, "description": "Présence et longueur optimale du titre (50-60 car.)"},
    {"code": "C2",  "nom": "Meta Description",     "poids": 10, "score_max": 10, "description": "Présence et longueur optimale (150-160 car.)"},
    {"code": "C3",  "nom": "Balise H1 unique",     "poids": 10, "score_max": 10, "description": "Présence d'un seul H1 avec contenu significatif"},
    {"code": "C4",  "nom": "Structure Headings",   "poids": 8,  "score_max": 8,  "description": "Hiérarchie logique H2 vers H3"},
    {"code": "C5",  "nom": "Balise Canonical",     "poids": 8,  "score_max": 8,  "description": "Présence de link rel canonical"},
    {"code": "C6",  "nom": "Attributs Alt Images", "poids": 10, "score_max": 10, "description": "100% des images ont un attribut alt non vide"},
    {"code": "C7",  "nom": "Temps de réponse",     "poids": 12, "score_max": 12, "description": "Délai HTTP moins de 2s"},
    {"code": "C8",  "nom": "HTTPS / Sécurité",     "poids": 10, "score_max": 10, "description": "URL en HTTPS"},
    {"code": "C9",  "nom": "Structure URL",        "poids": 7,  "score_max": 7,  "description": "URL courte et lisible"},
    {"code": "C10", "nom": "Meta Viewport",        "poids": 10, "score_max": 10, "description": "Présence de meta viewport"},
]

async def init():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✅ Tables créées !")

    async with AsyncSessionLocal() as session:
        for c in criteres:
            critere = CriteresSEO(**c)
            session.add(critere)
        try:
            await session.commit()
            print("✅ 10 critères SEO insérés !")
        except Exception as e:
            print("⚠️ Critères déjà existants :", str(e))

if __name__ == "__main__":
    asyncio.run(init())