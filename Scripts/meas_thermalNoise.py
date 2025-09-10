import pyvisa
import Main.PSA as PSA
import Main.Measurements as Meas

TIMEOUT = 600000

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


# M3

PSA.attenuation(psa,'OFF',0)
PSA.vert_scal(psa, 'LIN')
PSA.frequency(psa, '1e6', 0)
PSA.bandwidth(psa, 'OFF', 'ON', '91e3')
PSA.sweep(psa, 8192, '110e-3')
PSA.avg_type(psa, 'SCAL')
PSA.detection(psa, 'OFF', 'SAMP')
PSA.pre_amp(psa, 'OFF')
PSA.avg_en(psa, 'OFF')

for a in range(50):
  print("On M3, trace "+str(a+1))
  Meas.measure_noise(psa, r"C:\Users\HSY210000\Documents\Measurements\Measurement3\meas"+str(a+1)+".csv")

# M4

PSA.attenuation(psa,'OFF',0)
PSA.vert_scal(psa, 'LOG')
PSA.frequency(psa, '1e6', 0)
PSA.bandwidth(psa, 'OFF', 'ON', '91e3')
PSA.sweep(psa, 8192, '110e-3')
PSA.avg_type(psa, 'LOG')
PSA.detection(psa, 'OFF', 'SAMP')
PSA.pre_amp(psa, 'OFF')
PSA.avg_en(psa, 'OFF')

for a in range(50):
  print("On M4, trace "+str(a+1))
  Meas.measure_noise(psa, r"C:\Users\HSY210000\Documents\Measurements\Measurement4\meas"+str(a+1)+".csv")



# M5

PSA.attenuation(psa,'OFF',0)
PSA.vert_scal(psa, 'LOG')
PSA.frequency(psa, '1e6', 0)
PSA.bandwidth(psa, 'OFF', 'ON', '91e3')
PSA.sweep(psa, 8192, '110e-3')
PSA.avg_type(psa, 'RMS')
PSA.detection(psa, 'OFF', 'SAMP')
PSA.pre_amp(psa, 'OFF')
PSA.avg_en(psa, 'OFF')

for a in range(50):
  print("On M5, trace "+str(a+1))
  Meas.measure_noise(psa, r"C:\Users\HSY210000\Documents\Measurements\Measurement5\meas"+str(a+1)+".csv")


# M6

PSA.attenuation(psa,'OFF',0)
PSA.vert_scal(psa, 'LOG')
PSA.frequency(psa, '1e6', 0)
PSA.bandwidth(psa, 'OFF', 'ON', '91e3')
PSA.sweep(psa, 8192, '110e-3')
PSA.avg_type(psa, 'SCAL')
PSA.detection(psa, 'OFF', 'SAMP')
PSA.pre_amp(psa, 'OFF')
PSA.avg_en(psa, 'OFF')

for a in range(50):
  print("On M6, trace "+str(a+1))
  Meas.measure_noise(psa, r"C:\Users\HSY210000\Documents\Measurements\Measurement6\meas"+str(a+1)+".csv")


# M7

PSA.attenuation(psa,'OFF',0)
PSA.vert_scal(psa, 'LOG')
PSA.frequency(psa, '1e6', 0)
PSA.bandwidth(psa, 'OFF', 'ON', '91e3')
PSA.sweep(psa, 8192, '110e-3')
PSA.avg_type(psa, 'LOG')
PSA.detection(psa, 'OFF', 'SAMP')
PSA.pre_amp(psa, 'OFF')
PSA.wait_for_op(psa,TIMEOUT)

for a in range(50):
  PSA.avg_en(psa, 'ON')
  PSA.avg(psa,2000)
  print("On M7, trace "+str(a+1))
  Meas.measure_noise(psa, r"C:\Users\HSY210000\Documents\Measurements\Measurement7\meas"+str(a+1)+".csv")
  PSA.avg_en(psa, 'OFF')



# M8

PSA.attenuation(psa,'OFF',0)
PSA.vert_scal(psa, 'LOG')
PSA.frequency(psa, '1e6', 0)
PSA.bandwidth(psa, 'OFF', 'ON', '91e3')
PSA.sweep(psa, 8192, '110e-3')
PSA.avg_type(psa, 'RMS')
PSA.detection(psa, 'OFF', 'SAMP')
PSA.pre_amp(psa, 'OFF')
PSA.avg_en(psa, 'OFF')
PSA.wait_for_op(psa,TIMEOUT)

for a in range(50):
  PSA.avg_en(psa, 'ON')
  PSA.avg(psa,2000)
  print("On M8, trace "+str(a+1))
  Meas.measure_noise(psa, r"C:\Users\HSY210000\Documents\Measurements\Measurement8\meas"+str(a+1)+".csv")
  PSA.avg_en(psa, 'OFF')


