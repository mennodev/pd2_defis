import os
import glob
import streamlit as st
from pyogrio import read_dataframe
from streamlit_image_comparison import image_comparison

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


# side bar
st.sidebar.title('CLMS inventory')
page = st.sidebar.radio('Go to', ['Corine Land Cover', 'Costal Zones', 'Riparian Zones', 'Urban Atlas',
                                  #'Imperviousness',
                                  'Small Woody Features', 'Grassland', 'Tree Cover Change Mask',
                                  #'Water and Wetness'
                                  ])

# CLMS title
st.title('Copernicus Land Monitoring Services (CLMS) data for intensive farming monitoring (IFM)')

# clc
if page == 'Corine Land Cover':
    st.header('Corine land cover (CLC)')
    # description
    st.write('Corine Land Cover is a biophysical land cover / land use European database. This project, launched '
            'in 1985, is managed by the European Environment Agency (EEA) and covers 39 states. The first CORINE '
            'Land Cover (CLC) has been produced in 1990 and updates have been produced in 2000, 2006, 2012, and 2018.'
            'The inventory contains 44 land cover classes. The product has a Minimum Mapping Unit (MMU) of 25 hectares '
             '(ha) for areal phenomena and a minimum width of 100 m for linear phenomena. The time series are '
             'complemented by change layers every 6 years, which highlight changes in land cover with a MMU of 5 ha.')
    st.write('The CLC nomenclature is organized on three levels. The first level (five items) indicates the major '
             'categories of land cover. The second level composed of 15 items and the third level composed of 44 items.')

    # clc map
    st.subheader('CLC map')
    # display clc map according to year selected by the user (status + change)
    years = ['1990', '2000', '2006', '2012', '2018']
    y = st.selectbox("Select a year : ", options=years)
    st.image(f'data/images/clms/clc_{y}.png', caption=f"CLC map ({y})", use_column_width=True)
    if y != '1990':
        change_map = glob.glob(f'data/images/clms/clc_change_map*{y[-2:]}.png')[0]
        change_table = glob.glob(f'data/images/clms/clc_change_table*{y[-2:]}.png')[0]
        d1 = os.path.basename(change_map).split("_")[-1][0:2]
        if d1 == '90':
            d1 = '1990'
        else:
            d1 = f'20{d1}'
        d2 = f'20{os.path.basename(change_map).split("_")[-1][3:5]}'
        st.subheader(f'CLC change map {d1} - {d2}')
        st.image(change_map, caption=f"CLC change map ({d1} - {d2})", use_column_width=True)
        st.subheader(f'CLC change table {d1} - {d2}')
        st.image(change_table, caption=f"CLC change table ({d1} - {d2})", use_column_width=True)

    #highlights
    st.subheader('Highlights')
    generate_box()
    st.markdown(
        """
        <div class="rounded-box">
            <ul>
                <li>Corine Land Cover product provides key information on major trends, especially artificial development and forest management.</li>
                <li>Data on agriculture covers 1990-2000 and 2000-2006, with less information from 2006-2012, and no changes identified between 2012-2018.</li>
                <li>Agricultural changes involve internal conversions between annual crops and grassland, but the detection threshold only captures areas ≥5 hectares.</li>
                <li>Monitoring agricultural changes requires higher frequency (annual update) and finer spatial resolution at the plot level.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True
    )

# cz
if page == 'Costal Zones':
    st.header('Costal zones (CZ)')
    # decription
    st.write('The coastal Zones product provides detailed land cover and land use information for 71 thematic land '
             'cover classes for all European coastal territory to a landward distance of 10 km with total area '
             'mapped of approximatively 730,000km². The product has a six-year update cycle and is now available '
             'for the 2012 and 2018 reference years with the 2012-2018 change layer. The dataset has a Minimum Mapping '
             'Unit (MMU) of 0.5 ha and a Minimum Mapping Width (MMW) of 10 m and is available as vector data. ')

    # cz map
    st.subheader('CZ map')
    # display clc map according to year selected by the user (status + change)
    years = ['2012', '2018']
    y = st.selectbox("Select a year : ", options=years)
    st.image(f'data/images/clms/cz_{y}.png', caption=f"RZ map ({y})", use_column_width=True)
    st.subheader('CZ change map 2012 - 2018')
    st.image(f'data/images/clms/cz_change_12-18.png', caption=f"CZ change map (2012-2018)", use_column_width=True)
    st.subheader('CZ change table 2012 - 2018')
    st.image(f'data/images/clms/cz_change_table_12-18.png', caption=f"CZ change table (2012-2018)", use_column_width=True)

    #highlights
    st.subheader('Highlights')
    generate_box()
    st.markdown(
        """
        <div class="rounded-box">
            <ul>
                <li>Analysis of Table 5 (2012-2018 coastal zones) reveals two main flows: urban dynamics (red) and forest cover changes (green)</li>
                <li>The CZ database uses smaller surface thresholds (0.5 ha) compared to Corine land cover (5 ha).</li>
                <li>Agricultural changes (yellow) are weakly represented, with only a few hectares identified.</li>
                <li>Improved identification of agricultural and grass cover changes is needed.</li>
                <li>Monitoring agricultural changes requires higher frequency (annual update) and finer spatial resolution at the plot level.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True
    )


