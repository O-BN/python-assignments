filename = "Day05/digits.txt"

with open(filename, "r") as fh:
    text = fh.read()

for char in text:
    if char in text:
        print(char)