import streamlit as st
import ee
import geemap
import folium

st.set_page_config(
    page_title="NDVI Viewer",
    page_icon="https://cdn-icons-png.flaticon.com/512/2516/2516640.png",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get help': "https://github.com/IndigoWizard/NDVI-Viewer",
        'Report a bug': "https://github.com/IndigoWizard/NDVI-Viewer/issues",
        'About': "This app was developped by [IndigoWizard](https://github.com/IndigoWizard/NDVI-Viewer) for the purpose of environmental monitoring and geospatial analysis"
    }
)

st.markdown(
    """
    <style>
        /* Header*/
        .st-emotion-cache-1avcm0n{
            height: 1rem;
        }
        /* Smooth scrolling*/
        .main {
            scroll-behavior: smooth;
        }
        /* main app body with less padding*/
        .st-emotion-cache-z5fcl4 {
            padding-block: 0;
        }
    
        /*Sidebar*/
        .st-emotion-cache-10oheav {
            padding: 0 1rem;
        }
    
        /*Sidebar : inside container*/
        .css-ge7e53 {
            width: fit-content;
        }
    
        /*Sidebar : image*/
        .css-1kyxreq {
            display: block !important;
        }
    
        /*Sidebar : Navigation list*/
        div.element-container:nth-child(4) > div:nth-child(1) > div:nth-child(1) > ul:nth-child(1) {
            margin: 0;
            padding: 0;
            list-style: none;
        }
        div.element-container:nth-child(4) > div:nth-child(1) > div:nth-child(1) > ul:nth-child(1) > li {
            padding: 0;
            margin: 0;
            padding: 0;
            font-weight: 600;
        }
        div.element-container:nth-child(4) > div:nth-child(1) > div:nth-child(1) > ul:nth-child(1) > li > a {
            text-decoration: none;
            transition: 0.2s ease-in-out;
            padding-inline: 10px;
        }
    
        div.element-container:nth-child(4) > div:nth-child(1) > div:nth-child(1) > ul:nth-child(1) > li > a:hover {
            color: rgb(46, 206, 255);
            transition: 0.2s ease-in-out;
            background: #131720;
            border-radius: 4px;
        }
    
        /* Sidebar: socials*/
        div.css-rklnmr:nth-child(6) > div:nth-child(1) > div:nth-child(1) > p {
            display: flex;
            flex-direction: row;
            gap: 1rem;
        }
    
        /* Upload info box */
        /*Upload button: dark theme*/
        .st-emotion-cache-1erivf3 {
            display: flex;
            flex-direction: column;
            align-items: inherit;
            font-size: 14px;
        }
        .css-u8hs99.eqdbnj014 {
            display: flex;
            flex-direction: row;
            margin-inline: 0;
        }
        /*Upload button: light theme*/
        .st-emotion-cache-1gulkj5 {
            display: flex;
            flex-direction: column;
            align-items: inherit;
            font-size: 14px;
        }
    
        .st-emotion-cache-u8hs99 {
            display: flex;
            flex-direction: row;
            margin-inline: 0;
        }
        /*Legend style*/
    
        .ndvilegend {
            transition: 0.2s ease-in-out;
            border-radius: 5px;
            box-shadow: 0 0 5px rgba(0, 0, 0, 0.2);
            background: rgba(0, 0, 0, 0.05);
        }
        .ndvilegend:hover {
            transition: 0.3s ease-in-out;
            box-shadow: 0 0 5px rgba(0, 0, 0, 0.8);
            background: rgba(0, 0, 0, 0.12);
            cursor: pointer;
        }
        .reclassifiedndvi {
            transition: 0.2s ease-in-out;
            border-radius: 5px;
            box-shadow: 0 0 5px rgba(0, 0, 0, 0.2);
            background: rgba(0, 0, 0, 0.05);
        }
        .reclassifiedndvi:hover {
            transition: 0.3s ease-in-out;
            box-shadow: 0 0 5px rgba(0, 0, 0, 0.8);
            background: rgba(0, 0, 0, 0.12);
            cursor: pointer;
        }
    
        /*Form submit button: generate map*/
        button.st-emotion-cache-19rxjzo:nth-child(1) {
            width: 100%;
        }
    </style>
    """, unsafe_allow_html=True)


# Initializing the Earth Engine library
# Use ee.Initialize() only on local machine! Comment back before deployement (Unusable on deployment > use geemap init+auth bellow)
# ee.Initialize()
# geemap auth + initialization for cloud deployment
@st.cache_data(persist=True)
def ee_authenticate(token_name="EARTHENGINE_TOKEN"):
    geemap.ee_initialize(token_name=token_name)


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
folium.Map.add_ee_layer = add_ee_layer