# rz
if page == 'Riparian Zones':
    st.header('Riparian zones (RZ)')
    # description
    st.write('The RZ data provides detailed land cover and land use information for 55 thematic classes in a '
             'variable buffer zone of selected rivers across Europe for the 2012 and 2018 reference year. The dataset '
             'has a Minimum Mapping Unit (MMU) of 0.5 ha and a Minimum Mapping Width (MMW) of 10 m and is available '
             'as vector data. It is updated every six years, and currently consists of three layers—a land cover/land '
             'use layer for 2012 and 2018 and a change layer for 2012-2018. ')

    # rz map
    st.subheader('RZ map')
    # display clc map according to year selected by the user (status + change)
    years = ['2012', '2018']
    y = st.selectbox("Select a year :", options=years)
    st.image(f'data/images/clms/rz_{y}.png', caption=f"RZ map ({y})", use_column_width=True)
    st.subheader('RZ change map 2012 - 2018')
    st.image(f'data/images/clms/rz_change_12-18.png', caption=f"RZ change map (2012-2018)", use_column_width=True)
    st.subheader('RZ change table 2012 - 2018')
    st.image(f'data/images/clms/rz_change_table_12-18.png', caption=f"RZ change table (2012-2018)", use_column_width=True)

    #highlights
    st.subheader('Highlights')
    generate_box()
    st.markdown(
        """
        <div class="rounded-box">
            <ul>
                <li>Land cover changes are primarily due to artificialization (red) and conversion of mining extraction to grassy areas (blue).</li>
                <li>No agricultural rotations between grassland and annual crops (yellow) are represented.</li>
                <li>Buffer strips along watercourses protect soils from erosion, improve structure, and reduce diffuse pollution risks.</li>
                <li>Buffer strips support biodiversity and crop auxiliaries.</li>
                <li>Monitoring crop types and changes over time in riparian zones is crucial, including the proportion of grassed areas and annual crops (e.g., corn, wheat, cabbage).</li>
                <li>It requires annual update.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True
    )


# ua
if page == 'Urban Atlas':
    st.header('Urban Atlas (UA)')
    # description
    st.write('The Urban Atlas data provides land cover and land use data with the integrated population '
             'estimates in 788 Functional Urban Areas (FUA) with more than 50,000 inhabitants in EEA39 countries for '
             'the 2018, 2012 and 2006 reference year. The dataset maps land cover and land use for 17 urban classes '
             'with the Minimum Mapping Unit (MMU) of 0.25 ha and for 10 rural classes with the MMU of 1 ha and is '
             'available as vector data and updated every 6 years. Urban Atlas data are available for the 2006, 2012 '
             'and 2018 reference years including the two change products for 2006-2012 and 2012-2018. Only reference '
             'year 2012 and 2018 are available for the Functional Urban Area (FUA) of Saint-Brieuc city.  ')

    # ua map
    st.subheader('UA map')
    # display clc map according to year selected by the user (status + change)
    years = ['2012', '2018']
    y = st.selectbox("Select a year: ", options=years)
    st.image(f'data/images/clms/ua_{y}.png', caption=f"RZ map ({y})", use_column_width=True)
    st.subheader('UA change map 2012 - 2018')
    st.image(f'data/images/clms/ua_change_12-18.png', caption=f"UA change map (2012-2018)", use_column_width=True)
    st.subheader('UA change table 2012 - 2018')
    st.image(f'data/images/clms/ua_change_table_12-18.png', caption=f"UA change table (2012-2018)", use_column_width=True)

    #highlights
    st.subheader('Highlights')
    generate_box()
    st.markdown(
        """
        <div class="rounded-box">
            <ul>
                <li>The Urban Atlas provides detailed land cover and land use maps for various urban areas in Europe.</li>
                <li>It includes data on street trees, building heights, and population estimates.</li>
                <li>The products focus on urban expansion over agricultural, natural areas, industrial lands, roadways, and mining sites.</li>
                <li>The database primarily addresses land artificialization, not agricultural or natural space changes.</li>
                <li>No improvements in monitoring artificialization are necessary, as imperviousness data is updated every 3 years.</li>
                <li>The agricultural monitoring requires annual update.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True
    )


