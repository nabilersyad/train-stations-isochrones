import folium
import pandas as pd
#helper method to setup any input dataframe into dictionaries that can be input into OSR isochrone methods and folium maps
def dictSetup(dataframe):
    station_dict = dataframe.to_dict(orient='index')
    for name, station in station_dict.items():
        station['locations'] = [station['Longitude'],station['Latitude']]
    return station_dict

#input a Folium Map and Stations dictionary containing ISO data. this will draw the ISO lines on the folium map object
def isoVisualizer(maps,stations, map_icon = 'train'):
    style_function = lambda x: {'color': '#4ef500' if x['properties']['value']<400 else ('#2100f5' if x['properties']['value']<700.0 else '#f50000'),
                                'fillOpacity' : 0.35 if x['properties']['value']<400 else (0.25 if 400.0<x['properties']['value']<700.0 else 0.05),
                                'weight':2,
                                'fillColor' :'#4ef500' if x['properties']['value']<400 else ('#2100f5' if 400.0<x['properties']['value']<700.0 else '#f50000')}
                                                    #('#6234eb' if x['properties']['value']==600.0 else '#6234eb')
    
    for name, station in stations.items():
        station_iso_temp = station['iso']
        station_iso_temp = station_iso_temp.replace("'", '"')
        folium.features.GeoJson(station_iso_temp,style_function = style_function).add_to(maps) # Add GeoJson to map
        if map_icon!="":
            folium.map.Marker(list(reversed(station['locations'])), # reverse coords due to weird folium lat/lon syntax
                                icon=folium.Icon(color='lightgray',
                                            icon_color='#cc0000',
                                            icon=map_icon,
                                            prefix='fa',
                                                ),
                            popup=station['Name'],
                            ).add_to(maps) # Add apartment locations to map
            
    print("Done!")

#Perform isochrone request and generates a new item in the stations dictionary containing isochrone data for that station.
#this will save the isochrones requested from Open Route Service in dictionaries that we created from dictSetup()
def isoGeoJsonRetriever(parameters,stations,client):
    for name, station in stations.items():
        print("Retrieving Isochrone of {} station".format(station['Name']))
        parameters['locations'] = [station['locations']]
        station['iso'] = client.isochrones(**parameters)
        print("Success")
    return

#helper method to create new dictionary that is a subset of the larger list of dictionaries
#used if you want to separate stations by station lines into smaller dictionaries 
def stationSubset(stations,station_list):
    return { your_key: stations[your_key] for your_key in station_list }

#method that use input dataframe coordinates to make API calls to ORS to retrieve isochrones for train stations in the dataframe. Will return isochrone maps of a line and dictionary of stations
def toMap(data,line,params_iso,client):
    # Set up folium map
    if not line in data.values:
        print('{} is not in data frame'.format(line))
        temp = data['Route Name'].unique()
        print('Choose from the following: ')
        print(temp)
        return
    if line != None:
        data = data[data['Route Name']==line]
    starting_location = (data['Latitude'].iloc[0],data['Longitude'].iloc[0])
    mapped = folium.Map(tiles='OpenStreetMap', location=starting_location, zoom_start=11)

    stations = dictSetup(data[data['Route Name']==line])

    isoGeoJsonRetriever(params_iso,stations,client)
    isoVisualizer(mapped,stations)
    return mapped,stations

#Will store full isochrone data in a column. a bit messy but i wasn't sure the alternative to do this
def dictToDataFrame(maps,dataframe):
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
            iso = eval(iso)
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
