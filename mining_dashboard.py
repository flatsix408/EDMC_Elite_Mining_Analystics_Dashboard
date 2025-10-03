import os
import json
import PySimpleGUI as sg
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def load_sessions(folder):
    sessions = []
    for fname in os.listdir(folder):
        if fname.endswith(".json"):
            path = os.path.join(folder, fname)
            with open(path, "r") as f:
                try:
                    data = json.load(f)
                    sessions.append({"filename": fname, "data": data})
                except Exception as e:
                    print(f"Error loading {fname}: {e}")
    return sessions

def summarize_sessions(sessions):
    summary = []
    for s in sessions:
        meta = s["data"].get("meta", {})
        commodities = s["data"].get("commodities", {})
        events = s["data"].get("events", [])
        overall_tph = meta.get("overall_tph", {})
        tons = overall_tph.get("tons", 0)
        tph = overall_tph.get("tons_per_hour", 0) or 0
        start_time = meta.get("start_time")
        end_time = meta.get("end_time")
        duration = meta.get("duration_seconds", 0)
        mining_refined_count = sum(1 for e in events if e.get("type") == "mining_refined")
        # For pie chart option
        content_summary = meta.get("content_summary", {"High": 0, "Medium": 0, "Low": 0})
        summary.append({
            "File": s["filename"],
            "Start": start_time,
            "End": end_time,
            "Duration (s)": round(duration,1),
            "Tons": tons,
            "TPH": round(tph, 2) if tph else 0,
            "Refined Events": mining_refined_count,
            "Commander": meta.get("commander", ""),
            "Location": meta.get("ring", meta.get("location", {}).get("body", "")),
            "High": content_summary.get("High", 0),
            "Medium": content_summary.get("Medium", 0),
            "Low": content_summary.get("Low", 0),
        })
    return pd.DataFrame(summary)

def aggregate_stats(df):
    total_tons = df["Tons"].sum()
    avg_tons = df["Tons"].mean()
    total_duration = df["Duration (s)"].sum()
    avg_tph = df["TPH"].mean()
    total_refined = df["Refined Events"].sum()
    return {
        "Total Tons": total_tons,
        "Avg Tons per Session": avg_tons,
        "Total Duration (s)": total_duration,
        "Avg TPH": avg_tph,
        "Total Refined Events": total_refined,
    }

def event_log_string(events):
    log = []
    for e in events:
        ts = e.get("timestamp", "")
        typ = e.get("type", "")
        details = e.get("details", {})
        log.append(f"{ts} | {typ} | {json.dumps(details)}")
    return "\n".join(log)

def draw_figure(canvas, figure):
    if canvas.children:
        for child in canvas.winfo_children():
            child.destroy()
    figure_canvas_agg = FigureCanvasTkAgg(figure, master=canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg

def plot_chart(chart_type, df):
    plt.close("all")
    fig, ax = plt.subplots(figsize=(7,4))
    
    if chart_type == "Tons mined per session":
        ax.bar(df["File"], df["Tons"], color="royalblue")
        ax.set_ylabel("Tons mined")
        ax.set_title("Tons mined per session")
        plt.xticks(rotation=45, ha='right', fontsize=8)
    elif chart_type == "TPH histogram":
        ax.hist(df["TPH"], bins=min(10, len(df)), color="seagreen", edgecolor="black")
        ax.set_xlabel("Tons per hour")
        ax.set_ylabel("Session count")
        ax.set_title("TPH Distribution")
    elif chart_type == "Refined events per session":
        ax.bar(df["File"], df["Refined Events"], color="firebrick")
        ax.set_ylabel("Refined Events")
        ax.set_title("Number of 'mining_refined' events per session")
        plt.xticks(rotation=45, ha='right', fontsize=8)
    elif chart_type == "Asteroid content (pie)":
        # Sum the content types across all sessions
        sizes = [df["High"].sum(), df["Medium"].sum(), df["Low"].sum()]
        labels = ["High", "Medium", "Low"]
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', colors=["gold", "skyblue", "grey"])
        ax.set_title("Asteroid content summary (all sessions)")
    else:
        ax.text(0.5, 0.5, "Select a chart type", ha='center', va='center')
    plt.tight_layout()
    return fig

def main():
    sg.theme("LightBlue3")
    chart_options = [
        "Tons mined per session",
        "TPH histogram",
        "Refined events per session",
        "Asteroid content (pie)"
    ]
    layout = [
        [sg.Text("Select folder with session JSON files:"), sg.InputText(size=(40,1), key="FOLDER"), sg.FolderBrowse()],
        [sg.Button("Load Sessions"), sg.Exit()],
        [sg.Text("Session Summary:")],
        [sg.Table(values=[[""]*8], headings=["File","Start","End","Duration (s)","Tons","TPH","Refined Events","Commander"], 
                  key="SUMMARY", auto_size_columns=False, col_widths=[20,18,18,10,7,7,13,12], enable_events=True, 
                  max_col_width=30, size=(None,10))],
        [sg.Text("Aggregated Stats:")],
        [sg.Multiline("", size=(75,4), key="AGG", disabled=True)],
        [sg.Text("Charts:")],
        [sg.Combo(chart_options, default_value=chart_options[0], key="CHART_TYPE", readonly=True), sg.Button("Show Chart")],
        [sg.Canvas(key="CANVAS", size=(600,350))],
        [sg.Text("Select a session row then click 'View Event Log' below.")],
        [sg.Button("View Event Log"), sg.Multiline("", size=(95,15), key="LOG", disabled=True)]
    ]
    window = sg.Window("Elite Mining Analytics Dashboard", layout, finalize=True)
    sessions = []
    df = pd.DataFrame()
    fig_agg = None
    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, "Exit"):
            break
        elif event == "Load Sessions":
            folder = values["FOLDER"]
            if not os.path.isdir(folder):
                sg.popup("Please select a valid folder.")
                continue
            sessions = load_sessions(folder)
            if not sessions:
                sg.popup("No JSON session files found.")
                continue
            df = summarize_sessions(sessions)
            if df.empty:
                window["SUMMARY"].update(values=[[""]*8])
                window["AGG"].update("")
                window["LOG"].update("")
            else:
                window["SUMMARY"].update(values=df[df.columns[:8]].values.tolist())
                agg = aggregate_stats(df)
                agg_text = "\n".join(f"{k}: {v:.2f}" if isinstance(v, float) else f"{k}: {v}" for k,v in agg.items())
                window["AGG"].update(agg_text)
                window["LOG"].update("")
        elif event == "Show Chart":
            if df.empty:
                sg.popup("Load sessions first.")
                continue
            chart_type = values["CHART_TYPE"]
            fig = plot_chart(chart_type, df)
            draw_figure(window["CANVAS"].TKCanvas, fig)
        elif event == "View Event Log":
            selected = values["SUMMARY"]
            if not selected or not sessions:
                sg.popup("Select a session row first.")
                continue
            idx = selected[0]
            log_events = sessions[idx]["data"].get("events", [])
            log_str = event_log_string(log_events)
            window["LOG"].update(log_str)
    window.close()

if __name__ == "__main__":
    main()