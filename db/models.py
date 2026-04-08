from sqlalchemy import Column, String, SmallInteger, Integer, Boolean, Text, DateTime, JSON, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from db.database import Base


class RequeteAnalyse(Base):
    __tablename__ = "requete_analyse"

    id               = Column(String(36), primary_key=True)
    url              = Column(String(2048), nullable=False)
    url_hash         = Column(String(64), nullable=False, index=True)
    created_at       = Column(DateTime, default=datetime.utcnow)
    ip_hash          = Column(String(64), nullable=True, index=True)
    user_agent       = Column(Text, nullable=True)
    response_time_ms = Column(Integer, nullable=True)
    http_status      = Column(SmallInteger, nullable=True)
    final_url        = Column(String(2048), nullable=True)
    is_https         = Column(Boolean, nullable=False, default=False)
    error_message    = Column(Text, nullable=True)

    rapport = relationship("RapportSEO", back_populates="requete", cascade="all, delete")


class RapportSEO(Base):
    __tablename__ = "rapport_seo"

    id                 = Column(String(36), primary_key=True)
    requete_id         = Column(String(36), ForeignKey("requete_analyse.id", ondelete="CASCADE"), nullable=False)
    global_score       = Column(SmallInteger, nullable=False)
    grade              = Column(String(2), nullable=False)
    page_title         = Column(String(512), nullable=True)
    meta_description   = Column(String(512), nullable=True)
    h1_text            = Column(Text, nullable=True)
    word_count         = Column(Integer, nullable=True)
    images_total       = Column(SmallInteger, nullable=True)
    images_without_alt = Column(SmallInteger, nullable=True)
    has_canonical      = Column(Boolean, nullable=False, default=False)
    has_viewport       = Column(Boolean, nullable=False, default=False)
    analyzed_at        = Column(DateTime, default=datetime.utcnow)

    requete   = relationship("RequeteAnalyse", back_populates="rapport")
    resultats = relationship("ResultatCritere", back_populates="rapport", cascade="all, delete")


class CriteresSEO(Base):
    __tablename__ = "criteres_seo"

    code        = Column(String(10), primary_key=True)
    nom         = Column(String(128), nullable=False)
    description = Column(Text, nullable=True)
    poids       = Column(SmallInteger, nullable=False)
    score_max   = Column(SmallInteger, nullable=False, default=100)

    resultats = relationship("ResultatCritere", back_populates="critere")


class ResultatCritere(Base):
    __tablename__ = "resultat_critere"

    id             = Column(String(36), primary_key=True)
    rapport_id      = Column(String(36), ForeignKey("rapport_seo.id", ondelete="CASCADE"), nullable=False)
    critere_code = Column(String(10), ForeignKey("criteres_seo.code"), nullable=False)
    score          = Column(SmallInteger, nullable=False)
    max_score      = Column(SmallInteger, nullable=True)
    weight         = Column(SmallInteger, nullable=True)
    status         = Column(String(10), nullable=False)
    details        = Column(JSON, nullable=True)
    recommendations = Column(JSON, nullable=True)

    rapport = relationship("RapportSEO", back_populates="resultats")
    critere = relationship("CriteresSEO", back_populates="resultats")


class Historique(Base):
    __tablename__ = "historique"

    id               = Column(String(36), primary_key=True)
    url              = Column(String(2048), nullable=False)
    created_at       = Column(DateTime, default=datetime.utcnow)
    response_time_ms = Column(Integer, nullable=True)
    http_status      = Column(SmallInteger, nullable=True)
    global_score     = Column(SmallInteger, nullable=True)
    grade            = Column(String(2), nullable=True)
    page_title       = Column(String(512), nullable=True)
    has_canonical    = Column(Boolean, nullable=True)
    has_viewport     = Column(Boolean, nullable=True)
    is_https         = Column(Boolean, nullable=True)
    error_message    = Column(Text, nullable=True)