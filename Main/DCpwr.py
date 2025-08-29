# Driver for DC Power Supply


## Get handle

def get_handle (instr_id):
  try:
    handle = rm.open_resource(instr_id)
  except:
    print("Unable to open GPIB connection to the power supplies. Exiting...")
    sys.exit()
  
  return handle



## Set over-voltage protection

def set_OVP (handle, output, OVP_en, OVP):

  handle.write("INST:SEL OUTP"+str(output))
  handle.write("VOLT:PROT:STAT "+str(OVP_en))
  handle.write("VOLT:PROT "+str(OVP))



## Set current limit

def set_current (handle, output, curr_limit):
   
  handle.write("INST:SEL OUTP"+str(output))
  handle.write("CURR "+str(curr_limit))



## Set voltage

def set_voltage (handle, output, voltage):

  handle.write("INST:SEL OUTP"+str(output))
  handle.write("VOLT "+str(voltage))




## Turn output on/off

def output_en (handle, output, output_en):

  handle.write("INST:SEL OUTP"+str(output))
  handle.write("OUTP "+str(output_en))
