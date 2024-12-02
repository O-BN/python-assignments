
# rectangle variable as inputs
width = float(input("insert the rectangle width"))
length = float(input("insert the rectangle length"))

print(f"Area of the rectangle is: {width*length} and the perimeter is {2*(width+length)}")



#while_loop option
while True:
    user_input = input("Insert the rectangle width: ")
    try:
        width = float(user_input)
        break  # Exit loop if input is valid
    except ValueError:
        print("Invalid input. Please enter a numeric value.")

while True:
    user_input = input("Insert the rectangle length: ")
    try:
        width = float(user_input)
        break  # Exit loop if input is valid
    except ValueError:
        print("Invalid input. Please enter a numeric value.")