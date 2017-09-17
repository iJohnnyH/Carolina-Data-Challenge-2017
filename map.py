import matplotlib.pyplot as mp
import matplotlib.cm
#import datadotworld as dw
import numpy as np
import json
import requests
import csv

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

county_stuff = {}
district = {}
rep = [0,0,0,0,0,0,0,0,0,0,0,0,0,0]
dem = [0,0,0,0,0,0,0,0,0,0,0,0,0,0]
county_stuffog = {}
county_stuffrn = {}
reploss = 0 
demloss = 0
total = 0
disW = [False,False,False,False,False,False,False,False,False,False,False,False,False,False]
for i in range (1,14):
    district[i] = set();
visited = {}

with open('By_The_Numbers.csv', mode ='r') as w:
    reader = csv.DictReader(w)
    for row in reader: 
        if row['county'] == 'Mcdowell':
            county_stuff['McDowell'] = [int(row['rep']) , int(row['dem'])]
            total = total + int(row['rep']) + int(row['dem'])
            if (int(row['rep']) > int(row['dem'])):
                county_stuffog['McDowell'] = True
            elif (int(row['rep']) < int(row['dem'])):  
                county_stuffog['McDowell'] = False  
        else:
            county_stuff[row['county']] = [int(row['rep']) , int(row['dem'])]
            total = total + int(row['rep']) + int(row['dem'])
            if (int(row['rep']) > int(row['dem'])):
                county_stuffog[row['county']] = True
            elif (int(row['rep']) < int(row['dem'])):  
                county_stuffog[row['county']] = False  
