#Run this whenever i need to compile all the city files
import pandas as pd
from datetime import date
import os

# Constants
data_folder = 'resources/data'
file_kl = 'klang_valley_stations_isochrones.csv'
file_sg = 'mrtsg_isochrones.csv'
file_mtl = 'montreal_metro_isochrones.csv'
#file_kuching = 'uching_provisional_stations_isochrones.csv'

#we don't actually need every column for the overall dataframe. so we will select a few relevant columns
iso_col = [
    'Name', 'Route Name', 'Latitude', 'Longitude', 'Line Colour',
    '5 Minute Range Area', '10 Minute Range Area', '15 Minute Range Area', 
    '5 Minute Reach Factor', '10 Minute Reach Factor', '15 Minute Reach Factor',
    '5 Minute Population', '10 Minute Population', '15 Minute Population',
    'City', 'Colour Hex Code', 'iso'
]


# Calling csv files containing isochrones data from all metros of KL, Singapore and Montreal into dataframes
# Function to read data
def read_data(file_name):
    """Reads a CSV file into a DataFrame, selecting only the columns of interest."""
    file_path = os.path.join(data_folder, file_name)
    try:
        data = pd.read_csv(file_path)
        return data[iso_col]
    except FileNotFoundError:
        print(f"File {file_name} not found.")
        return pd.DataFrame(columns=iso_col)  # Return an empty DataFrame with the right columns

# Main script
if __name__ == "__main__":
    #each city are assigned a separate unique dataframe
    data_kl = read_data(file_kl)
    data_sg = read_data(file_sg)
    data_mtl = read_data(file_mtl)
    #data_kuching = read_data(file_kuching)

    # Combine data
    data_all = pd.concat([data_kl, data_sg, data_mtl])
    all_cities_folder = 'all_cities'
    # Write data to all_cities_iso with date
    file_url = os.path.join(data_folder,all_cities_folder, 'all_cities_iso_' + str(date.today()) + '.csv')
    data_all.to_csv(file_url, index=False)

    # Write data to all_cities_iso for regular use
    file_url = os.path.join(data_folder, 'all_cities_iso' + '.csv')
    data_all.to_csv(file_url, index=False)