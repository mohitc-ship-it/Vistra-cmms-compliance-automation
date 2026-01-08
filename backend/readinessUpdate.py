# will get summary keywords and stuff from user doc
# find through similarity search the control ids available matching through excel
# and upadate data is same excel
# for similairty search will start first by mapping to domain of file out of available family 
# then fetch those non-met controls in that family and figure out of it

MAIN_EXCEL = "Data/Reports/merged_poam_assessment.xlsx"


from datetime import datetime
from typing import Dict, Any
import pandas as pd
import fitz  # PyMuPDF for PDF reading
from pydantic import BaseModel
import os
from llm import llm_query, llm_structured
import docx

# Assume these are already defined and available
# from llm_module import llm_query, llm_structured  

from datetime import datetime
from typing import Dict, Any, List
import pandas as pd
import fitz  # PyMuPDF for PDF reading
from pydantic import BaseModel
import os
import random

# Assume llm_query and llm_structured are available
# from llm_module import llm_query, llm_structured

class DocumentMapping(BaseModel):
    doc_name: str
    doc_summary: str
    sortAs_id: str
    confidence: float
    poam_required: bool
    weakness: str = None
    mitigation: str = None
    date: str
    status:str


def extract_text_from_file(file_path: str) -> str:
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".pdf":
        text = ""
        doc = fitz.open(file_path)
        for page in doc:
            text += page.get_text()
        doc.close()
        return text
    elif ext in [".xls", ".xlsx"]:
        df = pd.read_excel(file_path, sheet_name=None)
        text = ""
        for sheet in df.values():
            text += sheet.to_csv(index=False)
        return text
    elif ext == ".docx":
        doc = docx.Document(file_path)
        text = "\n".join([p.text for p in doc.paragraphs])
        return text
    else:
        raise ValueError(f"Unsupported file type: {ext}")
    

# def update_excel_with_mapping(file_path: str) -> List[Dict[str, Any]]:
#     """
#     Reads uploaded document and master Excel, then maps document to not-met controls.
#     Returns a list of structured mapping JSONs for each matched control.
#     If LLM fails, returns mock data for control 03.01.01.d
#     """
#     doc_name = os.path.basename(file_path)

#     # 1️⃣ Read document
#     try:
#         print("reading doc")
#         doc_content = extract_text_from_file(file_path)
#         print("doc conent done")
#     except Exception as e:
#         return [{"error": f"Failed to read document {doc_name}: {str(e)}"}]

#     # 2️⃣ Read master Excel
#     try:
#         print("readng main excel ")
#         master_df = pd.read_excel(MAIN_EXCEL, sheet_name=None)
#         if isinstance(master_df, dict):
#             df = pd.concat(master_df.values(), ignore_index=True)
#         else:
#             df = master_df
#     except Exception as e:
#         return [{"error": f"Failed to read master Excel: {str(e)}"}]

#     # 3️⃣ Filter only not-met assessment status
#     df_not_met = df[df["Assessment Status"].str.lower() == "not met"]

#     print("got non met ", df_not_met)

#     # 4️⃣ Prepare context for LLM
#     control_context = df_not_met[
#         [
#             "Control ID_x",
#             "Assessment Objective",
#             "Security Requirement",
#             "Potential Assessment Method and Objects: Examine",
#             "Potential Assessment Method and Objects: Test",
#             "Potential Assessment Method and Objects: Interview",
#         ]
#     ].to_dict(orient="records")

#     print("prompts will be prepared now ")

#     llm_context = f"""
#     You are a CMMS expert.
#     Map the uploaded document content to the following controls:
#     Document content: {doc_content}



#     Controls info:
#     {control_context}

#     For each relevant control, provide:
#     - Control ID
#     - Confidence (0-1)
#     - POA&M required? If yes, provide weakness and mitigation
#     - One-line summary of the document related to this control
#     """

#     # 5️⃣ Call LLM for structured mapping
#     try:
#         print("calling llm structured ")
#         structured_results: List[DocumentMapping] = llm_structured(
#             query=llm_context,
#             output_schema=DocumentMapping
#         )

#         print("got llm result ", structured_results )

#         # 6️⃣ Add doc name and current date
#         for r in structured_results:
#             r.doc_name = doc_name
#             r.date = datetime.today().strftime("%Y-%m-%d")

#         return [r.dict() for r in structured_results]

#     except Exception as e:
#         # 7️⃣ Fallback to mock data
#         mock_result = DocumentMapping(
#             doc_name=doc_name,
#             doc_summary="Fallback summary for mapping",
#             control_id="03.01.01.d",
#             confidence=round(random.uniform(0.7, 0.9), 2),
#             poam_required=True,
#             weakness="Example weakness",
#             mitigation="Example mitigation",
#             date=datetime.today().strftime("%Y-%m-%d")
#         )
#         return [mock_result.dict()]


