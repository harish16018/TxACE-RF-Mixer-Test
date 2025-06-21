# RF MIXER FULL CHIP MEASUREMENT CODE

from aardvark_py import *
import sys
import pyvisa
import time
import numpy as np
import re
import csv
import datetime
import os

# Global Constants
SPI_BITRATE = 100 # Hz
SPI_MODE = 1 # pol=0 ; phase=1


# Parameters (from GUI)

input_file_dir     = sys.argv[1]
output_file_dir    = sys.argv[2]
trace_file_dir     = sys.argv[3]
dcA1_V             = sys.argv[4]
dcA1_C             = sys.argv[5]
dcA1_OVP           = sys.argv[6]
dcA2_V             = sys.argv[7]
dcA2_C             = sys.argv[8]
dcA2_OVP           = sys.argv[9]
dcB1_V_lower       = sys.argv[10]
dcB1_V_increase    = sys.argv[11]
dcB1_C             = sys.argv[12]
dcB1_OVP           = sys.argv[13]
init_mxgRF_freq    = sys.argv[14]
init_mxgRF_pow     = sys.argv[15]
init_mxgLO_freq    = sys.argv[16]
init_mxgLO_pow     = sys.argv[17]
IF_avg_type        = sys.argv[18]
IF_avg_count       = sys.argv[19]
IF_marker_Xpos     = sys.argv[20]
mxgRF_off_freq     = sys.argv[21]
mxgRF_off_pow      = sys.argv[22]

ref_lvl_IF         = sys.argv[23]
auto_att_IF        = sys.argv[24]
man_att_IF         = sys.argv[25]
center_freq_IF     = sys.argv[26]
span_IF            = sys.argv[27]
auto_res_ban_IF    = sys.argv[28]
auto_vid_ban_IF    = sys.argv[29]
res_ban_IF         = sys.argv[30]
sweep_points_IF    = sys.argv[31]
sweep_time_IF      = sys.argv[32]
auto_det_IF        = sys.argv[33]
man_det_IF         = sys.argv[34]
vert_scal_IF       = sys.argv[35]
int_pre_amp_IF     = sys.argv[36]

ref_lvl_N          = sys.argv[37]
auto_att_N         = sys.argv[38]
man_att_N          = sys.argv[39]
center_freq_N      = sys.argv[40]
span_N             = sys.argv[41]
auto_res_ban_N     = sys.argv[42]
auto_vid_ban_N     = sys.argv[43]
res_ban_N          = sys.argv[44]
sweep_points_N     = sys.argv[45]
sweep_time_N       = sys.argv[46]
auto_det_N         = sys.argv[47]
man_det_N          = sys.argv[48]
vert_scal_N        = sys.argv[49]
int_pre_amp_N      = sys.argv[50]




####################################
#
# GET INPUT CSV FILENAMES
#
####################################
def get_filenames ():
  file_names = []
  for root, dirs, files in os.walk(input_file_dir):
    for file in files:
        if file.endswith(".csv"):
            file_names.append(file)
  
  if (not file_names):
    print("No CSV files found in the specified input directory "+input_file_dir+" Exiting program...")
    sys.exit()

  return file_names

####################################
#
# DETECT AARDVARK DEVICE
#
####################################
def detect_aardvark():
  (num, port, id) = aa_find_devices_ext(16,16)
  if (num == 0): 
    print("Aardvark device not found. Exiting program...")
    sys.exit()
  return port[0]

####################################
#
# CONFIGURE AARDVARK DEVICE
#
####################################
def setup_aardvark ():
  port = detect_aardvark()
  mode = SPI_MODE
  bitrate = SPI_BITRATE

  handle = aa_open(port)
  aa_configure(handle, AA_CONFIG_SPI_I2C)
  aa_target_power(handle, AA_TARGET_POWER_BOTH)

  # Setup the clock phase
  aa_spi_configure(handle, mode >> 1, mode & 1, AA_SPI_BITORDER_MSB)

  # Set the bitrate
  aa_spi_bitrate(handle, SPI_BITRATE)
  return handle

####################################
#
# SEND OUT HEX CODE FROM AARDVARK DEVICE
#
####################################
def send_hex(handle, hex_code):
  print(hex_code)
  data_out = array('B', hex_code)
  data_in = array_u08(len(data_out))
  (count,data_in) = aa_spi_write(handle, data_out, data_in)

  # Aardvark error status
  if (count < 0):
            print("error: %s" % aa_status_string(count))
  elif (count != len(data_out)):
            print("error: only a partial number of bytes written")
            print("  (%d) instead of full (%d)" % (count, num_write))


