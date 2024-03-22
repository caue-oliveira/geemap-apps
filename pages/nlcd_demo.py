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

colors = {
    'Complexo Alcalino, Nefelinitos': '#D5EEB4',  # Cor para 'JKλian'
    'Complexo Alcalino, Gabros Alcalinos': '#F3F802',  # Cor para 'JKλiaga'
    'JKλiasv': '#14E8C3',  # Cor para 'JKλiasv'
    'Complexo Alcalino, Ijolitos e melteigitos': '#128BB3',  # Cor para 'JKλiaop'
    'D1f': '#EFA10B',  # Cor para 'D1f'
    'Dpg': '#F3B26B',  # Cor para 'Dpg'
    'NP3γsnird': '#E41C50',  # Cor para 'NP3γsnird'
    'NP3γsnirm': '#FEC0EF',  # Cor para 'NP3γsnirm'
    'NP3γsnirsv': '#FEC0EF',  # Cor para 'NP3γsnirsv'
    'NP3γsnirsf': '#FCFBDD',  # Cor para 'NP3γsnirsf'
    'NP3γsnirsg': '#B60D12',  # Cor para 'NP3γsnirsg'
    'NP3γsnirt': '#E41C50',  # Cor para 'NP3γsnirt'
    'NP3γsnirgr': '#BEA387',  # Cor para 'NP3γsnirgr'
    'NP2γst': '#F5CBB6',  # Cor para 'NP2γst'
    'NP2aγalgf': '#E7A5AE',  # Cor para 'NP2aγalgf'
    'NP2aγalg': '#FC555A',  # Cor para 'NP2aγalg'
    'NP2aγalhbt': '#623184',  # Cor para 'NP2aγalhbt'
    'NP1γnaa': '#623184',  # Cor para 'NP1γnaa'
    'NP1γnaum': '#546087',  # Cor para 'NP1γnaum'
    'NP1γnagt': '#9364C0',  # Cor para 'NP1γnagt'
    'NP1apox': '#BEE96E',  # Cor para 'NP1apox'
    'NP1apocc': '#ED94EC',  # Cor para 'NP1apocc'
    'NP1apoch': '#6D8232',  # Cor para 'NP1apoch'
    'NP1apoum': '#10401E',  # Cor para 'NP1apoum'
    'NP1apaum': '#35441C',  # Cor para 'NP1apaum'
    'NP1apaa': '#6D8232',  # Cor para 'NP1apaa'
    'NP1apoa': '#315144',  # Cor para 'NP1apoa'
    'NP1apax': '#BFEF4F',  # Cor para 'NP1apax'
    'NP1αch': '#C2C2C1',  # Cor para 'NP1αch'
    'NP1apach': '#9900ff',  # Cor para 'NP1apach'
    'NP1δmb': '#5CCEAC',  # Cor para 'NP1δmb'
    'PP3γr': '#990099',  # Cor para 'PP3γr'
}

def color_by_sigla(feature):
    sigla = feature['properties'].get('Nome', '')  # Obtém o valor da propriedade 'Sigla', ou uma string vazia se não existir
    return {
        'stroke': False,
        'fillColor': colors.get(sigla, '#ffffff'),
        'fillOpacity': 0.8
    }
folium.GeoJson(unds, style_function=color_by_sigla).add_to(m)


# call to render Folium map in Streamlit, but don't get any data back
# from the map (so that it won't rerun the app when the user interacts)
st_folium(m, width=1000, returned_objects=[])