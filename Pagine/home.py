import dash
from dash import html
import dash_bootstrap_components as dbc

dash.register_page(
    __name__,
    path='/',
    name='Home'
)

layout = dbc.Container([
    html.H1("DASHBOARD SETTORE PRIMARIO", className="text-center mt-5"),

    dbc.Row(
        [
            dbc.Col(
                dbc.Button(
                    "RACCOLTA DATI PRECEDENTI (STORICO)",
                    color="info",
                    size="lg",
                    className="m-2",
                    href="/storico"
                ),
                width="auto"
            ),
            dbc.Col(
                dbc.Button(
                    "ANDAMENTI FUTURI (PREVISIONI)",
                    color="success",
                    size="lg",
                    className="m-2",
                    href="/previsioni"
                ),
                width="auto"
            )
        ],
        className="mt-5",
        justify="center"
    )
], fluid=True)
