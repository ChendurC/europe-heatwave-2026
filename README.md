# 🌡️ European Heatwave Crisis 2026 — Interactive Dashboard

A real-data analytics dashboard tracking the 2026 European heatwave across 12 countries, with ML-based temperature forecasting for July–August 2026.

🔴 **[Live Dashboard →](https://europe-heatwave-2026-z7ar9atfnevjcdqmmxh8ru.streamlit.app/)**

---

## Overview

This project analyses real temperature data from January–June 2026 across 12 European countries and forecasts the expected heatwave peak for July–August 2026 using linear regression trained on 11 years of historical data (2015–2025).

---

## Key Findings

| Metric | Value |
|---|---|
| Peak actual temperature (Jan–Jun 2026) | 40.3°C — France |
| Predicted peak temperature (Jul–Aug 2026) | 41.2°C — Greece |
| Countries tracked | 12 |
| Historical baseline | 2015–2024 (10 years) |
| Forecast method | Linear regression (numpy polyfit) |

---

## Dashboard Features

- **Temperature Map** — Choropleth map of average temperatures across Europe
- **Country Comparison** — Bar charts comparing actual vs. historical baseline
- **ML Forecast** — July–August 2026 predictions with confidence intervals
- **Health & Response** — Estimated health impacts and government response tracker

---

## Tech Stack

| Tool | Purpose |
|---|---|
| Python | Data pipeline & ML forecasting |
| Open-Meteo API | Real historical & 2026 temperature data (free, no auth) |
| pandas / numpy | Data processing & linear regression |
| Streamlit | Interactive web dashboard |
| Plotly | Charts, choropleth maps, visualisations |

---

## Project Structure

```
europe-heatwave-2026/
├── pipeline/
│   └── generate_data.py      # Fetches real data + runs ML forecast
├── dashboard/
│   └── app.py                # Streamlit dashboard (4 tabs)
├── data/
│   ├── temperature_data.csv
│   ├── monthly_trends.csv
│   ├── forecast_jul_aug.csv
│   ├── health_impact.csv
│   └── response_data.csv
└── requirements.txt
```

---

## How to Run Locally

```bash
git clone https://github.com/ChendurC/europe-heatwave-2026.git
cd europe-heatwave-2026
pip install -r requirements.txt
python pipeline/generate_data.py   # fetch real data
streamlit run dashboard/app.py
```

---

## Author

**Chendur Murugan Cheran**  
MSc Business Analytics — University of Exeter  
[GitHub](https://github.com/ChendurC) | [LinkedIn](https://www.linkedin.com/in/chendur-murugan-cheran/)
