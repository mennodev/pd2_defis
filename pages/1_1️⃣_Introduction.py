import geopandas as gpd
import streamlit as st
import folium
from streamlit_folium import st_folium

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
st.write('In this pilot project, we aim to demonstrate an integrated approach to monitoring various aspects of '
         'biodiversity linked to a specific region. Our focus will be on the geographically confined area of Brittany, '
         'France, particularly the Bay of Saint-Brieuc, which faces a range of environmental challenges related to '
         'intensive agriculture and livestock farming. Brittany’s long coastline, diverse wetlands, and Natura 2000 '
         'sites coexist with extensive livestock operations, including pig farms that contribute to significant '
         'nitrogen emissions, and intensive agriculture that relies heavily on fertilizers. The excess nitrogen from '
         'both livestock and fertilizers negatively impacts the region’s fragile wetlands, Natura 2000 areas, and even '
         'the surrounding ocean.')

st.write('Nitrogen run-off from fertilizers into surface waters has led to widespread algae blooms in recent decades, '
         'suffocating coastal ecosystems. Additionally, the ongoing removal of hedgerows and subsequent soil '
         'erosion have further degraded the local environment.')

st.write('Through this regional approach, we will showcase how Earth Observation (EO) technologies can be leveraged '
         'to monitor the impacts of nitrogen emissions and deposition. We will focus on using EO missions to observe '
         'how nitrogen surpluses affect Brittany’s wetlands and coastal areas, and how intensive farming impacts '
         'Natura 2000 sites. The effectiveness of current sensors for mapping these interactions will be tested, '
         'along with the potential of new, higher-cadence EO sensors. We will also explore whether higher-frequency '
         'monitoring is more suitable for future biodiversity protection laws, and how nitrogen emissions and '
         'deposition influence nearby nature reserves.')

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
# init study map
study_map = folium.Map(location=[48.589098, -2.432541],
                       zoom_start=9,
                       attr='© OpenStreetMap contributors')

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