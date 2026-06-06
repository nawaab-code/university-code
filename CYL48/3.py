import pandas as pd

# --- Series from a List ---
marks_list = [85, 90, 78, 92, 88]
series_list = pd.Series(marks_list, index=['Math', 'Science', 'English', 'History', 'PE'])
print("Series from List:\n", series_list)

# --- Series from a Dictionary ---
marks_dict = {'Math': 85, 'Science': 90, 'English': 78, 'History': 92, 'PE': 88}
series_dict = pd.Series(marks_dict)
print("\nSeries from Dictionary:\n", series_dict)
