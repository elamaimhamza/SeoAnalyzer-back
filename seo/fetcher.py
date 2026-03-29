import requests 
import time

def fetch_url(url: str) -> dict:
    
    
    """
    Va chercher le HTML d'une URL sur internet.

    Paramètre :
        url : l'URL à analyser 

    Retourne :
        html             : le contenu HTML de la page
        status_code      : code HTTP ex: 200, 404, 500
        final_url        : l'URL finale après redirections
        response_time_ms : temps de réponse en millisecondes
        is_https         : True si le site utilise HTTPS
    """
    
    headers = {"User-Agent": "SEOAnalyzer/1.0"}
    start   = time.time()

    try:
        response = requests.get(
            url,
            timeout         = 10,    # max 10 secondes
            allow_redirects = True,  # suit les redirections
            headers         = headers
        )
        response_time_ms = int((time.time() - start) * 1000)

        return {
            "html":             response.text,
            "status_code":      response.status_code,
            "final_url":        str(response.url),
            "response_time_ms": response_time_ms,
            "is_https":         str(response.url).startswith("https")
        }

    except requests.exceptions.Timeout:
        raise Exception("Le site n'a pas répondu dans les 10 secondes")

    except requests.exceptions.ConnectionError:
        raise Exception("Impossible de se connecter au site")

    except requests.exceptions.RequestException as erreur:
        raise Exception(f"Erreur de connexion : {str(erreur)}")