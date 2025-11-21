# Write a python program to Build a number guessing game. When the user enters not an integer raise the Exception and print the total number of guesses.
import random

def guess(number):
    right=random.randint(1,10)
    if number==right:
        return True
    else:
        return False
    
def enter(count):
    try:
        number=int(input("Please enter an integer between 1 and 10: \t"))
    except:
        print("Value entered wasn't an integer.")
        print(f"Number of guesses:\t{count}")
    else:
        return number

def main():
    count=0
    while True:
        if guess(enter(count))==True:
            print("Right Guess.")
            break
        else:
            print("Try again.")
            count+=1

main()