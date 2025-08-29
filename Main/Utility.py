# Utility Functions

import pandas as pd

def save_trace_to_csv (csv_path, x_val, y_val):
  
  df = pd.DataFrame(zip(x_val,y_val))

  try:
    df.to_csv(csv_path, index=False, header=False)
  except Exception as e:
    print("Unable to write trace to file: "+csv_path+" due to "+ str(e) +". Exiting program...")
    sys.exit()
  