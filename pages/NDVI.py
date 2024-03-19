import ee
import warnings
import fiona
import geopandas as gpd
import folium
import streamlit as st
import geemap.foliumap as geemap
from datetime import date

st.set_page_config(layout="wide")
warnings.filterwarnings("ignore")

# Defina o mapa globalmente
m = geemap.Map(
    basemap="HYBRID",
    plugin_Draw=True,
    Draw_export=True,
    locate_control=True,
    plugin_LatLngPopup=False,
)

m.add_basemap("HYBRID")