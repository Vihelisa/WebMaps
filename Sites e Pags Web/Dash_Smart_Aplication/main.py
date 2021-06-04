#Importações:
import os
import pandas as pd
import uvicorn as uvicorn
from datetime import date
from fastapi import FastAPI
import plotly.express as px
import plotly.graph_objs as obj
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from starlette.middleware.wsgi import WSGIMiddleware


import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output


#Variáveis:
open_file = 'sample_irriga_239'
style='.csv'
folder_file = 'Files'

#Start the dash app:
app = dash.Dash(
    __name__,
    requests_pathname_prefix="/dash/",
    meta_tags=[
        {"lang": "pt-BR"},
        {"http-equiv": "Content-Language", "content": "pt-br"},
    ],
    )

#Abrindo o arquivo para fazer o Dataframe:
path_file = os.path.join(folder_file, open_file+style)
df = pd.read_csv(path_file)
#df = df.set_index('_date')
#print(df)

slider = dcc.RangeSlider(
    id="slider",
    # value=[df["date"].min(), df["date"].max()],
    value=[20, 40],
    min=0,
    max=65,
    step=5,
    marks={
        0: "5-16",
        1: "5-15",
        2: "5-14",
        3: "5-13",
        4: "5-12",
        5: "5-11",
        6: "5-10",
        7: "5-9",
        8: "5-8",
        9: "5-7",
        10: "5-6",
        11: "5-5",
        12: "5-4",
        13: "5-3",
        14: "5-2",
        15: "5-1",
        16: "4-30",
        17: "4-29",
        18: "4-28",
        19: "4-27",
        20: "4-26",
        21: "4-25",
        22: "4-24",
        23: "4-23",
        24: "4-22",
        25: "4-21",
        26: "4-20",
        27: "4-19",
        28: "4-18",
        29: "4-17",
        30: "4-16",
        31: "4-15",
        32: "4-14",
        33: "4-13",
        34: "4-12",
        35: "4-11",
        36: "4-10",
        37: "4-9",
        38: "4-8",
        39: "4-7",
        40: "4-6",
        41: "4-5",
        42: "4-4",
        43: "4-3",
        44: "4-2",
        45: "4-1",
        46: "3-31",
        47: "3-30",
        48: "3-29",
        49: "3-28",
        50: "3-27",
        51: "3-26",
        52: "3-25",
        53: "3-24",
        54: "3-23",
        55: "3-22",
        56: "3-21",
        57: "3-20",
        58: "3-19",
        59: "3-18",
        60: "3-17",
        61: "3-16",
        62: "3-15",
        63: "3-14",
        64: "3-13",
    },
)

app.title = "WEB TEST"

#APP Layout:
app.layout = html.Div(
    children=[
        html.Header(lang="pt-BR", title="eita"),
        dcc.DatePickerRange(
            end_date=date(2017, 6, 21),
            display_format="MMMM Y, DD",
            start_date_placeholder_text="MMMM Y, DD",
        ),
        html.H1(children="TITULO PRINCIPAL"),
        html.Div(
            children="SUBTITULO Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin sit amet mauris at ipsu"
        ),
        dcc.Graph(id="temp-plot"),
        slider,
    ],
)


#Conectar o gráfico plotly com os componentes do dash
@app.callback(Output("temp-plot", "figure"), [Input("slider", "value")])
def add_graph(slider):
    print(type(slider))
    trace_high = obj.Scatter(
        x=df["date"],
        y=df["tempoIrriga"],
        mode="lines+markers",
        name="Irrigation Time",
    )
    trace_low = obj.Scatter(
        x=df["date"], 
        y=df["cadRoot"],
        mode="lines+markers", 
        name="Cad Root",
    )
    trace_etc = obj.Scatter(
        x=df["date"], y=df["etc"], mode="lines+markers", name="etc"
    )
    trace_ATD = obj.Scatter(
        x=df["date"], y=df["ATD"], mode="lines+markers", name="ATD"
    )

    layout = obj.Layout(
        xaxis=dict(range=[slider[0], slider[1]]),
        yaxis={"title": "Nome do eixo vertical"},
    )

    figure = obj.Figure(data=[trace_low], layout=layout)
    return figure


if __name__ == '__main__':
    server = FastAPI()

    @server.get("/")
    async def root():
        return 1

    server.mount("/dash", WSGIMiddleware(app.server))
    uvicorn.run(server, host="0.0.0.0", port=5500)



'''
print(option_slctd)
print(type(option_slctd))
    
    container = "the date chosen by was:{}.format(option_slctd)

    dff = df.copy()
    dff = dff[dff['date'] == option_slctd]
    
        def Layout_Graph(df):
        Layout = go.Layout(
                height = 600,
                margin=go.layout.Margin(l=50),
                title = 'Insira o título aqui',
                xaxis={'title':'Data', 
                'tickformat':"%d/%m/%Y"}      #se usar %b ele coloca o mês com as 3 primeiras letras
        )
        return Layout

    def Plot_Graph(fig, df):
        fig.add_trace(go.Scatter(x=df['date'], y=df['AFD'], mode='lines', 
                    name='AFD'), secondary_y=False)
        fig.add_trace(go.Scatter(x=df['date'], y=df['cadRoot'], mode='lines', 
                    name='cadRoot'), secondary_y=False)
        fig.add_trace(go.Scatter(x=df['date'], y=df['etc'], mode='lines',
                                name='etc'), secondary_y=True)
        fig.add_trace(go.Scatter(x=df['date'], y=df['ATD'], mode='lines',
                                name='ATD'), secondary_y=True)
    
    #Gráfico plotly:
    layout = Layout_Graph(df)
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    Plot_Graph(fig, df)
    fig.update_layout(layout)
    fig.update_layout(showlegend = True)

    fig.update_yaxes(title='AFD e cadRoot', secondary_y=False)
    fig.update_yaxes(title='ATD e etc', secondary_y=True)

    
def upgrade_graph(df):
    data = []
    for col in df:
        if 'Date' in col:
            continue
        elif 'AFD' or 'cadRoot' in col:
            data_graph = go.Scatter({
                'x':df['date'],
                'y':df[col],
                'mode':'lines+markers',
                'name':col,
                'secondary_y': False
            })
        else:
            data_graph = go.Scatter({
                'x':df['date'],
                'y':df[col],
                'mode':'lines+markers',
                'name':col,
                'secondary_y': True
            })
        data.append(data_graph)

    layout = dict(
        height = 600,
        margin=go.layout.Margin(l=50),
        xaxis={'title':'Data','tickformat':"%d/%m/%Y"}      #se usar %b ele coloca o mês com as 3 primeiras letras
    )

    #fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig = go.Figure(data=data, layout=layout)
    fig.update_layout(showlegend = True)
    fig.update_yaxes(title='AFD e cadRoot', secondary_y=False)
    fig.update_yaxes(title='ATD e etc', secondary_y=True)

    #div_plot = plot(fig, output_type='div', include_plotlyjs=False)
    return fig

fig = upgrade_graph(df)
'''