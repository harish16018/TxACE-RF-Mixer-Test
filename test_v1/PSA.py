# Driver for PSA


## Get handle

def get_handle (instr_id):
  try:
    handle = rm.open_resource(instr_id)
  except:
    print("Unable to open GPIB connection to the PSA. Exiting...")
    sys.exit()
  
  return handle



## Reset instrument

def reset (handle):
  handle.write("*RST")



## Configure averaging type

def config_aver_type (handle, avg_type):
  handle.write("AVER:TYPE "+str(avg_type))



## Wait for operation

def wait_for_op (handle, timeout):
  handle.timeout = timeout
  handle.query("*OPC?")

