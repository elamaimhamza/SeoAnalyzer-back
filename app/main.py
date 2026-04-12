import sys
import os
import uuid
import hashlib
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.schemas import AnalyseRequete, AnalyseReponse
from seo.analyzer import analyser
from db.database import AsyncSessionLocal
from db.models import RequeteAnalyse, RapportSEO, ResultatCritere, Historique

app = FastAPI(
    title       = "SEO Analyzer API",
    description = "Analyse SEO de n'importe quelle URL",
    version     = "1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins     = ["http://localhost:5173","https://seo-analyzer-front.vercel.app"],
    allow_credentials = True,
    allow_methods     = ["*"],
    allow_headers     = ["*"],
)

@app.get("/")
async def racine():
    return {"message": "SEO Analyzer API fonctionne !"}

@app.post("/api/v1/analyze", response_model=AnalyseReponse)
async def analyser_url(requete: AnalyseRequete, request: Request):
    try:
        #Étape 1 : Analyse SEO 
        resultat = analyser(str(requete.url))

        #Étape 2 : Sauvegarde en MySQL 
        async with AsyncSessionLocal() as session:

            # Hash de l'URL
            url_hash = hashlib.sha256(
                str(requete.url).encode()
            ).hexdigest()

            # Hash de l'IP (RGPD)
            ip_client = request.client.host if request.client else ""
            ip_hash   = hashlib.sha256(ip_client.encode()).hexdigest()

            # 1. Sauvegarder RequeteAnalyse
            requete_db = RequeteAnalyse(
                id               = str(uuid.uuid4()),
                url              = str(requete.url),
                url_hash         = url_hash,
                created_at       = datetime.utcnow(),
                ip_hash          = ip_hash,
                user_agent       = request.headers.get("user-agent", ""),
                response_time_ms = resultat["temps_reponse_ms"],
                http_status      = resultat["statut_http"],
                final_url        = resultat["url_finale"],
                is_https         = resultat["est_https"],
                error_message    = None
            )
            session.add(requete_db)
            await session.flush()

            # 2. Sauvegarder RapportSEO
            rapport_db = RapportSEO(
                id                 = str(uuid.uuid4()),
                requete_id         = requete_db.id,
                global_score       = resultat["score_global"],
                grade              = resultat["grade"],
                page_title         = resultat["criteres"][0]["details"].get("titre"),
                meta_description   = resultat["criteres"][1]["details"].get("description"),
                h1_text            = resultat["criteres"][2]["details"].get("texte_h1"),
                images_total       = resultat["criteres"][5]["details"].get("total_images"),
                images_without_alt = resultat["criteres"][5]["details"].get("sans_alt"),
                has_canonical      = resultat["criteres"][4]["details"].get("canonical_present", False),
                has_viewport       = resultat["criteres"][9]["details"].get("viewport_present", False),
                analyzed_at        = datetime.utcnow()
            )
            session.add(rapport_db)
            await session.flush()

            # 3. Sauvegarder les 10 ResultatCritere
            for critere in resultat["criteres"]:
                resultat_db = ResultatCritere(
                    id             = str(uuid.uuid4()),
                    rapport_id      = rapport_db.id,
                    critere_code = critere["code"],
                    score          = critere["score"],
                    status         = critere["statut"],
                    details        = critere["details"],
                    recommendations= critere["recommandations"]
                )
                session.add(resultat_db)

            # 4. Sauvegarder Historique
            historique_db = Historique(
                id               = str(uuid.uuid4()),
                url              = str(requete.url),
                created_at       = datetime.utcnow(),
                response_time_ms = resultat["temps_reponse_ms"],
                http_status      = resultat["statut_http"],
                global_score     = resultat["score_global"],
                grade            = resultat["grade"],
                page_title       = resultat["criteres"][0]["details"].get("titre"),
                has_canonical    = resultat["criteres"][4]["details"].get("canonical_present", False),
                has_viewport     = resultat["criteres"][9]["details"].get("viewport_present", False),
                is_https         = resultat["est_https"],
                error_message    = None
            )
            session.add(historique_db)

            # 5. Commit final
            await session.commit()

        return resultat

    except Exception as erreur:
        print("❌ ERREUR EXACTE :", str(erreur))  # ← ajoute cette ligne
        raise HTTPException(
            status_code = 400,
            detail      = f"Erreur lors de l'analyse : {str(erreur)}"
        )
