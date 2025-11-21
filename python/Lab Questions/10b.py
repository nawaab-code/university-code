# Write a python function partition() that splits a list of soccer players into two groups.
# More precisely, it takes a list of first names (strings) as input and prints the names of those soccer players whose first name starts with a letter between and including A and M.
# 
# 
# >>>partition([‘Eleanor’, ‘Evelyn’, ‘Sammy’, ‘Owen’, ‘Gavin’])
# Eleanor
# Evelyn
# Gavin
# >>>partition([‘Xena’, ‘Sammy’, ‘Owen’])

def partition(names):
    for name in names:
        if ('A'<= name[0] <='M') or ('a'<= name[0]<='m'):
            print(name)

def main():
    a=0
    list=[]
    for _ in range(int(input("Enter the number of players:\t"))):
        list.append(input("Enter player name:\t"))
        a+=1

    partition(list)
main()