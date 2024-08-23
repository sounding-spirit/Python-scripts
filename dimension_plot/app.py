from flask import Flask, render_template, request
import plotly.express as px
import pandas as pd


app = Flask(__name__)

# Sample data for scatter plot
df = pd.read_csv('dimension_data_seperate.csv')

# Function to create scatter plot
def create_scatter_plot():
    fig = px.scatter(df, 
                     x="WIDTH", 
                     y="HEIGHT",
                     hover_data=["FILENAME ID"], 
                    #  trendline="ols"
                     )
    
    
    plotAnnotes = []
    for x in range(0,len(df["FILENAME ID"]),20):
        plotAnnotes.append(dict(x=df["WIDTH"][x],
                            y=df["HEIGHT"][x],
                            text="""<a href="https://plot.ly/">{}</a>""".format(df["FILENAME ID"][x]),
                            showarrow=False,
                            ))
    fig.add_layout_image(
    dict(
        source="https://sounding-spirit-sftp-upload.s3.us-east-1.amazonaws.com/textract_output/1926-Nakcok-UTL/images/1926-Nakcok-UTL-0001.jpg",
        x=12,
        y=8.5,
    ))
    fig.update_layout_images(dict(
        xref="paper",
        yref="paper",
        sizex=0.3,
        sizey=0.3,
        xanchor="right",
        yanchor="bottom"
    ))
    fig.update_layout(dict(
        annotations=plotAnnotes
    ))
    fig.data[0].on_click(plot_click)
    return fig.to_html(include_plotlyjs='cdn',full_html=False)

def plot_click(data):
    pointData = data.points[0]
    print(pointData)

# Route to display scatter plot
@app.route('/')
def index():
    scatter_plot = create_scatter_plot()
    # print(scatter_plot)
    return '''
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
</head>

<body>
    <div id="plot"
'''+scatter_plot[4:]+'''
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <script>
        var plot = document.getElementById('plot');
        plot.onclick=function(data){
        console.log(data);
            var pointData = data.points[0];
            fetch('/click', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                },
                body: JSON.stringify({points: [pointData]})
            }).then(response => response.text())
            .then(data => alert(data));
        };
    </script>
</body>

</html>
'''

# Route to handle clicks on the scatter plot
@app.route('/click', methods=['POST'])
def handle_click():
    point_data = request.json
    clicked_point_label = point_data['points'][0]['text']
    return f'You clicked on point: {clicked_point_label}'

if __name__ == '__main__':
    app.run(debug=True)
