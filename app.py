# Libs import
import streamlit as st

# Page configuration STARTS
st.set_page_config(layout="wide")

# Customize the sidebar
markdown = """
    Cauê Oliveira Miranda \n
    caue.oliveira99@gmail.com \n
    [GitHub](https://github.com/caue-oliveira) | [LinkedIn](https://www.linkedin.com/in/caueoliveira99) | [Currículo](https://www.canva.com/design/DAF4RWCBOuk/zsbheu6nUrXpw8PWQpcpjw/view?utm_content=DAF4RWCBOuk&utm_campaign=designshare&utm_medium=link&utm_source=viewer)
"""
    # Side bar info
st.sidebar.title("Contato")
st.sidebar.info(markdown)
logo = "data/SGRS_LG.png"
st.sidebar.image(logo)

# Customize page title
st.title("Portfolio de Cauê Oliveira")

st.markdown(
    """
    Olá, meu nome é Cauê Oliveira. Seja bem-vindo à minha página. \n
    Sou geólogo formado pela Universidade de Brasília, com uma paixão especial pelas geotecnologias. Desenvolvi este espaço para compartilhar um pouco das minhas habilidades e projetos. \n
    
    Os projetos que desenvolvi podem ser acessados na guia lateral à esquerda da página. Aqui você encontrará uma variedade de projetos no Google Earth Engine, tanto utilizando o JavaScript quanto a API do Python, além de painéis Power BI e mapas que elaborei. \n
    
    Sinta-se à vontade para explorar e entrar em contato caso tenha alguma pergunta ou oportunidade de colaboração.
    """
)

st.subheader("Sobre")

markdown = """
Essa página foi desenvolvida utilizando o [streamlit](https://streamlit.io), a partir do projeto open-source do Professor Qiusheng Wu da Universidade do Tennessee ([GitHub repository](https://github.com/giswqs/geemap-apps)). 
"""

st.markdown(markdown)
# Page configuration ENDS