####################################
#
# INITIALIZE POWER SUPPLY A
#
# (Over-voltage protection and current limit)
#
####################################
def init_dcA (dcA):

  dcA1_OVP_en = 1
  dcA2_OVP_en = 1

  dcA.write("INST:SEL OUTP1") # Output 1
  dcA.write("CURR "+str(dcA1_C))
  dcA.write("VOLT:PROT:STAT "+str(dcA1_OVP_en))
  dcA.write("VOLT:PROT "+str(dcA1_OVP))

  dcA.write("INST:SEL OUTP2") # Output 2
  dcA.write("CURR "+str(dcA2_C))
  dcA.write("VOLT:PROT:STAT "+str(dcA2_OVP_en))
  dcA.write("VOLT:PROT "+str(dcA2_OVP))


####################################
#
# INITIALIZE POWER SUPPLY B
#
# (Over-voltage protection and current limit)
#
####################################
def init_dcB (dcB):

  dcB1_OVP_en = 1

  dcB.write("INST:SEL OUTP1") # Output 1
  dcB.write("CURR "+str(dcB1_C))
  dcB.write("VOLT:PROT:STAT "+str(dcB1_OVP_en))
  dcB.write("VOLT:PROT "+str(dcB1_OVP)) 


####################################
#
# INITIALIZE DMM
#
####################################
def init_DMM (dmm):

  dmm_auto_range_en = 0
  dmm.write("CURR:DC:RANG:AUTO "+str(dmm_auto_range_en)) # Enable auto range

  dmm.write("CONF:CURR:DC") # Configure the DMM to measure DC current

  dmm_sample_count = 20 
  dmm.write("SAMP:COUN "+str(dmm_sample_count)) # Set the sample count to 20




####################################
#
# INITIALIZE MXGs
#
####################################
def init_MXG (mxg_RF, mxg_LO):

  mxgRF_mod_en = 0
  mxgLO_mod_en = 0
  mxgLO_oe = 0
  mxgRF_oe = 0

  mxg_RF.write("FREQ "+str(init_mxgRF_freq))
  mxg_RF.write("POW "+str(init_mxgRF_pow))
  mxg_RF.write("OUTP:MOD "+str(mxgRF_mod_en)) # Disable Modulation
  mxg_RF.write("OUTP "+str(mxgRF_oe)) # Output off

  mxg_LO.write("FREQ "+str(init_mxgLO_freq))
  mxg_LO.write("POW "+str(init_mxgLO_pow))
  mxg_LO.write("OUTP:MOD "+str(mxgLO_mod_en)) # Disable Modulation
  mxg_LO.write("OUTP "+str(mxgLO_oe)) # Output off



####################################
#
# INITIALIZE PSA
#
####################################
def init_psa (psa,ref_lvl,auto_att,man_att,center_freq,span,auto_res_ban,auto_vid_ban,res_ban,sweep_points,sweep_time,auto_det,man_det,vert_scal,int_pre_amp):

  # Reset
  psa.write("*RST")

  # Configure level
  psa.write("DISP:WIND:TRAC:Y:RLEV "+str(ref_lvl)) # Set reference level
  psa.write("POW:ATT:AUTO "+str(auto_att)) # Turn auto attenuation ON/OFF
  psa.write("POW:ATT "+str(man_att)) # Set manual attenuation

  # Configure Frequency
  psa.write(":FREQ:CENT "+str(center_freq)) # Set center frequency
  psa.write(":FREQ:SPAN "+str(span)) # Set span

  # Configure Sweep Coupling
  psa.write("BAND:AUTO "+str(auto_res_ban)) # Turn auto resolution bandwidth ON/OFF
  psa.write("BAND:VID:AUTO "+str(auto_vid_ban)) # Turn auto video bandwidth ON/OFF
  psa.write("BAND "+str(res_ban)) # Set manual resolution bandwidth
  psa.write("SWE:POIN "+str(sweep_points)) # Set sweep points
  psa.write("SWE:TIME "+str(sweep_time)) # Set sweep time

  # Configure Acquistion
  psa.write("DET:AUTO "+str(auto_det)) # Turn auto detector ON/OFF
  psa.write("DET "+str(man_det)) # Set manual detector type (Average/Sample)
  psa.write(":DISP:WIND:TRAC:Y:SPAC "+str(vert_scal)) # Set vertical scale type (Linear/Logarithmic)

  # Configure Amplitude
  psa.write("POW:GAIN "+str(int_pre_amp)) # Turn internal pre-amp ON/OFF



