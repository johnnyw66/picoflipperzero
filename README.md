# picoflipperzero
Playing back FlipperZero sub files using a Pico (running MicroPython) and a FS1000A 433Mhz TX board


![Alt text](pico.jpg?raw=true "Pico") ![Alt text](fs1000a.png?raw=true "FS1000A")



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

When playing back the data the code simply sets a single Pico GPIO line appropriately.

```
def xmit_flat(data,gpio_pin = 16):
    pin = machine.Pin(gpio_pin, machine.Pin.OUT)
    for delay in data:
        pin.value(1 if (delay > 0) else 0)
        time.sleep_us(abs(delay))

    pin.value(0)
    
```

Using pure Python for bit-banging is generally not ideal due to Python’s inherent performance limitations. Bit-banging, which involves manually toggling GPIO pins at precise timing intervals to simulate communication protocols, requires a high degree of timing accuracy and speed. Python, being an interpreted and high-level language, introduces significant overhead with each operation, making it difficult to achieve the precise, real-time control necessary for tasks like handling fast data transfer rates. Additionally, Python’s garbage collection, dynamic typing, and lack of direct access to hardware registers further complicate achieving the low-latency and consistent timing needed in bit-banging applications. For such tasks, lower-level languages like C or assembly are typically preferred, as they allow for much finer control over timing and hardware interactions.




## And improved version - pioreplay.py

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

## Thanks

Thanks to Derek Jamison for his explanation on the FlipperZero '.sub' RAW_DATA format!

https://github.com/jamisonderek/flipper-zero-tutorials/

https://www.youtube.com/@MrDerekJamison








