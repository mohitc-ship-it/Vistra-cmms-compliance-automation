import pandas as pd
import random
from faker import Faker
from datetime import datetime

# Initialize Faker
fake = Faker()

# Load your existing Excel file
df = pd.read_excel("Merged_CMMC_Data.xlsx")  # replace with your actual file

# Ensure these columns exist
for col in ["Doc Name", "Doc Summary", "Confidence", "Date"]:
    if col not in df.columns:
        df[col] = None

# Iterate and fill conditionally
for idx, row in df.iterrows():
    if row.get("Assessment Status") == "Met":
        # Fill only if empty
        if pd.isna(row.get("Doc Name")):
            df.at[idx, "Doc Name"] = fake.file_name(extension="pdf")
        if pd.isna(row.get("Doc Summary")):
            df.at[idx, "Doc Summary"] = fake.sentence(nb_words=8)
        if pd.isna(row.get("Confidence")):
            df.at[idx, "Confidence"] = round(random.uniform(0.5, 1.0), 2)
        if pd.isna(row.get("Date")):
            df.at[idx, "Date"] = fake.date_between(start_date="-2y", end_date="today")

# Save back to Excel
df.to_excel("Mapped_Random_Data.xlsx", index=False)
print("Excel updated with conditional random values!")
