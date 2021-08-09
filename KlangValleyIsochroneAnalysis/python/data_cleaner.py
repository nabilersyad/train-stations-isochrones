#Run this whenever i need to compile all the city files
import pandas as pd

# Calling csv files containing isochrones data from all metros of KL, Singapore and Montreal into dataframes

file_kl = '../resources/data/klang_valley_stations_isochrones_2021-07-29.csv'
file_sg = '../resources/data/mrtsg_iso.csv'
file_mtl = '../resources/data/montreal_metro_iso.csv'

#each city are assigned a separate unique dataframe
data_kl = pd.read_csv(file_kl)
data_sg = pd.read_csv(file_sg)
data_mtl = pd.read_csv(file_mtl)

#we don't actually need every column for the overall dataframe. so we will select a few relevant columns
columns = ['Name','Route Name','Latitude','Longitude','Line Colour',
            '5 Minute Range Area', '10 Minute Range Area','15 Minute Range Area', 
            '5 Minute Reach Factor','10 Minute Reach Factor', '15 Minute Reach Factor',
            '5 Minute Population', '10 Minute Population', '15 Minute Population','City']



#combining the kl, singapore and montreal dataframes
data_all = pd.concat([data_kl[columns],data_sg[columns],data_mtl[columns]])

file_url ='../resources/data/all_cities_iso.csv'
data_all.to_csv(file_url,index_label=False)