####################################
#
# SET BIASES (ON POWER SUPPLY A - OUTPUTS 1 AND 2)
#
####################################
def set_biases (dcA):

  dcA.write("INST:SEL OUTP1") # Output 1
  dcA.write("VOLT "+str(dcA1_V))

  dcA.write("INST:SEL OUTP2") # Output 2
  dcA.write("VOLT "+str(dcA2_V))

  dcA_oe = 1
  dcA.write("OUTP "+str(dcA_oe)) # Turn on outputs 1 and 2



####################################
#
# LOWER SHIFT REGISTER VDD (DC B OUTPUT 2)
#
####################################
def lower_VDD (dcB):
  
  dcB_oe = 1
  dcB.write("VOLT "+str(dcB1_V_lower)) # Lower VDD
  dcB.write("OUTP "+str(dcB_oe)) # Output on



####################################
#
# INCREASE SHIFT REGISTER VDD (DC B OUTPUT 2)
#
####################################
def increase_VDD (dcB):

  dcB.write("VOLT "+str(dcB1_V_increase)) # Increase VDD



####################################
#
# MEASURE INVERTER CURRENT USING DMM
#
####################################
def measure_inv_current (dmm):

  # Reading 20 samples from the DMM
  dmm.timeout = 30000 # Set timeout time to 30s
  dmm.write("TRIG:SOUR BUS") # Set the trigger to the software bus (remote interface)
  dmm.write("INIT") # Set the DMM in the wait-for-trigger state
  dmm.write("*TRG") # Trigger the DMM
  samples = dmm.query("FETC?") # Retrieve the samples from the DMM as a string

  samp_lst = samples.split(",")[:-1] # Convert the string of samples into a list and ignoring the last value (which is '\n')
  for i in range(len(samp_lst)): 
    samp_lst[i] = float(samp_lst[i]) # Convert all the samples from string into float

  meas_DC_current = sum(samp_lst) / 20
  meas_DC_current *= 1000 # Convert to milli amps

  return meas_DC_current


####################################
#
# TURN ON LO
#
####################################
def LO_on (mxg_LO):

  mxgLO_oe = 1
  mxg_LO.write("OUTP "+str(mxgLO_oe)) # Output on



####################################
#
# TURN ON RF
#
####################################
def RF_on (mxg_RF):

  mxgRF_oe = 1
  mxg_RF.write("OUTP "+str(mxgRF_oe)) # Output on




####################################
#
# MEASURE IF CONVERSION GAIN
#
####################################
def measure_IF_tone (psa):

  psa.timeout = 60000 # Set VISA timeout to 60s for PSA

  psa.write("CALC:MARK1:STAT 1") # Turn on marker 1
  
  psa.write("CALC:MARK1:X "+str(IF_marker_Xpos)) # Set marker 1 x-position

  # Turn on averaging
  avg_en = 1
  psa.write("AVER "+str(avg_en))

  # Set averaging type
  psa.write("AVER:TYPE "+str(IF_avg_type)) # Set averaging type (Logarithmic/RMS/Scalar)
  
  # Wait for the average count to complete by polling the instrument (Wait for operation)

  psa.write("*CLS") # Clear status registers
  psa.write("AVER:COUN "+str(IF_avg_count)+"; *OPC") # Set average count and tell the instrument to set the bit when done (this command starts the averaging process)

  psa.write("*WAI") # Call Wait-For-Operation to ensure any alignment finishes before averaging begins

  status = 0; # Bit of event status register (ESR) to be checked

  while(True):
    if(int(status) == 1):
      break; # Polling is over since ESR condition satisfied

    status = psa.query("*ESR?")

  marker1_y_meas = psa.query("CALC:MARK1:Y?") # Query marker 1 y-position (amplitude (power))

  # Turn off averaging
  avg_en = 0
  psa.write("AVER "+str(avg_en))

  psa.write("*WAI") # Call Wait-For-Operation to ensure any alignment finishes before PSA is reset to measure noise (next step)
  
  return marker1_y_meas



