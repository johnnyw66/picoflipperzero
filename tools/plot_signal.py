import matplotlib.pyplot as plt
import numpy as np
import argparse
import logging

def str_arr_to_int_arr(arr):
    # String array to int array
    return [abs(int(arr[i])) for i in range(len(arr))]

# Parse Raw data from FlipperZero sub files.
# Load the pulse timings (in microseconds) 
# Assume data is a sequence of high/low durations: [high, low, high, low, ...]
# Low durations are negative.

def load_data(file_path, frame=1):
    matched = 0
    data_line = "RAW_Data: "
#
#
    raw_data = []
    
    with open(file_path, 'r', encoding='ascii') as file:
        for ln, line in enumerate(file):
            # Strip leading/trailing whitespace (like newline characters)
            line = line.strip()

            if line.startswith(data_line):
                logging.info(f"Processing line: {ln}")
                
                # Process each line here
                data = line[len(data_line):].split(' ')
                # pair_adjacent_element() Useful for spitting out to a CSV file.
                pd = str_arr_to_int_arr(data)
                logging.info(f"Line , {ln}, length ,{len(pd)}")
                if ((len(pd) % 2 == 0) and matched==frame):
                    logging.info(f"Adding Line {ln}")
                    raw_data.extend(pd)
                matched += 1
                
    return raw_data



# Convert the timings to a time vs signal list for plotting
def convert_to_waveform(pulse_timings):
    if not pulse_timings:
        logging.info("No data to process.")
        return [], []
    
    time = [0]  # start time at 0
    signal = []
    
    current_signal = 1  # Start with high (1)
    
    for duration in pulse_timings:
        signal.append(current_signal)   # Add current signal value
        time.append(time[-1] + duration)  # Add the duration to time
        current_signal = 1 - current_signal  # Toggle between high (1) and low (0)

    # Append the last signal state to match time points
    signal.append(current_signal)
    
    return time, signal

def analyse_pulse_subsection(pulse_timings, start=0, end=None):
    if end is None:
        end = len(pulse_timings)
    
    # Select the subsection
    subsection = pulse_timings[start:end]
    
    # Classify into high and low signal timings
    high_signals = subsection[::2]  # Even indices are high signals
    low_signals = subsection[1::2]  # Odd indices are low signals
    
    return subsection, high_signals, low_signals



# Function to display signal waveform and histograms
def display_distributions(time, signal, high_signals, low_signals):
    if not signal:
        logging.info("No signals in this subsection.")
        return
    
    # Compute min, max, unique values for high and low
    min_high, max_high, unique_high = np.min(high_signals), np.max(high_signals), len(set(high_signals))
    min_low, max_low, unique_low = np.min(low_signals), np.max(low_signals), len(set(low_signals))
    
    logging.info(f"High: Min: {min_high}, Max: {max_high}, Unique: {unique_high}")
    logging.info(f"Low: Min: {min_low}, Max: {max_low}, Unique: {unique_low}")
    
    # Create subplots to display 3 windows
    fig, axs = plt.subplots(3, 1, figsize=(8, 12))
    
    # Plot signal waveform
    axs[0].step(time, signal, where='post', label='Logic Signal')
    axs[0].set_ylim(-0.5, 1.5)
    axs[0].set_title('Logic Signal Waveform')
    axs[0].set_xlabel('Time (microseconds)')
    axs[0].set_ylabel('Signal (High/Low)')
    axs[0].grid(True)
    
    # Plot high signal timings distribution
    axs[1].hist(high_signals, bins='auto', alpha=0.7, label='High Signal Timings', color='green')
    axs[1].set_title('Distribution of High Signal Durations')
    axs[1].set_xlabel('Time (microseconds)')
    axs[1].set_ylabel('Frequency')
    
    # Plot low signal timings distribution
    axs[2].hist(low_signals, bins='auto', alpha=0.7, label='Low Signal Timings', color='red')
    axs[2].set_title('Distribution of Low Signal Durations')
    axs[2].set_xlabel('Time (microseconds)')
    axs[2].set_ylabel('Frequency')

    # Adjust layout for better visualization
    plt.tight_layout()
    plt.show()




