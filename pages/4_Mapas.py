import streamlit as st
import base64
import textwrap

def render_svg(svg):
    """Renders the given svg string."""
    b64 = base64.b64encode(svg.encode('utf-8')).decode("utf-8")
    html = r'<img src="data:image/svg+xml;base64,%s"/>' % b64
    st.write(html, unsafe_allow_html=True)

st.title("Exposição de Mapas")

st.subheader('Mapa de Classificação Supervisionada do Plano Piloto')
st.markdown('''
    Este mapa é produto de uma classificação supervisionada que realizei com o plugin Semi-Automatic Classification Plugin no QGIS na Região Administrativa do Plano Piloto em Brasília-DF.
           '''
            )
st.subheader('Mapa de Localização de Projeto de Mineração')
st.markdown('''
    Escreva aqui
           '''
            )
mapa_lt = 'data/portfolio.svg'
render_svg(mapa_lt)

st.subheader('Mapa de Localização de Projeto de Mineração')
st.markdown('''
    Escreva aqui
           '''
            )