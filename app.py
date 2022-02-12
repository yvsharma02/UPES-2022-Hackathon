from crypt import methods
from flask import Flask, render_template, request
import pickle
import numpy as np

# my_prediction = 0

filename = 'Earthquake_predictor.pkl'
model = pickle.load(open(filename, 'rb'))

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/navigate/', methods=['POST'])
def navigate():
    page = request.form.get("nav_page")
    return render_template(page)

@app.route('/templates/contact.html')
def contact():
    return render_template('contact.html')

@app.route('/templates/earthquake.html')
def earthquake():
    return render_template('earthquake.html')

@app.route('/templates/flood.html')
def flood():
    return render_template('flood.html')

@app.route('/templates/landslides.html')
def landslides():
    return render_template('landslides.html')

@app.route('/templates/predict.html', methods=['GET', 'POST'])
def predict():
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
        # return render_template('predict.html', prediction=prediction)
    # return strmy_prediction
    return render_template('predict.html', prediction=my_prediction)

if __name__ == '__main__':
    app.run(debug=True)