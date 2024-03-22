# Libs
import streamlit as st
import folium
from streamlit_folium import st_folium
from branca.element import Template, MacroElement

# Arquivo GeoJSON
unds = ('data/unidades.geojson')

# Page Config STARTS
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

st.title("Mapa Geológico do Projeto Arenópolis - TF 2023 UnB")
st.markdown(
    """
    O Trabalho Final (TF) é um projeto de mapeamento geológico realizado pelos alunos de geologia da Universidade de Brasília, equivalente ao Trabalho de Conclusão de Curso (TCC).
    
    O mapa abaixo é o resultado do Projeto Arenópolis (2023) realizado em 15 dias de trabalho de campo e a partir da colaboração de 21 alunos.
    
    O objetivo dessa ferramenta é servir como um mapa de visualização simples, no qual é possível obter informações sobre as unidades geológicas ao passar o mouse sobre elas e escolher um mapa base de preferência.
 """
)
# Page config ENDS

# Map config STARTS
m = folium.Map(location=[-16.39374927779391, -51.663956293293964], tiles= 'openstreetmap', zoom_start=11)
folium.TileLayer('OpenTopoMap').add_to(m)
folium.TileLayer('Esri.WorldImagery').add_to(m)

# Dicionário de cores para cada unidade geológica presente
colors = {
    'Complexo Alcalino, Nefelinitos': '#D5EEB4',  # Cor para 'JKλian'
    'Complexo Alcalino, Gabros Alcalinos': '#F3F802',  # Cor para 'JKλiaga'
    'Complexo Alcalino, Subvulcânicas': '#14E8C3',  # Cor para 'JKλiasv'
    'Complexo Alcalino, Ijolitos e melteigitos': '#128BB3',  # Cor para 'JKλiaop',
    'Complexo Alcalino, Diques de basanito e fonolito': '#128BB3',
    'Bacia do Paraná, Formação Furnas': '#EFA10B',  # Cor para 'D1f'
    'Bacia do Paraná, Formação Ponta Grossa': '#F3B26B',  # Cor para 'Dpg'
    'Granitóide': '#AF252C',
    'Tonalito Indiferenciado': '#D80D8D',
    'Granito Serra do Iran, Diorito': '#E41C50',  # Cor para 'NP3γsnird'
    'Granito Serra do Iran, Monzogranito': '#FEC0EF',  # Cor para 'NP3γsnirm'
    'Granito Serra do Iran, Subvulcânica': '#FEC0EF',  # Cor para 'NP3γsnirsv'
    'Granito Serra do Iran, Sienogranito Fino': '#FCFBDD',  # Cor para 'NP3γsnirsf'
    'Granito Serra do Iran, Sienogranito Grosso': '#B60D12',  # Cor para 'NP3γsnirsg'
    'Granito Serra do Iran, Tonalito': '#E41C50',  # Cor para 'NP3γsnirt'
    'Granito Serra do Iran, Granodiorito': '#BEA387',  # Cor para 'NP3γsnirgr'
    'Granito Rio Caiapó, Granito Equigranular Fino': '#FC555A',
    'Granito Rio Caiapó, Granito Porfirítico Grosso': '#D65355',
    'Granito Rio Caiapó, Diorito': '#B9494D',
    'Córrego do Horácio': '#A9C1C4',
    'Granito Serra do Tatu': '#F5CBB6',  # Cor para 'NP2γst'
    'Ribeirão Água Limpa, Granito fino': '#E7A5AE',  # Cor para 'NP2aγalgf'
    'Ribeirão Água Limpa, Granito': '#FC555A',  # Cor para 'NP2aγalg'
    'Ribeirão Água Limpa, Granito Milonítico': '#FC555A',
    'Ribeirão Água Limpa, Hb Bt Tonalito': '#623184',  # Cor para 'NP2aγalhbt'
    'Gnaisse Arenópolis, Anfibolito': '331549',  # Cor para 'NP1γnaa
    'Gnaisse Arenópolis, Gnaisse Granítico': '#B282BF',
    'Gnaisse Arenópolis, Ultramáfica': '#546087',  # Cor para 'NP1γnaum'
    'Gnaisse Arenópolis, Gnaisse Tonalítico': '#9364C0',  # Cor para 'NP1γnagt'
    'Gnaisse Arenópolis, Calcissilicática': '#ED94EC',
    'Córrego da Onça, Qz-Msc-Xisto': '#BEE96E',  # Cor para 'NP1apox'
    'Córrego da Onça, Calcissilicática': '#0288E8',  # Cor para 'NP1apocc'
    'Córrego da Onça, Chert': '#6D8232',  # Cor para 'NP1apoch'
    'Córrego da Onça, Ultramáfica': '#10401E',  # Cor para 'NP1apoum'
    'Córrego da Onça, Anfibolito': '#315144',  # Cor para 'NP1apoa'
    'Córrego do Santo Antônio, Qz-Msc Xisto': '#BFEF4F',  # Cor para 'NP1apax'
    'Córrego do Santo Antônio, Metaultramáfica': '#35441C',  # Cor para 'NP1apaum'
    'Córrego do Santo Antônio, Anfibolito': '#6D8232',  # Cor para 'NP1apaa'
    'Córrego do Santo Antônio, Mármore': '#2CB2BF',
    'Córrego do Santo Antônio, Quartzito': '#4AC209',
    'Córrego do Santo Antônio, Gabro': '#2F7B6D',
    'Córrego do Santo Antônio, Chert': '#9900ff',  # Cor para 'NP1apach'
    'Morro do Baú, Gabro': '#5CCEAC',  # Cor para 'NP1δmb'
    'Gnaisse Ribeirão': '#990099',  # Cor para 'PP3γr'
}

