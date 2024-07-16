from dash import html, Input, Output, dcc, dash_table


def tabla(data):
    layout = dash_table.DataTable(
        data.to_dict("records"),
        [{"name": i, "id": i} for i in data.columns],
        style_cell_conditional=[
            {
                "if": {"column_id": "circunscripción"},
                "textAlign": "center",
                "width": "12%",
            },
            {
                "if": {"column_id": "organismo"},
                "textAlign": "left",
                "width": "15%",
                "textOverflow": "ellipsis",
                "overflow": "hidden",
            },
            {
                "if": {"column_id": "causas resueltas"},
                "width": "12%",
            },
        ],
        style_header={
            "textAlign": "center",
            "backgroundColor": "rgb(210, 210, 210)",
            "color": "black",
            "fontWeight": "bold",
        },
        css=[{"selector": "table", "rule": "table-layout: fixed"}],
        style_data_conditional=[
            {
                "if": {"row_index": "odd"},
                "backgroundColor": "rgb(220, 220, 220)",
            }
        ],
        page_size=10,
        tooltip_data=[
            {
                column: {"value": str(value), "type": "markdown"}
                for column, value in row.items()
            }
            for row in data.to_dict("records")
        ],
        tooltip_duration=None,
    )
    return layout
