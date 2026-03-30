# 🌫️ Air Pollutant Monitor — Real-Time Simulation with Alarm System

A Python desktop application that simulates real-time air quality monitoring by replaying historical sensor data, with colour-coded alerts, audible alarms, and exportable plots.

---

## 📋 Overview

The application reads historical air pollutant measurements from CSV files collected at **Urad, Satu Mare, Romania** (lat: 47.6833, lon: 22.4667) and replays them sequentially to simulate live sensor readings. When pollutant concentrations exceed safety thresholds, the app highlights the values and triggers an audible beep alarm.

---

## 📊 Dataset

All CSV files share the structure: `time (UNIX), latitude, longitude, altitude, value`

| File | Pollutant | Column |
|---|---|---|
| `Urad_PM1.csv` | Particulate Matter < 1 µm | `pm1` |
| `Urad_PM10.csv` | Particulate Matter < 10 µm | `pm10` |
| `Urad_PM25.csv` | Particulate Matter < 2.5 µm | `pm25` |
| `Urad__NO2.csv` | Nitrogen Dioxide | `gas2` |
| `Urad_O3.csv` | Ozone | `gas1` |
| `Urad_SO2.csv` | Sulfur Dioxide | `gas3` |
| `Urad__CO.csv` | Carbon Monoxide | `gas4` |
| `Urad_Hum.csv` | Relative Humidity | `humidity` |

> Timestamps are stored in **UNIX format** and converted to datetime on load.

---

## ⚙️ How It Works

### 1. Data Loading (`readData`)
PM1, PM10, and PM2.5 CSVs are loaded into separate Pandas DataFrames, concatenated into a single DataFrame (duplicate columns removed), and the `time` column is converted from UNIX epoch to human-readable datetime.

### 2. Simulation Loop (`simRead`)
The app steps through the DataFrame row by row at 10 ms intervals using Tkinter's `after()` scheduler, mimicking a live data stream. Each reading is:
- Displayed in a scrolling **Tkinter textbox**
- Stored in a **NumPy array** (`dateSim`) for later plotting
- Checked against safety thresholds

### 3. Alarm System

| Pollutant | ⚠️ Warning (yellow) | 🔴 Alarm (red + beep) |
|---|---|---|
| PM1 | > 50 µg/m³ | > 100 µg/m³ |
| PM10 | > 100 µg/m³ | > 120 µg/m³ |
| PM2.5 | > 50 µg/m³ | > 100 µg/m³ |

Alarm beep: **1000 Hz, 300 ms** via `winsound.Beep()`

### 4. Plotting (`plotData` / `savePlot`)
After pausing the simulation, a Matplotlib chart of PM1, PM10, and PM2.5 over time can be displayed and exported as a **PDF file**.

---

## 🖥️ GUI Controls

| Button | Function |
|---|---|
| **Pornește simularea** | Start / resume the data replay |
| **Pune pe pauză** | Pause the simulation |
| **Reprezintă grafic** | Plot the recorded data (available on pause) |
| **Salvează grafic** | Export the plot as a PDF |

---

## 🚀 Setup

### Requirements
```bash
pip install pandas numpy matplotlib
```
> `tkinter` and `winsound` are included in the standard Python distribution on Windows.

### Run
```bash
python alarm.py
```

> **Note:** Update the CSV file paths in `readData()` to match your local directory before running.

---

## 📁 Project Structure

```
air-pollutant-monitor/
├── alarm.py            # Main application
├── Urad_PM1.csv        # PM1 sensor data
├── Urad_PM10.csv       # PM10 sensor data
├── Urad_PM25.csv       # PM2.5 sensor data
├── Urad__NO2.csv       # NO2 sensor data
├── Urad_O3.csv         # O3 sensor data
├── Urad_SO2.csv        # SO2 sensor data
├── Urad__CO.csv        # CO sensor data
├── Urad_Hum.csv        # Humidity data
└── README.md
```

---

## 🛠️ Tech Stack

| Library | Purpose |
|---|---|
| `pandas` | CSV loading, DataFrame manipulation, UNIX time conversion |
| `numpy` | Efficient in-memory storage of simulation readings |
| `tkinter` | GUI window, textbox, buttons |
| `matplotlib` | Time-series plotting and PDF export |
| `winsound` | Audible beep alarm (Windows only) |

---

## 📚 References

- [Python Docs](https://docs.python.org/)
- [StackOverflow](https://stackoverflow.com)

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.
