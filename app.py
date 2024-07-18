"""
  Tablero JUSTAT

    Modulos:
    * app.py: Aplicación.
    * graficos.py: Layout y callbacks para los gráficos.
    * selectores.py: Componentes de selcción de datos.

Juan Felipe Restrepo <juan.restrepo@under.edu.ar
2024-07-18
"""

import dash
import dash_bootstrap_components as dbc
from dash import html
import pandas as pd

from selectores import dropDownCircuns, dateSlider
from graficos import barrasCausas, scatterAutosSentencias
from tabla import tabla

DATAFILE = "./data/APGyECausasResueltas01.csv"

# Cargar datos
data = pd.read_csv(DATAFILE, index_col=0)
data["año_mes"] = pd.to_datetime(data["año_mes"]).dt.strftime("%Y-%m")
start_date = data["año_mes"].min()
final_date = data["año_mes"].max()
dropdown_options = list(set(data["circunscripción"]))
numdate = {num: date for num, date in enumerate(data["año_mes"].unique())}
data_size = data.shape[0]


def Header():
    logo_justat = html.Img(
        src="https://www.jusentrerios.gov.ar/wp-content/uploads/2021/02/logo_justat_logo_justat.jpg",
        style={
            "float": "right",
            "height": 45,
        },
    )

    title = html.H2(
        "Tablero de Estadísticas",
        style={"margin-top": 5},
    )

    return dbc.Row(
        [dbc.Col(title), dbc.Col(logo_justat)],
        align="center",
        justify="between",
        className="mt-4",
    )


# Start the app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

app.layout = dbc.Container(
    [
        Header(),
        dbc.Stack(
            [
                dbc.Placeholder(
                    color="primary", size="xs", className="me-1 mt-1 w-100"
                ),
                dbc.Card(
                    [
                        dbc.CardHeader(
                            html.H4("Fuero Civil - Primera Inst. Civ. y Com.")
                        ),
                        dbc.CardBody(
                            [
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            [
                                                html.H5(
                                                    "Resoluciones",
                                                    className="mb-2",
                                                ),
                                                html.H6(
                                                    f"Periodo: {start_date} -- {final_date}",
                                                    className="m-0",
                                                ),
                                            ],
                                            width=10,
                                        ),
                                        dbc.Col(
                                            dbc.Badge(
                                                f"{data_size} registros",
                                                color="primary",
                                                class_name="m-1",
                                            ),
                                            width=1,
                                        ),
                                    ],
                                    align="end",
                                    justify="between",
                                ),
                                tabla(data),
                            ],
                            className="position-relative",
                        ),
                    ]
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dbc.Card(
                                    [
                                        dbc.CardHeader(
                                            html.H4(
                                                "Causas Resueltas por Circunscripción:"
                                            )
                                        ),
                                        dbc.CardBody(
                                            [
                                                dbc.Stack(
                                                    [
                                                        html.H6("Periodo:"),
                                                        dateSlider(data),
                                                        barrasCausas(data),
                                                    ],
                                                    gap=3,
                                                )
                                            ]
                                        ),
                                    ]
                                )
                            ],
                            width=6,
                        ),
                        dbc.Col(
                            [
                                dbc.Card(
                                    [
                                        dbc.CardHeader(html.H4("Sentencias vs Autos:")),
                                        dbc.CardBody(
                                            [
                                                dbc.Stack(
                                                    [
                                                        html.H6("Circunscripción:"),
                                                        dropDownCircuns(data),
                                                        scatterAutosSentencias(data),
                                                    ],
                                                    gap=3,
                                                )
                                            ]
                                        ),
                                    ]
                                ),
                            ],
                            width=6,
                        ),
                    ],
                ),
            ],
            gap=3,
        ),
    ],
    fluid=False,
    id="main-container",
)


if __name__ == "__main__":
    app.run_server(debug=True)
