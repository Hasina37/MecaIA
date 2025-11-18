# utils/requestOpenRouter.py
import requests
import json
from django.conf import settings

def get_openrouter_explanation(diagnosis: str, severity: str, cost: str, symptoms: list) -> str:
    """
    Appelle OpenRouter pour générer une explication textuelle pour le diagnostic automobile.
    """

    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    prompt = f"""
    Tu es un expert en mécanique automobile.
    Voici le diagnostic d'un véhicule :
    - Diagnostic : {diagnosis}
    - Gravité : {severity}
    - Coût estimatif : {cost}
    - Symptômes observés : {', '.join(symptoms)}

    Rédige une explication concise et claire pour un mécanicien ou un utilisateur non expert.
    ⚠️ Ta réponse doit être uniquement du texte clair (pas de JSON).
    """

    payload = {
        "model": "gpt-4o-mini",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 500
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=15)
        response.raise_for_status()
        data = response.json()
        explanation = data["choices"][0]["message"]["content"].strip()
        return explanation

    except requests.exceptions.RequestException as e:
        return f"Explication indisponible (erreur OpenRouter: {str(e)})"
