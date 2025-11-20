import requests
from django.conf import settings
import json

def get_openrouter_explanation(symptoms: list) -> dict:
    """
    Appelle OpenRouter pour générer :
    - diagnostic
    - gravité
    - coût estimatif
    - explication
    Le tout en JSON structuré.
    """

    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    prompt = f"""
    Tu es un expert en mécanique automobile.
    Symptômes observés : {', '.join(symptoms)}.
    
    Analyse la situation et retourne STRICTEMENT un JSON :
    {{
      "diagnosis": "...",
      "severity": "Léger / Moyen / Critique",
      "cost": "... Ariary",
      "explanation": "Texte clair"
    }}
    Pas d'autres mots, pas de texte autour, uniquement le JSON valide.
    """

    body = {
        "model": "gpt-4o-mini",
        "messages": [{"role": "user", "content": prompt}],
    }

    try:
        response = requests.post(url, headers=headers, json=body, timeout=15)
        response.raise_for_status()
        content = response.json()["choices"][0]["message"]["content"].strip()

        return json.loads(content)

    except Exception as e:
        return {
            "diagnosis": "Erreur IA",
            "severity": "Inconnu",
            "cost": "Inconnu",
            "explanation": f"Erreur OpenRouter : {str(e)}",
        }
