from django.shortcuts import render
import plotly.express as px
import pandas as pd


def histogram_view(request):
    data = {
        "magnitude": [7.0, 6.9, 7.0, 7.3, 6.6, 7.0, 6.8, 6.7, 6.8, 7.6],
        "depth": [14, 25, 579, 37, 624, 660, 630, 20, 20, 26]
    }
    df = pd.DataFrame(data)

    fig = px.histogram(df, x="magnitude", nbins=10, title="Distribution des magnitudes")
    graph_html = fig.to_html(full_html=False)
    return render(request, "graphiques/histogram.html", {"graph": graph_html})


def scatter_view(request):
    data = {
        "magnitude": [7.0, 6.9, 7.0, 7.3, 6.6, 7.0, 6.8, 6.7, 6.8, 7.6],
        "depth": [14, 25, 579, 37, 624, 660, 630, 20, 20, 26]
    }
    df = pd.DataFrame(data)

    fig = px.scatter(
        df,
        x="depth",
        y="magnitude",
        title="Magnitude en fonction de la profondeur",
        labels={"depth": "Profondeur (km)", "magnitude": "Magnitude"},
        color="magnitude",
        size="magnitude"
    )
    graph_html = fig.to_html(full_html=False)
    return render(request, "graphiques/scatter.html", {"graph": graph_html})


def boxplot_view(request):
    data = {
        "magnitude": [7.0, 6.9, 7.0, 7.3, 6.6, 7.0, 6.8, 6.7, 6.8, 7.6],
        "depth": [14, 25, 579, 37, 624, 660, 630, 20, 20, 26]
    }
    df = pd.DataFrame(data)

    fig = px.box(
        df,
        y="magnitude",
        points="all",
        title="Distribution des magnitudes (Boxplot)",
        labels={"magnitude": "Magnitude"}
    )
    graph_html = fig.to_html(full_html=False)
    return render(request, "graphiques/boxplot.html", {"graph": graph_html})


def bar_view(request):
    data = {
        "region": ["Nord", "Sud", "Est", "Ouest"],
        "seismes": [12, 7, 5, 9]
    }
    df = pd.DataFrame(data)

    fig = px.bar(
        df,
        x="region",
        y="seismes",
        title="Nombre de séismes par région",
        color="region"
    )
    graph_html = fig.to_html(full_html=False)
    return render(request, "graphiques/bar.html", {"graph": graph_html})


def pie_view(request):
    data = {
        "region": ["Nord", "Sud", "Est", "Ouest"],
        "seismes": [12, 7, 5, 9]
    }
    df = pd.DataFrame(data)

    fig = px.pie(
        df,
        names="region",
        values="seismes",
        title="Répartition des séismes par région",
        hole=0.3  # si tu veux un donut chart, mets 0.3 ; sinon enlève
    )
    graph_html = fig.to_html(full_html=False)
    return render(request, "graphiques/pie.html", {"graph": graph_html})


def line_view(request):
    data = {
        "annee": [2015, 2016, 2017, 2018, 2019, 2020],
        "seismes": [5, 7, 6, 8, 4, 9]
    }
    df = pd.DataFrame(data)

    fig = px.line(
        df,
        x="annee",
        y="seismes",
        title="Évolution du nombre de séismes par année",
        markers=True
    )
    graph_html = fig.to_html(full_html=False)
    return render(request, "graphiques/line.html", {"graph": graph_html})


def heatmap_view(request):
    # Exemple de dataset
    df = pd.DataFrame({
        "Magnitude": [7.0, 6.9, 7.0, 7.3, 6.6, 7.0, 6.8, 6.7, 6.8, 7.6],
        "Profondeur": [14, 25, 579, 37, 624, 660, 630, 20, 20, 26],
        "Victimes": [120, 80, 300, 50, 400, 200, 150, 90, 60, 500]
    })

    # Matrice de corrélation
    corr = df.corr()

    # Création de la heatmap
    fig = px.imshow(
        corr,
        text_auto=True,
        color_continuous_scale="RdBu_r",
        title="Carte thermique des corrélations"
    )

    graph_html = fig.to_html(full_html=False)
    return render(request, "graphiques/heatmap.html", {"graph": graph_html})


