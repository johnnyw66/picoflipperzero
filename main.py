import machine
import time


# Connect Pico GPIO 16 to ATAD on  'FS1000A' 433Mhz TX Boards
# Connect Pico 3.3V to VCC on FS1000A
# Connect Pico GND to GND on FS1000A


raw_data = [] #Global! :(


# No longer used - but useful for pre-processing for CSV files - 
def pair_adjacent_elements(arr):
    # Ensure the array length is even
    if len(arr) % 2 != 0:
        raise ValueError("The array length must be even.")

    # Pair adjacent elements (even, odd) and convert them into tuples
    return [(int(arr[i]), int(arr[i + 1])) for i in range(0, len(arr), 2)]

def str_arr_to_int_arr(arr):
    # String array to int array
    return [int(arr[i]) for i in range(len(arr))]


def xmit_flat(data,gpio_pin = 16):
    pin = machine.Pin(gpio_pin, machine.Pin.OUT)
    for delay in data:
        pin.value(1 if (delay > 0) else 0)
        time.sleep_us(abs(delay))

    pin.value(0)
    
# Use this with the paired tuples data     
def xmit_paired(data,gpio_pin = 16):
    pin = machine.Pin(gpio_pin, machine.Pin.OUT)
    
    for high,low in data:
        if (low >= 0):
            raise ValueError("Low Delays must be negative!")
                
        pin.value(1)
        time.sleep_us(high)
        pin.value(0)
        time.sleep_us(-low)
    

def xmit_data(data, num_of_plays, gpio_pin = 16):
    

    for play in range(num_of_plays):
        print("Transmitting...",play,"out of",num_of_plays) 
#        xmit_paired(data,gpio_pin)
        xmit_flat(data,gpio_pin)
        print("Done")
        time.sleep(4)
    


def process_file(file_path):
    matched = 0
    data_line = "RAW_Data: "
#     raw_data = []
    
    with open(file_path, 'r', encoding='ascii') as file:
        for ln, line in enumerate(file):
            # Strip leading/trailing whitespace (like newline characters)
            line = line.strip()
            # Unfortunately I run out of RAM on my Pico - when processing the data
            # So far I've managed to get away with producing a 'Princeton' ring
            # from the first 3 blocks of 512.
            # At some point I intended to compress this to a bitmap
            # and use PIO
            
            # I've managed to playback and ring my Byron DB2311 Bell 
            # with this        
            if line.startswith(data_line) and matched < 4:
                print("Processing line:", ln)
                
                # Process each line here
                data = line[len(data_line):].split(' ')

                # pair_adjacent_element() Useful for spitting out to a CSV file.
                #pd = pair_adjacent_elements(data)
                pd = str_arr_to_int_arr(data)

                raw_data.extend(pd)
                matched += 1
                
    return raw_data


# Example usage 
file_path = 'doorbell.sub'
#file_path = 'CarOpen.sub'
#file_path = 'CarClose.sub'
#file_path = 'ByronBell.sub'

pd = process_file(file_path)
# 40 days and 40 nights of hell
xmit_data(pd, 1000000, gpio_pin=16)