# # imp
# if page == 'Imperviousness':
#     st.header('Imperviousness')
#     # description
#     st.write('Impermeable surfaces such as roads and buildings prevent rainwater from infiltrating the ground, '
#              'leading to increased runoff, flooding and reduced groundwater recharge.  According to Copernicus, '
#              'Imperviousness products detect the spatial distribution and evolution over time of artificially sealed '
#              'areas at continental level. The main products are Imperviousness Density, which provides data on '
#              'imperviousness density in a range from 0 to 100% (for dates 2006, 2009, 2012, 2015, 2018), and maps of '
#              'classified changes at variable resolution (10, 20, 100m). These data are available in raster format and '
#              'updated every 3 years.')
#
#     # imp map
#     st.subheader('Imperviousness map')
#     # display clc map according to year selected by the user (status + change)
#     years = ['2006', '2009', '2012', '2015', '2018']
#     y = st.selectbox("Select a year: ", options=years)
#     st.image(f'data/images/clms/imp_{y}.png', caption=f"RZ map ({y})", use_column_width=True)
#     if y != '2006':
#         change_map = glob.glob(f'data/images/clms/imp_change*{y[-2:]}.png')[0]
#         d1 = f'20{os.path.basename(change_map).split("_")[-1][0:2]}'
#         d2 = f'20{os.path.basename(change_map).split("_")[-1][3:5]}'
#         st.subheader(f'Imperviousness change map {d1} - {d2}')
#         st.image(change_map, caption=f"Imperviousness change map ({d1} - {d2})", use_column_width=True)
#
#     # wip
#     st.markdown('<p style="color:Red; font-size: 20px; background-color:Yellow">To be completed</p>', unsafe_allow_html=True)

