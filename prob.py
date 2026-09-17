import pandas as pd

# =====================================================================
# PHASE 1 — Basic
# =====================================================================
print("--- PHASE 1: BASICS ---")

# 1. Series
my_list = [10, 20, 30, 40]
series_data = pd.Series(my_list)
print("Pandas Series:\n", series_data, "\n")

# 2. DataFrame from Dictionary (with intentional missing & duplicate rows)
data_dict = {
    "Name": ["Abir", "Bijoy", "Chayan", "Abir", "Esha"],
    "Age": [23, None, 22, 23, 29],  # None acts as a missing value (NaN)
    "City": ["Dhaka", "Khulna", "Sylhet", "Dhaka", "Dhaka"],
    "Salary":,
    "Department": ["IT", "HR", "IT", "IT", "HR"],
}
df = pd.DataFrame(data_dict)
print("Initial DataFrame:\n", df, "\n")

# 3. DataFrame from List
list_data = [["Anik", 24], ["Binu", 26]]
df_from_list = pd.DataFrame(list_data, columns=["Name", "Age"])

# 4. DataFrame Properties
print("Shape (Rows, Columns):", df.shape)
print("Columns:", df.columns.tolist())
print("Data Types:\n", df.dtypes)
print("\n--- df.info() output ---")
df.info()
print("\n--- df.describe() output ---")
print(df.describe(), "\n")


# =====================================================================
# PHASE 2 — Data Access
# =====================================================================
print("--- PHASE 2: DATA ACCESS ---")

# 1. Column Select
print("Select Name Column:\n", df["Name"], "\n")

# 2. Multiple Columns Select
print("Select Name and Salary Columns:\n", df[["Name", "Salary"]], "\n")

# 3. loc[] (Label-based)
print("loc - Row 0, 'Name' column:", df.loc[0, "Name"])

# 4. iloc[] (Integer position-based)
print("iloc - Row 0, Column 3 (Salary):", df.iloc[0, 3], "\n")

# 5. Slicing
print("Slicing rows 1 to 3 using iloc:\n", df.iloc[1:4], "\n")


# =====================================================================
# PHASE 4 — Data Cleaning
# =====================================================================
print("--- PHASE 4: DATA CLEANING ---")

# 1. Missing Values (isnull)
print("Check for null values:\n", df.isnull().sum())

# Fill missing Age with the mean/average age (fillna)
mean_age = df["Age"].mean()
df["Age"] = df["Age"].fillna(mean_age)
print("\nDataFrame after filling missing Age:\n", df, "\n")

# Alternative: You can use df.dropna() to remove rows with missing values

# 2. Duplicate (duplicated & drop_duplicates)
print("Is row duplicated?: \n", df.duplicated())
df = df.drop_duplicates()
print("\nDataFrame after dropping duplicates:\n", df, "\n")

# 3. Data type change (astype)
df["Age"] = df["Age"].astype(int)
print("Data types after conversion:\n", df.dtypes, "\n")


# =====================================================================
# PHASE 5 — Data Analysis
# =====================================================================
print("--- PHASE 5: DATA ANALYSIS ---")

# 1. Aggregate Functions
print("Total Salary sum:", df["Salary"].sum())
print("Average Salary:", df["Salary"].mean())
print("Minimum Age:", df["Age"].min())
print("Maximum Age:", df["Age"].max())
print("Count of entries in Name:", df["Name"].count(), "\n")

# 2. groupby()
print("Average Salary by Department:\n", df.groupby("Department")["Salary"].mean(), "\n")

# 3. value_counts()
print("Count of employees in each City:\n", df["City"].value_counts(), "\n")


# =====================================================================
# PHASE 6 — Real Data & Combining
# =====================================================================
print("--- PHASE 6: REAL DATA & COMBINING ---")

# 1. CSV read/write
df.to_csv("employees.csv", index=False)
df_loaded = pd.read_csv("employees.csv")
print("Data successfully loaded from CSV.\n")

# 2. Concat
# df_extra = pd.DataFrame(
#     {"Name": ["Fahim"], "Age":, "City": ["Rajshahi"], "Salary":, "Department": ["IT"]}
# )
# df_concatenated = pd.concat([df, df_extra], axis=0, ignore_index=True)
# print("DataFrame after Concat:\n", df_concatenated, "\n")

# 3. Merge / Join
dept_info = pd.DataFrame({"Department": ["IT", "HR"], "Floor": ["3rd Floor", "5th Floor"]})
df_merged = pd.merge(df_concatenated, dept_info, on="Department")
print("DataFrame after Merging Department info:\n", df_merged)