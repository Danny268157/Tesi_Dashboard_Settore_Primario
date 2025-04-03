import numpy as np
import pandas as pd
import datetime

Stagioni = {
    'primavera': {
        '00:00-08:00': {
            'Temperatura (°C)': (-1.7, 19.4),
            'Umidità relativa (%)': (29, 97),
            'Precipitazioni (mm)': (0, 7.4),
            'Velocità del vento (km/h)': (0, 33.9),
            'Indice di radiazione solare (W/m²)': (0, 410.3),
            'Qualità dell\'aria (AQI)': (21, 32),
            'Consumo energetico (kWh)': (40, 90),
            'Efficienza macchinari (%)': (55, 65),
            'Valore di mercato del prodotto (€/kg)': (1.10, 1.30),
            'Costo unitario di produzione (€/kg)': (0.60, 0.80),
            'Fatturato (€)': (80, 120),
            'Profitto netto (€)': (28, 81),
            'Consumo d\'acqua (m³)': (1, 2.5),
            'Consumo di carburante (L)': (2, 5),
            'Emissioni di CO2 (kg)': (61, 84),
            'Produzione di rifiuti organici (kg)': (0.7, 1.9),
            'Domanda prevista (%)': (40, 110),
            'Soddisfazione lavoratori (%)': (40, 50),
            'Fluttuazione della domanda (%)': (30, 70),
            'Produzione (kg)': (20, 60),
            'Efficienza della produzione (%)': (60, 70),
            'Scarti di produzione (kg)': (1, 4),
        },
        '08:00-16:00': {
            'Temperatura (°C)': (-0.8, 29.1),
            'Umidità relativa (%)': (21, 94),
            'Precipitazioni (mm)': (0, 2.9),
            'Velocità del vento (km/h)': (0, 53.3),
            'Indice di radiazione solare (W/m²)': (34.7, 857.1),
            'Qualità dell\'aria (AQI)': (26, 39),
            'Consumo energetico (kWh)': (150, 250),
            'Efficienza macchinari (%)': (80, 92),
            'Valore di mercato del prodotto (€/kg)': (1.40, 1.80),
            'Costo unitario di produzione (€/kg)': (0.80, 1.10),
            'Fatturato (€)': (450, 550),
            'Profitto netto (€)': (147, 330),
            'Consumo d\'acqua (m³)': (4, 7),
            'Consumo di carburante (L)': (10, 20),
            'Emissioni di CO2 (kg)': (153, 211),
            'Produzione di rifiuti organici (kg)': (2.8, 8.2),
            'Domanda prevista (%)': (40, 110),
            'Soddisfazione lavoratori (%)': (55, 70),
            'Fluttuazione della domanda (%)': (30, 70),
            'Produzione (kg)': (150, 300),
            'Efficienza della produzione (%)': (85, 95),
            'Scarti di produzione (kg)': (4, 17.5),
        },
        '16:00-24:00': {
            'Temperatura (°C)': (0.6, 27.9),
            'Umidità relativa (%)': (24, 97),
            'Precipitazioni (mm)': (0, 6.6),
            'Velocità del vento (km/h)': (0, 39.7),
            'Indice di radiazione solare (W/m²)': (0, 552.7),
            'Qualità dell\'aria (AQI)': (24, 36),
            'Consumo energetico (kWh)': (100, 180),
            'Efficienza macchinari (%)': (70, 85),
            'Valore di mercato del prodotto (€/kg)': (1.20, 1.50),
            'Costo unitario di produzione (€/kg)': (0.70, 0.90),
            'Fatturato (€)': (250, 350),
            'Profitto netto (€)': (115, 245),
            'Consumo d\'acqua (m³)': (2, 4.5),
            'Consumo di carburante (L)': (6, 12),
            'Emissioni di CO2 (kg)': (92, 126),
            'Produzione di rifiuti organici (kg)': (1.5, 4.5),
            'Domanda prevista (%)': (40, 110),
            'Soddisfazione lavoratori (%)': (45, 60),
            'Fluttuazione della domanda (%)': (30, 70),
            'Produzione (kg)': (80, 180),
            'Efficienza della produzione (%)': (75, 85),
            'Scarti di produzione (kg)': (2, 10),
        },
    },
    'estate': {
        '00:00-08:00': {
            'Temperatura (°C)': (-1.7, 19.4),
            'Umidità relativa (%)': (29, 97),
            'Precipitazioni (mm)': (0, 7.4),
            'Velocità del vento (km/h)': (0, 33.9),
            'Indice di radiazione solare (W/m²)': (0, 410.3),
            'Qualità dell\'aria (AQI)': (21, 32),
            'Consumo energetico (kWh)': (40, 90),
            'Efficienza macchinari (%)': (55, 65),
            'Valore di mercato del prodotto (€/kg)': (1.10, 1.30),
            'Costo unitario di produzione (€/kg)': (0.60, 0.80),
            'Fatturato (€)': (80, 120),
            'Profitto netto (€)': (28, 81),
            'Consumo d\'acqua (m³)': (1, 2.5),
            'Consumo di carburante (L)': (2, 5),
            'Emissioni di CO2 (kg)': (61, 84),
            'Produzione di rifiuti organici (kg)': (0.7, 1.9),
            'Domanda prevista (%)': (40, 110),
            'Soddisfazione lavoratori (%)': (40, 50),
            'Fluttuazione della domanda (%)': (30, 70),
            'Produzione (kg)': (20, 60),
            'Efficienza della produzione (%)': (60, 70),
            'Scarti di produzione (kg)': (1, 4),
        },
        '08:00-16:00': {
            'Temperatura (°C)': (-0.8, 29.1),
            'Umidità relativa (%)': (21, 94),
            'Precipitazioni (mm)': (0, 2.9),
            'Velocità del vento (km/h)': (0, 53.3),
            'Indice di radiazione solare (W/m²)': (34.7, 857.1),
            'Qualità dell\'aria (AQI)': (26, 39),
            'Consumo energetico (kWh)': (150, 250),
            'Efficienza macchinari (%)': (80, 92),
            'Valore di mercato del prodotto (€/kg)': (1.40, 1.80),
            'Costo unitario di produzione (€/kg)': (0.80, 1.10),
            'Fatturato (€)': (450, 550),
            'Profitto netto (€)': (147, 330),
            'Consumo d\'acqua (m³)': (4, 7),
            'Consumo di carburante (L)': (10, 20),
            'Emissioni di CO2 (kg)': (153, 211),
            'Produzione di rifiuti organici (kg)': (2.8, 8.2),
            'Domanda prevista (%)': (40, 110),
            'Soddisfazione lavoratori (%)': (55, 70),
            'Fluttuazione della domanda (%)': (30, 70),
            'Produzione (kg)': (150, 300),
            'Efficienza della produzione (%)': (85, 95),
            'Scarti di produzione (kg)': (4, 17.5),
        },
        '16:00-24:00': {
            'Temperatura (°C)': (0.6, 27.9),
            'Umidità relativa (%)': (24, 97),
            'Precipitazioni (mm)': (0, 6.6),
            'Velocità del vento (km/h)': (0, 39.7),
            'Indice di radiazione solare (W/m²)': (0, 552.7),
            'Qualità dell\'aria (AQI)': (24, 36),
            'Consumo energetico (kWh)': (100, 180),
            'Efficienza macchinari (%)': (70, 85),
            'Valore di mercato del prodotto (€/kg)': (1.20, 1.50),
            'Costo unitario di produzione (€/kg)': (0.70, 0.90),
            'Fatturato (€)': (250, 350),
            'Profitto netto (€)': (115, 245),
            'Consumo d\'acqua (m³)': (2, 4.5),
            'Consumo di carburante (L)': (6, 12),
            'Emissioni di CO2 (kg)': (92, 126),
            'Produzione di rifiuti organici (kg)': (1.5, 4.5),
            'Domanda prevista (%)': (40, 110),
            'Soddisfazione lavoratori (%)': (45, 60),
            'Fluttuazione della domanda (%)': (30, 70),
            'Produzione (kg)': (80, 180),
            'Efficienza della produzione (%)': (75, 85),
            'Scarti di produzione (kg)': (2, 10),
        },
    },
    'autunno': {
        '00:00-08:00': {
            'Temperatura (°C)': (-1.7, 19.4),
            'Umidità relativa (%)': (29, 97),
            'Precipitazioni (mm)': (0, 7.4),
            'Velocità del vento (km/h)': (0, 33.9),
            'Indice di radiazione solare (W/m²)': (0, 410.3),
            'Qualità dell\'aria (AQI)': (21, 32),
            'Consumo energetico (kWh)': (40, 90),
            'Efficienza macchinari (%)': (55, 65),
            'Valore di mercato del prodotto (€/kg)': (1.10, 1.30),
            'Costo unitario di produzione (€/kg)': (0.60, 0.80),
            'Fatturato (€)': (80, 120),
            'Profitto netto (€)': (28, 81),
            'Consumo d\'acqua (m³)': (1, 2.5),
            'Consumo di carburante (L)': (2, 5),
            'Emissioni di CO2 (kg)': (61, 84),
            'Produzione di rifiuti organici (kg)': (0.7, 1.9),
            'Domanda prevista (%)': (40, 110),
            'Soddisfazione lavoratori (%)': (40, 50),
            'Fluttuazione della domanda (%)': (30, 70),
            'Produzione (kg)': (20, 60),
            'Efficienza della produzione (%)': (60, 70),
            'Scarti di produzione (kg)': (1, 4),
        },
        '08:00-16:00': {
            'Temperatura (°C)': (-0.8, 29.1),
            'Umidità relativa (%)': (21, 94),
            'Precipitazioni (mm)': (0, 2.9),
            'Velocità del vento (km/h)': (0, 53.3),
            'Indice di radiazione solare (W/m²)': (34.7, 857.1),
            'Qualità dell\'aria (AQI)': (26, 39),
            'Consumo energetico (kWh)': (150, 250),
            'Efficienza macchinari (%)': (80, 92),
            'Valore di mercato del prodotto (€/kg)': (1.40, 1.80),
            'Costo unitario di produzione (€/kg)': (0.80, 1.10),
            'Fatturato (€)': (450, 550),
            'Profitto netto (€)': (147, 330),
            'Consumo d\'acqua (m³)': (4, 7),
            'Consumo di carburante (L)': (10, 20),
            'Emissioni di CO2 (kg)': (153, 211),
            'Produzione di rifiuti organici (kg)': (2.8, 8.2),
            'Domanda prevista (%)': (40, 110),
            'Soddisfazione lavoratori (%)': (55, 70),
            'Fluttuazione della domanda (%)': (30, 70),
            'Produzione (kg)': (150, 300),
            'Efficienza della produzione (%)': (85, 95),
            'Scarti di produzione (kg)': (4, 17.5),
        },
        '16:00-24:00': {
            'Temperatura (°C)': (0.6, 27.9),
            'Umidità relativa (%)': (24, 97),
            'Precipitazioni (mm)': (0, 6.6),
            'Velocità del vento (km/h)': (0, 39.7),
            'Indice di radiazione solare (W/m²)': (0, 552.7),
            'Qualità dell\'aria (AQI)': (24, 36),
            'Consumo energetico (kWh)': (100, 180),
            'Efficienza macchinari (%)': (70, 85),
            'Valore di mercato del prodotto (€/kg)': (1.20, 1.50),
            'Costo unitario di produzione (€/kg)': (0.70, 0.90),
            'Fatturato (€)': (250, 350),
            'Profitto netto (€)': (115, 245),
            'Consumo d\'acqua (m³)': (2, 4.5),
            'Consumo di carburante (L)': (6, 12),
            'Emissioni di CO2 (kg)': (92, 126),
            'Produzione di rifiuti organici (kg)': (1.5, 4.5),
            'Domanda prevista (%)': (40, 110),
            'Soddisfazione lavoratori (%)': (45, 60),
            'Fluttuazione della domanda (%)': (30, 70),
            'Produzione (kg)': (80, 180),
            'Efficienza della produzione (%)': (75, 85),
            'Scarti di produzione (kg)': (2, 10),
        },
    },
    'inverno': {
        '00:00-08:00': {
            'Temperatura (°C)': (-1.7, 19.4),
            'Umidità relativa (%)': (29, 97),
            'Precipitazioni (mm)': (0, 7.4),
            'Velocità del vento (km/h)': (0, 33.9),
            'Indice di radiazione solare (W/m²)': (0, 410.3),
            'Qualità dell\'aria (AQI)': (21, 32),
            'Consumo energetico (kWh)': (40, 90),
            'Efficienza macchinari (%)': (55, 65),
            'Valore di mercato del prodotto (€/kg)': (1.10, 1.30),
            'Costo unitario di produzione (€/kg)': (0.60, 0.80),
            'Fatturato (€)': (80, 120),
            'Profitto netto (€)': (28, 81),
            'Consumo d\'acqua (m³)': (1, 2.5),
            'Consumo di carburante (L)': (2, 5),
            'Emissioni di CO2 (kg)': (61, 84),
            'Produzione di rifiuti organici (kg)': (0.7, 1.9),
            'Domanda prevista (%)': (40, 110),
            'Soddisfazione lavoratori (%)': (40, 50),
            'Fluttuazione della domanda (%)': (30, 70),
            'Produzione (kg)': (20, 60),
            'Efficienza della produzione (%)': (60, 70),
            'Scarti di produzione (kg)': (1, 4),
        },
        '08:00-16:00': {
            'Temperatura (°C)': (-0.8, 29.1),
            'Umidità relativa (%)': (21, 94),
            'Precipitazioni (mm)': (0, 2.9),
            'Velocità del vento (km/h)': (0, 53.3),
            'Indice di radiazione solare (W/m²)': (34.7, 857.1),
            'Qualità dell\'aria (AQI)': (26, 39),
            'Consumo energetico (kWh)': (150, 250),
            'Efficienza macchinari (%)': (80, 92),
            'Valore di mercato del prodotto (€/kg)': (1.40, 1.80),
            'Costo unitario di produzione (€/kg)': (0.80, 1.10),
            'Fatturato (€)': (450, 550),
            'Profitto netto (€)': (147, 330),
            'Consumo d\'acqua (m³)': (4, 7),
            'Consumo di carburante (L)': (10, 20),
            'Emissioni di CO2 (kg)': (153, 211),
            'Produzione di rifiuti organici (kg)': (2.8, 8.2),
            'Domanda prevista (%)': (40, 110),
            'Soddisfazione lavoratori (%)': (55, 70),
            'Fluttuazione della domanda (%)': (30, 70),
            'Produzione (kg)': (150, 300),
            'Efficienza della produzione (%)': (85, 95),
            'Scarti di produzione (kg)': (4, 17.5),
        },
        '16:00-24:00': {
            'Temperatura (°C)': (0.6, 27.9),
            'Umidità relativa (%)': (24, 97),
            'Precipitazioni (mm)': (0, 6.6),
            'Velocità del vento (km/h)': (0, 39.7),
            'Indice di radiazione solare (W/m²)': (0, 552.7),
            'Qualità dell\'aria (AQI)': (24, 36),
            'Consumo energetico (kWh)': (100, 180),
            'Efficienza macchinari (%)': (70, 85),
            'Valore di mercato del prodotto (€/kg)': (1.20, 1.50),
            'Costo unitario di produzione (€/kg)': (0.70, 0.90),
            'Fatturato (€)': (250, 350),
            'Profitto netto (€)': (115, 245),
            'Consumo d\'acqua (m³)': (2, 4.5),
            'Consumo di carburante (L)': (6, 12),
            'Emissioni di CO2 (kg)': (92, 126),
            'Produzione di rifiuti organici (kg)': (1.5, 4.5),
            'Domanda prevista (%)': (40, 110),
            'Soddisfazione lavoratori (%)': (45, 60),
            'Fluttuazione della domanda (%)': (30, 70),
            'Produzione (kg)': (80, 180),
            'Efficienza della produzione (%)': (75, 85),
            'Scarti di produzione (kg)': (2, 10),
        },
    },
}
def Ottieni_Stagione(dt):
    month = dt.month
    if month in [3, 4, 5]:
        return 'primavera'
    elif month in [6, 7, 8]:
        return 'estate'
    elif month in [9, 10, 11]:
        return 'autunno'
    else:
        return 'inverno'

