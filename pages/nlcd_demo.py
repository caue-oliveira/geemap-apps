import streamlit as st
import folium
import random
import string
from streamlit_folium import st_folium

unds = ('data/unidades.geojson')


st.set_page_config(layout="wide")

st.sidebar.info(
    """
    - Web App URL: <https://streamlit.geemap.org>
    - GitHub repository: <https://github.com/giswqs/streamlit-geospatial>
    """
)

st.sidebar.title("Contact")
st.sidebar.info(
    """
    Qiusheng Wu: <https://wetlands.io>
    [GitHub](https://github.com/giswqs) | [Twitter](https://twitter.com/giswqs) | [YouTube](https://www.youtube.com/c/QiushengWu) | [LinkedIn](https://www.linkedin.com/in/qiushengwu)
    """
)

st.title("Mapa Geológico do Projeto Arenópolis - TF 2023 UnB")

# center on Liberty Bell, add marker
m = folium.Map(location=[-16.39374927779391, -51.663956293293964], zoom_start=10)
folium.GeoJson(unds).add_to(m)
folium.Marker(
    [-16.39374927779391, -51.663956293293964], popup="Liberty Bell", tooltip="Liberty Bell"
).add_to(m)


def generate_color_mapping(features):
    color_mapping = {}
    for feature in features:
        sigla = feature['properties']['Sigla']
        if sigla not in color_mapping:
            # Gerar cor aleatória para a sigla
            color = "#{:06x}".format(random.randint(0, 0xFFFFFF))
            color_mapping[sigla] = color
    return color_mapping

color_mapping = generate_color_mapping(unds['features'])

# Função de estilo para atribuir cores aleatórias com base na propriedade 'Sigla'
def style_function(feature):
    sigla = feature['properties']['Sigla']
    return {
        'stroke': False,
        'fillColor': color_mapping.get(sigla),
        'fillOpacity': 0.8
    }

folium.GeoJson(
    unds,
    style_function=style_function
).add_to(m)

# call to render Folium map in Streamlit, but don't get any data back
# from the map (so that it won't rerun the app when the user interacts)
st_folium(m, width=1000, returned_objects=[])