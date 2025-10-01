import pyvisa
import Main.PSA as PSA
import Main.Measurements as Meas
import Main.Aardvark as Aardvark
import Main.MXG as MXG
import Main.DMM as DMM
import Main.DCpwr as DCpwr
import Main.Utility as Util

####################################
SPI_BITRATE = 100 # Hz
SPI_MODE = 1 # pol=0 ; phase=1
####################################
OVP_A = 
current_A = 

OVP_B = 
current_B =
####################################
v1_start =
v1_stop =  
v1_step = 

v2_start =
v2_stop =  
v2_step = 
####################################
hex_code = 
####################################
dmm_samples = 20
####################################
RF_init_freq = 
RF_init_pow =

LO_init_freq = 
LO_init_pow =

shift_reg_VDD_low =
shift_reg_VDD_normal = 
####################################
if_ref_lvl = 
if_auto_att_en = 
if_man_att = 
if_center_freq = 
if_span = 
if_auto_res_ban_en = 
if_auto_vid_ban_en = 
if_res_ban = 
if_sweep_points = 
if_sweep_time = 
if_auto_det_en =
if_man_det =
if_vert_scal = 
if_int_pre_amp_en =

if_marker_x_pos = 
if_avg_type =
if_avg_count = 
##################################
noise_ref_lvl = 
noise_auto_att_en = 
noise_man_att = 
noise_center_freq = 
noise_span = 
noise_auto_res_ban_en = 
noise_auto_vid_ban_en = 
noise_res_ban = 
noise_sweep_points = 
noise_sweep_time = 
noise_auto_det_en =
noise_man_det =
noise_vert_scal = 
noise_int_pre_amp_en =
##################################
output_file_dir = 




rm = pyvisa.ResourceManager();

# Open instrument connections and setup Aardvark SPI adapter

supply_A = DCpwr.get_handle('GPIB0::3::INSTR')
supply_B = DCpwr.get_handle('GPIB0::10::INSTR')
mxg_RF = MXG.get_handle('GPIB0::19::INSTR')
mxg_LO = MXG.get_handle('GPIB0::20::INSTR')
dmm = DMM.get_handle('GPIB0::23::INSTR')
psa = PSA.get_handle('TCPIP0::192.168.0.8::inst0::INSTR')

aardvark = Aardvark.setup_aardvark(mode=SPI_MODE, bitrate=SPI_BITRATE)


# Setup power supply A

DCpwr.set_OVP(supply_A, output=1, OVP_en='ON', OVP=OVP_A)
DCpwr.set_current(supply_A, output=1, curr_limit=current_A)

DCpwr.set_OVP(supply_A, output=2, OVP_en='ON', OVP=OVP_A)
DCpwr.set_current(supply_A, output=2, curr_limit=current_A)


# Setup power supply B

DCpwr.set_OVP(supply_B, output=1, OVP_en='ON', OVP=OVP_B)
DCpwr.set_current(supply_B, output=1, curr_limit=current_B)

DCpwr.set_OVP(supply_B, output=2, OVP_en='ON', OVP=OVP_B)
DCpwr.set_current(supply_B, output=2, curr_limit=current_B)


# Setup DMM

DMM.config_curr_meas(dmm, auto_range_en='ON') # DMM auto-range enabled and measure mode set to current
DMM.set_samples(dmm, sample_count=dmm_samples)


# Create arrays of voltage values

bias_v1 = Util.generate_array(v1_start, v1_stop, v1_step)
bias_v2 = Util.generate_array(v2_start, v2_stop, v2_step)

# Initialize arrays for measured results

pre_meas_current = []
post_meas_current = []
IF_gain = []
avg_noise = []

for i in bias_v1:
    pre_meas_current.append([])
    post_meas_current.append([])
    IF_gain.append([])
    avg_noise.append([])

# Convert hex-code into bytes

bin_hex = bytes.fromhex(hex_code)

# Loop through bias arrays and perform measurements

