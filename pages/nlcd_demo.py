import streamlit as st
import folium

from streamlit_folium import st_folium

unds = ('data/unidades.geojson')

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

st.title("Mapa Geológico do Projeto Arenópolis - TF 2023 UnB")

# center on Liberty Bell, add marker
m = folium.Map(location=[-16.39374927779391, -51.663956293293964], zoom_start=10)

folium.Marker(
    [-16.39374927779391, -51.663956293293964], popup="Liberty Bell", tooltip="Liberty Bell"
).add_to(m)

colors = {
        'D1f': '#ff0000',  # Cor para 'D1f'
        'JKλian': '#00ff00',  # Cor para 'JKλian'
        'JKλiaga': '#0000ff',  # Cor para 'JKλiaga'
        'JKλiasv': '#ff00ff',  # Cor para 'JKλiasv'
        'NP1apoa': '#ffff00',  # Cor para 'NP1apoa'
        'NP1apoum': '#00ffff',  # Cor para 'NP1apoum'
        'NPαch': '#ff9900',  # Cor para 'NPαch'
        'NP1apach': '#9900ff',  # Cor para 'NP1apach'
        'NP1apam': '#0099ff',  # Cor para 'NP1apam'
        'NP1apaq': '#ff0099',  # Cor para 'NP1apaq'
        'NP1apax': '#990000',  # Cor para 'NP1apax'
        'NP1γnacc': '#009900',  # Cor para 'NP1γnacc'
        'PP3γr': '#990099',  # Cor para 'PP3γr'
        'NP3γsnird': '#999999',  # Cor para 'NP3γsnird'
        'NP3γsnirm': '#660000',  # Cor para 'NP3γsnirm'
        'NP3γsnirsv': '#006600',  # Cor para 'NP3γsnirsv'
        'NP2γst': '#000066',  # Cor para 'NP2γst'
        'NP2aγalgf': '#660066',  # Cor para 'NP2aγalgf'
        'NP2aγalg': '#666600',  # Cor para 'NP2aγalg'
        'NP2aγalhbt': '#6600ff',  # Cor para 'NP2aγalhbt'
        'NP3γsnirsf': '#ff6600',  # Cor para 'NP3γsnirsf'
        'NP1apocc': '#00ff66',  # Cor para 'NP1apocc'
        'JKλiaop': '#6600cc',  # Cor para 'JKλiaop'
        'NP1γnaum': '#cc6600',  # Cor para 'NP1γnaum'
        'NP1apaum': '#0066cc',  # Cor para 'NP1apaum'
        'NP1apaa': '#cc0066',  # Cor para 'NP1apaa'
        'NP3γcaigg': '#ccff00',  # Cor para 'NP3γcaigg'
        'NP1γnaa': '#00ccff',  # Cor para 'NP1γnaa'
        'NP3γsnirsg': '#ffcc00',  # Cor para 'NP3γsnirsg'
        'NP3γcaigf': '#00ffcc',  # Cor para 'NP3γcaigf'
        'NP1γnagt': '#cc00ff',  # Cor para 'NP1γnagt'
        'NP3γcaid': '#ffcc99',  # Cor para 'NP3γcaid'
        'NP1apox': '#99ffcc',  # Cor para 'NP1apox'
        'NP3γsnirt': '#cc99ff',  # Cor para 'NP3γsnirt'
        'NP3γsnirgr': '#ff99cc',  # Cor para 'NP3γsnirgr'
        'Dpg': '#cc9999',  # Cor para 'Dpg'
        'NP1apoch': '#99cc99',  # Cor para 'NP1apoch'
        'NP1δmb': '#9999cc'  # Cor para 'NP1δmb'
    }

def color_by_sigla(feature):
    sigla = feature['properties'].get('Sigla', '')  # Obtém o valor da propriedade 'Sigla', ou uma string vazia se não existir
    return {
        'stroke': False,
        'fillColor': colors.get(sigla, '#ffffff'),  # Obtém a cor correspondente ao valor da 'Sigla' no mapeamento, ou branco (#ffffff) como padrão
    }
folium.GeoJson(unds, style_function=color_by_sigla).add_to(m)


# call to render Folium map in Streamlit, but don't get any data back
# from the map (so that it won't rerun the app when the user interacts)
st_folium(m, width=1000, returned_objects=[])