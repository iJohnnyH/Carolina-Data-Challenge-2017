import matplotlib.pyplot as mp
import matplotlib.cm
#import datadotworld as dw
import numpy as np
import json
import requests

from mpl_toolkits.basemap import Basemap
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
from matplotlib.colors import Normalize

gMapsAPIKey = 'AIzaSyDCt_yZ6rzR2zNLUdJ8Fb8ChEmBhu8-YE8'
dataset_key = 'https://data.world/justinmmott/nc-voter-registration'
dataset_local = dw.load_dataset(dataset_key)  # cached under ~/.dw/cache
#dataset_local.describe('actual_voter_registration')
results = dw.query('https://data.world/justinmmott/nc-voter-registration', 'SELECT * FROM actual_voter_registration')
print (results.table[1])

fig, ax = mp.subplots(figsize=(20,40))

botlat = 33.8
botlong = -84.3
toplat = 36.545
toplong = -75.4

m = Basemap(resolution = 'i',
           projection = 'tmerc',
           llcrnrlon=botlong, llcrnrlat=botlat, urcrnrlon=toplong, urcrnrlat=toplat,
           lat_0=(botlat+toplat)/2, lon_0=(botlong + toplong)/2)

m.drawmapboundary(fill_color='#46bcec')
m.fillcontinents(color='green',lake_color='#46bcec')
m.drawcoastlines()
#m.readshapefile('cb_2016_us_cd115_500k/cb_2016_us_cd115_500k', 'district')
m.readshapefile('cb_2016_us_county_500k/cb_2016_us_county_500k', 'county')
county_names = []
colors={}

m.readshapefile('cb_2016_us_state_500k/cb_2016_us_state_500k', 'states')
state_names = []
colors={}
for shape_dict in m.states_info:
    statename=shape_dict['NAME']
    if statename in ['South Carolina','Tennessee','Georgia','Virginia']:
        colors[statename]='#ffffff'
    state_names.append(statename)
ax = mp.gca()
for nshape,seg in enumerate(m.states):
    if state_names[nshape] in ['South Carolina','Tennessee','Georgia','Virginia']:
        color = colors[state_names[nshape]]
        poly = Polygon(seg,facecolor=color,edgecolor=color)
        ax.add_patch(poly)







########Onclick
def onclick(event):
    lonpt,latpt = m(event.xdata, event.ydata, inverse=True)
    PARAMS = {'latlng': str(latpt) + ',' + str(lonpt),
              'key': gMapsAPIKey}
    r = requests.get('https://maps.googleapis.com/maps/api/geocode/json', PARAMS)
    data = r.json()
    payload = data['results'][0]
    inNC = False;

    for component in payload['address_components']:
        if ('administrative_area_level_1' in component['types']):
            if (component['short_name'] == 'NC'):
                inNC = True
    if (inNC):
        for component in payload['address_components']:
            if ('administrative_area_level_2' in component['types']):
                county = component['long_name'].replace(' County','')
        for shape_dict in m.county_info:
            countyname=shape_dict['NAME']
            if (countyname == county):
                colors[countyname]='#AAAAAA'
            county_names.append(countyname)
        ax = mp.gca()
        for nshape,seg in enumerate(m.county):
            if (county_names[nshape] == county):
                color = colors[county_names[nshape]] 
                poly = Polygon(seg,facecolor=color,edgecolor=color)
                ax.add_patch(poly)
        print(county)

fig.canvas.mpl_connect('button_press_event', onclick)

mp.plot()
fig, ax = mp.subplots(figsize=(20,40))

m2 = Basemap(resolution = 'i',
           projection = 'tmerc',

           llcrnrlon=-84.3, llcrnrlat=33.8, urcrnrlon=-75.5, urcrnrlat=36.53,
           lat_0=35.165, lon_0=-79.9)
m2.drawmapboundary(fill_color='#46bcec')
m2.fillcontinents(color='green',lake_color='#46bcec')
m2.drawcoastlines()
#m2.drawcounties(linewidth=0.5, linestyle='solid', color='white', antialiased=1, facecolor='none', ax=None, zorder=None, drawbounds=True)
m2.readshapefile('cb_2013_us_cd113_500k/cb_2013_us_cd113_500k', 'district')

m2.readshapefile('cb_2016_us_state_500k/cb_2016_us_state_500k', 'states')
state_names = []
colors={}
for shape_dict in m.states_info:
    statename=shape_dict['NAME']
    if statename in ['South Carolina','Tennessee','Georgia','Virginia']:
        colors[statename]='#ffffff'
    state_names.append(statename)
ax = mp.gca()
for nshape,seg in enumerate(m.states):
    if state_names[nshape] in ['South Carolina','Tennessee','Georgia','Virginia']:
        color = colors[state_names[nshape]]
        poly = Polygon(seg,facecolor=color,edgecolor=color)
        ax.add_patch(poly)
mp.show()
