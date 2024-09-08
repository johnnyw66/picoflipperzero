import struct
import time
import machine
import gc

gc.collect()

free_ram = gc.mem_free()

print("Free RAM:bytes", free_ram)

def str_arr_to_bytearray(data):
    compressed_data = bytearray()
    return bytearray(b''.join([struct.pack('>H', abs(int(num))) for num in data]))


def str_arr_to_int_arr(arr):
    # String array to int array
    return [int(arr[i]) for i in range(len(arr))]


def process_file(file_path):
    matched = 0
    data_line = "RAW_Data: "
#
#
    raw_data = bytearray()
    
    with open(file_path, 'r', encoding='ascii') as file:
        for ln, line in enumerate(file):
            # Strip leading/trailing whitespace (like newline characters)
            line = line.strip()

            if line.startswith(data_line):
                print("Processing line:", ln)
                
                # Process each line here
                data = line[len(data_line):].split(' ')
                # pair_adjacent_element() Useful for spitting out to a CSV file.
                pd = str_arr_to_bytearray(data)
                print("Line ", ln, " length ",len(pd))
                #xmit_flat(pd,gpio_pin=16)
                if (len(pd) % 4 == 0 and matched >= 0):
                    print("Adding ",ln, len(pd), gc.mem_free(), matched)
                    raw_data.extend(pd)
                    #xmit_compressed_flat(pd)
                gc.collect()
                matched += 1
                
    return raw_data

def usleep(v):
    print(v)

def xmit_compressed_flat(data,gpio_pin = 16):
    pin = machine.Pin(gpio_pin, machine.Pin.OUT)

    for i in range(0, len(data), 4):
        chunk = data[i:i+4]
        value = struct.unpack('>I', chunk)[0]
        pin.value(1)
        time.sleep_us(value>>16)
        pin.value(0)
        time.sleep_us(value & 0xffff)


def xmit_compressed_data(data, num_of_plays, gpio_pin = 16):
    for play in range(num_of_plays):
        print("Transmitting...",play,"out of",num_of_plays) 
        xmit_compressed_flat(data,gpio_pin)
        time.sleep(4)
  
time.sleep(5)
file_path = 'doorbell.sub'
#file_path = 'CarOpen.sub'
#file_path = 'CarClose.sub'
#file_path = 'ByronBell.sub'

pd = process_file(file_path)
while True:
    xmit_compressed_data(pd, 2, gpio_pin=16)
    time.sleep(4)


