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
    'Complexo Alcalino, Subvulcânicas': '#14E8C3',  # Cor para 'JKλiasv'
    'Complexo Alcalino, Ijolitos e melteigitos': '#128BB3',  # Cor para 'JKλiaop'
    'Formação Furnas': '#EFA10B',  # Cor para 'D1f'
    'Formação Ponta Grossa': '#F3B26B',  # Cor para 'Dpg'
    'Granito Serra do Iran, Diorito': '#E41C50',  # Cor para 'NP3γsnird'
    'Granito Serra do Iran, Monzogranito': '#FEC0EF',  # Cor para 'NP3γsnirm'
    'Granito Serra do Iran, Subvulcânica': '#FEC0EF',  # Cor para 'NP3γsnirsv'
    'Granito Serra do Iran, Sienogranito Fino': '#FCFBDD',  # Cor para 'NP3γsnirsf'
    'Granito Serra do Iran, Sienogranito Grosso': '#B60D12',  # Cor para 'NP3γsnirsg'
    'Granito Serra do Iran, Tonalito': '#E41C50',  # Cor para 'NP3γsnirt'
    'Granito Serra do Iran, Granodiorito': '#BEA387',  # Cor para 'NP3γsnirgr'
    'Granito Serra do Tatu': '#F5CBB6',  # Cor para 'NP2γst'
    'Ribeirão Água Limpa, Granito fino': '#E7A5AE',  # Cor para 'NP2aγalgf'
    'Ribeirão Água Limpa, Granito': '#FC555A',  # Cor para 'NP2aγalg'
    'Ribeirão Água Limpa, Hb Bt Tonalito': '#623184',  # Cor para 'NP2aγalhbt'
    'Gnaisse Arenópolis, Anfibolito': '#623184',  # Cor para 'NP1γnaa'
    'Gnaisse Arenópolis, Ultramáfica': '#546087',  # Cor para 'NP1γnaum'
    'Gnaisse Arenópolis, Gnaisse Tonalítico': '#9364C0',  # Cor para 'NP1γnagt'
    'Córrego da Onça, Qz-Msc-Xisto': '#BEE96E',  # Cor para 'NP1apox'
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