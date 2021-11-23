#Run this whenever i need to compile all the city files
import pandas as pd
from datetime import date

# Calling csv files containing isochrones data from all metros of KL, Singapore and Montreal into dataframes

file_kl = 'resources/data/klang_valley_stations_isochrones.csv'
file_sg = 'resources/data/mrtsg_isochrones.csv'
file_mtl = 'resources/data/montreal_metro_isochrones.csv'
file_kuching = 'resources/data/kuching_provisional_stations_isochrones.csv'

#each city are assigned a separate unique dataframe
data_kl = pd.read_csv(file_kl)
data_sg = pd.read_csv(file_sg)
data_mtl = pd.read_csv(file_mtl)
data_kuching = pd.read_csv(file_kuching)


#we don't actually need every column for the overall dataframe. so we will select a few relevant columns
columns = ['Name','Route Name','Latitude','Longitude','Line Colour',
            '5 Minute Range Area', '10 Minute Range Area','15 Minute Range Area', 
            '5 Minute Reach Factor','10 Minute Reach Factor', '15 Minute Reach Factor',
            '5 Minute Population', '10 Minute Population', '15 Minute Population','City','iso']



#combining the kl, singapore and montreal dataframes
data_all = pd.concat([data_kl[columns],data_sg[columns],data_mtl[columns],data_kuching[columns]])

file_url ='resources/data/all_cities_iso_' + str(date.today())+ '.csv'
data_all.to_csv(file_url,index=False)