# EDMC_Elite_Mining_Analystics_Dashboard

Dashboarding component to compliment the Elite Mining Analytics located at https://github.com/SweetJonnySauce/EDMC-Mining-Analytics

---

## Mining Analytics Dashboard App

This repository now includes a cross-platform desktop dashboard for analyzing Elite Dangerous mining session data stored as JSON files.

### Features

- Select a folder containing multiple session `.json` files (as exported by EDMC-Mining-Analytics)
- View a summary table of all sessions:
  - Start/end time
  - Duration
  - Tons mined
  - Tons per hour (TPH)
  - Number of `mining_refined` events
- See aggregated stats (totals, averages)
- Select a session to view its chronological event log
- Generate charts and histograms:
  - Tons mined per session
  - Tons-per-hour (TPH) distribution (histogram)
  - Number of `mining_refined` events per session
  - Asteroid content type summary (pie chart)
- Cross-platform: works on Windows, macOS, and Linux

---

### Requirements

- **Python 3.7+**

#### Python Library Dependencies

- [PySimpleGUI](https://pysimplegui.readthedocs.io/en/latest/)
- [pandas](https://pandas.pydata.org/)
- [matplotlib](https://matplotlib.org/)

#### Installation

Open a terminal (or command prompt) and run:

```sh
pip install PySimpleGUI pandas matplotlib
```

---

### Usage

1. Save your session JSON files to a folder.
2. Run the dashboard:

   ```sh
   python mining_dashboard.py
   ```

3. Select your session folder in the app.
4. View summaries, stats, event logs, and choose charts to visualize your mining data.

---

### Example

#### Session Summary Table

| File                | Start Time           | End Time             | Duration (s) | Tons | TPH   | Refined Events | Commander        |
|---------------------|---------------------|----------------------|--------------|------|-------|----------------|------------------|
| session1.json       | 2025-10-02T22:56:47Z| 2025-10-02T22:57:11Z | 24.1         | 0    | 0     | 0              | sweetjonnysauce  |
| ...                 | ...                 | ...                  | ...          | ...  | ...   | ...            | ...              |

#### Charts

- Tons mined per session (bar chart)
- TPH histogram (distribution)
- Number of refined events per session (bar chart)
- Asteroid content summary (pie chart)

---

### Example JSON Structure

Each session `.json` file should follow this structure:
```json
{
  "meta": {
    "start_time": "...",
    "end_time": "...",
    "duration_seconds": ...,
    "overall_tph": { "tons": ..., "elapsed_seconds": ..., "tons_per_hour": ... },
    "content_summary": { "High": ..., "Medium": ..., "Low": ... },
    "commander": "...",
    ...
  },
  "commodities": { ... },
  "events": [
    { "type": "...", "timestamp": "...", "details": { ... } },
    ...
  ]
}
```

---

### Customization

To add new charts, metrics, or filtering, edit `mining_dashboard.py`.

---

Contributions welcome!
