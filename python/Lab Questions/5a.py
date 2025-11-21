# Write a python program to demonstrate built-in modules (Random,Time,Math)
import random
import time
import math

def ran():
    print(f"A random number between 1 and 100{random.randrange(1,100)}")
    print(f"A random number between 0 and 1{random.random()}")
    print(f"A random number between 1 and 100{random.randint(1,100)}")

def current():
    print(f"Current time in seconds: {time.time()}")
    print(f"Current time in a format: {time.ctime(time.time())}")

def calculate():
    print(f"PI value: {math.pi}")
    fac=int(input("Enter a integer: \t"))
    print(f"The Factorial of the entered number is: {math.factorial(fac)}")
    first=int(input("Enter first digit: "))
    second=int(input("Enter the second digit: "))
    print(f"{first} to the power of {second} = {math.pow(first,second)}")
    check=float(input("Enter a decimal value: "))
    print(f"The round up value: {math.ceil(check)}")
    print(f"The round down value: {math.floor(check)}")


def main():
    ran()
    current()
    calculate()

main()