for j in range (len(bias_v1)):
  
  for k in range (len(bias_v2)):

     print("DC A Output 1 :",bias_v1[j],"V"," Output 2 :",bias_v2[k],"V")

     # Set bias voltages on supply A
     DCpwr.set_voltage(supply_A, output=1, voltage=bias_v1[j])
     DCpwr.set_voltage(supply_A, output=2, voltage=bias_v2[k])

     DCpwr.output_en(supply_A, output=1, output_en=1)
     DCpwr.output_en(suppy_A, output=1, output_en=1)

     # Configure RF MXG
     MXG.set_freq(mxg_RF, freq=RF_init_freq)
     MXG.set_power(mxg_RF, power=RF_init_pow)
     MXG.config_output_mod(mxg_RF, mod_en=0)
     MXG.output_en(mxg_RF, output_en=0)

     # Configure LO MXG
     MXG.set_freq(mxg_LO, freq=LO_init_freq)
     MXG.set_power(mxg_LO, power=LO_init_pow)
     MXG.config_output_mod(mxg_LO, mod_en=0)
     MXG.output_en(mxg_LO, output_en=0)

     # Lower shift register VDD
     DCpwr.set_voltage(supply_B, output=2, voltage=shift_reg_VDD_low)
     DCpwr.output_en(suppy_B, output=2, output_en=1)
 
     # Send the hex code
     Aardvark.write_data(aardvark, bin_hex)

     # Increase shift register VDD
     DCpwr.set_voltage(supply_B, output=2, voltage=shift_reg_VDD_normal)

     # Read pre-measurement inverter current
     pre_meas_current[j][k] = DMM.meas_avg_curr(dmm, timeout=30000, sample_count=dmm_samples)

     # Turn on RF MXG
     MXG.output_en(mxg_RF, output_en=1)

     # Turn on LO MXG
     MXG.output_en(mxg_LO, output_en=1)

     # Configure PSA for IF gain measurement
     PSA.ref_lvl (psa, ref_lvl=if_ref_lvl)
     PSA.attenuation (psa, auto_att_en=if_auto_att_en, man_att=if_man_att):
     PSA.frequency (psa, center_freq=if_center_freq, span=if_span)
     PSA.bandwidth (psa, auto_res_ban_en=if_auto_res_ban_en, auto_vid_ban_en=if_auto_vid_ban_en, res_ban=if_res_ban)
     PSA.sweep (psa, sweep_points=if_sweep_points, sweep_time=if_sweep_time)
     PSA.detection (psa, auto_det_en=if_auto_det_en, man_det=if_man_det)
     PSA.vert_scal (psa, vert_scal=if_vert_scal)
     PSA.pre_amp (psa, int_pre_amp_en=if_int_pre_amp_en)

     # Measure IF conversion gain
     IF_gain[j][k] = Meas.measure_IF_tone(psa, marker_x_pos=if_marker_x_pos, avg_type=if_avg_type, avg_count=if_avg_count)

     # Turn off RF MXG
     MXG.set_freq(mxg_RF, freq=RF_off_freq)
     MXG.set_power(mxg_RF, power=RF_off_pow)
     MXG.output_en(mxg_RF, output_en=0)

     # Configure PSA for noise measurement
     PSA.ref_lvl (psa, ref_lvl=noise_ref_lvl)
     PSA.attenuation (psa, auto_att_en=noise_auto_att_en, man_att=noise_man_att):
     PSA.frequency (psa, center_freq=noise_center_freq, span=noise_span)
     PSA.bandwidth (psa, auto_res_ban_en=noise_auto_res_ban_en, auto_vid_ban_en=noise_auto_vid_ban_en, res_ban=noise_res_ban)
     PSA.sweep (psa, sweep_points=noise_sweep_points, sweep_time=noise_sweep_time)
     PSA.detection (psa, auto_det_en=noise_auto_det_en, man_det=noise_man_det)
     PSA.vert_scal (psa, vert_scal=noise_vert_scal)
     PSA.pre_amp (psa, int_pre_amp_en=noise_int_pre_amp_en)

     # Measure noise
     avg_noise[j][k] = Meas.measure_noise (psa, save_trace=False)

     # Turn off LO MXG
     MXG.output_en(mxg_LO, output_en=0)

     # Read post-measurement inverter current
     post_meas_current[j][k] = DMM.meas_avg_curr(dmm, timeout=30000, sample_count=dmm_samples)

# Write data to CSV

Utility.bias_current_matrix_to_csv(output_file_dir + "\\DMM_currents" + ".csv", bias_v1, bias_v2, pre_meas_current, post_meas_current)
Utility.bias_meas_matrix_to_csv(output_file_dir + "\\IF_gain" + ".csv", bias_v1, bias_v2, IF_gain)
Utility.bias_meas_matrix_to_csv(output_file_dir + "\\noise"  + ".csv", bias_v1, bias_v2, avg_noise)

# Close instrument connections

supply_A.close()
supply_B.close()
mxg_RF.close()
mxg_LO.close()
dmm.close()
psa.close()

print("Measurement Done")