def Ottieni_Ora(dt):
    hour = dt.hour
    if 0 <= hour < 8:
        return '00:00-08:00'
    elif 8 <= hour < 16:
        return '08:00-16:00'
    else:
        return '16:00-24:00'

def get_range(metric, stagione, time_phase):
    return Stagioni[stagione][time_phase][metric]

def random_uniform(metric, stagione, time_phase):
    min_val, max_val = get_range(metric, stagione, time_phase)
    return np.random.uniform(min_val, max_val)

def random_randint(metric, stagione, time_phase):
    min_val, max_val = get_range(metric, stagione, time_phase)
    return np.random.randint(min_val, max_val)

def smooth_value(prev_val, metric, stagione, time_phase, is_int=False):
    min_val, max_val = get_range(metric, stagione, time_phase)
    sigma = (max_val - min_val) * 0.1
    new_val = prev_val + np.random.normal(0, sigma)
    new_val = np.clip(new_val, min_val, max_val)
    return int(round(new_val)) if is_int else new_val

storico_dati = pd.DataFrame({
    'Timestamp': pd.Series(dtype='datetime64[ns]'),
    'Temperatura (°C)': pd.Series(dtype='float64'),
    'Umidità relativa (%)': pd.Series(dtype='int64'),
    'Precipitazioni (mm)': pd.Series(dtype='float64'),
    'Velocità del vento (km/h)': pd.Series(dtype='float64'),
    'Indice di radiazione solare (W/m²)': pd.Series(dtype='float64'),
    'Qualità dell\'aria (AQI)': pd.Series(dtype='int64'),
    'Consumo energetico (kWh)': pd.Series(dtype='float64'),
    'Efficienza macchinari (%)': pd.Series(dtype='int64'),
    'Valore di mercato del prodotto (€/kg)': pd.Series(dtype='float64'),
    'Costo unitario di produzione (€/kg)': pd.Series(dtype='float64'),
    'Fatturato (€)': pd.Series(dtype='float64'),
    'Profitto netto (€)': pd.Series(dtype='float64'),
    'Consumo d\'acqua (m³)': pd.Series(dtype='int64'),
    'Consumo di carburante (L)': pd.Series(dtype='int64'),
    'Emissioni di CO2 (kg)': pd.Series(dtype='int64'),
    'Produzione di rifiuti organici (kg)': pd.Series(dtype='float64'),
    'Domanda prevista (%)': pd.Series(dtype='int64'),
    'Soddisfazione lavoratori (%)': pd.Series(dtype='int64'),
    'Fluttuazione della domanda (%)': pd.Series(dtype='int64'),
    'Produzione (kg)': pd.Series(dtype='int64'),
    'Efficienza della produzione (%)': pd.Series(dtype='int64'),
    'Scarti di produzione (kg)': pd.Series(dtype='int64')
})

