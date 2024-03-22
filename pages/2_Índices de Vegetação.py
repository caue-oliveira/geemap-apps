import ee
import warnings
import calendar
import fiona
import geopandas as gpd
import folium
import streamlit as st
import geemap.foliumap as geemap
from datetime import date

st.set_page_config(layout="wide")
warnings.filterwarnings("ignore")

st.sidebar.title("Contato")
st.sidebar.info(
    """
        Cauê Oliveira Miranda \n
        caue.oliveira99@gmail.com \n
        [GitHub](https://github.com/caue-oliveira) | [LinkedIn](https://www.linkedin.com/in/caueoliveira99) | [Currículo](https://www.canva.com/design/DAF4RWCBOuk/zsbheu6nUrXpw8PWQpcpjw/view?utm_content=DAF4RWCBOuk&utm_campaign=designshare&utm_medium=link&utm_source=viewer)
    """
)
logo = "data/SGRS_LG.png"

st.sidebar.image(logo)

@st.cache_data
def ee_authenticate(token_name="EARTHENGINE_TOKEN"):
    geemap.ee_initialize(token_name=token_name)

@st.cache_data
def uploaded_file_to_gdf(data):
    import tempfile
    import os
    import uuid

    _, file_extension = os.path.splitext(data.name)
    file_id = str(uuid.uuid4())
    file_path = os.path.join(tempfile.gettempdir(), f"{file_id}{file_extension}")

    with open(file_path, "wb") as file:
        file.write(data.getbuffer())

    if file_path.lower().endswith(".kml"):
        fiona.drvsupport.supported_drivers["KML"] = "rw"
        gdf = gpd.read_file(file_path, driver="KML")
    else:
        gdf = gpd.read_file(file_path)

    return gdf

