import pandas as pd

data = {
    "Name": ["Rahim", "Karim", "Hasan"],
    "Age": [22, 25, 24],
    "Salary": [20000, 30000, 25000]
}

df = pd.DataFrame(data)

print(df)

df.shape       # Number of rows and columns?
df.columns     # Column names?
df.index       # Row index?
df.dtypes      # Data types?
df.info()      # Information about the entire DataFrame
df.describe()  # Statistics for numeric data

# Column       → df["Name"]
# Multiple     → df[["Name", "Salary"]]
# Row          → df.iloc[0]
# Position     → iloc[]
# Label        → loc[]
# Slicing      → iloc[0:2]
# New Column   → df["Bonus"] = ...
# Update       → df["Salary"] = ...
# Delete       → drop()
# Rename       → rename()
# Sort         → sort_values()
# Filter       → df[df["Age"] > 23]