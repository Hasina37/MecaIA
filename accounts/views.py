# views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from utils.requestOpenRouter import get_openrouter_explanation
from django.conf import settings

@login_required
def home(request):
    result = None

    if request.method == "POST":
        symptoms = request.POST.getlist('symptoms')
        other = request.POST.get('otherSymptoms')
        if other:
            symptoms.append(other.lower())

        # Vérifier si les symptômes correspondent aux règles manuelles
        if "fumée noire" in symptoms and "consommation élevée" in symptoms:
            diagnosis = "Problème d'injection"
            severity = "Critique"
            cost = "50 000 - 150 000 Ar"
        elif "moteur chauffe" in symptoms and "fuite liquide" in symptoms:
            diagnosis = "Radiateur défectueux"
            severity = "Moyen"
            cost = "20 000 - 60 000 Ar"
        elif "démarrage difficile" in symptoms and "batterie faible" in symptoms:
            diagnosis = "Panne batterie"
            severity = "Léger"
            cost = "10 000 - 20 000 Ar"
        else:
            # Ici, l'IA fera le diagnostic complet si aucune règle n'est trouvée
            # On envoie juste les symptômes, et on laisse l'IA retourner diagnostic, gravité et coût
            explanation_prompt = f"""
            Tu es un expert en mécanique automobile.
            Voici les symptômes observés : {', '.join(symptoms)}.
            Rédige un diagnostic précis, indique la gravité et fournis un coût estimatif en Ariary.
            ⚠️ Ta réponse doit être claire et concise, uniquement du texte.
            """
            diagnosis = "Diagnostic IA en cours"
            severity = ""
            cost = ""
            # On récupère le texte complet de l'IA
            explanation = get_openrouter_explanation("A déterminer", "A déterminer", "A déterminer", symptoms)
            
            # Ici, si tu veux, tu peux parser le texte de l'IA pour essayer d'extraire
            # diagnostic, gravité et coût, sinon tu peux juste afficher le texte complet
            result = {
                "diagnosis": diagnosis,
                "severity": severity,
                "cost": cost,
                "explanation": explanation
            }
            return render(request, 'home.html', {"result": result})

        # Si règles manuelles appliquées, on appelle l'IA juste pour l'explication
        explanation = get_openrouter_explanation(diagnosis, severity, cost, symptoms)

        result = {
            "diagnosis": diagnosis,
            "severity": severity,
            "cost": cost,
            "explanation": explanation
        }

    return render(request, 'home.html', {"result": result})
