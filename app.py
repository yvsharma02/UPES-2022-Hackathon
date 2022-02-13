from flask import Flask, render_template, request
import pickle
import numpy as np
from mpl_toolkits.basemap import Basemap
from flask import Response
import matplotlib.pyplot as plt
import pandas as pd
import requests
import io

filename = 'Earthquake_predictor.pkl'
model = pickle.load(open(filename, 'rb'))

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/home')
def return_home():
    return render_template('index.html')


@app.route('/navigate/', methods=['POST'])
def navigate():
    page = request.form.get("nav_page")
    return render_template(page)


@app.route('/contact/')
def contact():
    return render_template('contact.html')


@app.route('/earthquake')
def earthquake():
    return render_template('earthquake.html')


@app.route('/flood')
def flood():
    return render_template('flood.html')


@app.route('/landslides')
def landslides():
    return render_template('landslides.html')


@app.route('/cyclones')
def cyclone():
    return render_template('cyclones.html')


@app.route('/tsunami')
def tsunami():
    return render_template('tsunami.html')


@app.route('/predict')
def predict():
    return render_template('predict.html', curLat=0, curLong=0)


@app.route('/pred', methods=['GET', 'POST'])
def pred():
    my_prediction = 0
    if request.method == 'POST':
        lat = request.form.get('latitude')
        long = request.form.get('longitude')
        print(lat, long, type(lat), type(long))
        lat = float(lat)
        long = float(long)

        data = np.array([[lat, long]])
        my_prediction = model.predict(data)
        print(my_prediction)
    return render_template('predict.html', _mag=round(my_prediction[0][0], 4), _depth=round(my_prediction[0][1], 4), curLat=lat, curLong=long)


@app.route('/realtimeEQ.png')
def realtimeEQ():
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
    plt.figure(figsize=(14, 10))

    eq_map = Basemap(projection='robin',
                     resolution='l',
                     area_thresh=1000.0,
                     lat_0=0,
                     lon_0=-130)
    eq_map.drawcoastlines()
    eq_map.drawcountries()
    eq_map.fillcontinents(color='gray')
    eq_map.drawmapboundary()
    eq_map.drawmeridians(np.arange(0, 360, 30))
    eq_map.drawparallels(np.arange(-90, 90, 30))

    min_marker_size = 2.5
    for lon, lat, mag in zip(lons, lats, magnitudes):
        x, y = eq_map(lon, lat)
        msize = mag * min_marker_size
        marker_string = get_marker_color(mag)
        eq_map.plot(x, y, marker_string, markersize=msize)

    title_string = "Earthquakes of Magnitude 1.0 or Greater\n"
    title_string += "%s through %s" % (timestrings.iloc[-1][:16],
                                       timestrings.iloc[0][:16])
    plt.title(title_string)

    output = io.BytesIO()
    plt.savefig(output)
    return Response(output.getvalue(), mimetype='image/png')


if __name__ == '__main__':
    app.run(debug=True)
