import matplotlib.pyplot as plt
import numpy as np

def str_arr_to_int_arr(arr):
    # String array to int array
    return [abs(int(arr[i])) for i in range(len(arr))]

# Load the pulse timings (in microseconds) from a file
# Assume data is a sequence of high/low durations: [high, low, high, low, ...]
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
                print("Processing line:", ln)
                
                # Process each line here
                data = line[len(data_line):].split(' ')
                # pair_adjacent_element() Useful for spitting out to a CSV file.
                pd = str_arr_to_int_arr(data)
                print("Line ", ln, " length ",len(pd))
                if ((len(pd) % 2 == 0) and matched==frame):
                    print(f"Adding Line {ln}")
                    raw_data.extend(pd)
                matched += 1
                
    return raw_data



# Convert the timings to a time vs signal list for plotting
def convert_to_waveform(pulse_timings):
    if not pulse_timings:
        print("No data to process.")
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
        print("No signals in this subsection.")
        return
    
    # Compute min, max, unique values for high and low
    min_high, max_high, unique_high = np.min(high_signals), np.max(high_signals), len(set(high_signals))
    min_low, max_low, unique_low = np.min(low_signals), np.max(low_signals), len(set(low_signals))
    
    print(f"High: Min: {min_high}, Max: {max_high}, Unique: {unique_high}")
    print(f"Low: Min: {min_low}, Max: {max_low}, Unique: {unique_low}")
    
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



def display_distribution(signal_timings, signal_type='High'):
    if not signal_timings:
        print(f"No {signal_type} signals in this subsection.")
        return
    
    mean_time = np.mean(signal_timings)
    median_time = np.median(signal_timings)
    min_time = np.min(signal_timings)
    max_time = np.max(signal_timings)
    unique_values = len(set(signal_timings))
    
    print(f"{signal_type} Signals:")
    print(f"Mean Time: {mean_time:.2f} microseconds")
    print(f"Median Time: {median_time:.2f} microseconds")
    print(f"Min Time: {min_time} microseconds")
    print(f"Max Time: {max_time} microseconds")
    print(f"Number of Unique Values: {unique_values}")
    
    # Plot the distribution using a histogram
    plt.hist(signal_timings, bins='auto', alpha=0.7, label=f'{signal_type} Signals')
    plt.xlabel('Time (microseconds)')
    plt.ylabel('Frequency')
    plt.title(f'Distribution of {signal_type} Signal Durations')
    plt.legend()
    plt.show()


# Plotting function
def plot_waveform(time, signal):
    plt.step(time, signal, where='post')  # Plot step graph
    plt.ylim(-0.5, 1.5)  # Logic levels (low = 0, high = 1)
    plt.xlabel('Time (microseconds)')
    plt.ylabel('Signal')
    plt.title('Logic Signal Waveform')
    plt.grid(True)
    plt.show()

# Usage example
filename = 'doorbell.sub'  # Replace with your file
filename = 'princeton24.sub'  # Replace with your file

frame = 3
pulse_timings = load_data(filename, frame)
pulse_timings = pulse_timings[0:99]

if pulse_timings:
    # Analyze subsection (e.g., first 20 pulses)
    signal_timings, high_signals, low_signals = analyse_pulse_subsection(pulse_timings, start=0)

    time, signal = convert_to_waveform(signal_timings)

    display_distributions(time, signal, high_signals, low_signals)
    
    # Display statistics and distribution for high and low signals
    #display_distribution(high_signals, 'High')
    #display_distribution(low_signals, 'Low')
    #display_distributions(subsection, high_signals, low_signals)
else:
    print("No pulse timings to analyze.")

#plot_waveform(time, signal)

