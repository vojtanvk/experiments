#!/usr/bin/env python3
import re
import ast

# Input text file (the one that contains the bytearray(...) lines)
INPUT_FILE = "test"

# Output binary file
OUTPUT_FILE = "output2.bin"

# Read the text content
with open(INPUT_FILE, "r", encoding="utf-8") as f:
    text = f.read()

# Find all bytearray(...) patterns
matches = re.findall(r"bytearray\((b'.*?')\)", text, flags=re.DOTALL)

# Combine all binary chunks

with open(OUTPUT_FILE, "wb") as f:
    
    for m in matches:
        # Safely evaluate the byte string (e.g., b'\x05\x01...')
        bstr = bytearray(eval(m))
        bstr.extend(b"\0")
        f.write(bstr)

# Write the combined binary data to a file


# print(f"Extracted {len(matches)} bytearrays into {OUTPUT_FILE} ({len(binary_data)} bytes total)")
