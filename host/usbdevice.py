import sys
import time
import array
import usb1

TIMEOUT_MS = 1000

ENDPOINT_IN = 0x81
ENDPOINT_OUT = 0x1

PACKET_SIZE = 64

TRANSFER_LIMIT = 64

COMMAND_NONE = 0x01
COMMAND_DAC_STREAM = 0x02
COMMAND_PLL_READ = 0x03
COMMAND_PLL_WRITE = 0x04
COMMAND_MOD_READ = 0x05
COMMAND_MOD_WRITE = 0x06
COMMAND_DAC_REQUEST = 0x07

ENDIAN = "little"
PREAMBLE = (0xdeadbeef).to_bytes(4, ENDIAN)

def cbk(xfer):
    xfer.getUserData().bytes_written += PACKET_SIZE

class usbdevice:
    def __init__(self, handle, context):
        self.handle = handle
        self.context = context
        self.transfers = []
        self.buffers = []
        self.bytes_written = 0
        
        for i in range(TRANSFER_LIMIT):
            self.buffers.append(bytearray(PACKET_SIZE))
            xfer = handle.getTransfer()
            xfer.setBulk(ENDPOINT_OUT, self.buffers[i], timeout = TIMEOUT_MS, callback = cbk, user_data = self)
            
            self.transfers.append(xfer)
    
    def is_busy_async(self):
        for xfer in self.transfers:
            if xfer.isSubmitted():
                return True
                
        return False
        
    def write_async(self, data):
        assert(len(data) <= PACKET_SIZE)
        
        padding = PACKET_SIZE - len(data)
        
        if (padding > 0):
            data = data + bytearray(padding)
        
        for idx, xfer in enumerate(self.transfers):
            if xfer.isSubmitted():
                continue
            
            self.buffers[idx][:] = data
            #xfer.setBuffer(self.buffers[idx])
            xfer.submit()

            return
    
    def write_raw(self, data):
        bytes = 0
        try:
            bytes = self.handle.bulkWrite(ENDPOINT_OUT, data, timeout = TIMEOUT_MS)
        except usb1.USBErrorTimeout as e:
            print(f"Write timeout! Expected {len(data)}, transferred {e.transferred}")
            
        return bytes
    
    def read(self, len):
        return self.handle.bulkRead(ENDPOINT_IN, len, timeout = TIMEOUT_MS)
        
    def write(self, command, data):
        data = PREAMBLE + command.to_bytes(1, ENDIAN) + data
        """
        padding = 64 - len(data)
        
        if (padding > 0):
            data = data + bytearray(padding)
        """
        self.write_raw(data)