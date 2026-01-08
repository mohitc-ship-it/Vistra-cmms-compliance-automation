import pandas as pd

# Load the first Excel file (your uploaded/mapped data)
mapped_file = "MappedControlsHistory.xlsx"  # Replace with your file path
df_mapped = pd.read_excel(mapped_file)

# Load the second Excel file (your template with extra columns)
template_file = "Data/Reports/merged_poam_assessment_old.xlsx"  # Replace with your file path
df_template = pd.read_excel(template_file)

# Merge on 'Sort-As' and 'Control ID'
merged_df = pd.merge(
    df_template,
    df_mapped,
    how="left",  # keep all rows from template
    left_on=["Sort-As"],
    right_on=["Control ID"]
)

# Optional: reorder columns or fill missing values
# merged_df.fillna("-", inplace=True)

columns_to_remove = [
    "Control ID_y"
]

merged_df = merged_df.drop(columns=columns_to_remove, errors="ignore")

# Save the merged result
merged_df.to_excel("Merged_CMMC_Data.xlsx", index=False)
print("Merged file saved as 'Merged_CMMC_Data.xlsx'")
