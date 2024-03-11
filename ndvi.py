import ee
import geemap.foliumap as geemap

# Inicialize o Earth Engine
ee.Initialize()

# Defina o mapa
Map = geemap.Map(center=[-47.88281, -15.79382], zoom=12)

# Carregue uma imagem específica do dataset do MapBiomas para a cobertura do solo global (por exemplo, a imagem de 2019)
mapbiomas = ee.Image('projects/mapbiomas-workspace/public/collection8/mapbiomas_collection80_integration_v1').select('classification_2019')

# Adicione a imagem ao mapa
Map.addLayer(mapbiomas, {}, 'MapBiomas 2019')

# Exiba o mapa
Map
