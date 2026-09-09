import usbdevice



class ltc5599:
    def __init__(self, device):
        self.device = device
        
    def write_reg(self, address, setting, width, offset):
        mask = 0xffff & ~((2**width - 1) << offset)
        prev = int.from_bytes(self.read(address), usbdevice.ENDIAN)
        value = prev & mask
        value |= ((setting) << offset)
        
        self.write(address, value)
        
    def read_reg(self, address, width, offset):
        mask = 0xffff & ((2**width - 1) << offset)
        value = int.from_bytes(self.read(address), usbdevice.ENDIAN)
        
        return (value & mask) >> offset
        
    def set_lo(self, setting):
        self.write_reg(0x00, setting, 7, 0)
        
    def write(self, address, value):
        self.device.write(usbdevice.COMMAND_MOD_WRITE, address.to_bytes(1, usbdevice.ENDIAN) + value.to_bytes(1, usbdevice.ENDIAN))
        
    def read(self, address):
        self.device.write(usbdevice.COMMAND_MOD_READ, address.to_bytes(1, usbdevice.ENDIAN))
        
        return self.device.read(1)