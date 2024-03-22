import streamlit as st
import geopandas as gpd
import folium

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

unds = 'data/unidades.geojson'



# Calcula o centroide médio para posicionar o mapa
centroid_lat = gdf_filter.centroid.y.mean()
centroid_lon = gdf_filter.centroid.x.mean()

# Inicializa um mapa Folium
m = folium.Map(location=[centroid_lat, centroid_lon], zoom_start=5)

# Adiciona o GeoDataFrame como GeoJson ao mapa
folium.GeoJson(gdf_filter).add_to(m)

# Exibe o mapa no Streamlit
st.write(m)
