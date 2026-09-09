import sys
import time
import array
import usb1
import usbdevice
import lmx2571
import ltc5599

VENDOR_ID = 1155
PRODUCT_ID = 22336

regs = [
	0x3CA000,
	0x3A8C00,
	0x357806,
	0x2F0000,
	#0x2E001E,
	0x2A0210,
	0x290810,
	0x28101C,
	0x2711FB,
	0x233E87,
	0x220000,
	0x210000,
	0x200000,
	0x1F0000,
	0x1E0000,
	0x1D0000,
	0x1C0000,
	0x1B0000,
	0x1A0000,
	0x190000,
	0x18000E,
	0x170E84,
	0x168584,
	0x150101,
	0x14301B,
	0x1303E8,
	0x120000,
	0x110000,
	0x100000,
	0x0F0000,
	0x0E0000,
	0x0D0000,
	0x0C0000,
	0x0B0000,
	0x0A0000,
	0x090000,
	0x08000E,
	0x070E80,
	0x060584,
	0x050101,
	0x04201A,
	0x031200,
	0x020000,
	0x017A00,
	0x000483
]

with usb1.USBContext() as context:
    handle = context.openByVendorIDAndProductID(VENDOR_ID, PRODUCT_ID)
    
    if handle is None:
        print("USB device not found")
        sys.exit(0)
    
    print("Board OK")
    
    handle.claimInterface(1)
    
    device = usbdevice.usbdevice(handle)
    pll = lmx2571.lmx2571(device)
    modulator = ltc5599.ltc5599(device)
    
    pll.write(0, 1 << 13)
    time.sleep(0.01)
    
    for reg in regs:
        pll.write((reg >> 16) & 0xff, reg & 0xffff)
        
    pll.select_f1()
    pll.set_muxout(lmx2571.MUXOUT_READBACK)
    pll.set_dithermode(lmx2571.DITHER_STRONG)
    pll.disable_automute()
    pll.set_mult(1)
    pll.set_prescaler(lmx2571.PRESCALER_DIV2)
    pll.set_predivider(1)
    pll.set_postdivider(1)
    pll.set_frequency(446.1)
    pll.set_power_tx(31)
   
    modulator.set_lo(0x32)
    
    #pll.set_muxout(lmx2571.MUXOUT_LOCK_DETECT)

    