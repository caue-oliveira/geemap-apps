import streamlit as st
import geemap.foliumap as geemap
import ee
import folium

st.title("Interactive Map")

col1, col2 = st.columns([4, 1])
options = list(geemap.basemaps.keys())
index = options.index("OpenTopoMap")

# Earth Engine drawing method setup
def add_ee_layer(self, ee_image_object, vis_params, name):
    map_id_dict = ee.Image(ee_image_object).getMapId(vis_params)
    layer = folium.raster_layers.TileLayer(
        tiles=map_id_dict['tile_fetcher'].url_format,
        attr='Map Data &copy; <a href="https://earthengine.google.com/">Google Earth Engine</a>',
        name=name,
        overlay=True,
        control=True
    )
    layer.add_to(self)
    return layer

# Configuring Earth Engine display rendering method in Folium
folium.m.add_ee_layer = add_ee_layer

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

bsb = [
    [-48.2973, -15.4973],  # Sudoeste
    [-48.2973, -15.9761],  # Noroeste
    [-47.3894, -15.9761],  # Nordeste
    [-47.3894, -15.4973],  # Sudeste
    [-48.2973, -15.4973]  # Fechar polígono
]
sample_roi = ee.Geometry.Polygon(bsb)

collection = "Landsat TM-ETM-OLI Surface Reflectance"

if collection == "Landsat TM-ETM-OLI Surface Reflectance":
    img_collection = (
        ee.ImageCollection("LANDSAT/LC08/C02/T1_L2")
        .filterBounds(sample_roi)
        .sort('CLOUD_COVER')
    )

    # Seleciona a primeira imagem da coleção
    img = img_collection.first()

    # Clip da imagem
    clip_sr_img = img.clip(sample_roi).multiply(0.0000275).add(-0.2)

    # Calcula o NDVI
    ndvi = clip_sr_img.normalizedDifference(['SR_B5', 'SR_B4'])

    # Adiciona o NDVI ao mapa
    m.addLayer(ndvi, {'min': -0.2, 'max': 1, 'palette': ['B62F02', 'D87B32', 'FCF40D', '62C41C', '0A5C1C']}, 'NDVI')

m.add_ee_layer(ndvi, {'min': -0.2, 'max': 1, 'palette': ['B62F02', 'D87B32', 'FCF40D', '62C41C', '0A5C1C']}, 'NDVI')

count = img_collection.size().getInfo()
print("Quantidade de imagens na coleção:", count)