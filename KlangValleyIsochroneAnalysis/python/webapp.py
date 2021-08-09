## Testing out building a basic webapp for isochrone data
import pandas as pd
import streamlit as st
from PIL import Image
import plotly.express as px
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import isochrones

###Load Relevant Data###

##Loads image for 
image = Image.open('../resources/img/DSC09499.JPG')

# Calling csv files containing isochrones data from all metros of KL, Singapore and Montreal into dataframes
file_all_cities = '../resources/data/all_cities_iso.csv'

#kl, singapore and montreal dataframe
data_all = pd.read_csv(file_all_cities)


st.markdown("""
# Klang Valley Isochrone Analysis
* **Python libraries:** base64, pandas, streamlit \n
Some charts on isochrone analysis of train stations in KL

***
""")

st.image(image, use_column_width=True)

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


st.header(selected_city + ' Train Stations Isochrone Data')

if st.sidebar.button('Confirm Selection'):
    
    st.dataframe(selected_data)

    st.header('Mean Values of Selected Columns from the ' +selected_city + ' Dataframe')


    ### Print sample mean values
    st.subheader('Print values')
    st.write('5 Minute Range Area Average:  ' + str(round(selected_data['5 Minute Range Area'].mean(),3)) + ' km^2')
    st.write('10 Minute Range Area Average:  ' + str(round(selected_data['10 Minute Range Area'].mean(),3)) + ' km^2')
    st.write('15 Minute Range Area Average:  ' + str(round(selected_data['15 Minute Range Area'].mean(),3)) + ' km^2')


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

    st.write(fig)