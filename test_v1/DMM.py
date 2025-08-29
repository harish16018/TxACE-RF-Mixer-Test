# Driver for DMM (Digital Multi-Meter)


## Get handle

def get_handle (instr_id):
  try:
    handle = rm.open_resource(instr_id)
  except:
    print("Unable to open GPIB connection to the DMM. Exiting...")
    sys.exit()
  
  return handle


## Configure current measurement

def config_curr_meas (handle, auto_range_en):

  handle.write("CURR:DC:RANG:AUTO "+str(auto_range_en))
  handle.write("CONF:CURR:DC")


## Set measurement sample count

def set_samples (handle, sample_count):

  handle.write("SAMP:COUN "+str(sample_count))



## Measure average current

def meas_avg_curr (handle, timeout, sample_count):

  dmm.timeout = timeout
  dmm.write("TRIG:SOUR BUS") # Set the trigger to the software bus (remote interface)
  dmm.write("INIT") # Set the DMM in the wait-for-trigger state
  dmm.write("*TRG") # Trigger the DMM
  samples = dmm.query("FETC?") # Retrieve the samples from the DMM as a string

  samp_lst = samples.split(",")[:-1] # Convert the string of samples into a list and ignoring the last value (which is '\n')
  for i in range(len(samp_lst)): 
    samp_lst[i] = float(samp_lst[i]) # Convert all the samples from string into float

  meas_DC_current = sum(samp_lst) / sample_count
  meas_DC_current *= 1000 # Convert to milli amps

  return meas_DC_current







 