# swf
if page == 'Small Woody Features':
    st.header('Small Woody Fetures (SWF)')
    # description
    st.write('The Copernicus service Small Woody Features product provides data on woody features ≤ 30 m wide and '
             '≥ 30 m long, as well as patchy structures from 200 m² to 5,000 m² in area, with a spatial resolution '
             'of 5m. These data, available for 2015 and 2018, cover the EEA38 and the UK, providing a tool for '
             'understanding landscapes, assessing biodiversity and carbon sequestration, supporting sustainable land '
             'management and mitigating climate change. Small woody formations can also help to regulate water cycles '
             'and prevent soil erosion, functions that are particularly important in agricultural areas where soil '
             'health is extremely important. ')

    # swf map
    st.subheader('SWF map')
    # display clc map according to year selected by the user (status)
    years = ['2015', '2018']
    y = st.selectbox("Select a year: ", options=years)
    st.image(f'data/images/clms/swf_{y}.png', caption=f"SWF map ({y})", use_column_width=True)

    # analysis
    st.subheader('Analysis')
    # barplot grassland change 2015-2018
    grass_change_15_18 = read_dataframe('data/dataframes/swf_change_table_15-18.csv')
    grass_change_15_18['Catchment basin'] = grass_change_15_18['Catchment basin'].astype('int')
    grass_change_15_18['2015'] = grass_change_15_18['2015'].astype('float')
    grass_change_15_18['2018'] = grass_change_15_18['2018'].astype('float')
    st.bar_chart(grass_change_15_18,
                 x='Catchment basin',
                 y=['2015', '2018'],
                 y_label='Surface (ha)',
                 stack=False)

    # render swf comparison
    image_comparison(
        img1="data/images/clms/swf_henon_2015_5m.png",
        img2="data/images/clms/swf_henon_2018_5m.png",
        label1='SWF 2015',
        label2='SWF 2018',
        show_labels=True
    )
    # swf omissions / commissions
    gl_select = st.selectbox("Zoom on SWF data", options=['SWF 2015', 'SWF 2018'])
    if gl_select == 'SWF 2015':
        st.image('data/images/clms/swf_henon_2015_5m_err.png')
    elif gl_select == 'SWF 2018':
        st.image('data/images/clms/swf_henon_2018_5m_err.png')
    st.image('data/images/clms/swf_change_legend.png')

    #highlights
    st.subheader('Highlights')
    generate_box()
    st.markdown(
        """
        <div class="rounded-box">
            <ul>
                <li>SWF 2015 and SWF 2018 are not directly comparable, making it difficult to track changes in SWF cover, such as hedgerow destruction or restoration.</li>
                <li>A small extract from Saint Brieuc shows inconsistencies between the two datasets: omissions of SWFs (e.g., hedges) in both 2015 and 2018; features mapped in 2015 but missing in 2018, despite their continued existence; Improvements in the 2018 database include removal of false SWFs and addition of previously unmapped real SWFs.</li>
                <li>TSWF gain between 2015 and 2018 includes errors due to methodological changes</li>
                <li>Accurate and exhaustive identification of SWFs, including hedges and small woodland patches, is needed for monitoring their evolution over time.</li>
                <li>Annual monitoring could improve the assessment of gradual changes, such as hedgerow destruction.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True
    )

# grassland
if page == 'Grassland':
    st.header('Grassland')
    # legislation
    st.subheader('Legislation on grasslands')
    st.write('Grassland ecosystems have a lot to offer in terms of biodiversity: they are home to a large number of '
             'species, some of which are strictly dependent on this habitat. However, over the last few decades, this '
             'dynamic has clearly been unfavorable for grasslands: with a 33% loss between 1967 and 2007 the reduction '
             'in their surface area has been drastic. The action taken by the Natura 2000 network is an appropriate '
             'tool for conserving grasslands, but it is essentially limited to the perimeter of its sites. Outside '
             'protected sites, it is subject to the CAP regime. As part of the green payment introduced by the reform '
             'of the Common Agricultural Policy (CAP) in 2015, France made a commitment to collectively ensure the '
             'maintenance of permanent grassland areas (grassland over 5 years old) on national territory, and this is '
             'one of the three principles of the greening of the CAP. This commitment continues in the NSP and the '
             'new CAP program. ')

    # description
    st.write('The High-Resolution Layer Grassland is a pan-European binary product that provides a '
             'grassland/non-grassland mask, with triennial updates for 2015 and 2018. Its spatial resolution was '
             '20 meters in 2015 and improved to 10 meters in 2018. Annual updates are planned from 2024 onward. '
             'Additionally, a change detection layer for 2015–2018 is available to help distinguish real changes '
             'from false changes caused by the difference in resolution between the two products.')
    st.subheader('Grassland map')
    # display clc map according to year selected by the user (status + change)
    years = ['2015', '2018']
    y = st.selectbox("Select a year:", options=years)
    st.image(f'data/images/clms/grass_{y}.png', caption=f"RZ map ({y})", use_column_width=True)
    st.subheader('Grassland change map')
    st.image('data/images/clms/grass_change_15-18.png', caption=f"Grassland change map (2015-2018)", use_column_width=True)


    # analysis
    st.subheader('Analysis')
    st.write('The maps show the grassland areas in 2015 and 2018 by catchment basin. It is notable that the grassland '
             'areas in 2018 are significantly larger than in 2015, in some cases more than double (see diagram below). '
             'However, these differences observed between the two dates do not reflect real changes, they are mostly '
             'due to different methodologies and change in spatial resolution, making it impossible to map changes.')

    # barplot grassland change 2015-2018
    grass_change_15_18 = read_dataframe('data/dataframes/grass_change_table_15-18.csv')
    grass_change_15_18['Catchment basin'] = grass_change_15_18['Catchment basin'].astype('int')
    grass_change_15_18['2015'] = grass_change_15_18['2015'].astype('float')
    grass_change_15_18['2018'] = grass_change_15_18['2018'].astype('float')
    st.bar_chart(grass_change_15_18,
                 x='Catchment basin',
                 y=['2015', '2018'],
                 y_label='Surface (ha)',
                 stack=False)

    # render grassland comparison
    image_comparison(
        img1="data/images/clms/grass_2015-zoom.png",
        img2="data/images/clms/grass_2018-zoom.png",
        label1='Grassland 2015',
        label2='Grassland 2018',
        show_labels=True
    )
    st.caption('<div style="text-align: center">my caption</div>', unsafe_allow_html=True)

    st.image('data/images/clms/grass_change_15-18-zoom.png', caption='Zoom on grassland change map (2015-2018)')

    #highlights
    st.subheader('Highlights')
    generate_box()
    st.markdown(
        """
        <div class="rounded-box">
            <ul>
                <li>The 2015 and 2018 Grassland layers are not comparable due to different methodologies and surface thresholds used in their production.</li>
                <li>Changes observed in the layers are likely due to methodological differences rather than actual land cover changes between grassland and annual crops.</li>
                <li>The 2018 grassland layer appears accurate, but there is still a significant gap in reliable information on grassland to annual crop conversions.</li>
                <li>Accurate monitoring of grassland conversions is important for environmental, biodiversity, and pollution assessments.</li>
                <li>Producing the grassland layer annually would improve the accuracy and relevance of monitoring grassland changes.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True
    )


