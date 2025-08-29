# Aardvark functions using aardvark python library and dll

## Detect aardvark device

def detect_aardvark():
  (num, port, id) = aa_find_devices_ext(16,16)
  if (num == 0): 
    print("Aardvark device not found. Exiting program...")
    sys.exit()
  return port[0]



## Configure aardvark device

def setup_aardvark (mode, bitrate):
  port = detect_aardvark()

  handle = aa_open(port)
  aa_configure(handle, AA_CONFIG_SPI_I2C)
  aa_target_power(handle, AA_TARGET_POWER_BOTH)

  # Setup the clock phase
  aa_spi_configure(handle, mode >> 1, mode & 1, AA_SPI_BITORDER_MSB)

  # Set the bitrate
  aa_spi_bitrate(handle, bitrate)
  return handle


## Write data

def write_data(handle, data):
  data_out = array('B', data)
  data_in = array_u08(len(data_out))
  (count,data_in) = aa_spi_write(handle, data_out, data_in)

  # Aardvark error status
  if (count < 0):
            print("error: %s" % aa_status_string(count))
  elif (count != len(data_out)):
            print("error: only a partial number of bytes written")
            print("  (%d) instead of full (%d)" % (count, num_write))


