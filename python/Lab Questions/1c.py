# Write a python program to add 10 numbers by inputting each from the keyboard using for loop.
sum=0
for _ in range(10):
    sum+=(int(input("Enter value:\t")))
print(f"Total sum:\t{sum}")