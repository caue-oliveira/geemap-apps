import streamlit as st

st.set_page_config(layout="wide")

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

st.title("Web App Google Earth Engine - Open Buildings V3")
st.markdown('''
Esta aplicação web foi desenvolvida em JavaScript dentro do editor de código do Google Earth Engine para análise urbana.
 Utilizando dados do Open Buildings V3, ela calcula o número de edifícios dentro de uma área definida pelo usuário.\n
A ferramenta considera apenas construções com confiabilidade acima de 70%. Os usuários têm a opção de exportar os dados 
nos formatos SHP ou KML, proporcionando maior versatilidade na análise e utilização das informações disponíveis.\n
Para acessar o aplicativo, clique aqui: [Open Buildings Web App]('https://ee-caueoliveira99.projects.earthengine.app/view/openbuildings-caue')
''')