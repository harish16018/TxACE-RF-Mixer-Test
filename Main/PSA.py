# Driver for PSA

import pyvisa
import sys

## Get handle

def get_handle (rm, instr_id):
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

def avg_type (handle, avg_type):
  handle.write("AVER:TYPE "+str(avg_type)) # Set averaging type (LOGarithmic (Log-Power (video) averaging)/RMS/SCALar (Voltage averaging))


## Turn averaging on/off

def avg_en (handle, avg_en):
  handle.write("AVER "+str(avg_en))


## Perform averaging

def avg (handle, avg_count):
  handle.write("AVER:COUN "+str(avg_count))



## Wait for operation

def wait_for_op (handle, timeout):
  handle.timeout = timeout
  handle.query("*OPC?")



## Configure reference level

def ref_lvl (handle, ref_lvl):
  handle.write("DISP:WIND:TRAC:Y:RLEV "+str(ref_lvl))



## Configure attenuation

def attenuation (handle, auto_att_en, man_att):
  handle.write("POW:ATT:AUTO "+str(auto_att_en)) # Turn auto attenuation ON/OFF
  handle.write("POW:ATT "+str(man_att)) # Set manual attenuation



## Configure frequency

def frequency (handle, center_freq, span):
    handle.write(":FREQ:CENT "+str(center_freq)) # Set center frequency
    handle.write(":FREQ:SPAN "+str(span)) # Set span



## Configure bandwidth

def bandwidth (handle, auto_res_ban_en, auto_vid_ban_en, res_ban):
  handle.write("BAND:AUTO "+str(auto_res_ban_en)) # Turn auto resolution bandwidth ON/OFF
  handle.write("BAND:VID:AUTO "+str(auto_vid_ban_en)) # Turn auto video bandwidth ON/OFF
  handle.write("BAND "+str(res_ban)) # Set manual resolution bandwidth



## Configure sweep

def sweep (handle, sweep_points, sweep_time):
  handle.write("SWE:POIN "+str(sweep_points)) # Set sweep points
  handle.write("SWE:TIME "+str(sweep_time)) # Set sweep time



## Configure detection

def detection (handle, auto_det_en, man_det):
  handle.write("DET:AUTO "+str(auto_det_en)) # Turn auto detector ON/OFF
  handle.write("DET "+str(man_det)) # Set manual detector type (AVERage/SAMPle)



## Configure vertical scale type

def vert_scal (handle, vert_scal):
  handle.write("DISP:WIND:TRAC:Y:SPAC "+str(vert_scal)) # Set vertical scale type (LINear/LOGarithmic)


## Configure pre_amp

def pre_amp (handle, int_pre_amp_en):
  handle.write("POW:GAIN "+str(int_pre_amp_en))


## Set marker position

def set_marker (handle, marker_num, x_pos):
  handle.write("CALC:MARK"+str(marker_num)+":STAT 1") # Turn on marker
  handle.write("CALC:MARK"+str(marker_num)+":X "+str(x_pos)) # Set marker x-position


## Get marker value

def get_marker (handle, marker_num):
  y_pos = handle.query("CALC:MARK"+str(marker_num)+":Y?") # Query marker y-position
  return y_pos


## Get trace

def get_trace (handle):
  handle.write(r"MMEM:STOR:TRAC TRACE1, 'C:\MIXER.CSV'") # Current trace is stored on instrument at path
  trace_data = handle.query("MMEM:DATA? 'C:\\MIXER.CSV'") # Get the trace data from the file on instrument
  handle.write(r"MMEM:DEL 'C:\MIXER.CSV'") # Delete trace file on instrument 

  return trace_data





  
 

