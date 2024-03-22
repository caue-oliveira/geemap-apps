import streamlit as st
import folium

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
    'D1f': '#ff0000',  # Cor para 'Valor1'
    'JKλian': '#00ff00',  # Cor para 'Valor2'
    'JKλiaga': '#0000ff',
    'JKλiasv': 'D87B32',
    'NP1apoa':'#0A5C1C',
    # Adicione mais cores conforme necessário para outros valores de 'Sigla'
}

def color_by_sigla(feature):
    sigla = feature['properties'].get('Sigla', '')  # Obtém o valor da propriedade 'Sigla', ou uma string vazia se não existir
    return {
        'stroke': False,
        'fillColor': colors.get(sigla, '#ffffff'),  # Obtém a cor correspondente ao valor da 'Sigla' no mapeamento, ou branco (#ffffff) como padrão
    }
folium.GeoJson(unds, style_function=color_by_sigla).add_to(m)


# call to render Folium map in Streamlit, but don't get any data back
# from the map (so that it won't rerun the app when the user interacts)
st_folium(m, width=1000, returned_objects=[])