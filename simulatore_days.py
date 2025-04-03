import pandas as pd
import os

Metriche_Da_Sommare = [
    'Consumo energetico (kWh)',
    'Fatturato (€)',
    'Profitto netto (€)',
    'Consumo d\'acqua (m³)',
    'Consumo di carburante (L)',
    'Emissioni di CO2 (kg)',
    'Produzione di rifiuti organici (kg)',
    'Produzione (kg)',
    'Scarti di produzione (kg)'
]

def crea_giornata(file_input, file_output):
    df = pd.read_csv(file_input, parse_dates=['Timestamp'])

    df.set_index('Timestamp', inplace=True)
    agg_dict = {}
    for col in df.columns:
        if col in Metriche_Da_Sommare:
            agg_dict[col] = 'sum'
        else:
            agg_dict[col] = 'mean'

    df_daily = df.resample('D').agg(agg_dict).reset_index()

    df_daily.to_csv(file_output, index=False)


if __name__ == '__main__':
    anni = [2024, 2025, 2026]

    for anno in anni:
        file_orario = f"storico_dati_{anno}_hourly.csv"
        file_giornaliero = f"storico_dati_{anno}.csv"

        if os.path.exists(file_orario):
            crea_giornata(file_orario, file_giornaliero)

