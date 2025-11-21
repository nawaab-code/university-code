# Write a python program to define a function max_of_three() that takes three numbers as arguments adn returns the largest of them using default arguments

def max_of_three(a,b,c):
    return max(a,b,c)

def main():
    store=[]
    print("Enter three values:")
    for i in range(3):
        try:
            store.append(int(input(f"Enter the {i} value:\t")))
        except:
            print("Invalid input")
            exit()
    print(f"The max of the three numbers is:\t{max_of_three(store[0],store[1],store[2])}")

main()