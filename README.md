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


Install MicroPython on your Pico and upload the main.py source.

Upload your captured FlipperZero '.sub' file to the top directory of the Pico.

After editing the 'file_path' in **main.py** to match your '.sub' file - run **main.py** (automatically run on power reset).
```
file_path = 'doorbell.sub'
#file_path = 'CarOpen.sub'
#file_path = 'CarClose.sub'
#file_path = 'ByronBell.sub'

pd = process_file(file_path)
# 40 days and 40 nights of hell
xmit_data(pd, 1000000, gpio_pin=16)

```


## compress.py

**compress.py** is an alternative to **main.py** - this is my first attempt at compressing the Flipper Data and using PIO.

Running the clock at 2000000Hz - so adjustments are made with the delay data within the PIO instructions.
I ignore any RAW_DATA lines which are not a multiple of 4 bytes - usually those at the end of the data.
This version seems to produce a closer match to the audio produced by a Flipper. 

## Thanks

Thanks to Derek Jamison for his explanation on the FlipperZero '.sub' RAW_DATA format!

https://github.com/jamisonderek/flipper-zero-tutorials/

https://www.youtube.com/@MrDerekJamison








