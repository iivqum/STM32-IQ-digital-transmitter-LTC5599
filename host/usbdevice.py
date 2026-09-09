import sys
import time
import array
import usb1

TIMEOUT_MS = 1000

ENDPOINT_IN = 0x81
ENDPOINT_OUT = 0x1

COMMAND_NONE = 0x01
COMMAND_DAC_STREAM = 0x02
COMMAND_PLL_READ = 0x03
COMMAND_PLL_WRITE = 0x04
COMMAND_MOD_READ = 0x05
COMMAND_MOD_WRITE = 0x06

ENDIAN = "little"
PREAMBLE = (0xdeadbeef).to_bytes(4, ENDIAN)

class usbdevice:
    def __init__(self, handle):
        self.handle = handle
    
    def write_raw(self, data):
        self.handle.bulkWrite(ENDPOINT_OUT, data, TIMEOUT_MS)
    
    def read(self, len):
        return self.handle.bulkRead(ENDPOINT_IN, len, TIMEOUT_MS)
        
    def write(self, command, data):
        self.write_raw(PREAMBLE + command.to_bytes(1, ENDIAN) + data)