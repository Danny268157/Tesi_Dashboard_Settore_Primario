import dash
import dash_bootstrap_components as dbc
from simulatore_days import crea_giornata
from simulatore_hours import genera_dati_storici_ore
import os
from datetime import datetime

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


def genera_tutto():
    annate = [2024, 2025, 2026]
    for anno in annate:
        hourly_file = f"storico_dati_{anno}_hourly.csv"
        daily_file = f"storico_dati_{anno}.csv"
        if not os.path.exists(hourly_file):
            genera_dati_storici_ore(
                start_dt=datetime(anno, 1, 1),
                end_dt=datetime(anno + 1, 1, 1),
                freq_minuti=60,
                scrivi_csv=True,
                file_path=hourly_file
            )
        if not os.path.exists(daily_file):
            crea_giornata(hourly_file, daily_file)

genera_tutto()
if __name__ == '__main__':
    progetto.run(debug=True)
