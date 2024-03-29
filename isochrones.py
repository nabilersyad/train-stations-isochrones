""" Isochrone Analysis Module 

This module contains functions that will help generate isochrone maps 
by making API calls to openrouteservice.org (ORS)

"""

import folium
import pandas as pd
import json

#helper function to setup any input dataframe into dictionaries that can be input into ORS isochrone methods and folium maps
def dictSetup(dataframe):
    """ A function that converts dataframe into dictionaries inputs acceptable to ORS
    Note this function is no longer necessary in latest isochrones.py update
    
    Parameters
    ----------
    dataframe : DataFrame
        A pandas DataFrame object containing Longitude and Latitude columns

    Returns
    -------
    dict 
        A dict object containing key value 'locations'

    Example
    -------
    Will be added later lolz

    """

    station_dict = dataframe.to_dict(orient='index')
    #TODO: try and catch error if input dataframe does not have Longitude and Latitude Columns
    for name, station in station_dict.items():
        try:
            station['locations'] = [station['longitude'], station['latitude']]
        except KeyError:
            raise KeyError("Input dataframe must contain 'longitude' and 'latitude' columns")
    return station_dict

# #input a Folium Map and Stations dictionary containing ISO data. this will draw the ISO lines on the folium map object
# def isoVisualizer(maps,stations, map_icon = ""):
#     style_function = lambda x: {'color': '#4ef500' if x['properties']['value']<400 else ('#2100f5' if x['properties']['value']<700.0 else '#f50000'),
#                                 'fillOpacity' : 0.35 if x['properties']['value']<400 else (0.25 if 400.0<x['properties']['value']<700.0 else 0.05),
#                                 'weight':2,
#                                 'fillColor' :'#4ef500' if x['properties']['value']<400 else ('#2100f5' if 400.0<x['properties']['value']<700.0 else '#f50000')}
#                                                     #('#6234eb' if x['properties']['value']==600.0 else '#6234eb')
    
#     for name, station in stations.items():
#         station_iso_temp = station['iso']
#         if type(station_iso_temp) == str:
#             station_iso_temp = station_iso_temp.replace("'", '"')
#         folium.features.GeoJson(station_iso_temp,style_function = style_function).add_to(maps) # Add GeoJson to map
#         if map_icon!="":
#             folium.map.Marker(list(reversed(station['locations'])), # reverse coords due to weird folium lat/lon syntax
#                                 icon=folium.Icon(color='lightgray',
#                                             icon_color='#cc0000',
#                                             icon=map_icon,
#                                             prefix='fa',
#                                                 ),
#                             popup=station['Name'],
#                             ).add_to(maps) # Add apartment locations to map      
#     print("Done!")

# #input a Folium Map and Stations dictionary containing ISO data. this will draw the ISO lines on the folium map object
def isoVisualizer(maps,stations, map_icon = "", icon_color= '#cc0000'):
    """ Draws isochrones on folium map

        Parameters
        ----------
        maps: Map
            A Folium Map object 
        stations: DataFrame
            A Pandas DataFrame containing 'iso' column that contains isochrone data in JSON format acquired from ORS
        map_icon: str
            Icon to mark centre of isochrone maps. Refer to https://fontawesome.com/v4.7/icons/ for list of possible icons


        Example
        -------
        Will be added later lolz

    """
    #TODO allow more custom style functions
    #TODO check for input errors
    style_function = lambda x: {'color': '#4ef500' if x['properties']['value']<400 else ('#2100f5' if x['properties']['value']<700.0 else '#f50000'),
                                'fillOpacity' : 0.35 if x['properties']['value']<400 else (0.25 if 400.0<x['properties']['value']<700.0 else 0.05),
                                'weight':2,
                                'fillColor' :'#4ef500' if x['properties']['value']<400 else ('#2100f5' if 400.0<x['properties']['value']<700.0 else '#f50000')}
                                                    #('#6234eb' if x['properties']['value']==600.0 else '#6234eb')

    #necessary to create 'locations' column to know specific coordinates for marking
    stations['locations']  = stations.apply(lambda row: list([row.loc["longitude"],row.loc["latitude"]]) , axis = 1)
    
    for index, row in stations.iterrows():
        folium.features.GeoJson(row['iso'],style_function = style_function).add_to(maps) # Add GeoJson to map
        if map_icon!="":
            if row['colour_hex_code']!='':
                station_color = row['colour_hex_code']
            else:
                station_color =icon_color
            folium.map.Marker(list(reversed(row['locations'])), # reverse coords due to weird folium lat/lon syntax
                                icon=folium.Icon(color='lightgray',
                                            icon_color=station_color,
                                            icon=map_icon,
                                            prefix='fa',
                                                ),
                            popup=row['name'],
                            ).add_to(maps) # Add apartment locations to map      
    print("Done!")