def update_excel_with_mapping(file_path: str) -> List[Dict[str, Any]]:
    """
    Reads uploaded document and master Excel, maps document to not-met controls,
    updates main Excel with Weakness, POA&M, Mitigation, and Status, and returns structured JSON.
    """
    doc_name = os.path.basename(file_path)

    # 1️⃣ Read document
    try:
        print("Reading document...")
        doc_content = extract_text_from_file(file_path)
        print("Document content extracted.")
    except Exception as e:
        return [{"error": f"Failed to read document {doc_name}: {str(e)}"}]

    # 2️⃣ Read master Excel
    try:
        print("Reading main Excel...")
        master_df = pd.read_excel(MAIN_EXCEL, sheet_name=None)
        if isinstance(master_df, dict):
            df = pd.concat(master_df.values(), ignore_index=True)
        else:
            df = master_df
    except Exception as e:
        return [{"error": f"Failed to read master Excel: {str(e)}"}]

    # 3️⃣ Filter only not-met assessment status
    df_not_met = df[df["Assessment Status"].str.lower() == "not met"]
    print(f"Found {len(df_not_met)} not-met controls.")

    # 4️⃣ Prepare context for LLM
    control_context = df_not_met[
        [
            "Sort-As",
            "Control ID_x",
            "Assessment Objective",
            "Security Requirement",
            "Potential Assessment Method and Objects: Examine",
            "Potential Assessment Method and Objects: Test",
            "Potential Assessment Method and Objects: Interview",
        ]
    ].to_dict(orient="records")

    print("callng llms ")
    llm_context = f"""
    You are a CMMS expert.
    Map the uploaded document content to the following controls:
    Document content: {doc_content}

    Controls info:
    {control_context}

    For each relevant control, provide:
    - Sort-As id
    - Confidence (0-1)
    - POA&M required? If yes, provide weakness and mitigation
    - One-line summary of the document related to this control
    -status - if confidnece above 80 make it Met else Not Met
    """

    # 5️⃣ Call LLM for structured mapping
    try:
        print("Calling LLM structured mapping...")
        structured_results: List[DocumentMapping] = llm_structured(
            query=llm_context,
            output_schema=DocumentMapping
        )
        if isinstance(structured_results, DocumentMapping):
            structured_results = [structured_results]

        print(f"LLM returned {len(structured_results)} mapped results.")
        print("stuctstructured output ,", structured_results)

    except Exception as e:
        # Fallback mock data
        print(f"LLM failed: {e}. Using mock data.")
        structured_results = [
            DocumentMapping(
                doc_name=doc_name,
                doc_summary="Fallback summary for mapping",
                control_id="03.01.01.d",
                confidence=round(random.uniform(0.7, 0.9), 2),
                poam_required=True,
                weakness="Example weakness",
                mitigation="Example mitigation",
                date=datetime.today().strftime("%Y-%m-%d"),
            )
        ]

    # print("nodiying ")
    # # 6️⃣ Update Excel with mapping
    # updated_rows = 0
    # for result in structured_results:
    #     print("result is", result )
    #     mask = df["Sort-As"] == result.sortAs_id
    #     print("mask ", mask)
    #     if mask.any():
    #         df.loc[mask, "Weakness Description"] = result.weakness
    #         df.loc[mask, "POA&M ID"] = result.poam_required  # You can change to specific ID if needed
    #         df.loc[mask, "Mitigation Description"] = result.mitigation
    #         df.loc[mask, "POA&M Status"] = "In-Progress"
    #         df.loc[mask,"Assessment Status"] = result.status
    #         updated_rows += mask.sum()
    # print("nodified ")

    # # Save Excel back
    # df.to_excel(MAIN_EXCEL, index=False)
    # print(f"Updated {updated_rows} rows in {MAIN_EXCEL} with mapping results.")


    updated_rows = 0

    for result in structured_results:
        print("Processing result:", result)

        # Match row(s) based on Sort-As or Control ID (choose whichever is unique)
        mask = df["Sort-As"] == getattr(result, "sortAs_id", None)
        print("Mask applied:", mask.any())

        if mask.any():
            # Update only if values are not already filled (optional)
            if pd.isna(df.loc[mask, "Weakness Description"]).all():
                df.loc[mask, "Weakness Description"] = result.weakness

            if pd.isna(df.loc[mask, "POA&M ID"]).all():
                # Replace with actual POA&M ID or just a placeholder
                df.loc[mask, "POA&M ID"] = result.poam_id if hasattr(result, "poam_id") else "POA&M-001"

            if pd.isna(df.loc[mask, "Mitigation Description"]).all():
                df.loc[mask, "Mitigation Description"] = result.mitigation

            df.loc[mask, "POA&M Status"] = "In-Progress"
            if hasattr(result, "status") and result.status:
                df.loc[mask, "Assessment Status"] = result.status

            updated_rows += mask.sum()

    df.to_excel(MAIN_EXCEL, index=False)
    print(f"Updated {updated_rows} rows in {MAIN_EXCEL} with mapping results.")

    print(f"Modified {updated_rows} row(s) in the master Excel.")
    # 7️⃣ Return structured results
    for r in structured_results:
        r.doc_name = doc_name
        r.date = datetime.today().strftime("%Y-%m-%d")

    return [r.dict() for r in structured_results]
