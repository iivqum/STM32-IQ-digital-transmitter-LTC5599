import sys
import time
import array
import usb1

NUM_TRANSFERS = 5
TRANSFER_SIZE = 64

transfer_count = 0
start_time = 0
benchmark_time = 0

def callback(transfer):
    global transfer_count

    if transfer.getStatus() != usb1.TRANSFER_COMPLETED:
        print("TRANSFER FAIL", transfer.getStatus())
        transfer.submit()
        return
   
    transfer_count += 1
   
    if transfer_count == NUM_TRANSFERS:
        benchmark_time = time.perf_counter() - start_time
        print(benchmark_time, NUM_TRANSFERS * TRANSFER_SIZE / benchmark_time / (10**6))
    
with usb1.USBContext() as context:
    dev = context.openByVendorIDAndProductID(1155, 22336)
    
    if dev is None:
        print("Can't find device")
        sys.exit(1)
    
    dev.claimInterface(1)
    
    data = (0xdeadbeef).to_bytes(4, "little") + (0x03).to_bytes(1, "little") + (0x00).to_bytes(1, "little")
    
    # preamble
    dev.bulkWrite(0x1, data, 100)
    
    print(dev.bulkRead(0x81, 2, 100))
    
    """
    data = array.array("B", [0]) * TRANSFER_SIZE
    
    transfers = []
    #start_time = time.perf_counter()
    
    for i in range(NUM_TRANSFERS):
        tx = dev.getTransfer()
    
        tx.setBulk(0x1, data, callback, timeout = 100)
        transfers.append(tx)

    for tx in transfers:
        tx.submit()
    
    start_time = time.perf_counter()
    
    while any(x.isSubmitted() for x in transfers):
        context.handleEvents()
    """