#Perform isochrone request and generates a new item in the stations dictionary containing isochrone data for that station.
#this will save the isochrones requested from Open Route Service in dictionaries that we created from dictSetup()
# def isoGeoJsonRetriever(parameters,stations,client):
#     for name, station in stations.items():
#         print("Retrieving Isochrone of {} station".format(station['Name']))
#         parameters['locations'] = [station['locations']]
#         temp_iso = client.isochrones(**parameters)
#         station['iso'] = json.dumps(temp_iso)
#         print("Success")
#     return

#Perform isochrone request and generates a new column in the stations dataframe containing isochrone data for that station.
#this will save the isochrones requested from Open Route Service(ORS)
#ORS will return the isochrones in geoJSON format
def isoGeoJsonRetriever(parameters,stations,client):

    #ORS isochrones API takes input list of coordinates in field called location. This line creates that column
    stations['locations']  = stations.apply(lambda row: list([row.loc["longitude"],row.loc["latitude"]]) , axis = 1)
    iso_list = []

    for index, row in stations.iterrows():
        print("Retrieving Isochrone of {} station".format(stations.loc[index,'name']))
        parameters['locations'] = [row.loc['locations']]
    
        try:
            temp_iso = client.isochrones(**parameters)
            temp_iso = json.dumps(temp_iso)
            iso_list.append(temp_iso)
            print("Success")
        except Exception as e:
            print(f"Failed to retrieve isochrone for station {stations.loc[index,'name']}: {e}")
            iso_list.append(None)  # or some other default value
    
    stations['iso'] = iso_list

    return

#helper method to create new dictionary that is a subset of the larger list of dictionaries
#used if you want to separate stations by station lines into smaller dictionaries 
def stationSubset(stations,station_list):
    return { your_key: stations[your_key] for your_key in station_list }

# #method that uses input dataframe coordinates to make API calls to ORS to retrieve isochrones for train stations in the dataframe. Will return isochrone maps of a line and dictionary of stations
# def toMapORS(data,line,params_iso,client):
#     # Set up folium map
#     if not line in data.values:
#         print('{} is not in data frame'.format(line))
#         temp = data['Route Name'].unique()
#         print('Choose from the following: ')
#         print(temp)
#         return
#     if line != None:
#         data = data[data['Route Name']==line]
#     starting_location = (data['Latitude'].iloc[0],data['Longitude'].iloc[0])
#     mapped = folium.Map(tiles='OpenStreetMap', location=starting_location, zoom_start=11)

#     stations = dictSetup(data[data['Route Name']==line])

#     isoGeoJsonRetriever(params_iso,stations,client)
#     isoVisualizer(mapped,stations)
#     return mapped,stations

def toMapORS(data,line,params_iso,client):
    # Set up folium map
    if not line in data.values:
        print('{} is not in data frame'.format(line))
        temp = data['route_name'].unique()
        print('Choose from the following: ')
        print(temp)
        return
    if line != None:
        data = data[data['route_name']==line]
    starting_location = (data['latitude'].iloc[0],data['longitude'].iloc[0])
    mapped = folium.Map(tiles='OpenStreetMap', location=starting_location, zoom_start=11)

    isoGeoJsonRetriever(params_iso,data,client)
    isoVisualizer(mapped,data)
    return mapped,data

# #method that uses input dataframe with iso. Returns Map of isochrones.
# def isoMapper(data,icon = 'train'):
#     ## Set up folium map
#     starting_location = (data['Latitude'].iloc[0],data['Longitude'].iloc[0])
#     mapped = folium.Map(tiles='OpenStreetMap', location=starting_location, zoom_start=13)

