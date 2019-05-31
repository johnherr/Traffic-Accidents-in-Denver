import numpy as np
import pandas as pd
import datetime
import folium
from folium.plugins import HeatMap

df = pd.read_pickle('data/pickled_df')
df = df.dropna()

denver_map = folium.Map(location=[39.73782,-104.971338],
                        zoom_start=13,
                        tiles="Cartodbpositron")


#Heat_map
heat_map = folium.FeatureGroup(name = 'heat_map')
max_amount = float(60)
heat_map.add_child( HeatMap( list(zip(df['GEO_LAT'].values, df['GEO_LON'].values)), 
                   min_opacity=0.2,
                   max_val=max_amount,
                   radius=5.5, blur=3.5, 
                   max_zoom=1, 
                 ))
denver_map.add_child(heat_map)


def map_plotter(df, feature_map, color):
    for index, row in df.iterrows():
        folium.CircleMarker(location=(row['GEO_LAT'], row['GEO_LON']),
                                    radius=.75,
                                    color=color,
                                    popup=str('Fatalities: ' + str(row['FATALITIES']) \
                                              + '\nDate: ' + row['DATE'].strftime('%x') \
                                              + '\nTime: '+ row['DATE'].strftime('%X') \
                                              + '\nDriver was: ' + str(row['TU1_DRIVER_HUMANCONTRIBFACTOR'])
                                             ),
                                    fill=True).add_to(feature_map)

#Add bicycle layer 
bike_map = folium.FeatureGroup(name = 'bike_map')
bike_df = df[df['BICYCLE_IND'] > 0]
map_plotter(bike_df, bike_map, "#e32522") #red dots
denver_map.add_child(bike_map)

#Add DUI layer 
dui_map = folium.FeatureGroup(name = 'dui_map')
dui_df = df[df['TU1_DRIVER_HUMANCONTRIBFACTOR'] == 'DUI/DWAI/DUID']
map_plotter(dui_df, dui_map, '#e38f22') #orange dots
denver_map.add_child(dui_map)

#Add bicycle layer 
fatalities_map = folium.FeatureGroup(name = 'fatalities_map')
fatalities_df = df[df['FATALITIES'] > 0]
map_plotter(fatalities_df, fatalities_map, "#7612ce") #purple dots
denver_map.add_child(fatalities_map)


folium.LayerControl().add_to(denver_map) #Add layer control to toggle on/off
denver_map.save('folium_heat.html')