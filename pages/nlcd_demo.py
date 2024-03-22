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

folium.Marker(
    [-16.39374927779391, -51.663956293293964], popup="Liberty Bell", tooltip="Liberty Bell"
).add_to(m)


# Função para gerar cores hexadecimais aleatórias
def random_color_hex():
    color = "#{:06x}".format(random.randint(0, 0xFFFFFF))
    return color
color_mapping = {}
# Mapear cada valor único de 'Sigla' para uma cor aleatória
def generate_color_mapping(features):
    siglas = set(feature['properties']['Sigla'] for feature in features)
    color_mapping = {sigla: random_color_hex() for sigla in siglas}
    return color_mapping

# Função de estilo para atribuir cores com base na propriedade 'Sigla'
def style_function(feature):
    sigla = feature['properties']['Sigla']
    return {
        'fillColor': color_mapping.get(sigla),
        'color': 'black',
        'weight': 2,
        'fillOpacity': 0.8
    }

# Adicionar o GeoJSON ao mapa com a função de estilo
folium.GeoJson(
    unds,
    style_function=style_function  # Não inclua os parênteses aqui
).add_to(m)

# call to render Folium map in Streamlit, but don't get any data back
# from the map (so that it won't rerun the app when the user interacts)
st_folium(m, width=1000, returned_objects=[])