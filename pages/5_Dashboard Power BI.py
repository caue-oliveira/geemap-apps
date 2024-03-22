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

st.title("Dashboard Power BI - Política Pró-Minerais Estratégicos")

st.markdown('''
 O dashboard foi elaborado durante meu período no Departamento de Transformação e Tecnologia Mineral do Ministério de Minas e Energia. A plataforma interativa foi desenvolvida no Power BI, com o objetivo de trazer transparência para a 
 Política de Apoio ao Licenciamento Ambiental de Projetos de Investimentos para a Produção de Minerais Estratégicos (Pró-Minerais Estratégicos) e o Comitê Interministerial de Análise de Projetos de Minerais Estratégicos (CTAPME). \n
 A ferramenta permite acessar informações acerca dos projetos de mineração habilitados na política, sendo possível investigar 
 daddos dos empreendimentos, investimento, títulos minerários, produção, reservas, recursos e informações gerais sobre 
 o licenciamento ambiental.
''')

st.image('data/openbuildings.png')

st.image('data/openbuildings_zoom.png')