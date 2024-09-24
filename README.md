# Playing back FlipperZero files using a Raspberry Pi Pico

![Alt text](flipperzero.png?raw=true "FlipperZero")
![Alt text](pico.jpg?raw=true "Pico") ![Alt text](fs1000a.png?raw=true "FS1000A")



Playing back FlipperZero sub files using a Pico (running MicroPython) and a FS1000A 433Mhz TX board





Proof of concept - 

Can I ring my 433hz Byron door bell by capturing data with a FlipperZero - (Sub-Hz App) and playing it back with a Pico and FS1000A?


## Building Instructions

Wire up a Pico to your 433 Mhz FS1000A (You can buy these from AliExpress for pennies).

![Alt text](fritz.jpg?raw=true "Fritzing")


## BOM

Component|Quantity|Supplier|Approx Cost
---------|--------|--------|-----------
Raspberry Pi W Pico|1|The Pi Hut|£6.00
FS1000A 433MHz TX Module|1|eBay/Aliexpress|£1.00

## Wiring

Raspberry Pi W Pico|FS1000A
---------|--------
GND|GND
3.3v|VCC
GPIO16|ATAD




Note: In the PicoW Python Source Code - Pins are usually reference by their Pico 'GP' Pin names not the Pico board pin numbers.


## Code Instructions


Install MicroPython on your Pico and upload the **main.py**, **replaysub.py**, **pioreplay.py** and your own flipper sub source.

Upload your captured FlipperZero '.sub' file to the top directory of the Pico.

After editing the 'file_path' in **replaysub.py** to match your '.sub' file - run **main.py** by power cycling your Pico.
```
file_path = 'doorbell.sub'
#file_path = 'CarOpen.sub'
#file_path = 'CarClose.sub'
#file_path = 'ByronBell.sub'

pd = process_file(file_path)
# 40 days and 40 nights of hell
xmit_data(pd, 1000000, gpio_pin=16)

```
## How it works

The Flipper **sub** files produced, contain raw data lines which are simply paired delay values of high and low signals.
Low signals are negative, High signals are positive. Values are in microseconds. 
```
RAW_Data: 99 -598 165 -166 131 -894 165 -588 97 -264 163 -1314 165 -230 195 -294 327 -166 231 -134 167 -98 235 -100 689 -132 493 -64 393 -98 97 -100 195 -166 429 -130 1785 -98 167 -66 197 -918 229 -1774 657 -100 393 -98 233 -134 331 -100 423 -66 393 -98 263 -66 227 -130 129 -164 489 -98 229 -66 327 -66 131 -66 263 -98 821 -100 631 -982 67 -760 165 -3130 99 -528 65 -68 65 -266 265 -134 165 -132 133 -232 529 -196 463 -232 231 -66 165 -134 299 -168 433 -762 129 -96 329 -66 1649 -3170 339 -942 321 -964 973 -320 315 -958 319 -938 955 -318 969 -310 335 -938 977 -318 317 -962 945 -324 315 -974 945 -314 959 -312 355 -932 337 -944 321 -956 325 -940 341 -954 953 -292 969 -324 317 -976 943 -316 351 -952 951 -3204 299 -980 289 -982 943 -318 349 -922 349 -936 955 -344 951 -318 315 -954 945 -322 333 -950 945 -348 317 -956 933 -328 973 -290 355 -942 321 -958 325 -936 343 -956 309 -970 935 -330 975 -290 319 -978 945 -316 347 -956 949 -3192 335 -952 319 -958 945 -318 353 -926 337 -948 943 -314 989 -318 317 -958 963 -310 301 -950 979 -318 351 -924 973 -288 983 -310 335 -958 309 -958 313 -964 317 -956 349 -922 975 -316 963 -316 309 -958 969 -314 313 -978 973 -3152 343 -964 317 -956 973 -290 317 -974 319 -952 971 -318 961 -308 319 -940 955 -344 301 -944 983 -310 355 -922 951 -318 965 -318 311 -964 323 -974 293 -966 343 -918 343 -932 965 -340 951 -322 327 -952 943 -350 315 -956 969 -3180 335 -952 321 -954 947 -318 353 -922 347 -938 951 -342 951 -312 313 -972 935 -352 315 -954 949 -320 327 -944 947 -340 963 -318 317 -956 315 -936 329 -944 321 -984 295 -970 953 -312 977 -292 337 -946 979 -312 303 -968 981 -3170 349 -922 323 -962 975 -318 315 -954 317 -966 963 -310 955 -316 349 -922 975 -290 337 -944 979 -310 335 -938 981 -316 953 -324 307 -944 321 -964 321 -972 319 -938 341 -956 935 -328 975 -290 353 -950 941 -314 349 -954 967 -3186 311 -952 321 -960 977 -316 315 -960 317 -1000 943 -324 955 -292 345 -968 943 -314 345 -956 947 -316 311 -966 949 -328 937 -324 351 -940 321 -954 319 -940 341 -954 349 -924 945 -324 977 -308 303 -982 943 -316 349 -960 937 -3186 353 -936 323 -946 977 -318 317 -958 335 -944 943 -316 989 -282 353 -930 971 -294 343 -940 971 -316 349 -924 979 -292 997 -290 319 -944 355 -952 323 -938 343 -918 347 -958 965 -296 965 -310 333 -940 977 -318 353 -926 973 -3168 323 -978

```
As an example **sub** raw data entry, above, we can see that the data starts with a high value for **99** microseconds, followed by a low value for **598** microseconds. This is followed by sending the line high for **165** microseconds and then low for **166** microseconds.


