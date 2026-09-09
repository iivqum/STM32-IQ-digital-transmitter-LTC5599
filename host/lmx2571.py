import usbdevice

REGS = [
	0x3C, 0x3A, 0x35, 0x2F, 0x2E, 0x2A, 0x29, 0x28,
	0x27, 0x23, 0x22, 0x21, 0x20, 0x1F, 0x1E, 0x1D,
	0x1C, 0x1B, 0x1A, 0x19, 0x18, 0x17, 0x16, 0x15,
	0x14, 0x13, 0x12, 0x11, 0x10, 0x0F, 0x0E, 0x0D,
	0x0C, 0x0B, 0x0A, 0x09, 0x08, 0x07, 0x06, 0x05,
	0x04, 0x03, 0x02, 0x01, 0x00
]
# MHz
MIN_VCO_FREQUENCY = 4300
MAX_VCO_FREQUENCY = 5376
REFERENCE_FREQUENCY = 24

DITHER_DISABLED = 0
DITHER_WEAK = 1
DITHER_MEDIUM = 2
DITHER_STRONG = 3

CP_GAIN_1X = 0
CP_GAIN_2X = 1
CP_GAIN_1P5X = 2
CP_GAIN_2P5X = 3

OUTBUF_TYPE_OPEN_DRAIN = 0
OUTBUF_TYPE_PUSHPULL = 1

MUXOUT_READBACK = 0
MUXOUT_LOCK_DETECT = 1

CHANNEL_F1 = 0x00
CHANNEL_F2 = 0x10

F2_LOOPFILTER_R4_BYPASS = 0
F2_LOOPFILTER_R4_3K2 = 1
F2_LOOPFILTER_R4_1K6 = 2
F2_LOOPFILTER_R4_1K1 = 3
F2_LOOPFILTER_R4_800 = 4
F2_LOOPFILTER_R4_640 = 5
F2_LOOPFILTER_R4_533 = 6
F2_LOOPFILTER_R4_457 = 7

LOOPFILTER_R3_BYPASS = 0
LOOPFILTER_R3_3K2 = 1
LOOPFILTER_R3_1K6 = 2
LOOPFILTER_R3_1K1 = 3
LOOPFILTER_R3_800 = 4
LOOPFILTER_R3_640 = 5
LOOPFILTER_R3_533 = 6
LOOPFILTER_R3_457 = 7

OUT_DIVIDER2_1 = 0
OUT_DIVIDER2_2 = 1
OUT_DIVIDER2_4 = 2
OUT_DIVIDER2_8 = 3
OUT_DIVIDER2_16 = 4
OUT_DIVIDER2_32 = 5
OUT_DIVIDER2_64 = 6

OUT_DIVIDER1_4 = 0
OUT_DIVIDER1_5 = 1
OUT_DIVIDER1_6 = 2
OUT_DIVIDER1_7 = 3

PRESCALER_DIV2 = 0
PRESCALER_DIV4 = 1

MOD_ORDER_0 = 0
MOD_ORDER_1 = 1
MOD_ORDER_2 = 2
MOD_ORDER_3 = 3
MOD_ORDER_4 = 4

def BITF(value, width, offset):
    return 0xffff & ~((2**width - 1) << offset) | ((value & width) << offset)

