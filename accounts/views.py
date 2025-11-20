# views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from utils.requestOpenRouter import get_openrouter_explanation


def is_relevant_to_car(text):
    keywords = [
        "moteur", "voiture", "pneu", "fumée", "démarrage", "batterie",
        "frein", "accélération", "carburant", "huile", "radiateur",
        "embrayage", "transmission", "direction", "vibration",
        "fuite", "consommation", "klaxon", "échappement"
    ]
    text = text.lower()
    return any(word in text for word in keywords)


@login_required
def home(request):
    result = None

    if request.method == "POST":
        symptoms = request.POST.getlist('symptoms')
        other = request.POST.get('otherSymptoms')

        if other:
            # Vérification si le texte libre a un rapport avec la mécanique
            if not is_relevant_to_car(other):
                return render(request, 'home.html', {
                    "result": {
                        "diagnosis": "Invalide",
                        "severity": "-",
                        "cost": "-",
                        "explanation": "Ce que vous avez saisi n’a aucun rapport avec l’automobile."
                    }
                })

            symptoms.append(other.lower())

        # ------- RÈGLES MANUELLES -------
        if "fumée noire" in symptoms and "consommation élevée" in symptoms:
            diagnosis = "Problème d'injection"
            severity = "Critique"
            cost = "50 000 - 150 000 Ar"
            explanation = get_openrouter_explanation(symptoms)["explanation"]

        elif "moteur chauffe" in symptoms and "fuite liquide" in symptoms:
            diagnosis = "Radiateur défectueux"
            severity = "Moyen"
            cost = "20 000 - 60 000 Ar"
            explanation = get_openrouter_explanation(symptoms)["explanation"]

        elif "démarrage difficile" in symptoms and "batterie faible" in symptoms:
            diagnosis = "Panne batterie"
            severity = "Léger"
            cost = "10 000 - 20 000 Ar"
            explanation = get_openrouter_explanation(symptoms)["explanation"]

        else:
            # ------- CAS IA COMPLET -------
            ia = get_openrouter_explanation(symptoms)

            return render(request, 'home.html', {"result": ia})

        # Résultat pour les cas manuels
        result = {
            "diagnosis": diagnosis,
            "severity": severity,
            "cost": cost,
            "explanation": explanation,
        }

    return render(request, 'home.html', {"result": result})
