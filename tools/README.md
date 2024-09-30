# Analysing FlipperZero 'sub' files.



```

Usage: plot_signal.py [-h] [-s] [-d] [-p PULSE_DURATION] [-b BITS] [-st START] [-e END] [-f FRAME] [-i INPUT]

Plot Signals Tool

options:
  -h, --help            show this help message and exit
  -s, --search          Try and search for repeating bit pattern (default: False)
  -d, --display         Display distributions (default: True)
  -p PULSE_DURATION, --pulse-duration PULSE_DURATION
                        Pulse Duration (default: 320)
  -b BITS, --bits BITS  protocol bit length (default: 24)
  -st START, --start START
                        start (default: 24)
  -e END, --end END     end (default: 74)
  -f FRAME, --frame FRAME
                        Frame (default: 3)
  -i INPUT, --input INPUT
                        Input file (default: doorbell.sub)

Example:

python3 plot_signal.py -f 3  -i ./doorbell.sub 

```








