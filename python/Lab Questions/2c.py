# Write a python program to define a function generate_n_chars() that takes an integer n and a character c and returns a string, n characters long. For example, generate_n_chars(5,"x") should return the string "xxxxx" using keyword only parameters

def generate_n_chars(n,s):
    r=""
    for i in range(1,n):
        r=r+s
    return r

def main():
    s=input("Enter a character to be converted to a string:\t")
    n=int(input("Enter the times the character to be multiplied:\t"))
    print(f"String:\t{generate_n_chars(n,s)}")

main()