# tccm
if page == 'Tree Cover Change Mask':
    st.header('Tree Cover Change Mask (TCCM)')
    st.write('This data provides pan-European information at a spatial resolution of 20 meters on changes across '
             'four thematic classes: unchanged areas with no tree cover, new tree cover, loss of tree cover, and '
             'unchanged areas with tree cover. These changes are tracked between the 2012/2015 and 2015/2018 reference '
             'years.')
    st.subheader('TCCM map')
    # display tccm map according to year selected by the user (change)
    years = ['2012-2015', '2015-2018']
    y = st.selectbox("Select a year:", options=years).replace('20', '')
    st.image(f'data/images/clms/tccm_{y}.png', caption=f"TCCM map ({y})", use_column_width=True)

    # barplot grassland change 2015-2018
    tccm = read_dataframe(f'data/dataframes/tccm_{y}.csv')
    tccm['Catchment basin'] = tccm['Catchment basin'].astype('int')
    tccm['Gain'] = tccm['Gain'].astype('float')
    tccm['Loss'] = tccm['Loss'].astype('float')
    st.bar_chart(tccm,
                 x='Catchment basin',
                 y=['Gain', 'Loss'],
                 y_label='Surface (ha)',
                 stack=False)

    #highlights
    st.subheader('Highlights')
    generate_box()
    st.markdown(
        """
        <div class="rounded-box">
            <ul>
                <li>The database does not provide information on the evolution of linear wooded elements.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True
    )

# # ww
# if page == 'Water and Wetness':
#     st.header('HRL Water and Wetness (WW)')
#     # display ww map according to year selected by the user (status)
#     years = ['2015', '2018']
#     y = st.selectbox("Select a year : ", options=years)
#     st.image(f'data/images/clms/waw_{y}.png', caption=f"WW map ({y})", use_column_width=True)
#
#     # wip
#     st.markdown('<p style="color:Red; font-size: 20px; background-color:Yellow">To be completed</p>', unsafe_allow_html=True)