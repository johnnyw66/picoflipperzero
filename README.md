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

The Python code reads through the strings of raw data in the **sub** file builds an int array.

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
        chunk = data[i:i+4]
        value = struct.unpack('>I', chunk)[0]
        sm.put(value)
        
    sm.active(0)
    pin.value(0)
```
    


## Further Improvements?

Perhaps speed up the PIO clock?  If I did this I would need to add nop instructions in the two delay loops. This would reduce timing errors from the 5 set up instructions.

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








