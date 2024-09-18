import geopandas as gpd
import streamlit as st
import folium
from streamlit_folium import st_folium
from branca.element import Template, MacroElement

# function
def map_bv():
    bv_geom = gpd.read_file('data/geometries/bv_sb-4326.fgb', engine='pyogrio')
    bv_geom['DateCreationOH'] = bv_geom['DateCreationOH'].astype('string')
    bv_geom = bv_geom.rename(columns={'ida': 'BV Ref'})
    bv_geom = bv_geom.to_json()
    bv_style = {'fillColor': '#C0C0C0', 'color': '#696969'}
    folium.GeoJson(bv_geom,
                   style_function=lambda x: bv_style,
                   popup=folium.GeoJsonPopup(
                       fields=['BV Ref', 'area_km2'],
                       aliases=['BV Ref : ', 'Area (km²) : ']
                   )).add_to(study_map)


# 1. context
st.title('Context')
st.write('In this pilot we will demonstrate an integrated approach to monitor various biodiversity aspects that are '
         'linked to a specific region. We will focus on the geographically confined area of Brittany in France, and '
         'more specifically the Bay of Saint Brieuc, as the area is facing a complex of environmental issues related '
         'to (intensive) agriculture and livestock holding. The area of Brittany has a very long coastline, various '
         'wetlands and specific Natura2000 sites. At the same time the region also hosts significant intensive '
         'livestock farming including pigsties and chicken farming causing nitrogen emission and deposition, as well '
         'as intensive agriculture where large amounts of fertilizer are used. The surplus of nitrogen through '
         'emissions from livestock farming and fertilizer usage affects the vulnerable wetlands, Natura2000 areas and '
         'ultimately even the surrounding ocean negatively. The nitrogen from fertilizer usage is leaking via surface '
         'waters into the ocean causing large green algae blooms in recent decades, suffocating coastal ecosystems. '
         'Moreover, there’s an ongoing trend of felling of hedges (High Diversity Landscape Feature - HDLF) and '
         'subsequent soil erosion adding to the further degradation of the ecosystem.')

st.write('By taking this regional approach we will demonstrate how EO can aid in monitoring the effect of nitrogen '
         'emissions and depositions, how to leverage EO-missions focusing on marine and coastal areas to monitor '
         'effects of nitrogen surplus on wetlands and coastal zones of Brittany and how Natura2000 sites are affected '
         'by intensive livestock farming. The current sensors to map such interlinkages will be tested together with '
         'the limitations and cadence of new EO sensors. We will investigate if and how higher cadence is better '
         'suited for current and future legislation on biodiversity protection, nitrogen emissions and deposition and '
         'its effect on surrounding nature reserves in the region.  ')

# 2. Objectives
st.title('Objectives')
st.markdown(
    """
    - Explore and list the Copernicus products that can be used to monitor biodiversity, their limitations and the data that could be used for a better monitoring.
    - Demonstrate how EO monitoring solutions are (or can be) implemented in the environmental  monitoring and highlight cadence requirements.
    """)

# 3. study area
st.title('Study area')
st.write('The study area includes NATURA 2000 sites, part of an EU ecological network aimed at conserving wildlife and '
         'natural habitats. It focuses on the Bay of Saint-Brieuc in northern Brittany, France, which was designated '
         'as a "Natural Reserve" in April 1998. The bay, located between the Bréhat archipelago and Cap Fréhel, covers '
         'about 800 km², including the Yffiniac and Morieux coves. The study area also encompasses the surrounding '
         'catchment areas, totaling 1,225 km².')

# map study area
# legend
legend_template = """
{% macro html(this, kwargs) %}
<div id='maplegend' class='maplegend' 
    style='position: absolute; z-index: 9999; background-color: rgba(255, 255, 255, 0.5);
     border-radius: 6px; padding: 10px; font-size: 10.5px; right: 20px; top: 20px;'>     
<div class='legend-scale'>
  <ul class='legend-labels'>
    <li><span style='background: #87CEFA; border: 2px solid #1E90FF; opacity: 0.75;'></span>Natura 2000 sites</li>
    <li><span style='background: #e6e6e6; border: 2px solid #606060; opacity: 0.75;'></span>Catchment basins</li>
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
# init study map
study_map = folium.Map(location=[48.589098, -2.432541],
                       zoom_start=9,
                       attr='© OpenStreetMap contributors')

# Add the legend to the map
macro = MacroElement()
macro._template = Template(legend_template)
study_map.get_root().add_child(macro)

# map catchment basin
bv_map = map_bv()

# N2K sites map
n2k_style = {'fillColor': '#87CEFA', 'color': '#1E90FF'}
n2k_geom = gpd.read_file('data/geometries/n2000_sb-4326.fgb').to_json()
folium.GeoJson(n2k_geom,
               style_function=lambda x:n2k_style,
               popup=folium.GeoJsonPopup(
                   fields=['SITECODE', 'SITENAME', 'SITETYPE'],
                   aliases=['Site code : ', 'Site name : ', 'Site Type : ']
               )).add_to(study_map)

#folium.LayerControl().add_to(study_map)
# display
sm = st_folium(study_map, width=900, height=600)

st.header(f'Please navigate through the side bar to explore the PD2 content')
st.markdown('- To discover an inventory of Copernicus Land Monitoring Services (CLMS) that can be used to monitore farming pressure on local and regional environment and there limitations, click the link below : ')
link1 = st.page_link('pages/2_2️⃣_CLMS_inventory.py', label='2️⃣️ CLMS inventory')
st.markdown('- To discover third-party solutions to help monitoring farming activities with some limitations, please click the link below :')
link2 = st.page_link('pages/3_3️⃣_Third_Party_solutions.py', label='3️⃣️ Third Party solutions')
st.markdown('- To visualise practical consequences of intensive farming on biodiversity and limitations of current Sentinel-2 cadence, please click the link below :')
link3 = st.page_link('pages/4_4️⃣_Algaes_Detection.py', label='4️⃣️ Algaes Detection')