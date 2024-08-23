from flask import Flask, render_template, request
from flask_cors import CORS
import pandas as pd
import urllib.request

app = Flask(__name__)
CORS(app) # used CORS in order to access omeka

# read data from the dimension csv
df = pd.read_csv('dimension_data_seperate.csv')

@app.route('/data')
def get_date():
    # plot data
    data = {
        "x": df["WIDTH"].values.tolist(),
        "y":df["HEIGHT"].values.tolist(),
        "text":df["FILENAME ID"].values.tolist(),
        "mode":'markers',
        "type":'scatter',
        'hovertemplate':
            "<b>%{text}</b><br>" +
            "%{xaxis.title.text}: %{x}<br>" +
            "%{yaxis.title.text}: %{y}<br>" +
            "<extra></extra>"
    }

    # plot layout
    layout={
        'title':'Width vs. Height',
        'xaxis': {
          'title': "Width",
          'range': [ 0, 30 ],
        },
        'yaxis': {
          'title': "Height",
          'range': [ 0, 40 ],
        },
    }
    return {
        'data':data,
        'layout':layout,
    }

# search for the PID in omeka
# return cover image and link to the songbook
@app.route('/omeka-search')
def omeka_get():
    # get the PID from args
    PID = request.args.get("PID")

    # get the omeka website html
    fp = urllib.request.urlopen("https://omeka.soundingspirit.org/s/ssdl/index/search?fulltext_search="+PID)
    mybytes = fp.read()
    mystr = mybytes.decode("utf8")
    fp.close()

    # parse the html to get cover image url and the link to the songbook
    img_url=mystr.split("<img src=")[1].split('"')[1].replace("&#x3A;",":").replace("&#x2F;","/")
    link=mystr.split('<a class="resource-link" href=')[1].split('"')[1].replace("&#x3A;",":").replace("&#x2F;","/")
    # print("image url:",img_url)

    return {
        "image":img_url,
        "url":link
    }

# Route to display scatter plot
@app.route('/')
def index():
    return render_template("index.html")

# use "py app.py" to run the program
if __name__ == '__main__':
    app.run(debug=True)
