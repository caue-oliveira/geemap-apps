import streamlit as st
import geemap.foliumap as geemap

st.title("Interactive Map")

col1, col2 = st.columns([4, 1])
options = list(geemap.basemaps.keys())
index = options.index("OpenTopoMap")

with col2:

    basemap = st.selectbox("Select a basemap:", options, index)


with col1:
    # Defina o mapa globalmente
    m = geemap.Map(
        basemap="HYBRID",
        plugin_Draw=True,
        Draw_export=True,
        locate_control=True,
        plugin_LatLngPopup=False,
    )

    m.add_basemap("HYBRID")
    m.add_basemap(basemap)
    m.to_streamlit(height=700)

