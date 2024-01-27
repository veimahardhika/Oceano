from flask import Flask, render_template, request, send_file
import pandas as pd
import plotly
import plotly.graph_objects as go
import io
import json
import base64
import urllib.request
import urllib.error

app = Flask(__name__)

with open('indices.json', 'r') as json_file:
    data = json.load(json_file)

variable_to_dataset = {}

def load_data(variable):
    if variable not in variable_to_dataset:
        try:
            datafile = base64.b64decode(data[variable]).decode('utf-8')
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
            req = urllib.request.Request(datafile, headers=headers)
            response = urllib.request.urlopen(req)
            variable_to_dataset[variable] = pd.read_csv(response)
        except urllib.error.HTTPError as e:
            return "Gagal memuat data untuk {}. Error: {}".format(variable, e)

available_variables = list(data.keys())

def figPlotly(df, y_variable):

    fig = go.Figure(data=go.Scatter(x=df['Date'], y=df[y_variable]))

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
    selected_variable = 'Nino 3.4' 
    if request.method == 'POST':
        selected_variable = request.form.get('variable', 'Nino 3.4')

    selected_variable = selected_variable.replace('%20', ' ')
    load_data(selected_variable)
    
    selected_data = variable_to_dataset[selected_variable]
    selected_data_subset = selected_data[['Date', selected_variable]]
    
    dfhtml = selected_data_subset.to_html(index=False)
    graphJSON = figPlotly(selected_data, selected_variable)

    if 'download_csv' in request.form:
        output = io.BytesIO()
        selected_data_subset.to_csv(output, index=False, encoding='utf-8')
        output.seek(0)
        return send_file(output, as_attachment=True, download_name=f"{selected_variable}.csv", mimetype='application/octet-stream')
    
    
    return render_template('index.html', table=dfhtml, graphJSON=graphJSON, available_variables=available_variables)

@app.route("/get_variable_description", methods=['GET'])
def get_variable_description():
    variable = request.args.get('variable')
    # Gantilah dengan deskripsi yang sesuai dengan variabel Anda
    variable_descriptions = {
        'NINO1+2': 'Deskripsi untuk NINO1+2.',
        'ANOM1+2': 'Deskripsi untuk ANOM1+2.',
        'NINO3': 'Deskripsi untuk NINO3.',
        'ANOM3': 'Deskripsi untuk ANOM3.',
        'NINO3.4': 'Indeks Niño 3.4 adalah indeks yang paling sering digunakan untuk mendefinisikan peristiwa El Niño dan La Niña. Indeks ini merupakan rata-rata anomali suhu permukaan laut (SPL) di wilayah 5°N–5°S dan 170°–120°W. Indeks Niño 3.4 biasanya menggunakan rata-rata 5 bulan. Peristiwa El Niño atau La Niña terjadi ketika SPL Niño 3.4 melebihi +/- 0,4C selama periode enam bulan atau lebih.'
    }
    variable_description = variable_descriptions.get(variable, 'Deskripsi tidak tersedia.')
    return variable_description

if __name__ == '__main__':
    app.run(debug=False)