# Write a Python program to store PROFILE_DATA(user_id, name, DOB, qualification, work_experience) in a dictionary and pretty print the dictionary contents. (import pprint)

import pprint  # Import the pprint module

# Step 1: Create a dictionary to store profile data
PROFILE_DATA = {
    "user_id": 101,
    "name": "John Doe",
    "DOB": "1995-06-15",
    "qualification": "Master's in Computer Science",
    "work_experience": "5 years in Software Development"
}

# Step 2: Pretty print the dictionary
print("User Profile Data:")
pprint.pprint(PROFILE_DATA)