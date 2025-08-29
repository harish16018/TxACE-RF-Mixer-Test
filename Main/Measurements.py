# Measurements

from . import PSA
from . import Utility
import re



## Noise measurement 

def measure_noise (psa, csv_path):
  
  trace_data = PSA.get_trace(psa)

  substr = r"Trace \d\n.*?,.*?\n" # This is the unique substring with which the header string teriminates
  idx = re.search(substr, trace_data).end() # Find where the header string terminates
  val_str = trace_data[idx:] # Extracting just the trace values in the string
  values = val_str.split("\n")[:-2] # Convert into list, ignore last 2 empty strings in the end of the list due to splitting by '\n'
  
  x_val = []
  amp_val = []

  for x in range(len(values)): 
    x_val.append(float(values[x].split(', ')[0]))
    amp_val.append(float(values[x].split(', ')[1]))

  Utility.save_trace_to_csv(csv_path, x_val, amp_val)

  averaged_noise = sum(amp_val) / len(amp_val)

  return averaged_noise

  