# Analysing FlipperZero 'sub' files.



```

Usage: plot_signal.py [-h] [-s] [-d] [-p PULSE_DURATION] [-b BITS] [-st START] [-e END] [-f FRAME] [-i INPUT]

Plot Signals Tool

options:
  -h, --help            show this help message and exit
  -s, --search          Try and search for repeating bit pattern (default: False)
  -d, --disable         Disable distributions plot (default: True)
  -p PULSE_DURATION, --pulse-duration PULSE_DURATION
                        Pulse Duration (default: 270)
  -b BITS, --bits BITS  Protocol bit length (default: 24)
  -st START, --start START
                        start (default: 22)
  -e END, --end END     end (default: 124)
  -f FRAME, --frame FRAME
                        Frame number (512 chunk) (default: 1)
  -i INPUT, --input INPUT
                        Input file (default: example.sub)


Example:

python3 plot_signal.py -f 3  -i ./doorbell.sub 

```








