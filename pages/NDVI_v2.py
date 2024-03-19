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



# Método para desenhar
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


@st.cache_data
def ee_authenticate(token_name="EARTHENGINE_TOKEN"):
    geemap.ee_initialize(token_name=token_name)


st.sidebar.info(
    """
    - Side bar
    """
)

st.sidebar.title("Contact")
st.sidebar.info(
    """
    Cauê Oliveira Miranda
    [URL](https://github.com/giswqs) | [Linkedin](https://twitter.com/giswqs) | [Currículo](https://www.youtube.com/c/QiushengWu)
    """
)

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

    st.title("Create Satellite Timelapse")

    st.markdown(
        """
        An interactive web app for creating [Landsat](https://developers.google.com/earth-engine/datasets/catalog/landsat)/[GOES](https://jstnbraaten.medium.com/goes-in-earth-engine-53fbc8783c16) timelapse for any location around the globe. 
        The app was built using [streamlit](https://streamlit.io), [geemap](https://geemap.org), and [Google Earth Engine](https://earthengine.google.com). For more info, check out my streamlit [blog post](https://blog.streamlit.io/creating-satellite-timelapse-with-streamlit-and-earth-engine). 
    """
    )

    row1_col1, row1_col2 = st.columns([2, 1])

    if st.session_state.get("zoom_level") is None:
        st.session_state["zoom_level"] = 4

    st.session_state["ee_asset_id"] = None
    st.session_state["bands"] = None
    st.session_state["palette"] = None
    st.session_state["vis_params"] = None

    with row1_col1:
        ee_authenticate(token_name="EARTHENGINE_TOKEN")
        # Remove a criação do mapa daqui

    with row1_col2:

        keyword = st.text_input("Search for a location:", "")
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
            "Select a satellite image collection: ",
            [
                "Landsat TM-ETM-OLI Surface Reflectance",
                "Sentinel-2 MSI Surface Reflectance",
                "Any Earth Engine ImageCollection"
            ],
            index=1,
        )

        if collection in [
            "Landsat TM-ETM-OLI Surface Reflectance",
            "Sentinel-2 MSI Surface Reflectance",
            "Any Earth Engine ImageCollection"
        ]:
            roi_options = ["Uploaded GeoJSON"]
        else:
            roi_options = ["Uploaded GeoJSON"]

        if collection == "Any Earth Engine ImageCollection":
            keyword = st.text_input("Enter a keyword to search (e.g., MODIS):", "")
            if keyword:

                assets = geemap.search_ee_data(keyword)
                ee_assets = []
                for asset in assets:
                    if asset["ee_id_snippet"].startswith("ee.ImageCollection"):
                        ee_assets.append(asset)

                asset_titles = [x["title"] for x in ee_assets]
                dataset = st.selectbox("Select a dataset:", asset_titles)
                if len(ee_assets) > 0:
                    st.session_state["ee_assets"] = ee_assets
                    st.session_state["asset_titles"] = asset_titles
                    index = asset_titles.index(dataset)
                    ee_id = ee_assets[index]["id"]
                else:
                    ee_id = ""

                if dataset is not None:
                    with st.expander("Show dataset details", False):
                        index = asset_titles.index(dataset)
                        html = geemap.ee_data_html(st.session_state["ee_assets"][index])
                        st.markdown(html, True)

        sample_roi = st.selectbox(
            "Select a sample ROI or upload a GeoJSON file:",
            roi_options,
            index=0,
        )

    with row1_col1:

        with st.expander(
            "Steps: Draw a rectangle on the map -> Export it as a GeoJSON -> Upload it back to the app -> Click the Submit button. Expand this tab to see a demo 👉"
        ):
            video_empty = st.empty()

        data = st.file_uploader(
            "Upload a GeoJSON file to use as an ROI. Customize timelapse parameters and then click the Submit button 😇👇",
            type=["geojson", "kml", "zip"],
        )

        crs = "epsg:4326"

        if sample_roi != "Uploaded GeoJSON":

            if collection in [
                "Landsat TM-ETM-OLI Surface Reflectance",
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

        m.to_streamlit(height=600)

    with row1_col2:

        if collection in [
            "Landsat TM-ETM-OLI Surface Reflectance",
            "Sentinel-2 MSI Surface Reflectance",
        ]:

            if collection == "Landsat TM-ETM-OLI Surface Reflectance":
                sensor_start_year = 1984
                timelapse_title = "Landsat Index"

            elif collection == "Sentinel-2 MSI Surface Reflectance":
                sensor_start_year = 2015
                timelapse_title = "Sentinel-2 Timelapse"

            with st.form("submit_landsat_form"):

                roi = None
                if st.session_state.get("roi") is not None:
                    roi = st.session_state.get("roi")

                title = st.text_input(
                    "Enter a title to show on your image: ", timelapse_title
                )
                index_function = st.selectbox(
                    "Select an index function:",
                    [
                        "NDVI",
                        "NDWI",
                        "SAVI",
                        "NIR/SWIR1/Red",
                        "SWIR2/NIR/Red",
                        "SWIR2/SWIR1/Red",
                        "SWIR1/NIR/Blue",
                        "NIR/SWIR1/Blue",
                        "SWIR2/NIR/Green",
                        "SWIR1/NIR/Red",
                        "SWIR2/NIR/SWIR1",
                        "SWIR1/NIR/SWIR2",
                    ],
                    index=9,
                )

                frequency = st.selectbox(
                    "Select a temporal frequency:",
                    ["year", "quarter", "month"],
                    index=0,
                )

                with st.expander("Customize timelapse"):

                    cloud_pixel_percentage = st.slider(
                        "Cloud Coverage 🌥️:",
                        min_value=5,
                        max_value=100,
                        step=5,
                        value=85,
                        )
                    dimensions = st.slider(
                        "Maximum dimensions (Width*Height) in pixels", 768, 2000, 768
                    )
                    progress_bar_color = st.color_picker(
                        "Progress bar color:", "#0000ff"
                    )
                    years = st.slider(
                        "Start and end year:",
                        sensor_start_year,
                        today.year,
                        (sensor_start_year, today.year),
                    )
                    months = st.slider("Start and end month:", 1, 12, (1, 12))
                    font_size = st.slider("Font size:", 10, 50, 30)
                    font_color = st.color_picker("Font color:", "#ffffff")
                    apply_fmask = st.checkbox(
                        "Apply fmask (remove clouds, shadows, snow)", True
                    )
                    font_type = st.selectbox(
                        "Select the font type for the title:",
                        ["arial.ttf", "alibaba.otf"],
                        index=0,
                    )
                    fading = st.slider(
                        "Fading duration (seconds) for each frame:", 0.0, 3.0, 0.0
                    )
                    mp4 = st.checkbox("Save timelapse as MP4", True)

#### IMAGE PROCESSING INDEX
                def getNDVI(collection):
                    if collection == 'Landsat TM-ETM-OLI Surface Reflectance':
                        ndvi = clip_sr_img.normalizedDifference(['SR_B5', 'SR_B4'])
                        return ndvi
                    elif collection == 'Sentinel-2 MSI Surface Reflectance':
                        return img_collection.normalizedDifference(['B8', 'B4'])


 #### IMAGE PROCESSING END

                empty_text = st.empty()
                empty_image = st.empty()
                empty_fire_image = st.empty()
                empty_video = st.container()
                submitted = st.form_submit_button("Submit")
                if submitted:

                    if sample_roi == "Uploaded GeoJSON" and data is None:
                        empty_text.warning(
                            "Steps to create a timelapse: Draw a rectangle on the map -> Export it as a GeoJSON -> Upload it back to the app -> Click the Submit button. Alternatively, you can select a sample ROI from the dropdown list."
                        )
                    else:

                        empty_text.text("Computing... Please wait...")

                        start_date = str(months[0]).zfill(2) + "-01"
                        end_date = str(months[1]).zfill(2) + "-30"

                        try:
                            if collection == "Landsat TM-ETM-OLI Surface Reflectance":
                                img_collection = (
                                    ee.ImageCollection("LANDSAT/LC08/C02/T1_L2")
                                    .filterBounds(sample_roi)
                                    .filterDate(start_date, end_date)
                                    .sort(ee.Filter.lt('CLOUD_COVER', cloud_pixel_percentage))
                                )

                                img_filter = img_collection.first()

                                clip_sr_img = img_filter.clip(sample_roi).multiply(0.0000275).add(-0.2)
                                ndvi = clip_sr_img.normalizedDifference(['SR_B5', 'SR_B4'])
                                m.add_ee_layer(ndvi,
                                            {'min': -0.2, 'max': 1,
                                             'palette': ['B62F02', 'D87B32','FCF40D','62C41C','0A5C1C']},'NDVI'
                                )
                            elif collection == "Sentinel-2 MSI Surface Reflectance":
                                out_gif = geemap.sentinel2_timelapse(
                                    roi=roi,
                                )
                        except:
                            empty_text.error(
                                "An error occurred while computing the timelapse. Your probably requested too much data. Try reducing the ROI or timespan."
                            )
                            st.stop()

                        else:
                            empty_text.error(
                                "Deu ruim, menó"
                            )
try:
    app()
except Exception as e:
    pass