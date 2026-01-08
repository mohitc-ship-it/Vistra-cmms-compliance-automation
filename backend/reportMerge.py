# import pandas as pd

# # --- Load both Excel files ---
# file1 = "poam.xlsx"        # first file (with Related AO ID)
# file2 = "assessment.xlsx" # second file (with AO ID)

# df2 = pd.read_excel(file1)
# df1 = pd.read_excel(file2)

# # --- Clean up column names ---
# df1.columns = df1.columns.str.strip()
# df2.columns = df2.columns.str.strip()

# # --- Merge df1.Related AO ID with df2.AO ID ---
# merged_df = pd.merge(df1, df2, right_on="Related AO ID", left_on="AO ID", how="left")

# # --- Save merged output ---
# merged_df.to_excel("merged_poam_assessment.xlsx", index=False)

# print("✅ Merged successfully using 'Related AO ID' (file1) and 'AO ID' (file2)")

# # import pandas as pd

# # # --- Load the Excel file ---
# # file_path = "templateExcels/Example POA&M.xlsx"
# # df = pd.read_excel(file_path)
# # print(df.columns)

# # # --- Remove one or more columns ---
# # # Example: remove a single column
# # # df = df.drop(columns=["AO ID"])

# # # Example: remove multiple columns
# # df = df.drop(columns=[ 'Identified Date', 'Target Completion Date', 'Actual Completion Date','Responsible',], errors="ignore")

# # # --- Export to a new Excel file ---
# # output_path = "poam.xlsx"
# # df.to_excel(output_path, index=False)

# # print("✅ Columns removed and new file saved as:", output_path)


import pandas as pd

# --- Load POA&M and Assessment Excel files ---
poam_file = "Data/Reports/poam.xlsx"           # POA&M file
assessment_file = "Data/Reports/assessment.xlsx"  # Assessment file
control_info_file = "templateExcels/Control Info.xlsx"  # Control Info with CMMC Levels and SPRS

# Load files
df_poam = pd.read_excel(poam_file)
df_assessment = pd.read_excel(assessment_file)
df_control_info = pd.read_excel(control_info_file)

# --- Clean column names ---
df_poam.columns = df_poam.columns.str.strip()
df_assessment.columns = df_assessment.columns.str.strip()
df_control_info.columns = df_control_info.columns.str.strip()

# --- Merge POA&M with Assessment based on Related AO ID -> AO ID ---
merged_df = pd.merge(
    df_assessment,
    df_poam,
    left_on="AO ID",
    right_on="Related AO ID",
    how="left"
)

# --- Merge with Control Info based on 'Sort-As' ---
# Bring in Level 1, Level 2, SPRS Score
merged_df = pd.merge(
    merged_df,
    df_control_info[["Sort-As", "CMMC Level 1", "CMMC Level 2", "SPRS","Framework","CMMC ID"]],
    on="Sort-As",
    how="left"
)

# --- Create a new 'Level' column ---
def determine_level(row):
    if pd.notna(row["CMMC Level 1"]) and str(row["CMMC Level 1"]).strip() != "":
        return "Level 1"
    elif pd.notna(row["CMMC Level 2"]) and str(row["CMMC Level 2"]).strip() != "":
        return "Level 2"
    else:
        return "Unknown"

merged_df["Level"] = merged_df.apply(determine_level, axis=1)

# --- Fill missing SPRS Score with 0 if needed ---
merged_df["SPRS"] = merged_df["SPRS"].fillna(0)

columns_to_remove = [
    "Control Owner",
    "Weakness ID_x",
    "Assessment Name",
    "Related Control ID",
    "Related AO ID.Weakness ID_y",
    "CMMC Level 1",
    "CMMC Level 2"
]

merged_df = merged_df.drop(columns=columns_to_remove, errors="ignore")

# --- Save final merged output ---
print(merged_df.columns)
output_file = "merged_poam_assessment.xlsx"
merged_df.to_excel(output_file, index=False)

print(f"✅ Merged successfully! File saved as '{output_file}'")
