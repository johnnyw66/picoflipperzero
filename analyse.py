

def str_arr_to_int_arr(arr):
    # String array to int array
    return [abs(int(arr[i])) for i in range(len(arr))]

def generate_timings_from_file(file_path):
    matched = 0
    data_line = "RAW_Data: "
    timings = []
    
    with open(file_path, 'r', encoding='ascii') as file:
        for ln, line in enumerate(file):
            line = line.strip()
            if line.startswith(data_line):
                print("Processing line:", ln)
                # Process each line here
                data = line[len(data_line):].split(' ')
                pd = str_arr_to_int_arr(data)
                timings.extend(pd)
                matched += 1
    print("Parsing sub file completed.")            
    return timings


# Function to classify the pulses based on their length
def classify_pulses(timings):
    high_pulses = []
    low_pulses = []

    for i, timing in enumerate(timings):
        if i % 2 == 0:  # Even index -> high time
            high_pulses.append(timing)
        else:  # Odd index -> low time
            low_pulses.append(timing)

    return high_pulses, low_pulses

# Cleaning function to group pulses into common categories (rounding to nearest expected values)
def clean_timings(timings, tolerance=200):
    cleaned_timings = []
    for time in timings:
        if 400 <= time <= 600:
            cleaned_timings.append(500)
        elif 1400 <= time <= 1600:
            cleaned_timings.append(1500)
        elif 3800 <= time <= 4200:
            cleaned_timings.append(4000)
        else:
            cleaned_timings.append(None)  # Mark unexpected values for filtering
    return cleaned_timings

# Additional filtering to remove None or noisy pulses
def filter_noise(cleaned_timings):
    return [time for time in cleaned_timings if time is not None]

# Find patterns and group frames if long pauses are found
def find_frames(cleaned_timings, frame_gap=3000):
    frames = []
    current_frame = []
    
    for time in cleaned_timings:
        if time == 4000:  # Assuming a 4000 µs gap signifies a frame boundary
            if current_frame:
                frames.append(current_frame)
                current_frame = []
        else:
            current_frame.append(time)
    
    if current_frame:
        frames.append(current_frame)  # Add the last frame if it exists

    return frames

# Analyzing the timings to categorize them
def analyse_signal(timings):
    # First, clean the timings
    cleaned_timings = clean_timings(timings)

    # Filter out noise
    filtered_timings = filter_noise(cleaned_timings)

    # Find frames
    frames = find_frames(filtered_timings)

    print(f"Detected {len(frames)} frames:")
    for i, frame in enumerate(frames):
        print(f"Frame {i+1}: {frame}")
    
    # Now, classify the pulses in each frame
    for i, frame in enumerate(frames):
        high_pulses, low_pulses = classify_pulses(frame)

        print(f"\n--- Frame {i+1} ---")
        print("High Pulse Durations (µs):", high_pulses)
        print("Low Pulse Durations (µs):", low_pulses)

        # Basic statistical summary of high and low pulse times
        avg_high = 0 if len(high_pulses) == 0 else sum(high_pulses) /len(high_pulses)
        avg_low = 0 if len(low_pulses) == 0 else sum(low_pulses)/ len(low_pulses)


        unique_high = set(high_pulses)
        unique_low = set(low_pulses)

        print(f"Average High Pulse: {avg_high:.2f} µs")
        print(f"Average Low Pulse: {avg_low:.2f} µs")
        print(f"Unique High Pulses: {unique_high}")
        print(f"Unique Low Pulses: {unique_low}")
        
        # Check if timings match PT2262-like or EV1527-like patterns
        if len(unique_low) == 2 and all(1000 <= x <= 2000 for x in unique_low):
            print("Likely PT2262 Protocol Detected (PWM).")
        elif len(unique_low) == 2 and all(400 <= x <= 800 for x in unique_low):
            print("Likely EV1527 Protocol Detected (Manchester Encoding).")
        else:
            print("Unknown protocol.")

#timings = generate_timings_from_file("./doorbell.sub")
timings = generate_timings_from_file("./princeton24.sub")

# Run the analysis
analyse_signal(timings)

