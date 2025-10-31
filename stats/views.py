from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd

def index(request):
    if "data" not in request.session:
        return HttpResponse("Aucune donnée disponible. Importez d'abord un fichier dans 📂 Datasets.")

    # Récupération du DataFrame
    df = pd.read_json(request.session["data"])

    # Calcul des statistiques descriptives
    stats = df.describe(include="all").transpose().reset_index()
    stats = stats.fillna("")

    # Traduction des noms de colonnes
    translations = {
        "count": "Nombre de valeurs",
        "mean": "Moyenne",
        "std": "Écart-type",
        "min": "Minimum",
        "25%": "1er quartile (25%)",
        "50%": "Médiane (50%)",
        "75%": "3e quartile (75%)",
        "max": "Maximum",
        "unique": "Valeurs uniques",
        "top": "Valeur la plus fréquente",
        "freq": "Fréquence de la valeur la plus fréquente"
    }
    stats = stats.rename(columns=translations)

    context = {
        "columns": stats.columns.tolist(),
        "rows": stats.values.tolist()
    }
    return render(request, "stats/index.html", context)