#Class created for previous and next buttons for districts
"""z
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
visited1 = 0


########Onclick
def onclick(event):
    winR = 0
    winD = 0
    reploss = 0
    demloss = 0
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
                    if county in visited.keys():
                        visited1 = visited[county]
                        district[visited1].remove(county)
                    else:
                        visited[county] = c
                    district[c].add(county)

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
            
    elif event.button==2:
        for i in range(1,14):
            for x in district[i]:
                if(x == 'McDowell'):
                    rep[i] = rep[i] + 9069
                    dem[i] = dem[i] + 6438
                else:
                    rep[i] = rep[i] + int(county_stuff[x][0])
                    dem[i] =  dem[i] + int(county_stuff[x][1])


            if (rep[i] > dem[i]):
                reploss = reploss + (rep[i] - dem[i])
                disW[i] = True
                demloss = demloss + dem[i]
            elif (rep[i] < dem[i]):
                demloss = demloss + (dem[i] - rep[i])
                reploss = rep[i]

        e = (reploss - demloss)/total    
        m4 = Basemap(resolution = 'i',
           projection = 'tmerc',

           llcrnrlon=-84.3, llcrnrlat=33.8, urcrnrlon=-75.5, urcrnrlat=36.53,
           lat_0=35.165, lon_0=-79.9)
        m4.drawmapboundary(fill_color='#46bcec')
        m4.fillcontinents(color='green',lake_color='#46bcec')
        m4.drawcoastlines()
        #m2.drawcounties(linewidth=0.5, linestyle='solid', color='white', antialiased=1, facecolor='none', ax=None, zorder=None, drawbounds=True)
        m4.readshapefile('cb_2016_us_county_500k/cb_2016_us_county_500k', 'county')
        
        m4.readshapefile('cb_2016_us_state_500k/cb_2016_us_state_500k', 'states')
        statenumbers1=[]
        county_names1 = []
        colors1 = {}
        for x in district.keys():   
            for countyasdf in county_stuffog.keys():
                if(countyasdf in district[x]):
                    for shape_dict in m.county_info:
                        countyname1=shape_dict['NAME']
                        statenumber1=shape_dict['STATEFP']
                        if (countyname1 == countyasdf) and (statenumber1=="37"):
                            if(county_stuffog[countyname1]):
                                if disW[int(x)]:
                                    colors1[countyasdf] = 'red'
                                else:
                                    colors1[countyasdf] = 'blue'
                            else:
                                if disW[int(x)]:
                                    colors1[countyasdf] = 'red'
                                else:
                                    colors1[countyasdf] = 'blue'
                        county_names1.append(countyname1)
                        statenumbers1.append(statenumber1)
                    ax = mp.gca()
                    for nshape,seg in enumerate(m.county):
                        if (county_names1[nshape] == countyasdf) and (statenumbers1[nshape]=="37"):
                            color = colors1[countyasdf] 
                            poly = Polygon(seg,facecolor=color,edgecolor=color)
                            ax.add_patch(poly)

        for shape_dict in m.states_info:
            statename=shape_dict['NAME']
            if statename in ['South Carolina','Tennessee','Georgia','Virginia']:
                colors[statename]='#ffffff'
            state_names.append(statename)
        ax = mp.gca()
        for i in range(1,14):
            if(disW[i]):
                winR = winR +1
            else:
                winD = winD +1 
        for txt in text.texts:
            txt.set_visible(False)
        text2= ax
        for txt in ax.texts:
            txt.set_visible(False) 
        textvar2 = ax.text(1000, 0, "E "+str(round(e,3))+ "\nRep " + str(winR) + "\nDem " + str(winD), fontsize=30)
        for nshape,seg in enumerate(m.states):
            if state_names[nshape] in ['South Carolina','Tennessee','Georgia','Virginia']:
                color = colors[state_names[nshape]]
                poly = Polygon(seg,facecolor=color,edgecolor=color)
                ax.add_patch(poly)   
                mp.gcf().canvas.draw_idle()
    elif event.button==3:
        c=c+1
        if (c==14):
            c=1
        for txt in text.texts:
            txt.set_visible(False)    
        textvar = text.text(0, 0, c, fontsize=38)
        mp.draw()
fig.canvas.mpl_connect('button_press_event', onclick)
mp.title("Redistricting NC Counties")
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
district_nums = []
district_codes = []
district_colors=['#0000e6','#6600cc','#00ff00','#ff3300','#997a00','#663300','#006666','#cccccc','#4d0000','#ffcc99','#33331a','#d98c8c','#33ffcc']
colors={}
for district_dict in m2.district_info:
    districtnum=district_dict['STATEFP']
    districtcode=int(district_dict['CD113FP'])
    if (districtnum == '37') and (districtcode <= 13):
        colors[districtnum]=district_colors[districtcode-1]
    district_nums.append(districtnum)
    district_codes.append(districtcode)
ax = mp.gca()
for nshape,seg in enumerate(m2.district):
    if (district_nums[nshape] =='37') and (int(district_codes[nshape]) <= 13):
        color = district_colors[int(district_codes[nshape])-1]
        poly = Polygon(seg,facecolor=color,edgecolor=color)
        ax.add_patch(poly)

m2.readshapefile('cb_2016_us_state_500k/cb_2016_us_state_500k', 'states')
state_names = []
colors={}
for shape_dict in m2.states_info:
    statename=shape_dict['NAME']
    if statename in ['South Carolina','Tennessee','Georgia','Virginia']:
        colors[statename]='#ffffff'
    state_names.append(statename)
ax = mp.gca()
for nshape,seg in enumerate(m2.states):
    if state_names[nshape] in ['South Carolina','Tennessee','Georgia','Virginia']:
        color = colors[state_names[nshape]]
        poly = Polygon(seg,facecolor=color,edgecolor=color)
        ax.add_patch(poly)
mp.title("2013 District Map")
mp.plot()

fig, ax = mp.subplots(figsize=(20,40))

###################################

m3 = Basemap(resolution = 'i',
           projection = 'tmerc',

           llcrnrlon=-84.3, llcrnrlat=33.8, urcrnrlon=-75.5, urcrnrlat=36.53,
           lat_0=35.165, lon_0=-79.9)
m3.drawmapboundary(fill_color='#46bcec')
m3.fillcontinents(color='green',lake_color='#46bcec')
m3.drawcoastlines()
#m2.drawcounties(linewidth=0.5, linestyle='solid', color='white', antialiased=1, facecolor='none', ax=None, zorder=None, drawbounds=True)
m3.readshapefile('cb_2016_us_county_500k/cb_2016_us_county_500k', 'county')

m3.readshapefile('cb_2016_us_state_500k/cb_2016_us_state_500k', 'states')
statenumbers1=[]
county_names1 = []
colors1 = {}

for countyasdf in county_stuffog.keys():
    for shape_dict in m.county_info:
        countyname1=shape_dict['NAME']
        statenumber1=shape_dict['STATEFP']
        if (countyname1 == countyasdf) and (statenumber1=="37"):
            if(county_stuffog[countyname1]):
                colors1[countyasdf]= 'red'
            else:
                colors1[countyasdf]= 'blue'
        county_names1.append(countyname1)
        statenumbers1.append(statenumber1)
    ax = mp.gca()
    for nshape,seg in enumerate(m3.county):
        if (county_names1[nshape] == countyasdf) and (statenumbers1[nshape]=="37"):
            color = colors1[countyasdf] 
            poly = Polygon(seg,facecolor=color,edgecolor=color)
            ax.add_patch(poly)
for shape_dict in m.county_info:
    countyname=shape_dict['NAME']
    if countyname in ['McDowell']:
        colors[countyname]='red'
    county_names.append(countyname)
ax = mp.gca()
for nshape,seg in enumerate(m.county):
    if county_names[nshape] in ['McDowell']:
        color = colors[county_names[nshape]] 
        poly = Polygon(seg,facecolor=color,edgecolor=color)
        ax.add_patch(poly)

for shape_dict in m3.states_info:
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
mp.title("NC Counties by Majority Party")
mp.show()



