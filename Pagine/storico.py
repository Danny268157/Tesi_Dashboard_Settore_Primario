import os
import dash
from dash import dcc, html, Output, Input, no_update, callback_context
import dash_bootstrap_components as dbc
import logging
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import plotly.graph_objs as go
from simulatore_days import (crea_giornata, Metriche_Da_Sommare)
from simulatore_hours import (genera_dati_storici_ore)

dash.register_page(
    __name__,
    path='/storico',
    name='Storico'
)

last_mod_times = {}

MONTH_MAP_ITA = {
    1: 'Gennaio', 2: 'Febbraio', 3: 'Marzo',
    4: 'Aprile', 5: 'Maggio', 6: 'Giugno',
    7: 'Luglio', 8: 'Agosto',  9: 'Settembre',
    10: 'Ottobre', 11: 'Novembre', 12: 'Dicembre'
}
MONTH_MAP_ITA_BREVE = {
    1: 'Gen', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'Mag', 6: 'Giu',
    7: 'Lug', 8: 'Ago', 9: 'Set', 10: 'Ott', 11: 'Nov', 12: 'Dic'
}

def genera_dati_aggregati(file_path, hourly_file, anno):
    if not os.path.exists(hourly_file):
        start_dt = datetime(anno, 1, 1)
        end_dt = datetime(anno + 1, 1, 1)
        genera_dati_storici_ore(
            start_dt=start_dt,
            end_dt=end_dt,
            freq_minuti=60,
            scrivi_csv=True,
            file_path=hourly_file
        )
    crea_giornata(hourly_file, file_path)
    return pd.read_csv(file_path, parse_dates=['Timestamp'])

def format_data_italiana(data_obj):
    giorno = data_obj.day
    mese = data_obj.month
    return f"{giorno} {MONTH_MAP_ITA_BREVE[mese]}"

def get_virtual_now(anno):
    real_now = datetime.now()
    if real_now.year < anno:
        return datetime(anno, real_now.month, real_now.day,
                        real_now.hour, real_now.minute, real_now.second)
    else:
        return real_now

periodi_2024 = [
    {'label': 'Annuale', 'value': 'annuale'},
    {'label': 'Mensile', 'value': 'mensile'}
]
periodi_2025 = [
    {'label': 'Annuale', 'value': 'annuale'},
    {'label': 'Mensile', 'value': 'mensile'},
    {'label': 'Ultima Settimana', 'value': 'settimanale'},
    {'label': 'Giornata Attuale', 'value': 'giornaliero'}
]

FATTORE_1_NOME = "FATTORI AMBIENTALI"
METRICHE_FATTORE_1 = [
	'Temperatura (°C)',
	'Umidità relativa (%)',
	'Precipitazioni (mm)',
	'Velocità del vento (km/h)',
	'Indice di radiazione solare (W/m²)',
	'Qualità dell\'aria (AQI)',
]

FATTORE_2_NOME = "EFFICIENZA OPERATIVA"
METRICHE_FATTORE_2 = [
	'Consumo energetico (kWh)',
	'Efficienza macchinari (%)',
	'Soddisfazione lavoratori (%)',
]

FATTORE_3_NOME = "FATTORI ECONOMICI"
METRICHE_FATTORE_3 = [
	'Valore di mercato del prodotto (€/kg)',
	'Costo unitario di produzione (€/kg)',
	'Fatturato (€)',
	'Profitto netto (€)',
]

FATTORE_4_NOME = "USO DELLE RISORSE"
METRICHE_FATTORE_4 = [
	'Consumo d\'acqua (m³)',
	'Consumo di carburante (L)',
	'Emissioni di CO2 (kg)',
	'Produzione di rifiuti organici (kg)',

]

FATTORE_5_NOME = "DOMANDA E MERCATO"
METRICHE_FATTORE_5 = [
	'Domanda prevista (%)',
	'Fluttuazione della domanda (%)',

]

FATTORE_6_NOME = "ATTIVITA\' PRODUTTIVA"
METRICHE_FATTORE_6 = [
    'Efficienza della produzione (%)',
	'Produzione (kg)',
	'Scarti di produzione (kg)',
]

