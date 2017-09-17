import matplotlib.pyplot as mp
import matplotlib.cm
#import datadotworld as dw
import numpy as np
import json
import requests

from matplotlib.widgets import Button
from mpl_toolkits.basemap import Basemap
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
from matplotlib.colors import Normalize
from pynput import keyboard

gMapsAPIKey = 'AIzaSyDCt_yZ6rzR2zNLUdJ8Fb8ChEmBhu8-YE8'
#dataset_key = 'https://data.world/justinmmott/nc-voter-registration'
#dataset_local = dw.load_dataset(dataset_key,force_update=True)  # cached under ~/.dw/cache
#dataset_local.describe('by_the_numbers')
#county_names = dw.query('https://data.world/justinmmott/nc-voter-registration', 'SELECT county FROM by_the_numbers')


#Class created for previous and next buttons for districts
"""
class Index(object):
    ind = 1
    def next(self, event):
        self.ind += 1
        if (self.ind > 13):
            self.ind = 1
        for txt in text.texts:
            txt.set_visible(False)
        textvar = text.text(0, 0, self.ind, fontsize=28)
        #plt.draw()
        print (self.ind)
    def prev(self, event):
        self.ind -= 1
        if (self.ind < 1):
            self.ind = 13
        for txt in text.texts:
            txt.set_visible(False)
        textvar = text.text(0, 0, self.ind, fontsize=28)
        #plt.draw()
        print (self.ind)
"""

#Sets plot size
fig, ax = mp.subplots(figsize=(20,40))

botlat = 33.8
botlong = -84.3
toplat = 36.545
toplong = -75.4
#Creates map
m = Basemap(resolution = 'i',
           projection = 'tmerc',
           llcrnrlon=botlong, llcrnrlat=botlat, urcrnrlon=toplong, urcrnrlat=toplat,
           lat_0=(botlat+toplat)/2, lon_0=(botlong + toplong)/2)
#Draws lines for map
m.drawmapboundary(fill_color='#46bcec')
m.fillcontinents(color='green',lake_color='#46bcec')
m.drawcoastlines()
#m.readshapefile('cb_2016_us_cd115_500k/cb_2016_us_cd115_500k', 'district')
m.readshapefile('cb_2016_us_county_500k/cb_2016_us_county_500k', 'county')
county_names = []
colors={}

#Finds state lines and colors other states
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

"""
callback = Index()
axprev = mp.axes([0.5, 0.05, 0.2, 0.075])
axnext = mp.axes([0.75, 0.05, 0.2, 0.075])
text = mp.axes([0.0, 0.05, 0.0, 0.075])


text.axis('off')
bnext = Button(axnext, 'Next district')
bnext.on_clicked(callback.next)
bprev = Button(axprev, 'Previous district')
bprev.on_clicked(callback.prev)
"""
text= ax
textvar = text.text(0, 0, 1, fontsize=38)
c=1
########Onclick
def onclick(event):
    if event.button==1:
        global c,district_colors
        district_colors=['#0000e6','#6600cc','#00ff00','#ff3300','#997a00','#663300','#006666','#cccccc','#4d0000','#ffcc99','#33331a','#d98c8c','#33ffcc']
        lonpt,latpt = m(event.xdata, event.ydata, inverse=True)
        PARAMS = {'latlng': str(latpt) + ',' + str(lonpt),
                  'key': gMapsAPIKey}
        r = requests.get('https://maps.googleapis.com/maps/api/geocode/json', PARAMS)
        data = r.json()
        payload = data['results'][0]
        inNC = False;
        statenumbers=[]
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
                statenumber=shape_dict['STATEFP']
                if (countyname == county) and (statenumber=="37"):
                    colors[countyname]=district_colors[c-1]
                county_names.append(countyname)
                statenumbers.append(statenumber)
            ax = mp.gca()
            for nshape,seg in enumerate(m.county):
                if (county_names[nshape] == county) and (statenumbers[nshape]=="37"):
                    color = colors[county_names[nshape]] 
                    poly = Polygon(seg,facecolor=color,edgecolor=color)
                    ax.add_patch(poly)
                    mp.gcf().canvas.draw_idle()
            print(county)
    elif event.button==2:
        c=c-1
        if (c==0):
            c=13
        for txt in text.texts:
            txt.set_visible(False)    
        textvar = text.text(0, 0, c, fontsize=38)
        mp.draw()        
    elif event.button==3:
        c=c+1
        if (c==14):
            c=1
        for txt in text.texts:
            txt.set_visible(False)    
        textvar = text.text(0, 0, c, fontsize=38)
        mp.draw()
fig.canvas.mpl_connect('button_press_event', onclick)



mp.plot()
    



#########PLOT 2##############

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



