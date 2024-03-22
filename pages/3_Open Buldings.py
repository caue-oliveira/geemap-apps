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