def genera_figura(anno, periodo, mese, metric):
    def carica_o_crea(file_path, funzione_generazione, **kwargs):
        if not os.path.exists(file_path):
            df_temp = funzione_generazione(scrivi_csv=True, file_path=file_path, **kwargs)
        else:
            df_temp = pd.read_csv(file_path, parse_dates=['Timestamp'])
        return df_temp
    if anno == '2024':
        df_2024 = carica_o_crea(
            'storico_dati_2024.csv',
            lambda scrivi_csv, file_path: genera_dati_aggregati(file_path, 'storico_dati_2024_hourly.csv', 2024)
        )
        df = df_2024.copy()
        if periodo == 'annuale':
            df['Month'] = df['Timestamp'].dt.month
            if metric in Metriche_Da_Sommare:
                df_group = df.groupby('Month')[metric].sum().reset_index()
            else:
                df_group = df.groupby('Month')[metric].mean().reset_index()
            if df_group.empty:
                return go.Figure().update_layout(title="Nessun dato (Annuale 2024)")
            df_group['MonthName'] = df_group['Month'].map(MONTH_MAP_ITA)
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=df_group['MonthName'],
                y=df_group[metric],
                mode='lines+markers',
                hovertemplate='%{x}: %{y:.2f}<extra></extra>'
            ))
            fig.update_layout(
                title=f"{metric}",
                title_x = 0.5,
                xaxis_title='Annuale - 2024',
                yaxis_title=metric
            )
            return fig

        elif periodo == 'mensile':
            if mese is None:
                return go.Figure().update_layout(title="Nessun mese selezionato (2024)")
            mese_label = MONTH_MAP_ITA.get(mese, "Mese sconosciuto")
            df_month = df[(df['Timestamp'].dt.year == 2024) & (df['Timestamp'].dt.month == mese)].copy()
            if df_month.empty:
                return go.Figure().update_layout(title=f"Nessun dato per {mese_label} (2024)")
            df_month['Giorno'] = df_month['Timestamp'].dt.date
            df_group = df_month.groupby('Giorno')[metric].mean().reset_index().sort_values('Giorno')
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=df_group['Giorno'],
                y=df_group[metric],
                mode='lines+markers',
                hovertemplate='Data: %{x}<br>Valore: %{y:.2f}<extra></extra>'
            ))
            start_day = df_group['Giorno'].min()
            end_day = df_group['Giorno'].max()
            if start_day != end_day:
                num_days = (end_day - start_day).days
                tick_positions = np.linspace(0, num_days, 5, dtype=int)
                tickvals = [start_day + timedelta(days=int(i)) for i in tick_positions]
                ticktext = [format_data_italiana(d) for d in tickvals]
                fig.update_xaxes(
                    type='date',
                    tickmode='array',
                    tickvals=tickvals,
                    ticktext=ticktext
                )
            fig.update_layout(
                title=f"{metric}",
                title_x=0.5,
                xaxis_title=f"{mese_label} - 2024",
                yaxis_title=metric
            )
            return fig

        else:
            return go.Figure().update_layout(title="Periodo non disponibile per Dati 2024")


    else:
        virtual_now = get_virtual_now(2025)

        if periodo == 'giornaliero':
            file_path = 'storico_dati_2025_hourly.csv'
            df_2025 = carica_o_crea(
                file_path,
                genera_dati_storici_ore,
                risorse_iniziali=50,
                start_dt=datetime(2025, 1, 1),
                end_dt=datetime(2026, 1, 1),
                freq_minuti=60
            )
        else:
            file_path = 'storico_dati_2025.csv'
            df_2025 = carica_o_crea(
                file_path,
                lambda scrivi_csv, file_path: genera_dati_aggregati(file_path, 'storico_dati_2025_hourly.csv', 2025)
            )
            df = df_2025.copy()
        df = df_2025.copy()
        df = df[df['Timestamp'] <= virtual_now].copy()

        if periodo == 'annuale':
            df['Month'] = df['Timestamp'].dt.month
            current_month = virtual_now.month
            df = df[df['Month'] <= current_month].copy()
            if df.empty:
                return go.Figure().update_layout(title="Nessun dato (Annuale 2025)")
            if metric in Metriche_Da_Sommare:
                df_group = df.groupby('Month')[metric].sum().reset_index()
            else:
                df_group = df.groupby('Month')[metric].mean().reset_index()
            df_group['MonthName'] = df_group['Month'].map(MONTH_MAP_ITA)
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=df_group['MonthName'],
                y=df_group[metric],
                mode='lines+markers'
            ))
            fig.update_layout(
                title=f"{metric}",
                title_x=0.5,
                xaxis_title='Annuale - 2025',
                yaxis_title=metric
            )
            return fig

        elif periodo == 'mensile':
            if mese is None:
                return go.Figure().update_layout(title="Nessun mese selezionato (2025)")
            mese_label = MONTH_MAP_ITA.get(mese, "Mese sconosciuto")
            df_month = df[(df['Timestamp'].dt.year == 2025) & (df['Timestamp'].dt.month == mese)].copy()
            if mese == virtual_now.month:
                df_month = df_month[df_month['Timestamp'].dt.day <= virtual_now.day].copy()
            if df_month.empty:
                return go.Figure().update_layout(title=f"Nessun dato per {mese_label} (2025)")
            df_month['Giorno'] = df_month['Timestamp'].dt.date
            df_group = df_month.groupby('Giorno')[metric].mean().reset_index().sort_values('Giorno')
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=df_group['Giorno'],
                y=df_group[metric],
                mode='lines+markers'
            ))
            start_day = df_group['Giorno'].min()
            end_day = df_group['Giorno'].max()
            if start_day != end_day:
                num_days = (end_day - start_day).days
                tick_positions = np.linspace(0, num_days, 5, dtype=int)
                tickvals = [start_day + timedelta(days=int(i)) for i in tick_positions]
                ticktext = [format_data_italiana(d) for d in tickvals]
                fig.update_xaxes(
                    type='date',
                    tickmode='array',
                    tickvals=tickvals,
                    ticktext=ticktext
                )

            fig.update_layout(
                title=f"{metric}",
                title_x=0.5,
                xaxis_title=f"{mese_label} - 2025",
                yaxis_title=metric
            )
            return fig

        elif periodo == 'settimanale':
            cutoff = virtual_now - timedelta(days=7)
            df_week = df[(df['Timestamp'] >= cutoff) & (df['Timestamp'] <= virtual_now)].copy()
            if df_week.empty:
                return go.Figure().update_layout(title="Nessun dato (Settimanale - Dati 2025)")
            df_week['Giorno'] = df_week['Timestamp'].dt.date
            df_group = df_week.groupby('Giorno')[metric].mean().reset_index().sort_values('Giorno')
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=df_group['Giorno'],
                y=df_group[metric],
                mode='lines+markers'
            ))

            start_day = df_group['Giorno'].min()
            end_day = df_group['Giorno'].max()
            if start_day != end_day:
                ndays = (end_day - start_day).days
                tick_positions = np.linspace(0, ndays, 5, dtype=int)
                tickvals = [start_day + timedelta(days=int(i)) for i in tick_positions]
                ticktext = [format_data_italiana(d) for d in tickvals]
                fig.update_xaxes(
                    type='date',
                    tickmode='array',
                    tickvals=tickvals,
                    ticktext=ticktext
                )
            fig.update_layout(
                title=f"{metric}",
                title_x=0.5,
                xaxis_title='Ultima Settimana - 2025',
                yaxis_title=metric
            )
            return fig

        else:
            start_of_day = virtual_now.replace(hour=0, minute=0, second=0, microsecond=0)
            df_day = df[(df['Timestamp'] >= start_of_day) & (df['Timestamp'] <= virtual_now)].copy()
            if df_day.empty:
                return go.Figure().update_layout(title="Nessun dato (Giornaliero - Dati 2025)")
            df_day = df_day.sort_values('Timestamp').reset_index(drop=True)
            df_day['Ora'] = df_day['Timestamp'].dt.strftime('%H:%M')
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=df_day['Ora'],
                y=df_day[metric],
                mode='lines+markers'
            ))
            unique_ore = sorted(df_day['Ora'].unique())
            if len(unique_ore) > 1:
                n_ore = len(unique_ore) - 1
                tick_positions = np.linspace(0, n_ore, 4, dtype=int)
                tickvals = [unique_ore[i] for i in tick_positions]
                ticktext = tickvals
                fig.update_xaxes(
                    tickmode='array',
                    tickvals=tickvals,
                    ticktext=ticktext,
                    tickangle=0
                )
            fig.update_layout(
                title=f"{metric}",
                title_x=0.5,
                xaxis_title='Giornata Attuale - 2025',
                yaxis_title=metric
            )
            return fig



