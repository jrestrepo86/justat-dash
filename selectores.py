from dash import html, dcc


def dropDownCircuns(data):

    dropdown_options = list(set(data["circunscripción"]))

    layout = dcc.Dropdown(
        id="dropdown-circuns",
        options=dropdown_options,
        value="Paraná",
    )

    return layout


def dateSlider(data):
    numdate = {num: date for num, date in enumerate(data["año_mes"].unique())}
    layout = html.Div(
        dcc.RangeSlider(
            id="date-slider",
            min=list(numdate.keys())[0],  # the first date
            max=list(numdate.keys())[-1],  # the last date
            step=1,
            value=[0, len(list(numdate.keys())) - 1],
            marks={int(numd): date for numd, date in numdate.items()},
        ),
        style={"width": "95%"},
    )

    return layout
