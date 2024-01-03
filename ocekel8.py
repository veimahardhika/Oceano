from flask import Flask, render_template, request, Response
from io import StringIO
import pandas as pd
import plotly
import plotly.graph_objects as go
import json

# https://medium.com/@francescaguiducci/how-to-build-a-simple-personal-website-with-python-flask-and-netlify-d800c97c283d

app = Flask(__name__)

data1 = pd.read_csv('./indices.csv')
data2 = pd.read_csv('./indicesWeekly.csv')

variable_to_dataset = {
    'NINO1+2': data1,
    'ANOM1+2': data1,
    'NINO3': data1,
    'ANOM3': data1,
    'NINO4': data1,
    'ANOM4': data1,
    'NINO3.4': data1,
    'ANOM3.4': data1,
    'ONI': data1  
}

available_variables = list(variable_to_dataset.keys())

def figPlotly(df, y_variable):

    fig = go.Figure(data=go.Scatter(x=df['date'], y=df[y_variable]))

    fig.add_trace(go.Scatter(
            name="Totale Casi",
            mode="lines+markers",
            showlegend=True,
            marker=dict(
                symbol="circle-dot",
                size=6,
            ),
            line=dict(
                width=1,
                color="rgb(0,255,0)",
                dash="longdashdot"
            )
        )
    )
    fig.update_layout(
        title=dict(
            text =f"Index {y_variable}",
            y = 0.9,
            x = 0.5,
            xanchor = "center",
            yanchor = "top",
        ),
        legend=dict(
            y = 0.9,
            x = 0.03,
        ),
        xaxis_title="Tahun",
        yaxis_title=f"{y_variable}",
        
        font=dict(
            family="Calibri",
            size=20,
            color="black", #"#7f7f7f", 
        ),
        hovermode='x',  #['x', 'y', 'closest', False]
        plot_bgcolor = "rgb(240,240,240)",
        paper_bgcolor="rgb(255,255,255)"
    )

    #htmlfig = fig.write_html("fig.html")
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

@app.route("/", methods=['GET', 'POST'])
def index():
    selected_variable = 'NINO3.4'  # Default variable
    if request.method == 'POST':
        selected_variable = request.form.get('variable', 'NINO3.4')
    
    selected_data = variable_to_dataset[selected_variable]
    selected_data_subset = selected_data[['date', selected_variable]]
    
    dfhtml = selected_data_subset.to_html(index=False)
    graphJSON = figPlotly(selected_data, selected_variable)
    
    return render_template('index.html', table=dfhtml, graphJSON=graphJSON, available_variables=available_variables)

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=False, port=8080)