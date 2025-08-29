import pyvisa
import Main.PSA as PSA
import Main.Measurements as Meas

rm = pyvisa.ResourceManager()
psa_id = 'TCPIP0::192.168.0.8::inst0::INSTR'

psa = PSA.get_handle(rm, psa_id)

print("hello")


