import pyvisa
import Main.PSA as PSA
import Main.Measurements as Meas

rm = pyvisa.ResourceManager()
psa_id = 'TCPIP0::192.168.0.8::inst0::INSTR'

psa = PSA.get_handle(rm, psa_id)

# M1

PSA.attenuation(psa,'OFF',0)
PSA.vert_scal(psa, 'LIN')
PSA.frequency(psa, '1e6', 0)
PSA.bandwidth(psa, 'OFF', 'ON', '91e3')
PSA.sweep(psa, 8192, '110e-3')
PSA.avg_type(psa, 'LOG')
PSA.detection(psa, 'OFF', 'SAMP')
PSA.pre_amp(psa, 'OFF')
PSA.avg_en(psa, 'OFF')

for a in range(50):
  print("On M1, trace "+str(a+1))
  Meas.measure_noise(psa, r"C:\Users\HSY210000\Documents\Measurements\Measurement1\meas"+str(a+1)+".csv")



# M2

PSA.attenuation(psa,'OFF',0)
PSA.vert_scal(psa, 'LIN')
PSA.frequency(psa, '1e6', 0)
PSA.bandwidth(psa, 'OFF', 'ON', '91e3')
PSA.sweep(psa, 8192, '110e-3')
PSA.avg_type(psa, 'RMS')
PSA.detection(psa, 'OFF', 'SAMP')
PSA.pre_amp(psa, 'OFF')
PSA.avg_en(psa, 'OFF')

for a in range(50):
  print("On M2, trace "+str(a+1))
  Meas.measure_noise(psa, r"C:\Users\HSY210000\Documents\Measurements\Measurement2\meas"+str(a+1)+".csv")