class lmx2571:
    def __init__(self, device):
        self.device = device
        self.offset = 0x00
    
    def select_f1(self):
        self.offset = 0x00
        
    def select_f2(self):
        self.offset = 0x10
    
    def reset(self):
        self.write(0x00, 1 << 13)
    
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
    
    def set_dithermode(self, setting):
        self.write_reg(0x2f, setting, 2, 13)
   
    def set_cp_gain(self, setting):
        self.write_reg(0x28, setting, 2, 6)

    def set_cp_current(self, setting):
        self.write_reg(0x28, setting, 5, 8)
    
    def set_muxout(self, setting):
        self.write_reg(0x27, setting, 1, 3)

    def enable_lockdet(self, setting):
        self.write_reg(0x27, 1, 1, 0)

    def disable_lockdet(self, setting):
        self.write_reg(0x27, 0, 1, 0)
       
    def set_mult_settling_time(self, setting):
        self.write_reg(0x23, setting, 11, 3)
        
    def set_rx_output_mode(self, setting):
        self.write_reg(0x23, setting, 1, 1)
 
    def set_tx_output_mode(self, setting):
        self.write_reg(0x23, setting, 1, 0)
        
    def enable_automute(self):
        self.write_reg(0x23, 1, 1, 2)
 
    def disable_automute(self):
        self.write_reg(0x23, 0, 1, 2)
        
    def set_power_tx(self, power):
        self.write_reg(0x08 + self.offset, power, 5, 0)
        
    def set_power_rx(self, power):
        self.write_reg(0x07 + self.offset, power, 5, 8)
    
    def enable_tx(self):
        self.write_reg(0x07 + self.offset, 1, 1, 7)

    def disable_tx(self):
        self.write_reg(0x07 + self.offset, 0, 1, 7)

    def enable_rx(self):
        self.write_reg(0x07 + self.offset, 1, 1, 6)

    def disable_rx(self):
        self.write_reg(0x07 + self.offset, 0, 1, 6)
        
    def set_r4_loopfilter(self, setting):
        self.write_reg(0x07 + self.offset, setting, 3, 0)
        
    def set_r3_loopfilter(self, setting):
        self.write_reg(0x06 + self.offset, setting, 3, 13)
   
    def set_output_divider1(self, setting):
        self.write_reg(0x06 + self.offset, setting, 2, 8)

    def set_output_divider2(self, setting):
        self.write_reg(0x06 + self.offset, setting, 3, 10)

    def set_mult(self, setting):
        self.write_reg(0x06 + self.offset, setting, 5, 0)

    def set_postdivider(self, setting):
        self.write_reg(0x05 + self.offset, setting, 8, 8)

    def set_predivider(self, setting):
        self.write_reg(0x05 + self.offset, setting, 8, 0)

    def set_prescaler(self, setting):
        self.write_reg(0x04 + self.offset, setting, 1, 15)

    def set_modulator_order(self, setting):
        self.write_reg(0x04 + self.offset, setting, 3, 12)

    def set_ndiv(self, setting):
        self.write_reg(0x04 + self.offset, setting, 12, 0)

    def set_frac_den_lsb(self, setting):
        self.write_reg(0x03 + self.offset, setting, 16, 0)

    def set_frac_den_msb(self, setting):
        self.write_reg(0x01 + self.offset, setting, 8, 8)

    def set_frac_num_lsb(self, setting):
        self.write_reg(0x02 + self.offset, setting, 16, 0)

    def set_frac_num_msb(self, setting):
        self.write_reg(0x01 + self.offset, setting, 8, 0)

    def set_frequency(self, frequency):
        """
        Basic formula
            fout = fref * (N + frac) * prescaler / out_divider * MULT
            fvco = fref * (N + frac) * prescaler * MULT
            
            fvco needs to satisfy the minimum and maximum constraints to lock
        """
        #self.disable_tx()
        

        
        # Find the output divider combination that gives us a valid VCO
        solution = None
        div1_value = 0
        div2_value = 0
        out_divider = 1
        
        for div2 in range(7):
            for div1 in range(4):
                div1_value = div1
                div2_value = div2
                out_divider = (2**div2_value) * (div1_value + 4)
                fvco = frequency * out_divider
                
                if fvco > MIN_VCO_FREQUENCY and fvco < MAX_VCO_FREQUENCY:
                    solution = True
                    break
                    
            if solution:
                break
        
        if solution is None:
            raise ValueError(f"Invalid VCO frequency {frequency} MHz")
        
        prescaler = 2
        mult = 1
        resolution = REFERENCE_FREQUENCY * prescaler / out_divider * mult
        fvco = frequency * out_divider
        nvalue = int(frequency / resolution)
        frac = frequency / (REFERENCE_FREQUENCY * prescaler / out_divider * mult) - nvalue
        numerator = int(0xffffff * frac)
        
        self.set_output_divider1(div1_value)
        self.set_output_divider2(div2_value)
        self.set_ndiv(nvalue)
        self.set_frac_den_lsb(0xffff)
        self.set_frac_den_msb(0xff)
        self.set_frac_num_lsb(numerator & 0xffff)
        self.set_frac_num_msb((numerator >> 16) & 0xff)
        # Calibrate
        self.write_reg(0x00, 1, 1, 0)
        self.enable_tx()

    def write(self, address, value):
        self.device.write(usbdevice.COMMAND_PLL_WRITE, address.to_bytes(1, usbdevice.ENDIAN) + value.to_bytes(2, usbdevice.ENDIAN))
        
    def read(self, address):
        self.device.write(usbdevice.COMMAND_PLL_READ, address.to_bytes(1, usbdevice.ENDIAN))
        
        return self.device.read(2)