The Python code reads and parses the **sub** file through the strings of raw data building an int array.
```
def process_file(file_path):
    matched = 0
    data_line = "RAW_Data: "
    raw_data = []
    
    with open(file_path, 'r', encoding='ascii') as file:
        for ln, line in enumerate(file):
            # Strip leading/trailing whitespace (like newline characters)
            line = line.strip()
            if line.startswith(data_line):
                print("Processing line:", ln)
                
                # Process each line here
                data = line[len(data_line):].split(' ')
                pd = [int(data[i]) for i in range(len(data))]

                raw_data.extend(pd)
                matched += 1
                
    return raw_data
```

When playing back the data the code simply sets a single Pico GPIO line appropriately using these delay timings between making changes.
A technique known as **bit-banging**.

```
def xmit_flat(data,gpio_pin = 16):
    pin = machine.Pin(gpio_pin, machine.Pin.OUT)
    for delay in data:
        pin.value(1 if (delay > 0) else 0)
        time.sleep_us(abs(delay))

    pin.value(0)
    
```


Using pure Python for **bit-banging** is generally not ideal due to Python’s inherent performance limitations. Bit-banging, which involves manually toggling GPIO pins at precise timing intervals to simulate communication protocols, requires a high degree of timing accuracy and speed. Python, being an interpreted and high-level language, introduces significant overhead with each operation, making it difficult to achieve the precise, real-time control necessary for tasks like handling fast data transfer rates. Additionally, Python’s garbage collection, dynamic typing, and lack of direct access to hardware registers further complicate achieving the low-latency and consistent timing needed in bit-banging applications. For such tasks, lower-level languages like C or assembly are typically preferred, as they allow for much finer control over timing and hardware interactions.




## An improved version - pioreplay.py

The Programmable I/O (**PIO**) feature on the Raspberry Pi Pico helps solve the limitations of using pure Python for bit-banging by offloading timing-critical tasks to dedicated hardware. PIO allows for custom, precise control over GPIO pins without relying on the main CPU, eliminating the performance bottlenecks and timing inaccuracies that come with using Python.

**pioreplay.py** is an alternative to **replaysub.py** - this is my first attempt at compressing the Flipper Data and using PIO.

To run this alternative version - change the import on **main.py** from

```
import replaysub
```
to
```
import pioreplay
```

Since I am running the PIO clock at 2000000Hz - adjustments are made with the delay data within the PIO assembler.
I ignore any RAW_DATA lines which are not a multiple of 4 bytes - usually those at the end of the data.
The PIO instructions produces a closer match to the audio produced by the Flipper, compared to using Python code.


