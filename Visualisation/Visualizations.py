from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import numpy as np
import pandas as pd
import requests


url = 'http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/1.0_week.csv'
r = requests.get(url, allow_redirects=True)

open('earthquake_data.csv', 'wb').write(r.content)
# Open the earthquake data file.
filename = 'earthquake_data.csv'

data = pd.read_csv(filename)
data = data[["latitude", "longitude", "depth", "mag", "time"]]

lats = data["latitude"]
lons = data["longitude"]
magnitudes = data["mag"]
timestrings = data["time"]


def get_marker_color(magnitude):
    # Returns green for small earthquakes, yellow for moderate
    #  earthquakes, and red for significant earthquakes.
    if magnitude < 3.0:
        return ('go')
    elif magnitude < 5.0:
        return ('yo')
    else:
        return ('ro')

# Make this plot larger.
fig = plt.figure(figsize=(16,12))

eq_map = Basemap(projection='robin', resolution = 'l', area_thresh = 1000.0,
              lat_0=0, lon_0=-130)
eq_map.drawcoastlines()
eq_map.drawcountries()
eq_map.fillcontinents(color = 'gray')
eq_map.drawmapboundary()
eq_map.drawmeridians(np.arange(0, 360, 30))
eq_map.drawparallels(np.arange(-90, 90, 30))
 

min_marker_size = 2.5
for lon, lat, mag in zip(lons, lats, magnitudes):
    x,y = eq_map(lon, lat)
    msize = mag * min_marker_size
    marker_string = get_marker_color(mag)
    eq_map.plot(x, y, marker_string, markersize=msize)
    
title_string = "Earthquakes of Magnitude 1.0 or Greater\n"
title_string += "%s through %s" % (timestrings.iloc[-1][:16], timestrings.iloc[0][:16])

plt.title(title_string)
plt.savefig("figure.png")