def find_repeating_patternsX(binary_groups):
    # Concatenate all binary groups into a single string
    concatenated_string = ''.join(binary_groups)
    
    patterns = {}
    
    # Check for repeating patterns
    length = len(concatenated_string)
    
    for size in range(1, length // 2 + 1):  # Check for pattern sizes
        for start in range(length - size):  # Check each position
            pattern = concatenated_string[start:start + size]
            if concatenated_string.count(pattern) > 1:  # Check if pattern repeats
                if pattern in patterns:
                    patterns[pattern] += 1
                else:
                    patterns[pattern] = 1
    
    # Filter to show only patterns that repeat
    repeating_patterns = {k: v for k, v in patterns.items() if v > 1}
    
    return repeating_patterns

def find_long_repeating_patterns(binary_groups, min_length=12):
    # Concatenate all binary groups into a single string
    concatenated_string = ''.join(binary_groups)
    
    patterns = {}
    length = len(concatenated_string)
    
    # Check for repeating patterns of at least min_length
    for size in range(min_length, length // 2 + 1):  # Starting from min_length
        for start in range(length - size):  # Check each position
            pattern = concatenated_string[start:start + size]
            if concatenated_string.count(pattern) > 1:  # Check if pattern repeats
                if pattern in patterns:
                    patterns[pattern] += 1
                else:
                    patterns[pattern] = 1
    
    # Filter to show only patterns that repeat
    repeating_patterns = {k: v for k, v in patterns.items() if v > 1}
    
    return repeating_patterns

def convert_to_binary(pulse_timings, pulse_duration):
    binary_string = ""
    pulse_duration = 290
    # Iterate through pulse timings in pairs (high, low)
    for i in range(0, len(pulse_timings), 2):
        # Check high signal
        #xrint(pulse_timings[i], pulse_timings[i + 1])
        hbstr = '1'*(pulse_timings[i]//pulse_duration)
        lbstr = '0'*(pulse_timings[i+1]//pulse_duration)
        #xrint("HIGH DURATION ", pulse_timings[i], hbstr)
        #xrint("LOW DURATION ", pulse_timings[i + 1], lbstr)
        binary_string += (hbstr + lbstr)


    # Break down into groups of 8 bits (bytes)
    grouped_bits = [binary_string[i:i + 8] for i in range(0, len(binary_string), 8)]

    return grouped_bits

# Plotting function
def plot_waveform(time, signal):
    plt.step(time, signal, where='post')  # Plot step graph
    plt.ylim(-0.5, 1.5)  # Logic levels (low = 0, high = 1)
    plt.xlabel('Time (microseconds)')
    plt.ylabel('Signal')
    plt.title('Logic Signal Waveform')
    plt.grid(True)
    plt.show()


logging.basicConfig(format='%(name)s %(levelname)s: %(asctime)s: %(message)s', level=logging.DEBUG)
logging.getLogger('matplotlib').setLevel(logging.WARNING)

parser = argparse.ArgumentParser(description="Plot Signals Tool",
                                        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-s", "--search", action='store_true',default=False, help="Try and search for repeating bit pattern")
parser.add_argument("-d", "--display",  action='store_false', default=True, help="Display distributions")
parser.add_argument("-p", "--pulse-duration", default=320, help="Pulse Duration")
parser.add_argument("-b", "--bits", default=24, help="protocol bit length")
parser.add_argument("-st", "--start", default=24, help="start")
parser.add_argument("-e", "--end", default=74, help="end")
parser.add_argument("-f", "--frame", default=3, help="Frame")
parser.add_argument("-i", "--input", default="doorbell.sub", help="Input file")

args = parser.parse_args()
arg_config = vars(args)


# 326 us, 16 bits
# 320 us, 19 bits
# 316 us, 22 bits

filename = arg_config['input']  # Replace with your file
#filename = 'princeton24.sub'  # Replace with your file
search_pattern = arg_config['search']
display_dist = arg_config['display']
pulse_duration = int(arg_config['pulse_duration'])
num_bits = int(arg_config['bits'])
start_pulse = int(arg_config['start'])
end_pulse = int(arg_config['end'])
frame = int(arg_config['frame'])

pulse_timings = load_data(filename, frame)
pulse_timings = pulse_timings[start_pulse:end_pulse]

if pulse_timings:
    signal_timings, high_signals, low_signals = analyse_pulse_subsection(pulse_timings, start=0)

    time, signal = convert_to_waveform(signal_timings)
    binary_groups = convert_to_binary(pulse_timings, pulse_duration)
    logging.info(f"{binary_groups}")

    if (display_dist):
        display_distributions(time, signal, high_signals, low_signals)
    if (search_pattern):
        logging.info(f"Finding {num_bits}- bit patterns. Please wait....")
        # Find single repeating bit pattern
        for pulse_duration in range(280,5000):
            binary_groups = convert_to_binary(pulse_timings, pulse_duration)
            repeating_patterns = find_long_repeating_patterns(binary_groups, num_bits)
            if (len(repeating_patterns) == 1):
                logging.info("fRepeating patterns: #, {len(repeating_patterns)}, With pulse duration , {pulse_duration},  and bits , {num_bits}")
                logging.info("{repeating_patterns}")
                exit(-1)


else:
    logging.info("No pulse timings to analyze.")


