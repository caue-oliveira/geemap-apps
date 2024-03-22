# Libs import
import streamlit as st
import geemap.foliumap as geemap
from streamlit_pdf_viewer import pdf_viewer

# Page configuration STARTS
st.set_page_config(layout="wide")

# Customize the sidebar
markdown = """
    Cauê Oliveira Miranda
    caue.oliveira99@gmail.com
    [GitHub](https://github.com/caue-oliveira) | [LinkedIn](https://www.linkedin.com/in/qiushengwu) | [Currículo](https://www.canva.com/design/DAF4RWCBOuk/zsbheu6nUrXpw8PWQpcpjw/view?utm_content=DAF4RWCBOuk&utm_campaign=designshare&utm_medium=link&utm_source=viewer)
"""
    # Side bar info
st.sidebar.title("Contato")
st.sidebar.info(markdown)
logo = "data/SGRS_LG.png"
st.sidebar.image(logo)

# Customize page title
st.title("Portfólio de Cauê Oliveira")

st.markdown(
    """
    Olá, me chamo Cauê Oliveira. Sou geólogo formado pela Universidade de Brasília com uma paixão pelas geotecnologias.
    Desenvolvi esta página para mostrar um pouco das minhas habilidades e projetos. \n
    Aqui poderão ser encontrados projetos no Google Earth Engine, tanto no JavaScrpit quanto no Python API, painéis Power BI e mapas confeccionados por mim. 
    """
)

st.subheader("Sobre")

markdown = """
Essa página foi desenvolvida utilizando o [streamlit](https://streamlit.io), a partir do projeto open-source do Professor Qiusheng Wu da Universidade do Tennessee ([GitHub repository](https://github.com/giswqs/geemap-apps)). 
"""

st.markdown(markdown)
# Page configuration ENDS

pdf_viewer('data/cv_caue.pdf')
