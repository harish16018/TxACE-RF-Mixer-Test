# Driver for MXG


## Get handle

def get_handle (instr_id):
  try:
    handle = rm.open_resource(instr_id)
  except:
    print("Unable to open GPIB connection to the MXG. Exiting...")
    sys.exit()
  
  return handle


## Turn output on/off

def output_en (handle, output_en):

  handle.write("OUTP "+str(output_en))


## Set frequency

def set_freq (handle, freq):
  
  handle.write("FREQ "+str(freq))


## Set output power

def set_power (handle, power):
  
  handle.write("POW "+str(power))


## Turn output modulation on/off

def config_output_mod (handle, mod_en):
  
  handle.write("OUTP:MOD "+str(mod_en))

