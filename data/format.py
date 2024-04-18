def load_file(file_path):
    with open(file_path, 'r') as file:
        data = file.read()
    return data

# Usage
file_path = 'data\countries.txt'
data = load_file(file_path)
lines = data.split('\n')
trimmed_lines = [line.lstrip() for line in lines]
data = '\n'.join(trimmed_lines)
# Sort the lines in alphabetical order
sorted_data = sorted(trimmed_lines)
# Join the sorted lines with newline character
data = '\n'.join(sorted_data)

# Overwrite the file with the sorted data
with open(file_path, 'w') as file:
    file.write(data)
