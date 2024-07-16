import plotly.express as px
import plotly.graph_objects as go
from dash import html, Input, Output, dcc, callback


def barrasCausas(data):

    numdate = {num: date for num, date in enumerate(data["año_mes"].unique())}
    layout = html.Div(dcc.Graph(id="bar-chart-causas-resultas", figure={}))

    @callback(
        Output("bar-chart-causas-resultas", "figure"),
        [Input("main-container", "children"), Input("date-slider", "value")],
    )
    def bar_plot(trigger, date):
        start_date, end_date = date
        start_date = numdate[start_date]
        end_date = numdate[end_date]
        df = data[(data["año_mes"] >= start_date) & (data["año_mes"] <= end_date)]
        df = (
            df.groupby(["circunscripción"])[["causas resueltas", "a termino"]]
            .sum()
            .reset_index()
        )
        df["porcentaje"] = df["a termino"] / df["causas resueltas"] * 100
        total_causas = df["causas resueltas"].sum()

        fig = px.bar(
            df,
            x="circunscripción",
            y="causas resueltas",
            barmode="group",
            color="porcentaje",
            title="Long-Form Input",
            hover_name="circunscripción",
            hover_data={
                "circunscripción": False,
                "causas resueltas": True,
                "a termino": True,
                "porcentaje": ":.2f",
            },
            labels={"porcentaje": "% resueltas / a termino"},
            height=500,
        )
        fig.update_xaxes(tickangle=45)
        fig.update_layout(
            title=f"Causas Resueltas por Circunscripción - total: {total_causas}"
        )
        return fig

    return layout


def pieAutosSentencias(data):
    layout = html.Div(dcc.Graph(id="pie-chart-autos-sent", figure={}))

    @callback(
        Output("pie-chart-autos-sent", "figure"),
        Input("dropdown-circuns", "value"),
    )
    def sunburst_plot(circuns):
        circuns = [] if circuns is None else circuns
        if len(circuns) > 0:
            df = data[data["circunscripción"] == circuns]
            fig = px.scatter(
                df,
                x="sentencias",
                y="autos",
                size="causas resueltas",
                color="organismo",
                size_max=15,
                height=500,
                hover_name="organismo",
                hover_data={
                    "organismo": False,
                    "causas resueltas": True,
                    "autos": True,
                    "sentencias": True,
                },
            )
            fig.update_layout(
                title={
                    "text": f"Sentencias vs Autos - Circunscripción {circuns}",
                    "x": 0.1,
                    "y": 0.95,
                }
            )
        else:
            fig = go.Figure()
            fig.update_layout(title="Sentencias vs Autos")

        return fig

    return layout