####################################
#
# MEASURE NOISE
#
####################################
def measure_noise (psa,sweep_points, trace_csv_filename):

  psa.timeout = 60000 # Set VISA timeout to 60s for PSA

  file_data = np.empty((int(sweep_points), 2)) # 2 since two columns for x-values (freq/time) and y-values (amp)
  x_val = np.empty(int(sweep_points))
  amp_val = np.empty(int(sweep_points))

  psa.write("*WAI") # Call Wait-For-Operation to ensure any alignment finishes before trace is saved

  psa.write(r"MMEM:STOR:TRAC TRACE1, 'C:\MIXER.CSV'") # Current trace is stored on instrument at path

  trace_data = psa.query("MMEM:DATA? 'C:\\MIXER.CSV'") # Get the trace data from the file on instrument
  psa.write(r"MMEM:DEL 'C:\MIXER.CSV'") # Delete trace file on instrument

  # Trace CSV Processing
  substr = r"Trace \d\n.*?,.*?\n" # This is the unique substring with which the header string teriminates
  idx = re.search(substr, trace_data).end() # Find where the header string terminates
  val_str = trace_data[idx:] # Extracting just the trace values in the string
  values = val_str.split("\n")[:-2] # Convert into list, ignore last 2 empty strings in the end of the list due to splitting by '\n'

  for x in range(len(values)): 
    x_val[x] = float(values[x].split(', ')[0])
    amp_val[x] = float(values[x].split(', ')[1])

  # Write Trace to CSV
  file_data[:, 0] = x_val
  file_data[:, 1] = amp_val

  try:
    with open(trace_csv_filename, "w", newline="") as f:
      writer = csv.writer(f)
      writer.writerows(file_data)  # Write data
  except Exception as e:
    print("Unable to write trace to file: "+trace_csv_filename+" due to "+ str(e) +". Exiting program...")
    sys.exit()
 
  # Calculate average noise
  averaged_noise = float(np.average(amp_val))

  return averaged_noise



####################################
#
# TURN OFF LO
#
####################################
def MXG_LO_off (mxg_LO):

  mxgLO_oe = 0

  mxg_LO.write("OUTP "+str(mxgLO_oe)) # Output off



####################################
#
# TURN OFF RF
#
####################################
def MXG_RF_off (mxg_RF):

  mxgRF_oe = 0

  mxg_RF.write("FREQ "+str(mxgRF_off_freq))
  mxg_RF.write("POW "+str(mxgRF_off_pow))
  mxg_RF.write("OUTP "+str(mxgRF_oe)) # Output off





####################################################################################################################################
#
#  MAIN CODE
#
####################################################################################################################################

print("Opening instrument connections")


# Establish and verify connection with instruments

rm = pyvisa.ResourceManager();

DC_A_id = 'GPIB0::3::INSTR' 
DC_B_id = 'GPIB0::10::INSTR'
mxg_RF_id = 'GPIB0::19::INSTR'
mxg_LO_id = 'GPIB0::20::INSTR'
dmm_id = 'GPIB0::23::INSTR' 
psa_id = 'TCPIP0::192.168.0.8::inst0::INSTR'


try:
  DC_A = rm.open_resource(DC_A_id) 
  DC_B = rm.open_resource(DC_B_id)
except:
  print("Unable to open GPIB connection to the power supplies. Check both and try again.")
  sys.exit()


try:
 mxg_RF = rm.open_resource(mxg_RF_id)   
 mxg_LO = rm.open_resource(mxg_LO_id)
except:
  print("Unable to open GPIB connection to the MXGs. Check both and try again.")
  sys.exit()

try:
 dmm = rm.open_resource(dmm_id)  
except:
  print("Unable to open GPIB connection to the DMM. Check and try again.")
  sys.exit()

try:
    psa = rm.open_resource(psa_id)
except:
    print("Unable to open connection to PSA. Check LAN connection and try again")
    sys.exit()

print("All instruments connected successfully...")

#############################################################################################
# Setup up aardvark, power supply B, DMM, PSA, power supply A (biases)

print("Measurement Starting")

init_dcA(DC_A)
init_dcB(DC_B)
init_DMM(dmm)
handle = setup_aardvark() 


file_names = get_filenames()


# Main input file processing

