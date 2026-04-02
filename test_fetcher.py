import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from seo.fetcher import fetch_url
from bs4 import BeautifulSoup

resultat = fetch_url("https://www.eafc-uccle.be/")

print(" URL finale    :", resultat["final_url"])
print(" Status HTTP   :", resultat["status_code"])
print(" Temps réponse :", resultat["response_time_ms"], "ms")
print(" HTTPS         :", resultat["is_https"])
print()

# Test BeautifulSoup
soup = BeautifulSoup(resultat["html"], "lxml")

print(" Title         :", soup.find("title").get_text() if soup.find("title") else "Pas de title")
print(" H1            :", soup.find("h1").get_text() if soup.find("h1") else "Pas de H1")
print(" Meta desc     :", soup.find("meta", attrs={"name": "description"}))
print(" Images        :", len(soup.find_all("img")))
print(" Canonical     :", soup.find("link", rel="canonical"))