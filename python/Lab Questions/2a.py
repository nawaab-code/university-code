#  Write a python linearSearch() to read an array and search for the key element.
# Display the appropriate messeage. USE RECURSIVE TECHNIQUE

def linearSearch(value,search,compare):
    if compare>=0:
        if value[compare]==search:
            return True
        else:
            compare-=1
            return linearSearch(value,search,compare)
    else:
        return False

def main():
    values=[]
    size=int(input("Enter the size of the array:\t"))
    for i in range(size):
        values.append(input(f"Please enter the {i+1}st value:\t"))

    search=input("Enter the value to be searched:/t")

    if linearSearch(values,search,(size-1))==True:
        print("Found")
    else:
        print("Not found.")

main()


    