import struct
import time
import machine
import rp2
from machine import Pin
  
import gc

gc.collect()

free_ram = gc.mem_free()

print("Free RAM:bytes", free_ram)

# PIO to play out data entry - 
@rp2.asm_pio(in_shiftdir=rp2.PIO.SHIFT_RIGHT, out_shiftdir=rp2.PIO.SHIFT_LEFT, set_init=rp2.PIO.OUT_LOW)
def pulse():
    # Pull a 32-bit value into the OSR (Output Shift Register)
    pull(block)

    in_(osr, 16)      # Shift right by 16 bits, ISR now contains bottom 16 bits of OSR in its top 16 bits
    in_(isr, 15)      # Shift right ISR by 15 bits into ISR --> (OSR & 0xFFFF)=<<1
    mov(y, isr)       # y = BOTTOM 16 bits * 2
    out(x,17)         # x = TOP 16 bits * 2


    set(pins, 1)             # 1 cycle: Set the GPIO pin high
    label("high_loop")
    jmp(x_dec, "high_loop")  # 2 cycles per iteration: 1 for decrement, 1 for jump

    set(pins, 0)             # 1 cycle: Set the GPIO pin low
    label("low_loop")
    jmp(y_dec, "low_loop")   # 2 cycles per iteration: 1 for decrement, 1 for jump


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
    # Create a StateMachine instance and load the PIO program
    sm = rp2.StateMachine(0, pulse, freq=2000000, set_base=Pin(gpio_pin))
    # Start the StateMachine
    sm.active(1)
    for i in range(0, len(data), 4):
        chunk = data[i:i+4]
        value = struct.unpack('>I', chunk)[0]
        sm.put(value)
        
    sm.active(0)
    pin.value(0)
    
def xmit_compressed_flat_deprecated(data,gpio_pin = 16):
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
  
time.sleep(1)
file_path = 'doorbell.sub'
#file_path = 'CarOpen.sub'
#file_path = 'CarClose.sub'
#file_path = 'ByronBell.sub'

pd = process_file(file_path)
while True:
    xmit_compressed_data(pd, 2, gpio_pin=16)
    time.sleep(4)

