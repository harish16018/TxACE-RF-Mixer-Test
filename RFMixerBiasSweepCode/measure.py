# RF MIXER BIAS SWEEP CODE

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


hex_code = sys.argv[1]
output_file_dir = sys.argv[2]
dcA1_V_Start = sys.argv[3]
dcA1_V_Stop = sys.argv[4]
dcA1_V_Step = sys.argv[5]
dcA1_C = sys.argv[6]
dcA1_OVP = sys.argv[7]
dcA2_V_Start = sys.argv[8]
dcA2_V_Stop = sys.argv[9]
dcA2_V_Step = sys.argv[10]
dcA2_C = sys.argv[11]
dcA2_OVP = sys.argv[12]
dcB1_V_lower = sys.argv[13]
dcB1_V_increase = sys.argv[14]
dcB1_C = sys.argv[15]
dcB1_OVP = sys.argv[16]
init_mxgRF_freq = sys.argv[17]
init_mxgRF_pow = sys.argv[18]
init_mxgLO_freq = sys.argv[19]
init_mxgLO_pow = sys.argv[20]
IF_avg_type = sys.argv[21]
IF_avg_count = sys.argv[22]
IF_marker_Xpos = sys.argv[23]
mxgRF_off_freq = sys.argv[24]
mxgRF_off_pow = sys.argv[25]

ref_lvl_IF = sys.argv[26]
auto_att_IF = sys.argv[27]
man_att_IF = sys.argv[28]
center_freq_IF = sys.argv[29]
span_IF = sys.argv[30]
auto_res_ban_IF = sys.argv[31]
auto_vid_ban_IF = sys.argv[32]
res_ban_IF = sys.argv[33]
sweep_points_IF = sys.argv[34]
sweep_time_IF = sys.argv[35]
auto_det_IF = sys.argv[36]
man_det_IF = sys.argv[37]
vert_scal_IF = sys.argv[38]
int_pre_amp_IF = sys.argv[39]

ref_lvl_N = sys.argv[40]
auto_att_N = sys.argv[41]
man_att_N = sys.argv[42]
center_freq_N = sys.argv[43]
span_N = sys.argv[44]
auto_res_ban_N = sys.argv[45]
auto_vid_ban_N = sys.argv[46]
res_ban_N = sys.argv[47]
sweep_points_N = sys.argv[48]
sweep_time_N = sys.argv[49]
auto_det_N = sys.argv[50]
man_det_N = sys.argv[51]
vert_scal_N = sys.argv[52]
int_pre_amp_N = sys.argv[53]



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
def set_biases (dcA,v1,v2):

  dcA.write("INST:SEL OUTP1") # Output 1
  dcA.write("VOLT "+str(v1))

  dcA.write("INST:SEL OUTP2") # Output 2
  dcA.write("VOLT "+str(v2))

  dcA_oe = 1
  dcA.write("OUTP "+str(dcA_oe)) # Turn on outputs 1 and 2



####################################
#
# HELPER FUNCTION TO GENERATE ARRAYS WITH DC A OUTPUTS 1 AND 2 VOLTAGE VALUES
#
####################################
def gen_V_arrays ():
 v1 = []
 v2 = []

 i = 0
 while (round((float(dcA1_V_Start) + float(dcA1_V_Step)*i),2) <= float(dcA1_V_Stop)):
   v1.append(round((float(dcA1_V_Start) + float(dcA1_V_Step)*i),2))
   i += 1

 j = 0
 while (round((float(dcA2_V_Start) + float(dcA2_V_Step)*j),2) <= float(dcA2_V_Stop)):
   v2.append(round((float(dcA2_V_Start) + float(dcA2_V_Step)*j),2))
   j += 1

 return v1,v2



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
def measure_noise (psa,sweep_points):

  psa.timeout = 60000 # Set VISA timeout to 60s for PSA

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


###############################################################################
# Setup up aardvark, power supply A, power supply B, DMM, PSA

print("Measurement Starting")

init_dcA(DC_A)
init_dcB(DC_B)
init_DMM(dmm)
handle = setup_aardvark() 

# Generate DC A outputs 1 and 2 voltage value arrays

biasV_o1, biasV_o2 = gen_V_arrays()

# Convert the hex code into bytes

code_bin = bytes.fromhex(hex_code)

