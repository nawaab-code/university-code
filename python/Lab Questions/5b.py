# Create a user defined module using python to execute the following:
# a) area of circle
# b) area of triangle
# c) area of rectangle.

import math

def area_of_circle(radius):
    return (math.pi*(math.pow(radius,2)))

def area_of_triangle(height,breadth):
    return ((height*breadth)*0.5)

def area_of_rectangle(length,breadth):
    return (length*breadth)