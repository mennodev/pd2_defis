import geopandas as gpd
import pandas as pd
from pyogrio import read_dataframe
import streamlit as st
import folium
from streamlit_folium import st_folium
from streamlit_image_comparison import image_comparison


# 4. Algal bloom detection
# ------------------------
# functions
def generate_box():
    return st.markdown(
    """
    <style>
    .rounded-box {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #ddd;
    }
    .rounded-box ul {
        padding-left: 20px;
    }
    .rounded-box li {
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True
)


st.title('Algal bloom detection')
st.header('Description')
st.write('The intensive farming context of the region of Saint-Brieuc lead to nutrient runoff, contributing to the '
         'formation of algal blooms in the bay which is the outlet for all the contaminated waters. These blooms, '
         'characterized by the rapid proliferation of algae, pose significant threats to biodiversity by depleting '
         'oxygen levels in the water and disrupting aquatic ecosystems. The rotting of the algaes that stagnate also '
         'leads to significant air pollution with hydrogen sulphide, which threaten wildlife and passers-by. ')
st.image('data/images/algaes/algaes_detection.png', caption='Algaes proliferation detected over Saint-Brieuc bay’s beaches '
                                                     'with S2 satellite (composite S2 image and ground photos) ')

# image gallery
st.header('Ground photos gallery')
st.write('These photos were taken during the summer of 2024. They show the amount of green algae that spread over the bay.')
algaes_l = ['data/images/algaes/algaes1.png',
            'data/images/algaes/algaes2.png',
            'data/images/algaes/algaes3.png',
            'data/images/algaes/algaes4.png',
            'data/images/algaes/algaes5.jpg',
            'data/images/algaes/algaes6.jpg',
            'data/images/algaes/algaes7.jpg',
            'data/images/algaes/algaes8.jpg',
            'data/images/algaes/algaes9.jpg',
            'data/images/algaes/algaes10.jpg']

col1, col2, col3, col4 = st.columns(4)
for i, im in enumerate(algaes_l):
    with eval(f'col{i % 3 + 1}'):
        st.image(im, use_column_width='auto')

# s2 for algal bloom detection
st.header('Copernicus data for algal blooms monitoring')
st.write('Copernicus Sentinel-2 imagery can be used to detect algal blooms. By analysing spectral signatures, it is '
         'possible to identify areas experiencing abnormal levels of chlorophyll, indicative of algal presence. '
         'However, one major challenge in utilizing Sentinel-2 imagery for algal bloom detection is the intermittent '
         'availability of data due to **cloud cover**, making some images unusable for analysis. This limitation '
         'impedes timely monitoring and early detection of algal blooms, particularly during critical stages of their '
         'development. Furthermore, detecting algal blooms in coastal areas, such as the bay, is more effective during '
         'low tide when the water is shallow and the algae are more visible. This underscores the importance '
         'of having high-cadence data, potentially daily, to enable early detection and timely intervention. ')


# init study map
st.subheader('Location of the region of interest')
st.markdown('A sub-region of interest has been selected to monitor algaes proliferation. It is bordered by the city of '
            'Saint-Brieuc to the west, the city of Yffiniac to the south, and the city of Planguenoual to the east.')
study_map = folium.Map(location=[48.589098, -2.432541],
                       zoom_start=9,
                       attr='© OpenStreetMap contributors')

# map catchment basin
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

# map roi
roi = read_dataframe('data/geometries/roi.fgb').to_json()
#folium.Map(roi).add_to(study_map)
folium.GeoJson(roi).add_to(study_map)

sm = st_folium(study_map, width=900, height=600)

# plot s2 time series
st.subheader('Cloud cover limitation')
st.markdown('Cloud cover is the main limitation in monitoring of green algaes as they make it impossible to see '
            'surface of the Earth in the optical domain. Through the snapshot time series from March to November 2022 '
            'and 2023, you can visualize the amount of clouds present in the images.')
selected_year = st.selectbox("Select a year : ", ['2022', '2023'])
st.image(f'data/images/algaes/s2_ts_{selected_year}.png', caption=f'Sentinel-2 images for {selected_year}')
if selected_year == '2023':
    st.markdown(f'The {selected_year} time series shows many cloudy observations, and few images are actually usable during this period.')

# plot
cloud_df = read_dataframe(f'data/dataframes/cloud_stats_{selected_year}_df.csv')
cloud_df['date'] = pd.to_datetime(cloud_df['date'])
cloud_df['perc_cloud'] = cloud_df['perc_cloud'].astype(float)
cloud_df['perc_cloud_norm'] = cloud_df['perc_cloud_norm'].astype(float)

# let the user select cloud percentage
selected_perc = st.slider('Move the cursor below to change the percentage of clouds and cloud shadows covering the sud-region : ', min_value=0, max_value=100, value=100)
cloud23_df_filtered = cloud_df[cloud_df['perc_cloud'] <= selected_perc]
num_points = len(cloud23_df_filtered)
st.markdown(f'A total of {num_points} images found with less than {selected_perc} % of clouds.')
st.scatter_chart(cloud23_df_filtered,
                 x='date',
                 y='perc_cloud',
                 x_label='Date',
                 y_label='Cloud / cloud shadow (%)')

st.write('The analysis of the time series highlights several critical insights regarding the limitations of Copernicus '
         'Sentinel-2 capabilities in monitoring environmental phenomena such as algal blooms. The graphic above '
         'represents the percentage of clouds and cloud shadows present in each image throughout the time series. It '
         'shows the lack of clear data despite a 5 days revisit time. As the figure shows, 2023 has been particularly '
         'challenging due to the high prevalence of cloudy conditions. In fact, it wasn’t until mid-July that the '
         'first image with less than 20% cloud and cloud shadow cover was available. In 2022, despite a larger number '
         'of clear images, the are still long cloudy periods. This delay severely impacts the ability to monitor '
         'early-stage algal blooms.')

# s2 vs. s3
st.subheader('Sentinel-2 or Sentinel-3 ?')
st.write("The Sentinel-3 mission surveys Earth's oceans, land, ice and atmosphere to monitor and understand large "
         "scale global dynamics. Learn more about Sentinel-3 missions here : https://www.esa.int/Applications/Observing_the_Earth/Copernicus/Sentinel-3")
st.write('The "Ulyssys Water Quality Viewer (UWQV)", a custom script for the Sentinel-hub EO browser, can be uased to '
         'dynamically visualize chlorophyll conditions using Sentinel-2 and Sentinel-3 imagery (see the interactive '
         'figure below). Chlorophyll concentration serves as a general indicator of algae abundance, and therefore of '
         'energy and biomass input into the aquatic food web through photosynthesis. Since algal growth is often '
         'limited by nutrient availability, high chlorophyll concentrations are frequently the result of pollution '
         'from agricultural runoff. ')

st.write('We selected 3 dates where atmospheric conditions were very clear to visualise algaes and compare the ability of '
         'the two sensors to map.')
selected_date = st.selectbox('Select a date : ', ['04-20-2024', '06-09-2024', '06-29-2024'])
d = f'{selected_date[-4:]}_{selected_date[0:2]}_{selected_date[3:5]}'

# render swf/third-party comparison
image_comparison(
    img1=f"data/images/algaes/s2_{d}.png",
    img2=f"data/images/algaes/s3_{d}.png",
    label1='Sentinel-2',
    label2='Sentinel-3',
    show_labels=True
)

st.write("The results indicate that the Sentinel-2, while providing higher spatial resolution, can be less accurate in "
         "detecting algaes due to confusion with sediments, leading to false positives. In contrast, Sentinel-3's "
         "OLCI (Ocean and Land Cover Instrument) sensor covers more bands (21), enabling better spectral "
         "differentiation between algae and sediments, thus reducing confusion, but offering lower spatial resolution "
         "(300 meters). Also Sentinel-3's OLCI sensor has a revisit period of less than 2 days, offering almost daily "
         "data, unlike Sentinel-2. By combining the two sensors, it would be possible to better monitor algae bloom "
         "with high temporal and spatial resolution. ")

# highlights
st.subheader('Highlights')
generate_box()
st.markdown(
    """
    <div class="rounded-box">
        <ul>
            <li>The analysis of cloud and cloud shadow percentages indicates a lack of clear data despite the Sentinel-2's 5-days revisit time.</li>
            <li>The potential delay in obtaining clear images severely hampers the ability to monitor early-stage algal blooms.</li>
            <li>Increasing cadence to daily observations would increase the chances of obtaining clear images.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True
)