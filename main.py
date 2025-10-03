import os
import json
import PySimpleGUI as sg
import pandas as pd

def load_json_files_from_folder(folder):
    data = []
    for filename in os.listdir(folder):
        if filename.endswith(".json"):
            filepath = os.path.join(folder, filename)
            try:
                with open(filepath, "r") as f:
                    contents = json.load(f)
                    if isinstance(contents, list):
                        data.extend(contents)
                    else:
                        data.append(contents)
            except Exception as e:
                print(f"Failed to read {filename}: {e}")
    return data

def main():
    sg.theme("LightBlue2")
    layout = [
        [sg.Text("Select a folder containing JSON files:"), sg.InputText(), sg.FolderBrowse(key="FOLDER")],
        [sg.Button("Load Data"), sg.Exit()],
        [sg.Text("Loaded files:"), sg.Text("", size=(40,1), key="FILES")],
        [sg.Text("Data Preview:")],
        [sg.Multiline(size=(80,20), key="PREVIEW")]
    ]
    window = sg.Window("JSON Folder Analyzer", layout)
    data = []
    while True:
        event, values = window.read()
        if event in (sg.WINDOW_CLOSED, "Exit"):
            break
        elif event == "Load Data":
            folder = values["FOLDER"]
            if not folder or not os.path.isdir(folder):
                window["FILES"].update("Invalid folder")
                continue
            data = load_json_files_from_folder(folder)
            window["FILES"].update(f"{len(data)} records loaded from {folder}")
            if data:
                try:
                    df = pd.DataFrame(data)
                    preview = df.head().to_string(index=False)
                except Exception as e:
                    preview = f"Error creating DataFrame: {e}"
            else:
                preview = "No data loaded."
            window["PREVIEW"].update(preview)
    window.close()

if __name__ == "__main__":
    main()