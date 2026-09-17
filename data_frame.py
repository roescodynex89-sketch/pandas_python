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

