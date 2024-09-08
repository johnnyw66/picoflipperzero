# picoflipperzero
Playing back FlipperZero sub files using a Pico (running MicroPython) and a FS1000A 433Mhz TX board


Proof of concept - 

Can I ring my 433hz Byron door bell by capturing data with a FlipperZero - (Sub-Hz App) and playing it back with a Pico and FS1000A?


## Instructions

Wire up a Pico to your 433 Mhz FS1000A (You can buy these from AliExpress for pennies).


3.3v from the Pico to VCC on the FS1000A

Gnd from the Pico to GND on the FS1000A

GPIO16 from the Pico to ADAT on the FS1000A


Install MicroPython on your Pico and upload the main.py
Upload your captured FlipperZero '.sub' file to your Pico.

run main.py (automatically run on power reset)





