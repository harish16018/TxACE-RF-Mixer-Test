# Measurements

from . import PSA
from . import PXA
from . import Utility
import re



## PSA Noise measurement 

def measure_noise (handle, csv_path="", save_trace=False, instr='PSA'):
  
  if(instr == 'PSA'):
   trace_data = PSA.get_trace(handle)
   substr = r"Trace \d\n.*?,.*?\n" # This is the unique substring with which the header string teriminates
  elif(instr == 'PXA'):
   trace_data = PXA.get_trace(handle)
   substr = r"Trace \d\n.*?,.*?\n" #

  idx = re.search(substr, trace_data).end() # Find where the header string terminates
  val_str = trace_data[idx:] # Extracting just the trace values in the string
  values = val_str.split("\n")[:-2] # Convert into list, ignore last 2 empty strings in the end of the list due to splitting by '\n'
  
  x_val = []
  amp_val = []

  for x in range(len(values)): 
    x_val.append(float(values[x].split(', ')[0]))
    amp_val.append(float(values[x].split(', ')[1]))

  if save_trace:
    Utility.save_trace_to_csv(csv_path, x_val, amp_val)

  averaged_noise = sum(amp_val) / len(amp_val)

  return averaged_noise



## IF Conversion Gain measurement

def measure_IF_tone (psa, marker_x_pos, avg_type, avg_count):

  timeout = 60000 # VISA timeout 60s
  
  PSA.set_marker(psa, 1, marker_x_pos) # Set marker 1 x-position

  PSA.avg_en(psa, 1) # Turn averaging on

  PSA.avg_type(psa, avg_type) # Set averaging type

  PSA.avg(psa, avg_count) # Perform averaging

  PSA.wait_for_op(psa, timeout) # Wait for averaging to complete

  y_pos = PSA.get_marker(psa, 1) # Get marker 1 y-position

  PSA.avg_en(psa, 0) # Turn averaging off

  return y_pos # Return marker 1 y-position




  

  

  


  
  