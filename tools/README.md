# Analysing FlipperZero 'sub' files.



```
def process_file(file_path):
    matched = 0
    data_line = "RAW_Data: "
    raw_data = []
    
    with open(file_path, 'r', encoding='ascii') as file:
        for ln, line in enumerate(file):
            # Strip leading/trailing whitespace (like newline characters)
            line = line.strip()
            if line.startswith(data_line):
                print("Processing line:", ln)
                
                # Process each line here
                data = line[len(data_line):].split(' ')
                pd = [int(data[i]) for i in range(len(data))]

                raw_data.extend(pd)
                matched += 1
                
    return raw_data
```








