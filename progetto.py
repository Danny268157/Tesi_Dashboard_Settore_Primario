import dash
import dash_bootstrap_components as dbc

progetto =  dash.Dash(
            __name__,
            use_pages=True,
            pages_folder="Pagine",
            external_stylesheets=[dbc.themes.LUX],
            suppress_callback_exceptions=True
)


progetto.layout = dbc.Container(
    [dash.page_container],
    fluid=True
)

if __name__ == '__main__':
    progetto.run(debug=True)