# M9

PSA.attenuation(psa,'OFF',0)
PSA.vert_scal(psa, 'LIN')
PSA.frequency(psa, '1e6', 0)
PSA.bandwidth(psa, 'OFF', 'ON', '91e3')
PSA.sweep(psa, 8192, '110e-3')
PSA.avg_type(psa, 'LOG')
PSA.detection(psa, 'OFF', 'SAMP')
PSA.pre_amp(psa, 'OFF')
PSA.avg_en(psa, 'ON')
PSA.avg(psa,2000)
PSA.wait_for_op(psa,TIMEOUT)

for a in range(50):
  PSA.avg_en(psa, 'ON')
  PSA.avg(psa,2000)
  print("On M9, trace "+str(a+1))
  Meas.measure_noise(psa, r"C:\Users\HSY210000\Documents\Measurements\Measurement9\meas"+str(a+1)+".csv")
  PSA.avg_en(psa, 'OFF')



# M10

PSA.attenuation(psa,'OFF',0)
PSA.vert_scal(psa, 'LIN')
PSA.frequency(psa, '1e6', 0)
PSA.bandwidth(psa, 'OFF', 'ON', '91e3')
PSA.sweep(psa, 8192, '110e-3')
PSA.avg_type(psa, 'RMS')
PSA.detection(psa, 'OFF', 'SAMP')
PSA.pre_amp(psa, 'OFF')
PSA.avg_en(psa, 'OFF')
PSA.avg_en(psa, 'ON')
PSA.avg(psa,2000)
PSA.wait_for_op(psa,TIMEOUT)

for a in range(50):
  PSA.avg_en(psa, 'ON')
  PSA.avg(psa,2000)
  print("On M10, trace "+str(a+1))
  Meas.measure_noise(psa, r"C:\Users\HSY210000\Documents\Measurements\Measurement10\meas"+str(a+1)+".csv")
  PSA.avg_en(psa, 'OFF')


# M11

PSA.attenuation(psa,'OFF',0)
PSA.vert_scal(psa, 'LOG')
PSA.frequency(psa, '1e9', 0)
PSA.bandwidth(psa, 'OFF', 'ON', '91e3')
PSA.sweep(psa, 8192, '110e-3')
PSA.avg_type(psa, 'LOG')
PSA.detection(psa, 'OFF', 'SAMP')
PSA.pre_amp(psa, 'OFF')
PSA.avg_en(psa, 'OFF')

for a in range(50):
  print("On M11, trace "+str(a+1))
  Meas.measure_noise(psa, r"C:\Users\HSY210000\Documents\Measurements\Measurement11\meas"+str(a+1)+".csv")



# M12

PSA.attenuation(psa,'OFF',0)
PSA.vert_scal(psa, 'LOG')
PSA.frequency(psa, '1e9', 0)
PSA.bandwidth(psa, 'OFF', 'ON', '91e3')
PSA.sweep(psa, 8192, '110e-3')
PSA.avg_type(psa, 'RMS')
PSA.detection(psa, 'OFF', 'SAMP')
PSA.pre_amp(psa, 'OFF')
PSA.avg_en(psa, 'OFF')

for a in range(50):
  print("On M12, trace "+str(a+1))
  Meas.measure_noise(psa, r"C:\Users\HSY210000\Documents\Measurements\Measurement12\meas"+str(a+1)+".csv")


# M13

PSA.attenuation(psa,'OFF',0)
PSA.vert_scal(psa, 'LIN')
PSA.frequency(psa, '1e9', 0)
PSA.bandwidth(psa, 'OFF', 'ON', '91e3')
PSA.sweep(psa, 8192, '110e-3')
PSA.avg_type(psa, 'LOG')
PSA.detection(psa, 'OFF', 'SAMP')
PSA.pre_amp(psa, 'OFF')
PSA.avg_en(psa, 'OFF')

for a in range(50):
  print("On M13, trace "+str(a+1))
  Meas.measure_noise(psa, r"C:\Users\HSY210000\Documents\Measurements\Measurement13\meas"+str(a+1)+".csv")



# M14

PSA.attenuation(psa,'OFF',0)
PSA.vert_scal(psa, 'LIN')
PSA.frequency(psa, '1e9', 0)
PSA.bandwidth(psa, 'OFF', 'ON', '91e3')
PSA.sweep(psa, 8192, '110e-3')
PSA.avg_type(psa, 'RMS')
PSA.detection(psa, 'OFF', 'SAMP')
PSA.pre_amp(psa, 'OFF')
PSA.avg_en(psa, 'OFF')

for a in range(50):
  print("On M14, trace "+str(a+1))
  Meas.measure_noise(psa, r"C:\Users\HSY210000\Documents\Measurements\Measurement14\meas"+str(a+1)+".csv")