```
# PIO to play out data entry - 
@rp2.asm_pio(in_shiftdir=rp2.PIO.SHIFT_RIGHT, out_shiftdir=rp2.PIO.SHIFT_LEFT, set_init=rp2.PIO.OUT_LOW)
def pulse():
    # Pull a 32-bit value into the OSR (Output Shift Register)
    pull(block)

    in_(osr, 16)            # Shift right by 16 bits, ISR now contains bottom 16 bits of OSR in its top 16 bits
    in_(isr, 15)            # Shift right ISR by 15 bits into ISR --> (OSR & 0xFFFF)=<<1
    mov(y, isr)             # y = BOTTOM 16 bits * 2
    out(x,17)               # x = TOP 16 bits * 2

    set(pins, 1)             # 1 cycle: Set the GPIO pin high
    label("high_loop")
    jmp(x_dec, "high_loop")  # 2 cycles per iteration: 1 for decrement, 1 for jump

    set(pins, 0)             # 1 cycle: Set the GPIO pin low
    label("low_loop")
    jmp(y_dec, "low_loop")   # 2 cycles per iteration: 1 for decrement, 1 for jump

```
```

def xmit_compressed_flat(data,gpio_pin = 16):
    pin = machine.Pin(gpio_pin, machine.Pin.OUT)
    # Create a StateMachine instance and load the PIO program
    sm = rp2.StateMachine(0, pulse, freq=2000000, set_base=Pin(gpio_pin))
    # Start the StateMachine
    sm.active(1)
    for i in range(0, len(data), 4):
        # Our data has been compressed by merging the high and low delays into
        # a single 32 bit value - (each delay is 16 bits in length).
        # Additionally they have been placed into a byte array - so
        # we need to unpack them. We'll leave it to the PIO
        # state machine to manipulate the single 32 bit value
        # into two lots of delays needed. 
        chunk = data[i:i+4]
        value = struct.unpack('>I', chunk)[0]
        sm.put(value)
        
    sm.active(0)
    pin.value(0)
```
    


## Further Improvements?

Perhaps speed up the PIO clock?  If I did this I would need to add nop instructions in the two delay loops. This would reduce timing errors from the 5 set up instructions.
```
#run at 64Mhz
@rp2.asm_pio(in_shiftdir=rp2.PIO.SHIFT_RIGHT, out_shiftdir=rp2.PIO.SHIFT_LEFT, set_init=rp2.PIO.OUT_LOW)
def pulse64Mhz():
    # Pull a 32-bit value into the OSR (Output Shift Register)
    pull(block)

    in_(osr, 16)   # Shift right by 16 bits, ISR now contains bottom 16 bits of OSR in its top 16 bits
    in_(isr, 16)   # Shift right ISR by 16 bits into ISR = (OSR & 0xFFFF)
    mov(y, isr)    #   y = BOTTOM 16 bits * 16
    out(x,16)  	   #   x = TOP 16 bits
    
    set(pins, 1)   # 1 cycle: Set the GPIO pin high
    label("high_loop")
    nop() [29]
    nop() [31]
    jmp(x_dec, "high_loop")  # 64 cycles per iteration:  62 nops/delays + 1 for decrement, 1 for jump

    set(pins, 0)   # 1 cycle: Set the GPIO pin high
    label("low_loop")
    nop() [29]
    nop() [31]
    jmp(y_dec, "low_loop")  # 64 cycles per iteration:  62 nops/delays + 1 for decrement, 1 for jump

```
We are still using a Python **for-loop** to step through the data - so this will still be subject to Python's overhead and uncertainity when it comes to making precise timings.
At some point I intend to use **DMA (Direct Memory Access)** to remove the need for Python to populate the PIO buffer input.

I will need some external DMA library to help me. Perhaps - https://github.com/rkompass/RPi2040_mPy  ?

I also intend to improve the hardware by using a simple demux chip (CD4051BE). This will allow us to have up to 8 frequencies - supplied through various FS1000A boards. 
Ultimately - I could have a 'Replay Over MQTT' server - allowing me to playout **sub** files from a home mosquitto server.

Watch this space!!


## Thanks

Thanks to Derek Jamison for his explanation on the FlipperZero '.sub' RAW_DATA format!

https://github.com/jamisonderek/flipper-zero-tutorials/

https://www.youtube.com/@MrDerekJamison