layout = dbc.Container([

    dbc.Row(
        [
            dbc.Col(
                dcc.Link("← Home", href="/"),
                width="auto"
            ),
            dbc.Col(
                html.H2("RACCOLTA DATI PRECEDENTI (STORICO)", style={'textAlign': 'center'}),
                width=True
            )
        ],
        className="mt-4",
        justify="start",
        align="center"
    ),

    dbc.Row([
        dbc.Col([
            html.Label("Anno da visualizzare"),
            dcc.Dropdown(
                id='anno-selezionato-storico',
                options=[
                    {'label': 'Dati 2024', 'value': '2024'},
                    {'label': 'Dati 2025', 'value': '2025'}
                ],
                value='2024',
                clearable=False
            )
        ], width=3),

        dbc.Col([
            html.Label("Periodo"),
            dcc.Dropdown(
                id='periodo-selezionato-storico',
                options=[],
                value=None,
                clearable=False
            )
        ], width=3),

        dbc.Col([
            html.Label(id='label-mese', children=""),
            dcc.Dropdown(
                id='mese-selezionato-storico',
                options=[],
                value=1,
                clearable=False
            )
        ], width=3),

        dbc.Col([], width=3),
    ], className="mt-4"),

    dcc.Interval(
        id='interval-component-storico',
        interval=10 * 1000,
        n_intervals=0
    ),

    html.Hr(),

    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.Div(FATTORE_1_NOME),
                    dcc.Dropdown(
                        id='metric-fattore1',
                        options=[{'label': m, 'value': m} for m in METRICHE_FATTORE_1],
                        value=METRICHE_FATTORE_1[0],
                        clearable=False
                    )
                ]),
                dbc.CardBody([
                    dcc.Graph(
                        id='grafico-fattore1',
                        config={'displaylogo': False, 'showLink': False}
                    )
                ])
            ])
        ], width=4),

        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.Div(FATTORE_2_NOME),
                    dcc.Dropdown(
                        id='metric-fattore2',
                        options=[{'label': m, 'value': m} for m in METRICHE_FATTORE_2],
                        value=METRICHE_FATTORE_2[0],
                        clearable=False
                    )
                ]),
                dbc.CardBody([
                    dcc.Graph(
                        id='grafico-fattore2',
                        config={'displaylogo': False, 'showLink': False}
                    )
                ])
            ])
        ], width=4),

        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.Div(FATTORE_3_NOME),
                    dcc.Dropdown(
                        id='metric-fattore3',
                        options=[{'label': m, 'value': m} for m in METRICHE_FATTORE_3],
                        value=METRICHE_FATTORE_3[0],
                        clearable=False
                    )
                ]),
                dbc.CardBody([
                    dcc.Graph(
                        id='grafico-fattore3',
                        config={'displaylogo': False, 'showLink': False}
                    )
                ])
            ])
        ], width=4),
    ], className="mt-4"),

    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.Div(FATTORE_4_NOME),
                    dcc.Dropdown(
                        id='metric-fattore4',
                        options=[{'label': m, 'value': m} for m in METRICHE_FATTORE_4],
                        value=METRICHE_FATTORE_4[0],
                        clearable=False
                    )
                ]),
                dbc.CardBody([
                    dcc.Graph(
                        id='grafico-fattore4',
                        config={'displaylogo': False, 'showLink': False}
                    )
                ])
            ])
        ], width=4),

        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.Div(FATTORE_5_NOME),
                    dcc.Dropdown(
                        id='metric-fattore5',
                        options=[{'label': m, 'value': m} for m in METRICHE_FATTORE_5],
                        value=METRICHE_FATTORE_5[0],
                        clearable=False
                    )
                ]),
                dbc.CardBody([
                    dcc.Graph(
                        id='grafico-fattore5',
                        config={'displaylogo': False, 'showLink': False}
                    )
                ])
            ])
        ], width=4),

        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.Div(FATTORE_6_NOME),
                    dcc.Dropdown(
                        id='metric-fattore6',
                        options=[{'label': m, 'value': m} for m in METRICHE_FATTORE_6],
                        value=METRICHE_FATTORE_6[0],
                        clearable=False
                    )
                ]),
                dbc.CardBody([
                    dcc.Graph(
                        id='grafico-fattore6',
                        config={'displaylogo': False, 'showLink': False}
                    )
                ])
            ])
        ], width=4),
    ], className="mt-4"),

], fluid=True)


