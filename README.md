# picoflipperzero
Playing back FlipperZero sub files using a Pico (running MicroPython) and a FS1000A 433Mhz TX board


![Alt text](pico.jpg?raw=true "Pico") ![Alt text](fs1000a.png?raw=true "FS1000A")



Proof of concept - 

Can I ring my 433hz Byron door bell by capturing data with a FlipperZero - (Sub-Hz App) and playing it back with a Pico and FS1000A?


## Instructions

Wire up a Pico to your 433 Mhz FS1000A (You can buy these from AliExpress for pennies).


3.3v from the Pico to VCC on the FS1000A

Gnd from the Pico to GND on the FS1000A

GPIO16 from the Pico to ATAD on the FS1000A


Install MicroPython on your Pico and upload the main.py source.

Upload your captured FlipperZero '.sub' file to the top directory of the Pico.

After editing the 'file_path' in *main.py* to match your '.sub' file - run *main.py* (automatically run on power reset)



## compress.py

An alternative to main.py - this is my first attempt at compressing the Flipper Data. 
The main loop code now has more delays - which may effect the performance in audio reproduction.
I ignore any RAW_DATA lines which is not a multiple of 4 bytes - usually the end lines.





