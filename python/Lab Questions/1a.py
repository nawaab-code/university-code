# Write a python program to read 2 numbers from the keyboard and perform the basic arithmetic operations based on the choice. (1-Add, 2-Subtract, 3-Multiply, 4-Divide)
first=int(input("Enter the first value.:\t"))
second=int(input("Enter the second value:\t"))

choose=int(input("1:Add 2:Subtract 3:Multiply 4:Divide:\t"))

if(choose==1):
    print(f"Sum:\t{first+second}")
elif(choose==2):
    print(f"Subtracted:\t{first-second}")
elif(choose==3):
    print(f"Multipy:\t{first*second}")
elif(choose==4):
    print(f"Dividend:\t{first/second}")
else:
    print("Invalid Input.")

