#!/bin/bash
touch commands_only.txt

# initialize line number
line_number=1

# Read the input file line by line
while IFS= read -r line || [[ -n "$line" ]]; do
    # Check if the line number is a multiple of 3 + 1, if it is, skip it
    if (( line_number % 3 == 1 )); then
        line_number=$((line_number+1))
        continue
    fi
    # Check if the line is not empty
    if [[ -n $line ]]; then
        # Split the line by commas and store the commands in an array
        IFS=',' read -ra cmds <<< "$line"
        # Write each command to the output file
        for cmd in "${cmds[@]}"; do
            echo "$cmd" >> commands_only.txt
        done
    fi
    line_number=$((line_number+1))
done < "$1"