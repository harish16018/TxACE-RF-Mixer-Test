import tkinter as tk
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText
import subprocess
import threading
import sys

entry_widgets = []

parameters = ['Hex Code', 'Output CSV Directory',
'DC Supply A Output 1 Start Voltage','DC Supply A Output 1 Stop Voltage', 'DC Supply A Output 1 Step Voltage','DC Supply A Output 1 Current Limit', 'DC Supply A Output 1 Over-Voltage Limit', 
'DC Supply A Output 2 Start Voltage','DC Supply A Output 2 Stop Voltage', 'DC Supply A Output 2 Step Voltage',
'DC Supply A Output 2 Current Limit', 'DC Supply A Output 2 Over-Voltage Limit', 
'DC Supply B Output 1 Lowered Voltage', 'DC Supply B Output 1 Increased Voltage', 'DC B Supply Output 1 Current Limit', 
'DC B Supply Output 1 Over-Voltage Limit', 'MXG RF Initial Freq','MXG RF Initial Pow','MXG LO Initial Freq', 'MXG LO Initial Pow',
'IF Conversion Gain Avg Type (LOG/RMS)', 'IF Conversion Gain Avg Count', 'IF Conversion Gain Marker X-Position', 'MXG RF OFF Freq','MXG RF OFF Pow',
'Reference Level','Auto-Attenuation (OFF:0 / ON:1)','Manual Attenuation','Center Freq','Span','Auto-Resolution Bandwidth (OFF:0 / ON:1)', 'Auto-Video Bandwidth (OFF:0 / ON:1)',
'Resolution Bandwidth','Sweep Points','Sweep Time (seconds)','Auto-Detector (OFF:0 / ON:1)','Manual-Detector (AVG/SAMP)','Vertical-Scale (LOG/LIN)',
'Internal Pre-Amp (OFF:0 / ON:1)','Reference Level','Auto-Attenuation (OFF:0 / ON:1)','Manual Attenuation','Center Freq','Span','Auto-Resolution Bandwidth (OFF:0 / ON:1)', 'Auto-Video Bandwidth (OFF:0 / ON:1)',
'Resolution Bandwidth','Sweep Points','Sweep Time (seconds)','Auto-Detector (OFF:0 / ON:1)','Manual-Detector (AVG/SAMP)','Vertical-Scale (LOG/LIN)',
'Internal Pre-Amp (OFF:0 / ON:1)']

defaults = ['0A0A0A0A0A0A0A0A0A0A0A0A0A0A0A0A', 'C:\\Users\\HSY210000\\Downloads', '0.5', '0.5', '0.1', '100e-3', '2', '1', '1', '0.1', '100e-3', '2', '0.5', '1.1', '100e-3', '2',
'5.001e9', '-90', '5e9', '-90', 'LOG', '100', '1e-3', '5.0001e9', '-130', 
'-70', '1', '10', '1e6', '0', '0', '1', '100e3', '8100', '10e-3', '0', 'AVG', 'LOG', '0',
'-70', '0', '0', '1e6', '0', '0', '1', '100e3', '8000', '10e-3', '0', 'AVG', 'LOG', '0']

def run_script(run_button):
    inputs = []
    for i in range(len(entry_widgets)):
        value = entry_widgets[i].get()
        if not value:
            messagebox.showerror("Missing Input", parameters[i] + " is required.")
            return
        inputs.append(value)

    run_button.config(state=tk.DISABLED)

    def run_measurement_script():
        try:
            subprocess.run(['python', 'measure.py'] + inputs, check=True)

        except subprocess.CalledProcessError:
            messagebox.showerror("Error", "Error running the measurement script.")

        except FileNotFoundError:
            messagebox.showerror("Error", "Measurement script not found.")

        finally:
            root.after(0,run_button.config(state=tk.NORMAL))

    thread = threading.Thread(target=run_measurement_script)
    thread.start()


root = tk.Tk()
root.title("Measurement GUI")

# Allow the columns to be stretch

for i in range(8):  # For 4 label-entry pairs (0-7)
    root.columnconfigure(i, weight=1)

# Headers

headers = ["CSV & DC Supplies", "MXG & IF Gain", "PSA Settings for IF Gain", "PSA Settings for Noise"]
for i in range(len(headers)): 
  currHeader = tk.Label(root, text=headers[i], font=('Arial', 12, 'bold'))
  currHeader.grid(row=0, column=2*i, columnspan=2, pady=(10, 5))

# Defining the entry fields (53 fields necessary)
# Parameter indexes 0-16: Column 1, 16-25: Column 2, 25-39: Column 3, 39:53 Column 4

idx_ranges = ((0,16),(16,25),(25,39),(39,53))
label_col = 0
entry_col = 1
for start,stop in idx_ranges:
  for i in range(stop-start):
    row = i + 1	 # + 1 offset ensures rows start in the next "row" after headers

    label = tk.Label(root, text=parameters[start+i] + ":", font=('Arial', 8), width=40, anchor="e")
    label.grid(row=row, column=label_col, sticky="e", padx=(8, 2), pady=2)

    entry = tk.Entry(root)
    entry.insert(0, defaults[start + i])
    entry.grid(row=row, column=entry_col, padx=(5, 6), pady=2)

    entry_widgets.append(entry)
  label_col += 2
  entry_col += 2

# Run button

run_button = tk.Button(root, text="Run Script", font=('Arial',8), command=lambda: run_script(run_button))
run_button.grid(row=54, column=1, columnspan=6, pady=10)

root.resizable(True, True)  # Allow the window to be resizable

root.mainloop()