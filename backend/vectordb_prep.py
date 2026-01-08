import pandas as pd
from collections import defaultdict
import json

# File paths
control_info_path = "templateExcels/Control Info.xlsx"
assessment_path = "templateExcels/800-171 Assessment Template.xlsx"

# Read both Excel files
df_controls = pd.read_excel(control_info_path)
df_assessment = pd.read_excel(assessment_path)

# Group control info by Control ID
control_chunks = defaultdict(list)
for _, row in df_controls.iterrows():
    control_chunks[row["Control ID"]].append(row)

# Map assessment info by Control ID
assessment_info = {}
for _, row in df_assessment.iterrows():
    control_id = str(row["Control ID"]).strip()
    assessment_info[control_id] = {
        "Examine": str(row.get("Potential Assessment Method and Objects: Examine", "")).strip(),
        "Interview": str(row.get("Potential Assessment Method and Objects: Interview", "")).strip(),
        "Test": str(row.get("Potential Assessment Method and Objects: Test", "")).strip()
    }

embedding_data = []

# Process each control
for control_id, rows in control_chunks.items():
    text_chunks = []
    ao_ids = []

    for row in rows:
        # Handle NaN in levels
        levels = []
        if pd.notna(row["CMMC Level 1"]):
            levels.append(row["CMMC Level 1"])
        if pd.notna(row["CMMC Level 2"]):
            levels.append(row["CMMC Level 2"])

        # Collect AO IDs
        if pd.notna(row.get("AO ID")):
            ao_ids.append(str(row["AO ID"]))

        # Build sentence
        sentence = (
            f"This is a {row['Framework']} control in the {row['Family']} family. "
            f"It corresponds to {', '.join(levels) if levels else 'no CMMC level specified'}. "
            f"The control ID is {row['CMMC ID']} with title '{row['CMMC Title']}'. "
            f"Security requirement: {row['Security Requirement']}. "
            f"Assessment objective ({row['AO ID']}): {row['Assessment Objective']}. "
            f"POA&M allowed: {row['POA&M Allowed']}. "
            f"SPRS score: {row['SPRS']}."
        )
        text_chunks.append(sentence)

    # Combine sentences
    main_text = "\n".join(text_chunks)

    # Get potential assessment methods (if available)
    assessment_methods = []
    assess_data = assessment_info.get(control_id)
    if assess_data:
        for method_type, desc in assess_data.items():
            if desc and desc.lower() != "nan":
                assessment_methods.append({
                    "type": method_type,
                    "description": desc
                })

    # Build metadata
    first_row = rows[0]
    levels_cleaned = [lvl for lvl in [first_row.get("CMMC Level 1"), first_row.get("CMMC Level 2")] if pd.notna(lvl)]
    metadata = {
        "framework": first_row["Framework"],
        "family": first_row["Family"],
        "control_id": first_row["Control ID"],
        "cmmc_id": first_row["CMMC ID"],
        "title": first_row["CMMC Title"],
        "sprs": first_row["SPRS"],
        "cmmc_levels": levels_cleaned,
        "poam_allowed": first_row["POA&M Allowed"],
        "ao_ids": ao_ids,  # still keeping AO ID list
        "assessment_methods": assessment_methods , # ✅ new section
    }

    embedding_data.append({
        "text": main_text,
        "metadata": metadata,
        "last_ao_sentence" : rows[-1]["Assessment Objective"]
    })

# Save as JSON
with open("embedding_data.json", "w") as f:
    json.dump(embedding_data, f, indent=2)

print(f"✅ Prepared {len(embedding_data)} chunks with assessment methods for embedding")
