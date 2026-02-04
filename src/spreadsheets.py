import pandas as pd

# Create a dictionary representing your data
data = {
    'Name': ['Alice', 'Bob', 'Charlie'],
    'Age': [30, 25, 35],
    'City': ['New York', 'Los Angeles', 'Chicago']
}

# Convert the dictionary to a pandas DataFrame
df = pd.DataFrame(data)

# Write the DataFrame to an Excel (.xlsx) file
df.to_excel("t.xlsx", index=False)
# The index=False argument prevents pandas from writing row numbers as a column
