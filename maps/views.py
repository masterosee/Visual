from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
import plotly.express as px

def index(request):
    return HttpResponse("🗺️ Page Cartes")

def scatter_map_view(request):
    data = {
        "ville": ["Port-au-Prince", "Cap-Haïtien", "Les Cayes", "Jacmel"],
        "lat": [18.5944, 19.7594, 18.2000, 18.2343],
        "lon": [-72.3074, -72.1982, -73.7500, -72.5340],
        "magnitude": [7.0, 6.5, 6.8, 6.2]
    }
    df = pd.DataFrame(data)

    fig = px.scatter_mapbox(
        df,
        lat="lat",
        lon="lon",
        size="magnitude",
        color="magnitude",
        hover_name="ville",
        zoom=6,
        mapbox_style="carto-positron",
        title="🌍 Scatter Map - Séismes en Haïti"
    )

    graph_html = fig.to_html(full_html=False)
    return render(request, "maps/scatter_map.html", {"graph": graph_html})


def choropleth_map_view(request):
    data = {
        "pays": ["Haiti", "USA", "France", "Japon"],
        "iso_alpha": ["HTI", "USA", "FRA", "JPN"],
        "seismes": [50, 200, 120, 300]
    }
    df = pd.DataFrame(data)

    fig = px.choropleth(
        df,
        locations="iso_alpha",
        color="seismes",
        hover_name="pays",
        color_continuous_scale="Reds",
        projection="natural earth",
        title="🗺️ Choropleth Map - Séismes par pays"
    )

    graph_html = fig.to_html(full_html=False)
    return render(request, "maps/choropleth_map.html", {"graph": graph_html})
