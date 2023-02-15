## Testing out building a basic webapp for isochrone data
#from numpy.lib.arraysetops import union1d_dispatcher
import pandas as pd
import streamlit as st
from PIL import Image
import plotly.express as px
#import base64
import numpy as np
import isochrones
from streamlit_folium import folium_static
from branca.element import Template, MacroElement

from settings import template

# Set page title and favicon.
TRAIN__ICON_URl= 'resources/img/train_icon.png'

# Page layout
## adds page icon and Page expands to full width
st.set_page_config(
    page_title="Train Station Isochrones", page_icon=TRAIN__ICON_URl,
    layout="wide",
)
###Load Relevant Data###


##Loads image for 
#image = Image.open('../resources/img/DSC09499.JPG')

# Calling csv files containing isochrones data from all metros of KL, Kuching (provisional), Singapore and Montreal into dataframes
file_all_cities = 'resources/data/all_cities_iso.csv'

#kl, singapore and montreal dataframe
data_all = pd.read_csv(file_all_cities)


st.markdown("""
# Transit Station Pedestrian Accessibility Visualizer \n
[![Star](https://img.shields.io/github/stars/nabilersyad/train-stations-isochrones?style=social)](https://github.com/nabilersyad/train-stations-isochrones)
&nbsp[![Follow](https://img.shields.io/twitter/follow/NabilErsyad?style=social)](https://twitter.com/NabilErsyad)
&nbsp[![Buy me a coffee](https://img.shields.io/badge/Buy%20me%20a%20coffee--yellow.svg?logo=buy-me-a-coffee&logoColor=orange&style=social)](https://www.buymeacoffee.com/nabilersyad)

* **Python libraries:** pandas, streamlit \n
This web application will attempt to visualize the pedestrian accessibility of public transit stations across different cities using isochrone maps \n
Isochrone maps depict the accessible area from a point within a certain time threshold. \n
This application will visualize the isochrone maps according to the following parameters:

1. Walking access within a 5 minute timeframe
2. Walking access within a 10 minute timeframe
3. Walking access within a 15 minute timeframe

Choose your city and stations to be analyzed using the sidebar on the left
""")

#st.image(image, use_column_width=True)

#Sidebar section
######################
# Sidebar
######################
st.sidebar.header('Choose Your Parameters')

# Filter For City
list_city = data_all['City'].unique()
selected_city = st.sidebar.selectbox('City', list_city)

selected_data = data_all[data_all['City']==selected_city]

# Multiselect Filter For Transit Lines
container = st.sidebar.container()
list_routes = selected_data['Route Name'].unique()

all = st.sidebar.checkbox("Select all Stations")

if all:
    selected_routes = container.multiselect("Select one or more options:",
         list_routes,list_routes)

else:
    selected_routes = container.multiselect('Transit Routes', list_routes, list_routes[0])

selected_data = selected_data[(selected_data['Route Name'].isin(selected_routes))]

# Multiselect Filter For Individual Stations, Commented out of current layout to simplify look. Too many stations clutters the look


#list_stations = selected_data['Name'].unique()
#selected_stations= st.sidebar.multiselect('Stations', list_stations, list_stations)

#selected_data = selected_data[(selected_data['Name'].isin(selected_stations))]


st.write("""
***
""")

## Displays Dataframe of Kuala Lumpur's Train Stations


st.header(f'{selected_city} Train Stations Isochrone Data')

if st.sidebar.button('Confirm Selection'):

    #creates maps with isochrones using function from isochrones module
    selected_map = isochrones.isoMapper(selected_data)

    macro = MacroElement()
    macro._template = Template(template)
    macro.add_to(selected_map)
    folium_static(selected_map, width=960, height=600)

    #st.map()

    st.header('Statistical Average Values ')


    ### Print sample mean values
    st.subheader('Area')

    m1, m2, m3, m4, m5= st.columns((1,1,1,1,1))
    
    area_5_minutes_mean =  round(selected_data['5 Minute Range Area'].mean(),3)
    area_10_minutes_mean = round(selected_data['10 Minute Range Area'].mean(),3) 
    area_15_minutes_mean =round(selected_data['15 Minute Range Area'].mean(),3)
    
    m1.write('')
    m2.metric(label ='5 Minute Range Area Average (km^2)',value = area_5_minutes_mean)
    m3.metric(label ='10 Minute Range Area Average (km^2)',value = area_10_minutes_mean)
    m4.metric(label ='10 Minute Range Area Average (km^2)',value = area_15_minutes_mean)
    m5.write('')

    # draws all coverage in one chart along with all train lines
    fig = px.histogram(selected_data
                ,x='Route Name'
                ,y=['5 Minute Range Area','10 Minute Range Area','15 Minute Range Area']
                , barmode = 'group'
                , title="Area coverage within walking times from station"
                , template='plotly'
                , histfunc = 'avg'
                ,labels={'Route Name': "Lines",'value' : "Walk Area Coverage(km^2)"}
                ).update_xaxes(categoryorder='total ascending')

    st.plotly_chart(fig)

    st.dataframe(selected_data)

    #outdated way of implemented download button. Can delete whenever
    #def filedownload(df):
     # csv = df.to_csv(index=False)
      #b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
      #href = f'<a href="data:resources/data;base64,{b64}" download="cities_isochrones.csv">Download CSV File</a>'
      #return href
    #st.markdown(filedownload(selected_data), unsafe_allow_html=True)

    csv = selected_data.to_csv().encode('utf-8')
    st.download_button(
      label="Download data as CSV",
      data=csv,
      file_name=f'{selected_city}_data.csv',
      mime='text/csv'
      )

