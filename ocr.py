import pytesseract
import os
pytesseract.pytesseract.tesseract_cmd = r"C:/Program Files/Tesseract-OCR/tesseract.exe"

from PIL import Image
import re


pattern_p = r'P\D*([\d.]+)'
img = Image.open('hello.png')
text = pytesseract.image_to_string(img)
print(os.environ['PATH'])
image = Image.open("C:/Users/ojhaa/OneDrive/Documents/Desktop/extracted data/hello.png")


pattern_k = r'K\D*([\d.]+)'
pattern_n = r'N\D*([\d.]+)'

phosphorus_match = re.search(pattern_p, text)
potassium_match = re.search(pattern_k, text)
nitrogen_match = re.search(pattern_n, text)

# Extract the values
phosphorus_value = float(phosphorus_match.group(1)) if phosphorus_match else None
potassium_value = float(potassium_match.group(1)) if potassium_match else None
nitrogen_value = float(nitrogen_match.group(1)) if nitrogen_match else None


print(text)
print(phosphorus_value)
print(potassium_value)
print(nitrogen_value)

import re

def extract_numbers_on_same_line_after_n(input_string):
    # Define the regular expression pattern to match all numbers after (N) on the same line
    pattern = r'\(N\)(\d+(?:\s*\d+)*)'
    
    # Use the re.search function to find the first match
    match = re.search(pattern, input_string)
    
    # Check if a match was found
    if match:
        # Extract and split the matched numbers
        numbers_after_n = match.group(1)
        numbers_list = re.findall(r'\d+', numbers_after_n)
        return numbers_list
    else:
        # If no match was found, return None or an empty list as needed
        return None

# Example usage
input_string = "This is some text (N)123 45 6789 that we want to extract."
result = extract_numbers_on_same_line_after_n(input_string)
if result:
    print("Numbers after (N):", result)
else:
    print("No match found.")
