# 🌿 Dashboard Settore Primario

📊 **Progetto per la Tesi Universitaria** sviluppato in Python per la realizzazione di una **dashboard interattiva** in grado di monitorare e prevedere metriche chiave del settore primario (agricoltura, pesca, acquacultura, silvicoltura, estrazione mineraria).

> **Università Pegaso**  
> Autore: Daniele Ferreri
> Matricola : 0312401122
> Anno Accademico: 2024/2025

---

## 🧱 Struttura della Dashboard

La dashboard è divisa in tre sezioni principali:

- 🏠 **Home** – Pagina iniziale, che permette di navigare tra le due sezioni che presentano i dati.
- 📁 **Storico** – Analisi di dati passati dal 2024 al 2025 fino all'ora attuale.
- 📈 **Previsioni** – Simulazioni e stime future per il 2025 e il 2026 a partire dall'ora successiva a quella attuale.

Le metriche principali necessarie per analizzare gli andamenti nel settore primario vegono racchiusi in 6 **macro-categorie** e vengono quindi rappresentati in grafici interattivi e dinamici nelle due sezioni **Storico** e **Previsioni**: 

1. **Fattori Ambientali**
2. **Efficienza Operativa**
3. **Fattori Economici**
4. **Uso delle Risorse**
5. **Domanda e Mercato**
6. **Attività Produttiva**

---

## 📦 Librerie e Tecnologie

| Libreria                  | Utilizzo                                 | Versione utilizzata |
|---------------------------|------------------------------------------|-----------------------|
| `Dash`                   | Framework principale per la dashboard    | >= 2.18.2             |
| `Dash Bootstrap Components` | UI responsive e moderna con Bootstrap  | >= 2.0.0              |
| `Plotly`                 | Grafici interattivi                      | >= 6.0.1             |
| `Pandas`                 | Gestione e manipolazione dei dati        | >= 2.2.3              |
| `NumPy`                  | Simulazione valori e smoothing casuale   | >= 2.2.3             |

---

## 📁 Struttura del codice


```plaintext
├── progetto.py                   # File iniziale per l'avvio del progetto
├── \Pagine\home.py               # Pagina iniziale della Dashboard
├── \Pagine\storico.py            # Pagina per analisi dei dati storici
├── \Pagine\previsioni.py         # Pagina per analisi delle previsioni future
├── simulatore_hours.py           # Simulatore che genera i valori orari per le metriche
├── simulatore_days.py            # Simulatore che genera i valori giornalieri a partire da quelli orari
├── requisiti.txt                 # Requisiti necessari per l'avvio del progetto
