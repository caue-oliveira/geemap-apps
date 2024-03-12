# Importando as parada
import ee
import streamlit as st
import geemap.foliumap as geemap

# Configs página
    #Título
st.title("NDVI V2")


    # Colunas
col1, col2 = st.columns([4, 1])
options = list(geemap.basemaps.keys())
index = options.index("HYBRID")

with col2:

    basemap = st.selectbox("Select a basemap:", options, index)

with col1:
# Mapa default
    Map = geemap.Map(center=[-15.7801, -47.9292], zoom=12)
    Map.add_basemap(basemap)
    Map.to_streamlit(height=700)

# Área referência
coordinates_df = [
    [-48.2973, -15.4973],  # Sudoeste
    [-48.2973, -15.9761],  # Noroeste
    [-47.3894, -15.9761],  # Nordeste
    [-47.3894, -15.4973],  # Sudeste
    [-48.2973, -15.4973]  # Fechar polígono
]

bsb = ee.Geometry.Polygon(coordinates_df)

# Carregar a coleção de imagens Landsat-8 para o período especificado
landsat_img = ee.ImageCollection("LANDSAT/LC08/C02/T1_L2") \
            .filterBounds(bsb) \
            .filterDate('2022-01-01', '2024-03-03') \
            .filter(ee.Filter.lt('CLOUD_COVER', 1)) \
            .first()

# Aplicar a função à coleção de imagens
opticalBands = landsat_img.select(['SR_B1', 'SR_B2', 'SR_B3', 'SR_B4', 'SR_B5', 'SR_B6', 'SR_B7'])\
                       .multiply(0.0000275).add(-0.2)
ndvi = opticalBands.normalizedDifference(['SR_B5', 'SR_B4'])

# Adicionar a camada NDVI ao mapa
Map.addLayer(ndvi,
             {'min': -0.2, 'max': 1, 'palette': ['B62F02', 'D87B32','FCF40D','62C41C','0A5C1C']},
             'NDVI')