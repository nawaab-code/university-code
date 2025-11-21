# Program to create a text file where user inputs 5 lines of text then it finds the shortest and longest word in the file with there respective length

def find(filename):
    with open(filename,"r") as file:
        words=file.read().split()#words will store each word as a tuple since .split() seprate each word by whitespace or newline
    
    upper=max(words,key=len)# max will find the longest word by length since key=len, in the tuple 
    lower=min(words,key=len)

    print(f"Longest word is: {upper} with the length of {len(upper)}")# f is there so we can call variables/operations in {}
    print(f"Shortest word is: {lower} with the length of {len(lower)}")

def main():
    with open("newfile.txt","w") as file:
        print("Please enter 5 lines of text.")
        for _ in range(5):# _ is a placeholder
            line=input()
            file.write(line+"\n")
    find("newfile.txt")

main()