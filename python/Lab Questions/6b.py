# Develop a python program to sort the contents of a file and write the sorted contents to a new file.

with open("example.txt","r") as file:
    lines=file.read().splitlines()

lines.sort()

with open("newexample.txt","w") as file:
    file.writelines(lines)