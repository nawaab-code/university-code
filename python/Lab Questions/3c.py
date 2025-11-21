# Creating a list with elements from 1 to 9
list =list(range(1,10))

# Inserting element 10 at index no. 9
list.insert(9,10) # Insert we have specify the index no. while in append it straight goes to last empty block.
print(f"List after inserting the element:'t{list}")

# Removing the element 10
list.remove(10)
print(f"List after removing the element:'t{list}")

# Appending an element: '10' 
list.append(10)
print(f"List after appending the element:'t{list}")

# Length of the list
print(f"Length of the list:\t{len(list)}")

# Popping an element
print(f"Popped Element:\t{list.pop()}") # Pops last element in the list
print(f"List after popping the last element:\t{list}")

# Clearing the whole list
list.clear()
print(f"List after clearing:\t{list}")