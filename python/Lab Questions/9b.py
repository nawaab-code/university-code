# Write a python function named DivExp which takes TWO parameters a, b and returns a value c (c=a/b). Write suitable assertion for a>0 in function DivExp and raise an exception for when b=0. Develop a suitable program which reads two values from the console and calls a function DivExp.

def DivExp(a,b):
    assert a>0,"First number should be greater than 0."

    if b==0:
        raise ValueError("Value b can't be zero")
    else:
        return a/b
    
def main():
    try:
        a=float(input("Enter a number greater than 0: \t"))
        b=float(input("Enter a number not equal to 0: \t"))
        print(DivExp(a,b))
    except AssertionError as ae:
        print(ae)
    except ValueError as ve:
        print(ve)

main()