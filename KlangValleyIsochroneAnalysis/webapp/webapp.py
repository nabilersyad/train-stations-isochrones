## Testing out building a basic webapp for isochrone data

import pandas as pd
import streamlit as st
from PIL import Image
import plotly.express as px


image = Image.open('KlangValleyIsochroneAnalysis/resources/img/DSC09499.JPG')

st.write("""
# Klang Valley Isochrone Analysis

Some charts on isochrone analysis of train stations in KL

***
""")
st.image(image, use_column_width=True)

#Following is an example of an input text box
######################
# Input Text Box
######################
sequence_input = "GAACACGTGGAGGCAAACAGGAAGGTGAAGAAGAACTTATCCTATCAGGACGGAAGGTCCTGTGCTCGGG\nATCTTCCAGACGTCGCGACTCTAAATTGCCCCCTCTGAGGTCAAGGAACACAAGATGGTTTTGGAAATGC\nTGAACCCGATACATTATAACATCACCAGCATCGTGCCTGAAGCCATGCCTGCTGCCACCATGCCAGTCCT"

#sequence = st.sidebar.text_area("Sequence input", sequence_input, height=250)
#sequence = st.text_area("Sequence input", sequence_input, height=250)


st.write("""
***
""")

## Displays Dataframe of Kuala Lumpur's Train Stations
sequence= "GAACACGTGGAGGCAAACAGGAAGGTGAAGAAGAACTTATCCTATCAGGACGGAAGGTCCTGTGCTCGGG"

## Data loaded

file_kl = 'KlangValleyIsochroneAnalysis/resources/data/klang_valley_stations_isochrones_2021-07-29.csv'
data_kl = pd.read_csv(file_kl)
data_kl.drop(columns=data_kl.columns[0],axis=1,inplace=True)

city = 'Kuala Lumpur'
st.header(city + ' Train Stations Isochrone Data')
data_kl

st.header('Mean Values of Selected Columns from the ' +city + ' Dataframe')


### Print sample mean values
st.subheader('Print values')
st.write('5 Minute Range Area Average:  ' + str(round(data_kl['5 Minute Range Area'].mean(),3)) + ' km^2')
st.write('10 Minute Range Area Average:  ' + str(round(data_kl['10 Minute Range Area'].mean(),3)) + ' km^2')
st.write('15 Minute Range Area Average:  ' + str(round(data_kl['15 Minute Range Area'].mean(),3)) + ' km^2')


# draws all coverage in one chart along with all train lines
fig = px.histogram(data_kl
             ,x='Route Name'
             ,y=['5 Minute Range Area','10 Minute Range Area','15 Minute Range Area']
             , barmode = 'group'
             , title="Area coverage within walking times from station"
             , template='plotly'
             , histfunc = 'avg'
             ,labels={'Route Name': "Lines",'value' : "Walk Area Coverage(km^2)"}
            ).update_xaxes(categoryorder='total ascending')

st.write(fig)