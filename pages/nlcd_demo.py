import streamlit as st
import folium

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

def app():
    st.title("Mapa Geológico do Projeto Arenópolis - TF 2023 UnB")

    # Inicializa um mapa Folium
    m = folium.Map(location=[-16.39374927779391, -51.663956293293964], zoom_start=5)

    # Adiciona o GeoDataFrame como GeoJson ao mapa
    #folium.GeoJson(unds).add_to(m)

    # Exibe o mapa no Streamlit
    m.to_streamlit(height=700)

app()