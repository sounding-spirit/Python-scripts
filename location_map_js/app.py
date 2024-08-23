from flask import Flask, render_template, request
from flask_cors import CORS
import pandas as pd
import urllib.request
import geopandas
import matplotlib.pyplot as plt
import base64
from io import BytesIO

app = Flask(__name__)
CORS(app) # used CORS in order to access omeka

# read data from the dimension csv
df = pd.read_csv('location_coor.csv')
df2 = pd.read_csv('location_processed.csv')

@app.route('/data')
def get_date():

    # customdata = []
    # for x in df.index:
    #     customdata.append({
    #         "PID": df2.loc[x,"PID"]
    #         "title": df2.loc[x,"title"]
    #     })
    
    # plot data
    data = {
        "x": df["Long"].values.tolist(),
        "y":df["Lati"].values.tolist(),
        "text":df["Desc"].values.tolist(),
        "customdata":df["Leng"].values.tolist(), # TODO: see if more fields
        "marker":{
            "color":['rgb('+str(85+x*40)+', 0, '+str(85-x*40)+')' for x in df["Leng"].values.tolist()],
        },
        "mode":'markers',
        "type":'scatter',
        'hovertemplate':
            "Coordinate: [%{x},%{y}]<br>"+
            "Number of books: %{customdata}<br>"
            "<extra></extra>"   
    }

    # plot layout
    layout={
        'title':'Width vs. Height',
        'xaxis': {
          'title': "Longitude",
          'range': [ -180, 180 ],
        },
        'yaxis': {
          'title': "Latitude",
          'range': [ -90, 90 ],
        },
        "images":[
            {
                'x': 0,
                'y': 0,
                'sizex': 2,
                'sizey': 1,
                'source': "https://raw.githubusercontent.com/cldougl/plot_images/add_r_img/vox.png",
                'xanchor': "left",
                'xref': "paper",
                'yanchor': "bottom",
                'yref': "paper",
                "opacity": 0.4,
            },
        ],
    }
    return {
        'data':data,
        'layout':layout,
    }

# Route to display scatter plot
@app.route('/')
def index():
    # try to get some states (one state on a plot)
    # https://medium.com/@kavee625/plotting-data-on-the-world-map-with-geopandas-f03742615196
    return render_template("index.html")

# use "py app.py" to run the program
if __name__ == '__main__':
    app.run(debug=True)