@dash.callback(
    [Output('periodo-selezionato-storico', 'options'),
     Output('periodo-selezionato-storico', 'value')],
    Input('anno-selezionato-storico', 'value')
)
def aggiorna_opzioni_periodo(anno):
    if anno == '2024':
        return periodi_2024, 'annuale'
    else:
        return periodi_2025, 'annuale'


@dash.callback(
    [Output('mese-selezionato-storico', 'options'),
     Output('mese-selezionato-storico', 'value')],
    [Input('anno-selezionato-storico', 'value'),
     Input('periodo-selezionato-storico', 'value')]
)
def aggiorna_opzioni_mese(anno, periodo):
    if anno == '2024':
        opzioni = [{'label': MONTH_MAP_ITA[m], 'value': m} for m in range(1, 13)]
    else:
        virtual_now = get_virtual_now(2025)
        max_month = virtual_now.month
        opzioni = [{'label': MONTH_MAP_ITA[m], 'value': m} for m in range(1, max_month + 1)]

    if periodo == 'mensile':
        return opzioni, 1
    else:
        return opzioni, no_update


@dash.callback(
    [
        Output('mese-selezionato-storico', 'style'),
        Output('label-mese', 'children'
    )],
    Input('periodo-selezionato-storico', 'value')
)
def toggle_mese(periodo):
    if periodo == 'mensile':
        return (
            {'display': 'block'},
            "Mese"
        )
    else:
        return (
            {'display': 'none'},
            ""
        )


