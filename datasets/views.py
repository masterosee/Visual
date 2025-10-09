from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
import io
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors


def index(request):
    """
    Page principale du module Datasets :
    - Permet d'importer un fichier CSV/Excel
    - Affiche un aperçu des 10 premières lignes
    - Sauvegarde les données en session pour export
    """
    context = {}
    if request.method == "POST" and request.FILES.get("file"):
        file = request.FILES["file"]
        try:
            # Lecture du fichier selon son extension
            if file.name.endswith(".csv"):
                df = pd.read_csv(file)
            elif file.name.endswith((".xls", ".xlsx")):
                df = pd.read_excel(file)
            else:
                return HttpResponse("❌ Format non supporté. Utilisez CSV ou Excel.")

            # Sauvegarde en session (JSON)
            request.session["data"] = df.to_json()

            # Aperçu des 10 premières lignes (convertis en listes pour éviter l'erreur)
            context["columns"] = df.columns.tolist()
            context["rows"] = df.head(10).values.tolist()

        except Exception as e:
            return HttpResponse(f"⚠️ Erreur lors de la lecture du fichier : {e}")

    return render(request, "datasets/index.html", context)


def export_csv(request):
    """
    Exporte les données importées en CSV
    """
    if "data" not in request.session:
        return HttpResponse("❌ Aucune donnée à exporter. Importez d'abord un fichier.")

    df = pd.read_json(request.session["data"])

    buffer = io.StringIO()
    df.to_csv(buffer, index=False)

    response = HttpResponse(buffer.getvalue(), content_type="text/csv")
    response['Content-Disposition'] = 'attachment; filename="export.csv"'
    return response


def export_excel(request):
    """
    Exporte les données importées en Excel
    """
    if "data" not in request.session:
        return HttpResponse("❌ Aucune donnée à exporter. Importez d'abord un fichier.")

    df = pd.read_json(request.session["data"])

    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="Données")

    response = HttpResponse(
        buffer.getvalue(),
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response['Content-Disposition'] = 'attachment; filename="export.xlsx"'
    return response


def export_pdf(request):
    """
    Exporte les données importées en PDF (tableau simple)
    """
    if "data" not in request.session:
        return HttpResponse("❌ Aucune donnée à exporter. Importez d'abord un fichier.")

    df = pd.read_json(request.session["data"])

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer)

    # Construire le tableau (colonnes + données)
    data = [df.columns.tolist()] + df.values.tolist()
    table = Table(data)

    # Style du tableau
    table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.grey),
        ("TEXTCOLOR", (0,0), (-1,0), colors.whitesmoke),
        ("ALIGN", (0,0), (-1,-1), "CENTER"),
        ("GRID", (0,0), (-1,-1), 0.5, colors.black),
        ("FONTSIZE", (0,0), (-1,-1), 8),
    ]))

    doc.build([table])

    response = HttpResponse(buffer.getvalue(), content_type="application/pdf")
    response['Content-Disposition'] = 'attachment; filename="export.pdf"'
    return response
