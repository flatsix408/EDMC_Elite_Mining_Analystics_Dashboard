# Elite Mining Analytics Dashboard (Electron Edition)

This is a cross-platform desktop dashboard for analyzing Elite Dangerous mining session data (in JSON format), built using [Electron](https://www.electronjs.org/).  
It provides a modern interface to explore, summarize, and visualize your mining sessions with tables and interactive charts.
This dashboard is supplemental and is designed to by the used with EDMC Mining Analytics (https://github.com/SweetJonnySauce/EDMC-Mining-Analytics)

---

## Features

- **Folder picker** to load and analyze multiple JSON session files at once
- **Session summary table:** Start/end time, duration, tons mined, TPH, refined events, commander
- **Aggregated stats**: totals and averages across sessions
- **Event log viewer**: inspect detailed events for any session
- **Interactive charts** (powered by Chart.js):
  - Tons mined per session (bar)
  - Tons-per-hour (TPH) histogram
  - Refined events per session (bar)
  - Asteroid content type summary (pie chart)
- **Modern UI:** Orange background with black text, clean and readable layout
- **Works on Windows, macOS, and Linux**

---

## Prerequisites

- [Node.js](https://nodejs.org/) (version 16 or newer recommended)
- (Optional) [Git](https://git-scm.com/) if you want to clone this repository

---

## Installation

### 1. Download or Clone This Repository

#### Option 1: Download ZIP

- Click "Code" > "Download ZIP" on GitHub  
- Extract the ZIP file on your computer

#### Option 2: Clone with Git

```sh
git clone https://github.com/your-username/mining-dashboard-electron.git
cd mining-dashboard-electron
```

### 2. Install Dependencies

Open a terminal (Command Prompt on Windows, Terminal on macOS/Linux) in the project directory and run:

```sh
npm install
```

---

## Running the App

### Windows

```sh
npm start
```

### macOS

```sh
npm start
```

### Linux

```sh
npm start
```

This will launch the dashboard window.  
Use the "Select Folder" button to choose your mining session JSON directory.

---

## Packaging for Distribution

To package as a standalone app (.exe, .dmg, etc.), use tools like [electron-builder](https://www.electron.build/) or [electron-forge](https://www.electronforge.io/).  
See their docs for detailed instructions.

---

## JSON File Format

Each mining session should be a `.json` file with the following structure (example):

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

## Support

- For issues, open a GitHub issue in this repository.
- For feature requests or contributions, feel free to submit a pull request!

---
