import ee
import os
import warnings
import datetime
import calendar
import fiona
import geopandas as gpd
import folium
import streamlit as st
import geemap.colormaps as cm
import geemap.foliumap as geemap
from datetime import date
from shapely.geometry import Polygon

st.set_page_config(layout="wide")
warnings.filterwarnings("ignore")

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

    with row1_col1:
        ee_authenticate(token_name="EARTHENGINE_TOKEN")
        m = geemap.Map(
            basemap="HYBRID",
            plugin_Draw=True,
            Draw_export=True,
            locate_control=True,
            plugin_LatLngPopup=False,
        )
        m.add_basemap("ROADMAP")

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
                "Sentinel-2 MSI Surface Reflectance"
            ],
            index=1,
        )

        if collection in [
            "Landsat TM-ETM-OLI Surface Reflectance",
            "Sentinel-2 MSI Surface Reflectance"
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
                roi = st.session_state.get("roi")
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
                sensor_start_year = 2013

            elif collection == "Sentinel-2 MSI Surface Reflectance":
                sensor_start_year = 2015

            with st.form("submit_landsat_form"):

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
                            "Steps to create a timelapse: Draw a rectangle on the map -> Export it as a GeoJSON -> Upload it back to the app -> Click the Submit button. Alternatively, you can select a sample ROI from the dropdown list."
                        )
                    else:
                        try:
                            start_year = years[0]
                            end_year = years[1]
                            start_month = months[0]
                            end_month = months[1]
                            start_date = f"{start_year}-{start_month:02d}-01"
                            end_date = f"{end_year}-{end_month:02d}-{calendar.monthrange(end_year, end_month)[1]}"

                            if collection == "Landsat TM-ETM-OLI Surface Reflectance":
                                img_collection = (
                                    ee.ImageCollection("LANDSAT/LC08/C02/T1_L2")
                                    .filterBounds(roi)
                                    .filterDate(start_date, end_date)
                                    .sort('CLOUD_COVER')
                                )

                                img_filter = img_collection.first()

                                clip_sr_img = img_filter.clip(roi).multiply(0.0000275).add(-0.2)
                                ndvi = clip_sr_img.normalizedDifference(['SR_B5', 'SR_B4'])
                                m.add_layer(ndvi,
                                            {'min': -0.2, 'max': 1,
                                             'palette': ['B62F02', 'D87B32', 'FCF40D', '62C41C', '0A5C1C']}, 'NDVI'
                                            )
                                count = img_collection.size().getInfo()
                                empty_text.error("Quantidade de imagens disponíveis: " + str(count))

                            elif collection == "Sentinel-2 MSI Surface Reflectance":
                                empty_text.error("Sentinel in progress")
                        except Exception as e:
                            empty_text.error(
                                "An error occurred: " + str(e)
                            )
                            st.stop()

try:
    app()
except Exception as e:
    pass