@dash.callback(
    [
        Output('grafico-fattore1', 'figure'),
        Output('grafico-fattore2', 'figure'),
        Output('grafico-fattore3', 'figure'),
        Output('grafico-fattore4', 'figure'),
        Output('grafico-fattore5', 'figure'),
        Output('grafico-fattore6', 'figure')
    ],
    [
        Input('anno-selezionato-storico', 'value'),
        Input('periodo-selezionato-storico', 'value'),
        Input('mese-selezionato-storico', 'value'),
        Input('metric-fattore1', 'value'),
        Input('metric-fattore2', 'value'),
        Input('metric-fattore3', 'value'),
        Input('metric-fattore4', 'value'),
        Input('metric-fattore5', 'value'),
        Input('metric-fattore6', 'value'),
        Input('interval-component-storico', 'n_intervals')
    ]
)
def aggiorna_6_grafici(anno, periodo, mese,
                       met1, met2, met3, met4, met5, met6,
                       n_intervals):
    logging.info(f"[STORICO] Aggiornamento 6 grafici => anno={anno}, periodo={periodo}, mese={mese}")

    triggered_id = [p['prop_id'] for p in dash.callback_context.triggered][0]

    if triggered_id.startswith('interval-component-storico'):
        if anno == '2024':
            file_path = 'storico_dati_2024.csv'
            hourly_file = 'storico_dati_2024_hourly.csv'
            if os.path.exists(hourly_file) and os.path.exists(file_path):
                mod_hourly = os.path.getmtime(hourly_file)
                mod_daily = os.path.getmtime(file_path)
                if mod_hourly > mod_daily:
                    crea_giornata(hourly_file, file_path)
        else:
            if periodo == 'giornaliero':
                file_path = 'storico_dati_2025_hourly.csv'
            else:
                file_path = 'storico_dati_2025.csv'
                hourly_file = 'storico_dati_2025_hourly.csv'
                if os.path.exists(hourly_file) and os.path.exists(file_path):
                    mod_hourly = os.path.getmtime(hourly_file)
                    mod_daily = os.path.getmtime(file_path)
                    if mod_hourly > mod_daily:
                        crea_giornata(hourly_file, file_path)

        if os.path.exists(file_path):
            current_mod = os.path.getmtime(file_path)
            global last_mod_times
            last_mod = last_mod_times.get(file_path)

            if last_mod is not None and abs(current_mod - last_mod) < 1e-9:
                logging.info(f"[STORICO] File {file_path} invariato. No update (zoom resta).")
                return no_update

            last_mod_times[file_path] = current_mod

    fig1 = genera_figura(anno, periodo, mese, met1)
    fig2 = genera_figura(anno, periodo, mese, met2)
    fig3 = genera_figura(anno, periodo, mese, met3)
    fig4 = genera_figura(anno, periodo, mese, met4)
    fig5 = genera_figura(anno, periodo, mese, met5)
    fig6 = genera_figura(anno, periodo, mese, met6)

    return fig1, fig2, fig3, fig4, fig5, fig6