def app():

    today = date.today()

    st.title("Índices de Vegetação")

    st.markdown(
        """
Este web app interativo tem como objetivo criar índices de vegetação a partir de imagens dos satélites Landsat 8 e Sentinel 2. 
Atualmente, o aplicativo está em fase de desenvolvimento e oferece a capacidade de realizar análises de índices, estando
 apenas disponível o Índice de Vegetação por Diferença Normalizada (NDVI).  \n
O aplicativo permite fazer análises personalizadas, com filtros cobertura de nuvem e data. Os resultados são feitos por mosaicagem das imagens contidas dentro da geometria importada.
Essa ferramenta será valiosa pela sua simplicidade de manuseio, permitindo usuários realizarem rápidas análises para o monitoramento de vegetação em diversas regiões de forma automatizada. 
         """
    )

    row1_col1, row1_col2 = st.columns([2, 1])

    if st.session_state.get("zoom_level") is None:
        st.session_state["zoom_level"] = 4

    with row1_col1:
        ee_authenticate(token_name="EARTHENGINE_TOKEN")
        m = geemap.Map(
            basemap="ROADMAP",
            plugin_Draw=True,
            Draw_export=True,
            locate_control=True,
            plugin_LatLngPopup=False,
        )
        m.add_basemap("HYBRID")

    with row1_col2:

        keyword = st.text_input("Procure por uma localidade:", "")
        if keyword:
            locations = geemap.geocode(keyword)
            if locations is not None and len(locations) > 0:
                str_locations = [str(g)[1:-1] for g in locations]
                location = st.selectbox("Select a location:", str_locations)
                loc_index = str_locations.index(location)
                selected_loc = locations[loc_index]
                lat, lng = selected_loc.lat, selected_loc.lng
                folium.Marker(location=[lat, lng], popup=location).add_to(m)
                m.set_center(lng, lat, 12)
                st.session_state["zoom_level"] = 12

        collection = st.selectbox(
            "Selecione o satélite desejado: ",
            [
                "Landsat 8 OLI Surface Reflectance",
                "Sentinel-2 MSI Surface Reflectance",
            ],
            index=1,
        )

        if collection in [
            "Landsat 8 OLI Surface Reflectance",
            "Sentinel-2 MSI Surface Reflectance",
        ]:
            roi_options = ["Uploaded GeoJSON"]
        else:
            roi_options = ["Uploaded GeoJSON"]

        sample_roi = st.selectbox(
            "Select a sample ROI or upload a GeoJSON file:",
            roi_options,
            index=0,
        )

    with row1_col1:

        with st.expander(
            "Passos: Desenhe sua geometria no mapa -> Exporte-a no formato GeoJSON -> Faça o upload de sua geometria (de preferência em GeoJSON) -> Click no botão Submit para gerar sua imagem."
        ):
            video_empty = st.empty()

        data = st.file_uploader(
            "Faça o upload de um arquivo GeoJSON para usá-lo como área de interesse 👇. Personalize os parâmetros para o seu índice e clique no botão Submit na barra lateral.",
            type=["geojson", "kml", "zip"],
        )

        crs = "epsg:4326"

        if sample_roi != "Uploaded GeoJSON":

            if collection in [
                "Landsat 8 OLI Surface Reflectance",
                "Sentinel-2 MSI Surface Reflectance",
            ]:
                gdf = gpd.GeoDataFrame(
                    index=[0], crs=crs, geometry=[]
                )

            try:
                st.session_state["roi"] = geemap.gdf_to_ee(gdf, geodesic=False)
            except Exception as e:
                st.error(e)
                st.error("Please draw another ROI and try again.")
                return
            m.add_gdf(gdf, "ROI")

        elif data:
            gdf = uploaded_file_to_gdf(data)
            try:
                st.session_state["roi"] = geemap.gdf_to_ee(gdf, geodesic=False)
                m.add_gdf(gdf, "ROI")
            except Exception as e:
                st.error(e)
                st.error("Please draw another ROI and try again.")
                return

    with row1_col2:

        if collection in [
            "Landsat 8 OLI Surface Reflectance",
            "Sentinel-2 MSI Surface Reflectance",
        ]:

            if collection == "Landsat 8 OLI Surface Reflectance":
                sensor_start_year = 2013
                timelapse_title = "Landsat Index"

            elif collection == "Sentinel-2 MSI Surface Reflectance":
                sensor_start_year = 2015
                timelapse_title = "Sentinel-2 Timelapse"

            with st.form("submit_landsat_form"):

                roi = None
                if st.session_state.get("roi") is not None:
                    roi = st.session_state.get("roi")
                index_function = st.selectbox(
                    "Selecione o índice desejado:",
                    [
                        "NDVI",
                        "NDWI",
                        "SAVI",
                                            ],
                    index=9,
                )

                with st.expander("Customize options"):

                    cloud_pixel_percentage = st.slider(
                        "Cloud Coverage 🌥️:",
                        min_value=5,
                        max_value=100,
                        step=5,
                        value=85,
                        )

                    years = st.slider(
                        "Start and end year:",
                        sensor_start_year,
                        today.year,

                      (sensor_start_year, today.year),
                    )
                    months = st.slider("Start and end month:", 1, 12, (1, 12))

                empty_text = st.empty()
                submitted = st.form_submit_button("Submit")

                if submitted:
                    if sample_roi == "Uploaded GeoJSON" and data is None:
                        empty_text.warning(
                            "Passos: Desenhe sua geometria no mapa -> Exporte-a no formato GeoJSON -> Faça o upload de sua geometria (de preferência em GeoJSON) -> Click no botão Submit para gerar sua imagem."
                        )
                    else:
                        try:
                            start_year = years[0]
                            end_year = years[1]
                            start_month = months[0]
                            end_month = months[1]
                            start_date = f"{start_year}-{start_month:02d}-01"
                            end_date = f"{end_year}-{end_month:02d}-{calendar.monthrange(end_year, end_month)[1]}"

                            if collection == "Landsat 8 OLI Surface Reflectance":
                                img_collection = (
                                    ee.ImageCollection("LANDSAT/LC08/C02/T1_L2")
                                    .filterBounds(roi)
                                    .filterDate(start_date, end_date)
                                    .filter(ee.Filter.lt('CLOUD_COVER', cloud_pixel_percentage))
                                    .sort('CLOUD_COVER')
                                )

                                img_filter = img_collection.mosaic()

                                clip_sr_img = img_filter.clip(roi).multiply(0.0000275).add(-0.2)
                                ndvi = clip_sr_img.normalizedDifference(['SR_B5', 'SR_B4'])
                                m.add_layer(ndvi,
                                            {'min': -0.2, 'max': 1,
                                             'palette': ['B62F02', 'D87B32', 'FCF40D', '62C41C', '0A5C1C']}, 'NDVI'
                                            )

                                count = img_collection.size().getInfo()
                                empty_text.error("Total image available: " + str(count))

                            elif collection == "Sentinel-2 MSI Surface Reflectance":
                                img_collection = (
                                    ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")
                                    .filterBounds(roi)
                                    .filterDate(start_date, end_date)
                                    .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', cloud_pixel_percentage))
                                    .sort('system:time_start')
                                )

                                img_filter = img_collection.mosaic()

                                clip_sr_img = img_filter.clip(roi).multiply(0.0001)
                                ndvi = clip_sr_img.normalizedDifference(['B8', 'B4'])
                                m.add_layer(ndvi,
                                            {'min': -0.2, 'max': 1,
                                             'palette': ['B62F02', 'D87B32', 'FCF40D', '62C41C', '0A5C1C']}, 'NDVI'
                                            )
                                count = img_collection.size().getInfo()
                                empty_text.error("Total image available: " + str(count))

                        except Exception as e:
                            empty_text.error(
                                "An error occurred: " + str(e)
                            )
                            st.stop()

    with row1_col1:
        m.to_streamlit(height=600)
try:
    app()
except Exception as e:
    pass