#     ##Add legend to Map
#     #colormap = linear.RdYlBu_08.scale(station_stats[field_to_color_by].quantile(0.05),
#                                      # station_stats[field_to_color_by].quantile(0.95))

#     #converts Dataframe to Dictionary, necessary for the subsequent functions
#     stations = dictSetup(data)
#     isoVisualizer(mapped,stations,icon)

#     return mapped

#method that uses input dataframe with iso. Returns Map of isochrones.
def isoMapper(data,icon = 'train'):
    ## Set up folium map
    starting_location = (data['latitude'].iloc[0],data['longitude'].iloc[0])
    mapped = folium.Map(tiles='OpenStreetMap', location=starting_location, zoom_start=13)

    ##Add legend to Map
    #colormap = linear.RdYlBu_08.scale(station_stats[field_to_color_by].quantile(0.05),
                                     # station_stats[field_to_color_by].quantile(0.95))

    isoVisualizer(mapped,data,icon)

    return mapped

#Will store full isochrone data in a column. a bit messy but i wasn't sure the alternative to do this
def dictToDataFrame(maps,dataframe):
    #initializing a column 'isochrones' for the dataframe
    iso_df = pd.DataFrame(columns= list(pd.DataFrame.from_dict(maps[0][1]).T)) 
    for i in range(len(maps)):
        temp = pd.DataFrame.from_dict(maps[i][1]).T
        iso_df = iso_df.append(temp)
    dataframe['iso']=iso_df['iso']     
    return dataframe


# taking dataframe that now has the ISO, to parse isochrone data into dataframe columns containing relevant info such as walking coverage, population etc
def areaToDataframe(data):
    m2_to_km2 =1000000
    for station in data.index:
        iso = data.loc[station]['iso']
        if isinstance(iso, str):
            iso = json.loads(iso)
            area1 =  iso['features'][0]['properties']['area']/m2_to_km2 #area in iso is in m^2 Divide by 1000000 to get km^2
            area2 = (iso['features'][1]['properties']['area'])/m2_to_km2  #area in iso is in m^2 Divide by 1000000 to get km^2
            area3 = (iso['features'][2]['properties']['area'])/m2_to_km2 
            reach1 = (iso['features'][0]['properties']['reachfactor'])  
            reach2 = (iso['features'][1]['properties']['reachfactor']) 
            reach3 = (iso['features'][2]['properties']['reachfactor']) 
            pop1 = (iso['features'][0]['properties']['total_pop']) 
            pop2 = (iso['features'][1]['properties']['total_pop']) 
            pop3 = (iso['features'][2]['properties']['total_pop'])
        #for some reason errors keep popping out indicating key when trying to directly assign values to the data frame. so had to create separate variables and 
        # then assigning outside of if statement  
        elif isinstance(iso, dict):
            area1 =  iso['features'][0]['properties']['area']/m2_to_km2 #area in iso is in m^2 Divide by 1000000 to get km^2
            area2 = (iso['features'][1]['properties']['area'])/m2_to_km2  #area in iso is in m^2 Divide by 1000000 to get km^2
            area3 = (iso['features'][2]['properties']['area'])/m2_to_km2 
            reach1 = (iso['features'][0]['properties']['reachfactor'])  
            reach2 = (iso['features'][1]['properties']['reachfactor']) 
            reach3 = (iso['features'][2]['properties']['reachfactor']) 
            pop1 = (iso['features'][0]['properties']['total_pop']) 
            pop2 = (iso['features'][1]['properties']['total_pop']) 
            pop3 = (iso['features'][2]['properties']['total_pop'])
        #iso properties key ['group_index', 'value', 'center', 'area', 'reachfactor', 'total_pop']
        data.loc[station,'5 Minute Range Area'] = area1
        data.loc[station,'10 Minute Range Area'] = area2
        data.loc[station,'15 Minute Range Area'] = area3
        data.loc[station,'5 Minute Reach Factor'] = reach1
        data.loc[station,'10 Minute Reach Factor'] = reach2
        data.loc[station,'15 Minute Reach Factor'] = reach3
        data.loc[station,'5 Minute Population'] = pop1
        data.loc[station,'10 Minute Population'] = pop2
        data.loc[station,'15 Minute Population'] = pop3
    return data