# Função do estilo das geometrias com base na sigla
def color_by_sigla(feature):
    sigla = feature['properties'].get('Nome', '')  # Obtém o valor da propriedade 'Sigla', ou uma string vazia se não existir
    return {
        'stroke': False, # Linha de contorno = Falso
        'fillColor': colors.get(sigla, '#ffffff'), # Define as cores com base na sigla
        'fillOpacity': 0.8 # Opacidade do fill
    }

# Tooltip ao passar o mouse
tooltip = folium.GeoJsonTooltip(
    fields=["Nome", "Sigla", "Unidade", 'DominioEst'], # Parâmetros desejados
    aliases=["Nome: ", "Sigla: ", "Unidade Geológica: ", 'Domínio Estrutural: '], # Nome que vai aparecer
    localize=True,
    sticky=False,
    labels=True,
    style="""
        background-color: #F0EFEF;
        border: 2px solid black;
        border-radius: 3px;
        box-shadow: 3px;
    """,
    max_width=800,
)

# Adiciona a geometria GeoJson ao mapa
folium.GeoJson(unds, name= 'Mapa Geológico', style_function=color_by_sigla, tooltip=tooltip).add_to(m)

# Definindo o HTML da legenda
legend_template = """
{% macro html(this, kwargs) %}
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>jQuery UI Draggable - Default functionality</title>
  <link rel="stylesheet" href="//code.jquery.com/ui/1.12.1/themes/base/jquery-ui.css">

  <script src="https://code.jquery.com/jquery-1.12.4.js"></script>
  <script src="https://code.jquery.com/ui/1.12.1/jquery-ui.js"></script>
  
  <script>
  $( function() {
    $( "#maplegend" ).draggable({
                    start: function (event, ui) {
                        $(this).css({
                            right: "auto",
                            top: "auto",
                            bottom: "auto"
                        });
                    }
                });
});

  </script>
</head>
<body>

<div id='maplegend' class='maplegend' 
    style='position: absolute; z-index: 9999; background-color: rgba(255, 255, 255, 0.5);
     border-radius: 6px; padding: 5px; font-size: 9.5px; right: 50px; top: 90px;'>   
     
<div class='legend-title'>Legenda</div>  
<div class='legend-scale'>
  <ul class='legend-labels'>
    <li><span style='background: #D5EEB4; opacity: 0.75;'></span>Complexo Alcalino, Nefelinitos</li>
    <li><span style='background: #F3F802; opacity: 0.75;'></span>Complexo Alcalino, Gabros Alcalinos</li>
    <li><span style='background: #14E8C3; opacity: 0.75;'></span>Complexo Alcalino, Subvulcânicas</li>
    <li><span style='background: #128BB3; opacity: 0.75;'></span>Complexo Alcalino, Ijolitos e melteigitos</li>
    <li><span style='background: #128BB3; opacity: 0.75;'></span>Complexo Alcalino, Diques de basanito e fonolito</li>
    <li><span style='background: #EFA10B; opacity: 0.75;'></span>Bacia do Paraná, Formação Furnas</li>
    <li><span style='background: #F3B26B; opacity: 0.75;'></span>Bacia do Paraná, Formação Ponta Grossa</li>
    <li><span style='background: #AF252C; opacity: 0.75;'></span>Granitóide</li>
    <li><span style='background: #D80D8D; opacity: 0.75;'></span>Tonalito Indiferenciado</li>
    <li><span style='background: #E41C50; opacity: 0.75;'></span>Granito Serra do Iran, Diorito</li>
    <li><span style='background: #FEC0EF; opacity: 0.75;'></span>Granito Serra do Iran, Monzogranito</li>
    <li><span style='background: #FEC0EF; opacity: 0.75;'></span>Granito Serra do Iran, Subvulcânica</li>
    <li><span style='background: #FCFBDD; opacity: 0.75;'></span>Granito Serra do Iran, Sienogranito Fino</li>
    <li><span style='background: #B60D12; opacity: 0.75;'></span>Granito Serra do Iran, Sienogranito Grosso</li>
    <li><span style='background: #E41C50; opacity: 0.75;'></span>Granito Serra do Iran, Tonalito</li>
    <li><span style='background: #BEA387; opacity: 0.75;'></span>Granito Serra do Iran, Granodiorito</li>
    <li><span style='background: #FC555A; opacity: 0.75;'></span>Granito Rio Caiapó, Granito Equigranular Fino</li>
    <li><span style='background: #D65355; opacity: 0.75;'></span>Granito Rio Caiapó, Granito Porfirítico Grosso</li>
    <li><span style='background: #B9494D; opacity: 0.75;'></span>Granito Rio Caiapó, Diorito</li>
    <li><span style='background: #A9C1C4; opacity: 0.75;'></span>Córrego do Horácio</li>
    <li><span style='background: #F5CBB6; opacity: 0.75;'></span>Granito Serra do Tatu</li>
    <li><span style='background: #E7A5AE; opacity: 0.75;'></span>Ribeirão Água Limpa, Granito fino</li>
    <li><span style='background: #FC555A; opacity: 0.75;'></span>Ribeirão Água Limpa, Granito</li>
    <li><span style='background: #FC555A; opacity: 0.75;'></span>Ribeirão Água Limpa, Granito Milonítico</li>
    <li><span style='background: #623184; opacity: 0.75;'></span>Ribeirão Água Limpa, Hb Bt Tonalito</li>
    <li><span style='background: #331549; opacity: 0.75;'></span>Gnaisse Arenópolis, Anfibolito</li>
    <li><span style='background: #B282BF; opacity: 0.75;'></span>Gnaisse Arenópolis, Gnaisse Granítico</li>
    <li><span style='background: #546087; opacity: 0.75;'></span>Gnaisse Arenópolis, Ultramáfica</li

  </ul>
</div>
</div> 
<style type='text/css'>
  .maplegend .legend-scale ul {margin: 0; padding: 0; color: #0f0f0f;}
  .maplegend .legend-scale ul li {list-style: none; line-height: 18px; margin-bottom: 1.5px;}
  .maplegend ul.legend-labels li span {float: left; height: 16px; width: 16px; margin-right: 4.5px;}
</style>

{% endmacro %}
"""

# Add the legend to the map
macro = MacroElement()
macro._template = Template(legend_template)
m.get_root().add_child(macro) # Add a legenda ao mapa

folium.LayerControl().add_to(m) # Add o controle de layers
st_folium(m, width=1000) # Mapa ao streamlit