def genera_dati_storici_ore(risorse_iniziali=50,
                            start_dt=None,
                            end_dt=None,
                            freq_minuti=60,
                            scrivi_csv=False,
                            file_path='storico_dati_hours.csv'):
    global storico_dati

    if start_dt is None or end_dt is None or end_dt < start_dt:
        return storico_dati

    date_range = pd.date_range(start=start_dt, end=end_dt, freq=f'{freq_minuti}min')
    dati_simulati = []

    metriche = [
        'Temperatura (°C)',
        'Umidità relativa (%)',
        'Precipitazioni (mm)',
        'Velocità del vento (km/h)',
        'Indice di radiazione solare (W/m²)',
        'Qualità dell\'aria (AQI)',
        'Consumo energetico (kWh)',
        'Efficienza macchinari (%)',
        'Valore di mercato del prodotto (€/kg)',
        'Costo unitario di produzione (€/kg)',
        'Fatturato (€)',
        'Profitto netto (€)',
        'Consumo d\'acqua (m³)',
        'Consumo di carburante (L)',
        'Emissioni di CO2 (kg)',
        'Produzione di rifiuti organici (kg)',
        'Domanda prevista (%)',
        'Soddisfazione lavoratori (%)',
        'Fluttuazione della domanda (%)',
        'Produzione (kg)',
        'Efficienza della produzione (%)',
        'Scarti di produzione (kg)'
    ]
    metriche_int = [
        'Fluttuazione della domanda (%)',
        'Umidità relativa (%)',
        'Qualità dell\'aria (AQI)',
        'Efficienza macchinari (%)',
        'Efficienza della produzione (%)',
        'Consumo d\'acqua (m³)',
        'Emissioni di CO2 (kg)',
        'Consumo di carburante (L)',
        'Domanda prevista (%)',
        'Soddisfazione lavoratori (%)',
        'Produzione (kg)',
        'Scarti di produzione (kg)'
    ]

    prev_valori = {}
    first_timestamp = date_range[0]
    season = Ottieni_Stagione(first_timestamp)
    time_phase = Ottieni_Ora(first_timestamp)
    for metrica in metriche:
        if metrica == 'Consumo energetico (kWh)':
            prev_valori[metrica] = np.random.uniform(*get_range(metrica, season, time_phase))
        elif metrica in metriche_int:
            prev_valori[metrica] = random_randint(metrica, season, time_phase)
        else:
            prev_valori[metrica] = random_uniform(metrica, season, time_phase)

    for ora in date_range:
        season = Ottieni_Stagione(ora)
        time_phase = Ottieni_Ora(ora)
        record = {'Timestamp': ora}
        for metrica in metriche:
            is_int = metrica in metriche_int
            nuovo_val = smooth_value(prev_valori[metrica], metrica, season, time_phase, is_int=is_int)
            record[metrica] = nuovo_val
            prev_valori[metrica] = nuovo_val
        dati_simulati.append(record)

    storico_agg = pd.DataFrame(dati_simulati)
    storico_dati = pd.concat([storico_dati, storico_agg], ignore_index=True)

    if scrivi_csv:
        storico_dati.to_csv(file_path, index=False)
    return storico_dati

if __name__ == '__main__':
    df_hours = genera_dati_storici_ore(
        start_dt=datetime.datetime(2025, 1, 1),
        end_dt=datetime.datetime(2026, 1, 1),
        freq_minuti=60,
        scrivi_csv=True,
        file_path='storico_dati_2025_hourly.csv'
    )

    df_hours = genera_dati_storici_ore(
        start_dt=datetime.datetime(2024, 1, 1),
        end_dt=datetime.datetime(2025, 1, 1),
        freq_minuti=60,
        scrivi_csv=True,
        file_path='storico_dati_2024_hourly.csv'
    )

    df_hours = genera_dati_storici_ore(
        start_dt=datetime.datetime(2026, 1, 1),
        end_dt=datetime.datetime(2027, 1, 1),
        freq_minuti=60,
        scrivi_csv=True,
        file_path='storico_dati_2026_hourly.csv'
    )