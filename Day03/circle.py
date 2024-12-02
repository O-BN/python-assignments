import argparse
import math

parser = argparse.ArgumentParser(description="Calculate the area and circumference of a circle. Provide a positive radius.")

parser.add_argument('--radius', type=float, default=1.0, help= "The radius of the circle (default: 1.0).")

args = parser.parse_args()

def circle_calc(radius):
    area = math.pi*radius**2
    circumference = 2*math.pi*radius
    return area, circumference

if args.radius >0 :
    area,circumference = circle_calc(args.radius)
    print("Area:", area, "circumference:", circumference)
else:
    print ('Logical error. Value must be greater than zero.')