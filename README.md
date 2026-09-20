🐼 Pandas Learning

A practical introduction to Pandas for Python Data Analysis.

📌 Topics Covered

Phase 1 — DataFrame Basics

- What is Pandas?
- What is DataFrame?
- Creating a DataFrame
- DataFrame properties
  - "shape"
  - "columns"
  - "index"
  - "dtypes"
  - "size"
  - "ndim"
  - "info()"
  - "describe()"

Phase 2 — Data Access

- Column selection
- Row selection
- Indexing
  - "loc[]"
  - "iloc[]"
- Slicing
- Multiple column selection

Phase 3 — Data Manipulation

- Create a new column
- Update a column
- Delete a column
- Rename columns
- Sorting with "sort_values()"
- Filtering with conditions

---

1. Import Pandas

import pandas as pd

---

2. Create a DataFrame

data = {
    "name": ["Rahim", "Karim", "Hasan"],
    "age": [20, 22, 21],
    "city": ["Dhaka", "Rajshahi", "Chittagong"]
}

df = pd.DataFrame(data)

print(df)

Output

    name  age        city
0  Rahim   20       Dhaka
1  Karim   22    Rajshahi
2  Hasan   21  Chittagong

---

3. DataFrame Properties

"shape"

Returns rows and columns.

print(df.shape)

Output:

(3, 3)

---

"columns"

Returns column names.

print(df.columns)

Output:

Index(['name', 'age', 'city'], dtype='object')

---

"index"

Returns row indexes.

print(df.index)

Output:

RangeIndex(start=0, stop=3, step=1)

---

"dtypes"

Shows data type of each column.

print(df.dtypes)

Output:

name    object
age      int64
city    object
dtype: object

---

"size"

Returns total number of elements.

print(df.size)

Output:

9

---

"ndim"

Returns number of dimensions.

print(df.ndim)

Output:

2

---

"info()"

Shows DataFrame information.

df.info()

---

"describe()"

Shows statistical summary of numerical columns.

print(df.describe())

---

4. Column Selection

Select One Column

print(df["name"])

Output:

0    Rahim
1    Karim
2    Hasan
Name: name, dtype: object

---

Select Multiple Columns

print(df[["name", "age"]])

Output:

    name  age
0  Rahim   20
1  Karim   22
2  Hasan   21

---

5. Row Selection

Using Index

print(df.iloc[0])

Output:

name     Rahim
age         20
city     Dhaka
Name: 0, dtype: object

---

6. "loc[]"

"loc[]" is used for label-based selection.

print(df.loc[0])

Select specific columns:

print(df.loc[0, "name"])

Output:

Rahim

---

7. "iloc[]"

"iloc[]" is used for position-based selection.

print(df.iloc[0, 1])

Output:

20

Here:

0 → first row
1 → second column

---

8. Slicing

Select multiple rows:

print(df.iloc[0:2])

Output:

    name  age      city
0  Rahim   20     Dhaka
1  Karim   22  Rajshahi

Select rows and columns:

print(df.iloc[0:2, 0:2])

Output:

    name  age
0  Rahim   20
1  Karim   22

---

9. Create a New Column

df["country"] = "Bangladesh"

print(df)

Output:

    name  age        city    country
0  Rahim   20       Dhaka  Bangladesh
1  Karim   22    Rajshahi  Bangladesh
2  Hasan   21  Chittagong  Bangladesh

---

10. Update a Column

df["age"] = df["age"] + 1

print(df["age"])

Output:

0    21
1    23
2    22
Name: age, dtype: int64

---

11. Delete a Column

Using "drop()":

df = df.drop("country", axis=1)

print(df)

"axis=1" means column.

---

12. Rename Columns

df = df.rename(columns={
    "name": "student_name",
    "age": "student_age"
})

print(df)

Output:

  student_name  student_age        city
0        Rahim           21       Dhaka
1        Karim           23    Rajshahi
2        Hasan           22  Chittagong

---

13. Sorting

Sort Ascending

df = df.sort_values("student_age")

print(df)

---

Sort Descending

df = df.sort_values("student_age", ascending=False)

print(df)

---

14. Filtering

Filtering allows us to select rows based on conditions.

Age Greater Than 21

result = df[df["student_age"] > 21]

print(result)

---

Age Equal to 22

result = df[df["student_age"] == 22]

print(result)

---

Multiple Conditions

Use "&" for AND:

result = df[
    (df["student_age"] > 20) &
    (df["city"] == "Rajshahi")
]

print(result)

Use "|" for OR:

result = df[
    (df["city"] == "Dhaka") |
    (df["city"] == "Rajshahi")
]

print(result)

---

🧠 Quick Reference

Task| Pandas
Create DataFrame| "pd.DataFrame()"
Rows & Columns| "df.shape"
Column names| "df.columns"
Index| "df.index"
Data types| "df.dtypes"
Information| "df.info()"
Statistics| "df.describe()"
One column| "df["column"]"
Multiple columns| "df[["a", "b"]]"
Label selection| "df.loc[]"
Position selection| "df.iloc[]"
Create column| "df["new"] = ..."
Delete column| "df.drop()"
Rename| "df.rename()"
Sort| "df.sort_values()"
Filter| "df[condition]"

---

🚀 Next Topics

- Reading CSV files
- Reading Excel files
- Handling missing values
- "groupby()"
- Aggregation
- Merging / Joining
- Data cleaning
- Time Series with Pandas

---

🛠️ Tech Used

- Python
- Pandas
- NumPy

---

📚 Status

Pandas Fundamentals — Completed ✅