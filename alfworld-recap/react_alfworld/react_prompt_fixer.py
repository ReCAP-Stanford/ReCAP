import json
import sys

def process_value(value):
    """
    Processes a string by splitting on newline and prefixing lines:
    - First line: prefix with "user: "
    - Subsequent lines: if starting with '>', replace '>' with "assistant: "
      otherwise prefix with "user: "
    """
    lines = value.split('\n')
    processed_lines = [f"user: {lines[0]}\n{lines[1]}"]
    for i in range(2, len(lines)-1):
        print(lines[i])
        if lines[i][0] == '>':
            # Remove leading '>' and any following whitespace
            processed_lines.append(f"assistant: {lines[i][1:].lstrip()}")
        else:
            processed_lines.append(f"user: {lines[i]}")
    return '\n'.join(processed_lines)

def main():
    if len(sys.argv) != 3:
        print("Usage: python script.py input.json output.json")
        sys.exit(1)

    input_path, output_path = sys.argv[1], sys.argv[2]

    # Read the JSON file
    with open(input_path, 'r', encoding='utf-8') as infile:
        data = json.load(infile)

    # Process each value in the top-level key-value pairs
    processed_data = {}
    for key, value in data.items():
        if isinstance(value, str):
            processed_data[key] = process_value(value)
        else:
            processed_data[key] = value  # Leave non-string values unchanged

    # Write the processed data back to a new JSON file
    with open(output_path, 'w', encoding='utf-8') as outfile:
        json.dump(processed_data, outfile, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