for i in range(len(file_names)):

  codes_bin = [] # Hex-codes in bytes form (for aardvark)
  codes_str = [] # Hex-codes in str form (for output file)
  pre_DC = []
  post_DC = []
  IF_Y = []
  avg_noise = []
  tmstmp = []

  # Read in all the hex-codes in the current input file into a list where they are stored as bytes (binary)
  
  try:
    with open(input_file_dir+'\\'+file_names[i], 'r') as f:
     fr = csv.reader(f)
     for code in fr:
       hex_code = bytes.fromhex(code[0])
       codes_bin.append(hex_code)
       codes_str.append(code[0])
  except Exception as e:
    print("Unable to open hex codes file: "+file_names[i]+" due to "+ str(e) +". Exiting program...")
    sys.exit()

  print("Opened input CSV " + file_names[i] + " successfully and codes read...")
  

  # Hex-code processing
  
  for j in range(len(codes_bin)):
    current_hex = codes_str[j]
    current_hex_bin = codes_bin[j]
    
    
    trace_file_path = trace_file_dir + "\\" + str(i+1) + "_" + str(j+1) + "_" + current_hex + ".csv"

    pre_meas_DC_current = 0
    post_meas_DC_current = 0
    IF_marker_Y = 0
    averaged_noise = 0
    timestamp = 0

    set_biases(DC_A) # Setup amplifier biases

    time.sleep(0.5) # Delay


    init_MXG(mxg_RF, mxg_LO) # Initialize MXGs

    time.sleep(0.5) # Delay

    
    lower_VDD(DC_B) # Lower shift register VDD

    time.sleep(0.5) # Delay


    send_hex(handle, current_hex_bin) # Send out the hex-code

    time.sleep(0.5) # Delay


    increase_VDD(DC_B) # Increase shift register VDD back to normal

    time.sleep(0.5) # Delay


    pre_meas_DC_current = measure_inv_current(dmm) # Read pre-measurement inverter current from DMM

    time.sleep(0.5) # Delay


    LO_on(mxg_LO) # Turn on MXG LO

    time.sleep(0.5) # Delay


    RF_on(mxg_RF) # Turn on MXG RF

    time.sleep(0.5) # Delay


    init_psa(psa,ref_lvl_IF,auto_att_IF,man_att_IF,center_freq_IF,span_IF,auto_res_ban_IF,auto_vid_ban_IF,res_ban_IF,sweep_points_IF,sweep_time_IF,auto_det_IF,man_det_IF,vert_scal_IF,int_pre_amp_IF) # Initialize PSA for IF Gain

    time.sleep(0.5) # Delay


    IF_marker_Y = measure_IF_tone(psa) # Perform averaging and measure IF conversion gain tone

    time.sleep(0.5) # Delay


    MXG_RF_off(mxg_RF) # Turn off MXG RF

    time.sleep(0.5) # Delay


    init_psa(psa,ref_lvl_N,auto_att_N,man_att_N,center_freq_N,span_N,auto_res_ban_N,auto_vid_ban_N,res_ban_N,sweep_points_N,sweep_time_N,auto_det_N,man_det_N,vert_scal_N,int_pre_amp_N) # Re-initialize PSA for noise

    time.sleep(0.5) # Delay


    averaged_noise = measure_noise(psa,sweep_points_N, trace_file_path) # Measure noise

    time.sleep(0.5) # Delay


    MXG_LO_off(mxg_LO) # Turn off MXG LO

    time.sleep(0.5) # Delay


    post_meas_DC_current = measure_inv_current(dmm) # Read post-measurement inverter current from DMM

    time.sleep(0.5) # Delay

    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    pre_DC.append(pre_meas_DC_current)
    post_DC.append(post_meas_DC_current)
    IF_Y.append(IF_marker_Y)
    avg_noise.append(averaged_noise)
    tmstmp.append(timestamp)

  # Output file generation
  output_file_path = output_file_dir + "\\output" + str(i+1) + ".csv"
  data = zip(codes_str, pre_DC, IF_Y, avg_noise, post_DC, tmstmp) 

  try:
    with open(output_file_path, "w", newline="") as of:
      writer = csv.writer(of)
      writer.writerows(data)  # Write data
  except Exception as e:
    print("Unable to write output to file: "+output_file_path+" due to "+ str(e) +". Exiting program...")
    sys.exit()

# Close instrument connections

DC_A.close()
DC_B.close()
mxg_RF.close()
mxg_LO.close()
dmm.close()
psa.close()


print("Measurement Done")



  

  

  

  
  
