import streamlit as st
import leafmap.foliumap as leafmap
import folium
import geopandas as gpd

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

st.title("Marker Cluster")

# Download the shp from github
unds = '../unidades.zip'


gdf = gpd.read_file(unds)
gdf_filter = gdf [['Nome', 'Sigla', 'Unidade', 'DominioEst', 'geometry']].fillna(0)
gdf_filter = gdf_filter.to_crs(epsg=4326)

folium.LayerControl().add_to(m)
m = gdf_filter.explore(column='Sigla', name = 'Sigla')
m