
from django.shortcuts import render
import plotly.express as px
import pandas as pd
from django.http import HttpResponse

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
    return render(request, "timeseries/line.html", {"graph": graph_html})




def index(request):
    return HttpResponse("⏳ Page Séries temporelles")

def timeseries_view(request):
    data = {
        "date": pd.date_range(start="2020-01-01", periods=10, freq="M"),
        "magnitude": [6.5, 6.7, 7.0, 6.8, 7.2, 6.9, 7.1, 6.6, 7.3, 6.8]
    }
    df = pd.DataFrame(data)

    fig = px.area(
        df,
        x="date",
        y="magnitude",
        title="Magnitudes au fil du temps",
        markers=True
    )
    graph_html = fig.to_html(full_html=False)
    return render(request, "timeseries/timeseries.html", {"graph": graph_html})


def stacked_area_view(request):
    data = {
        "annee": [2015, 2016, 2017, 2018, 2019, 2020],
        "Region A": [5, 7, 6, 8, 4, 9],
        "Region B": [3, 4, 5, 6, 2, 5],
        "Region C": [2, 3, 4, 3, 3, 4],
    }
    df = pd.DataFrame(data)

    fig = px.area(
        df,
        x="annee",
        y=["Region A", "Region B", "Region C"],
        title="Évolution des séismes par région (aires empilées)"
    )
    graph_html = fig.to_html(full_html=False)
    return render(request, "timeseries/stacked_area.html", {"graph": graph_html})

import plotly.graph_objects as go
import pandas as pd
from django.shortcuts import render

def candlestick_view(request):
    # Exemple de données type "finance" ou mesures journalières
    df = pd.DataFrame({
        "date": pd.date_range(start="2020-01-01", periods=10, freq="D"),
        "open": [6.5, 6.7, 6.8, 7.0, 6.9, 7.1, 6.8, 6.6, 6.9, 7.2],
        "high": [6.8, 6.9, 7.0, 7.2, 7.1, 7.3, 7.0, 6.9, 7.1, 7.4],
        "low":  [6.3, 6.5, 6.6, 6.8, 6.7, 6.9, 6.6, 6.4, 6.7, 7.0],
        "close":[6.7, 6.8, 6.9, 7.1, 6.8, 7.0, 6.7, 6.8, 7.0, 7.3]
    })

    fig = go.Figure(data=[go.Candlestick(
        x=df["date"],
        open=df["open"],
        high=df["high"],
        low=df["low"],
        close=df["close"]
    )])

    fig.update_layout(
        title="📊 Candlestick Chart - Variations journalières",
        xaxis_title="Date",
        yaxis_title="Valeur"
    )

    graph_html = fig.to_html(full_html=False)
    return render(request, "timeseries/candlestick.html", {"graph": graph_html})


def multi_line_view(request):
    data = {
        "annee": [2015, 2016, 2017, 2018, 2019, 2020],
        "Region A": [5, 7, 6, 8, 4, 9],
        "Region B": [3, 4, 5, 6, 2, 5],
        "Region C": [2, 3, 4, 3, 3, 4],
    }
    df = pd.DataFrame(data)

    # Transformation en format long pour Plotly Express
    df_long = df.melt(id_vars="annee", var_name="Région", value_name="Séismes")

    fig = px.line(
        df_long,
        x="annee",
        y="Séismes",
        color="Région",
        markers=True,
        title="📈 Multi-Line Chart - Séismes par région"
    )

    graph_html = fig.to_html(full_html=False)
    return render(request, "timeseries/multi_line.html", {"graph": graph_html})


def bubble_chart_view(request):
    data = {
        "annee": [2015, 2016, 2017, 2018, 2019, 2020],
        "magnitude": [6.5, 6.7, 7.0, 6.8, 7.2, 6.9],
        "profondeur": [10, 30, 20, 25, 15, 40],  # taille des bulles
        "region": ["Nord", "Sud", "Est", "Ouest", "Nord", "Sud"]
    }
    df = pd.DataFrame(data)

    fig = px.scatter(
        df,
        x="annee",
        y="magnitude",
        size="profondeur",
        color="region",
        hover_name="region",
        title="🎈 Bubble Chart - Magnitude vs Année (taille = profondeur)"
    )

    graph_html = fig.to_html(full_html=False)
    return render(request, "timeseries/bubble.html", {"graph": graph_html})

def radar_chart_view(request):
    # Exemple de données : 3 régions comparées sur 5 critères
    categories = ["Séismes", "Magnitude", "Profondeur", "Population exposée", "Infrastructures"]
    df = pd.DataFrame({
        "Critère": categories,
        "Région A": [80, 70, 60, 50, 65],
        "Région B": [60, 65, 70, 55, 60],
        "Région C": [70, 75, 65, 60, 70],
    })

    # Transformation en format long
    df_long = df.melt(id_vars=["Critère"], var_name="Région", value_name="Valeur")

    fig = px.line_polar(
        df_long,
        r="Valeur",
        theta="Critère",
        color="Région",
        line_close=True,
        markers=True,
        title="🕸️ Radar Chart - Comparaison multi-critères"
    )

    fig.update_traces(fill="toself")  # Remplir les zones

    graph_html = fig.to_html(full_html=False)
    return render(request, "timeseries/radar.html", {"graph": graph_html})


def treemap_view(request):
    data = {
        "Continent": ["Amérique", "Amérique", "Amérique", "Europe", "Europe", "Asie", "Asie"],
        "Pays": ["Haïti", "USA", "Brésil", "France", "Allemagne", "Chine", "Japon"],
        "Séismes": [50, 200, 150, 120, 100, 300, 180]
    }
    df = pd.DataFrame(data)

    fig = px.treemap(
        df,
        path=["Continent", "Pays"],  # hiérarchie
        values="Séismes",
        color="Séismes",
        color_continuous_scale="RdBu",
        title="🌳 Treemap - Répartition des séismes par continent et pays"
    )

    graph_html = fig.to_html(full_html=False)
    return render(request, "timeseries/treemap.html", {"graph": graph_html})
