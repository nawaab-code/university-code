# write a python program to find factorial of of number using while loop


def enter():
    try:
        number=int(input("Enter a number to calculated for factorial:"))
    except:
        print("Invalid input, try again:")     
        return enter()
    else:
        return number

def main():
    number=enter()
    factorial=1
    while number>0:
        factorial*=number 
        number-=1

    print(f"The factorial of the number:\t{factorial}")

main()