pre_DC = []
post_DC = []
IF_Y = []
avg_noise = []

for k in range( len(biasV_o1) ):

    predc = []
    postdc = []
    ify  = []
    avgn = []
      
    for m in range( len(biasV_o2) ):

       print("DC A Output 1 :",biasV_o1[k],"V"," Output 2 :",biasV_o2[m],"V")
      
       pre_meas_DC_current = 0
       post_meas_DC_current = 0
       IF_marker_Y = 0
       averaged_noise = 0

       set_biases (DC_A,biasV_o1[k],biasV_o2[m])

       time.sleep(0.5) # Delay


       init_MXG(mxg_RF, mxg_LO) # Initialize MXGs

       time.sleep(0.5) # Delay

    
       lower_VDD(DC_B) # Lower shift register VDD

       time.sleep(0.5) # Delay


       send_hex(handle, code_bin) # Send out the hex-code

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


       averaged_noise = measure_noise(psa,sweep_points_N) # Measure noise

       time.sleep(0.5) # Delay


       MXG_LO_off(mxg_LO) # Turn off MXG LO

       time.sleep(0.5) # Delay


       post_meas_DC_current = measure_inv_current(dmm) # Read post-measurement inverter current from DMM

       time.sleep(0.5) # Delay

       predc.append(pre_meas_DC_current)
       postdc.append(post_meas_DC_current)
       ify.append(IF_marker_Y)
       avgn.append(averaged_noise)

    pre_DC.append(predc)
    post_DC.append(postdc)
    IF_Y.append(ify)
    avg_noise.append(avgn)

######################################################################


# Output file generation
noise_file_path = output_file_dir + "\\noise"  + ".csv"
currents_file_path = output_file_dir + "\\DMM_currents" + ".csv"
IF_file_path = output_file_dir + "\\IF_gain" + ".csv"


try:
  with open(noise_file_path, "w", newline="") as of:
    writer = csv.writer(of)
    
    # Write the header row: empty space, then the x_headers (columns)
    writer.writerow([''] + biasV_o1)
    
    # Manually transpose the data (turn rows into columns)
    for i in range(len(biasV_o2)):  # Loop through each row (y_header)
        row = [biasV_o2[i]]  # Start the row with the y_header
        for j in range(len(biasV_o1)):  # Loop through each column (x_header)
            row.append(avg_noise[j][i])  # Add the corresponding value from data
        writer.writerow(row)

except Exception as e:
    print("Unable to write output to file: "+noise_file_path+" due to "+ str(e) +". Exiting program...")
    sys.exit()


try:
 with open(IF_file_path, mode='w', newline='') as of:
    writer = csv.writer(of)
    
    # Write the header row: empty space, then the x_headers (columns)
    writer.writerow([''] + biasV_o1)
    
    # Manually transpose the data (turn rows into columns)
    for i in range(len(biasV_o2)):  # Loop through each row (y_header)
        row = [biasV_o2[i]]  # Start the row with the y_header
        for j in range(len(biasV_o1)):  # Loop through each column (x_header)
            row.append(IF_Y[j][i])  # Add the corresponding value from data
        writer.writerow(row)

except Exception as e:
    print("Unable to write output to file: "+IF_file_path+" due to "+ str(e) +". Exiting program...")
    sys.exit()


try:
 with open(currents_file_path, mode='w', newline='') as of:
    writer = csv.writer(of)
    currents = ['pre', 'post']
    
    # Write the first row: Empty space, followed by output1 headers
    writer.writerow([''] + [''] + biasV_o1)
    
    # Write the data rows for each output2 and its corresponding pre/post categories
    for i in range(len(biasV_o2)):  # Loop over output2 
        for j in range(len(currents)):  # Loop over pre and post
            # Prepare the row: output2 label, current type, and the values for output1
            row = [biasV_o2[i], currents[j]] + [pre_DC[k][i] if currents[j] == 'pre' else post_DC[k][i] for k in range(len(biasV_o1))]
            
            writer.writerow(row)

except Exception as e:
    print("Unable to write output to file: "+currents_file_path+" due to "+ str(e) +". Exiting program...")
    sys.exit()


# Close instrument connections

DC_A.close()
DC_B.close()
mxg_RF.close()
mxg_LO.close()
dmm.close()
psa.close()


print("Measurement Done")



  

  

  

  
  
