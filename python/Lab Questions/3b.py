# Step 1: Create a list of strings with items
strings = ["Python", "AI", "Machine Learning", "Data", "Science"]

# Step 2: Create an empty list to store tuples
tuples_list = []

# Step 3: Loop through each string and create a tuple (string, length)
for i in strings:
    tuples_list.append((i, len(i)))  # append will create a tuple each time with the item string as first value and length of the string as the second value.

# Step 4: Sort the list based on the second element (length of the string)
sorted_tuples = sorted(tuples_list, key=lambda x: x[1])
# key is the basis of sorting
# lambda is creating a single line functions where it is accepting a tuple and returns the second stored value fo the tuple which is the length of the string.

# Step 5: Print the sorted list of tuples
print(sorted_tuples)