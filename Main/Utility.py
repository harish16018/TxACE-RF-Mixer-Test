# Utility Functions

import pandas as pd

def save_trace_to_csv (csv_path, x_val, y_val):
  
  df = pd.DataFrame(zip(x_val,y_val))

  try:
    df.to_csv(csv_path, index=False, header=False)
  except Exception as e:
    print("Unable to write trace to file: "+csv_path+" due to "+ str(e) +". Exiting program...")
    sys.exit()

def generate_array (start, stop, step): # Rounds
  v = []

  i = 0
  while (round((float(start) + float(step)*i),2) <= float(stop)):
   v.append(round((float(start) + float(step)*i),2))
   i += 1

  return v

def bias_current_matrix_to_csv (csv_path, bias_v1, bias_v2, pre_meas, post_meas):

  try:
   with open(csv_path, mode='w', newline='') as output_file:
      writer = csv.writer(output_file)
      currents = ['pre', 'post']
    
      # Write the first row
      writer.writerow([''] + [''] + bias_v1)
    
      # Write the data rows for each voltage in bias_v2 and the corresponding pre and post current
      for i in range(len(bias_v2)):  # Loop over bias_v2
          for j in range(len(currents)):  
              # Prepare the row: output2 label, current type, and the values for output1
              row = [bias_v2[i], currents[j]] + [pre_meas[k][i] if currents[j] == 'pre' else post_meas[k][i] for k in range(len(bias_v1))]
            
              writer.writerow(row)

  except Exception as e:
      print("Unable to write output to file: "+csv_path+" due to "+ str(e) +". Exiting program...")
      sys.exit()


def bias_meas_matrix_to_csv(csv_path, bias_v1, bias_v2, meas_val):

  try:
    with open(csv_path, "w", newline="") as output_file:
      writer = csv.writer(output_file)
    
      # Write the header row
      writer.writerow([''] + bias_v1)
    
      # Manually transpose the data (turn rows into columns)
      for i in range(len(bias_v2)):  # Loop through each row
          row = [bias_v2[i]]  
          for j in range(len(bias_v1)):  # Loop through each column
              row.append(meas_val[j][i])  # Add the corresponding value from meas_val
          writer.writerow(row)

  except Exception as e:
      print("Unable to write output to file: "+csv_path+" due to "+ str(e) +". Exiting program...")
      sys.exit()
  