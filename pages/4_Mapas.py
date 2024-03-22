import streamlit as st

st.title("Exposição de Mapas")

st.subheader('Mapa de Uso e Cobertura do Solo do Plano Piloto')
st.markdown('''
    Este mapa é produto de uma classificação supervisionada realizada com o plugin Semi-Automatic Classification Plugin no QGIS, na Região Administrativa do Plano Piloto em Brasília-DF. \n
    A classificação foi feita com dados do sensor OLI do satélite Landsat 8.
           '''
            )
st.image('data/CLASSIFICATION.png')

st.subheader('Mapa de Linhas de Transmissão no Brasil')
st.markdown('''
    Este mapa exibe a rede de linhas de transmissão elétrica em todo o território brasileiro. Criado com base em dados atualizados do Operador Nacional do Sistema Elétrico (ONS), o mapa destaca as principais linhas com base nas suas tensões em kV.
               '''
            )
st.image('data/mapa_lt.png')

st.subheader('Mapa de Localização de Projeto de Mineração')
st.markdown('''
    Este mapa mostra a localização de um projeto de mineração no estado do Pará, Brasil. Nele destaca-se a planta do empreendimento e a presença de assentamentos do Instituto Nacional de Colonização e Reforma Agrária (INCRA) na região. 
           '''
            )
st.image('data/proj_min.png')