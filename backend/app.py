from fastapi import FastAPI, UploadFile, File, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from chatbot import chat
from chatbot import summarize_user_excel
import pandas as pd

app = FastAPI()

# Allow CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # change in production
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# Pydantic models
# -----------------------------
class Mapping(BaseModel):
    control: str
    status: str

class FileItem(BaseModel):
    name: str
    size: int
    type: str

class MapFilesRequest(BaseModel):
    files: List[FileItem]

class UploadedHistory(BaseModel):
    name: str
    size: int
    type: str
    mappedControls: Optional[List[Mapping]] = None

# -----------------------------
# In-memory "database"
# -----------------------------
HISTORY: List[UploadedHistory] = [
    UploadedHistory(
        name="existing_file.pdf",
        size=102400,
        type="application/pdf",
        mappedControls=[
            Mapping(control="AC.L1-3.1.1", status="Access limited to authorized users."),
            Mapping(control="AC.L1-3.1.2", status="Device use limited to authorized users."),
            Mapping(control="IA.L2-3.5.3", status="MFA required for network access."),
        ],
    )
]

# -----------------------------
# API endpoints
# -----------------------------

@app.get("/api/history", response_model=List[UploadedHistory])
async def get_history():
    """
    Return historical uploaded files.
    """
    return HISTORY


@app.post("/api/map-files", response_model=List[Mapping])
async def map_files(request: MapFilesRequest):
    """
    Simulate AI mapping for uploaded files.
    """
    mapped_controls = []
    for file in request.files:
        # For demo, just generate a fake mapping
        mapped_controls.append(Mapping(control="AC.L1-3.1.1", status=f"Mapped {file.name} control 1"))
        mapped_controls.append(Mapping(control="AC.L1-3.1.2", status=f"Mapped {file.name} control 2"))
        mapped_controls.append(Mapping(control="IA.L2-3.5.3", status=f"Mapped {file.name} control 3"))

        # Save to history
        HISTORY.append(UploadedHistory(
            name=file.name,
            size=file.size,
            type=file.type,
            mappedControls=[
                Mapping(control="AC.L1-3.1.1", status=f"Mapped {file.name} control 1"),
                Mapping(control="AC.L1-3.1.2", status=f"Mapped {file.name} control 2"),
                Mapping(control="IA.L2-3.5.3", status=f"Mapped {file.name} control 3"),
            ]
        ))

    return mapped_controls


# -----------------------------
# Run with:
# uvicorn main:app --reload
# -----------------------------


class ChatRequest(BaseModel):
    user_input: str


@app.post("/api/chat")
async def chat_endpoint(req: ChatRequest):
    user_input = req.user_input.strip()

    # ---- Routing Logic ----
    # (Simplified version of your pseudocode)
    # if "readiness" in user_input.lower() or "evaluation" in user_input.lower():
    #     retriever = create_retriever("./chroma_db_vistra", "cmms_rag")
    #     response = rag(user_input, retriever)
    # elif "what is" in user_input.lower() or "explain" in user_input.lower():
    #     response = llm_structured(user_input)
    # else:
    #     retriever = create_retriever("./chroma_db_vistra", "cmms_rag")
    #     response = rag(user_input, retriever)
    response = chat(user_input)

    return {"response": response}



DEFAULT_CONTROLS = [
    {"id": "AC.L1-3.1.1", "name": "Limit information system access to authorized users.", "level": "Level 1", "status": "Met"},
    {"id": "AC.L1-3.1.2", "name": "Limit use of devices to authorized users.", "level": "Level 1", "status": "Pending"},
    {"id": "IA.L2-3.5.3", "name": "Use multifactor authentication.", "level": "Level 2", "status": "Not Met"},
]

# Response models
class ControlRow(BaseModel):
    id: str
    name: str
    level: str
    status: str

class DashboardResponse(BaseModel):
    kpis: dict
    matched_rows: List[ControlRow]
    summary: dict

# @app.get("/api/dashboard")
# def get_dashboard(level: Optional[str] = Query("All")):
#     print("level ",level)
#     excel_file = "Data/Reports/merged_poam_assessment.xlsx"

#     try:
#         # Load Excel
#         df = pd.read_excel(excel_file)

#         # Standardize Assessment Status
#         df["Assessment Status"] = df["Assessment Status"].fillna("Not Assessed")

#         # Map statuses to match frontend expected values
#         def map_status(status):
#             if status == "Met":
#                 return "Met"
#             elif status == "Not Met":
#                 return "Not Met"
#             else:
#                 return "Pending"

#         df["status"] = df["Assessment Status"].apply(map_status)
#         df["level"] = df["Level"].fillna("Unknown").astype(str)
#         df["id"] = df["Sort-As"].fillna("").astype(str)
#         df["name"] = df["Assessment Objective"].fillna("").astype(str)

#         # Filter by level
#         if level != "All":
#             df = df[df["level"] == level]
#             print("filterd ", df.head())

#         # Prepare matched_rows for frontend
#         matched_rows = df[["id", "name", "level", "status"]].to_dict(orient="records")

#         return {"matched_rows": matched_rows}

#     except Exception as e:
#         print("Error fetching dashboard data:", e)
#         # Fallback static data for frontend
#         fallback_controls = [
#             {"id": "AC.L1-3.1.1", "name": "Limit information system access to authorized users.", "level": "Level 1", "status": "Met"},
#             {"id": "AC.L1-3.1.2", "name": "Limit use of devices to authorized users.", "level": "Level 1", "status": "Pending"},
#             {"id": "IA.L2-3.5.3", "name": "Use multifactor authentication.", "level": "Level 2", "status": "Not Met"},
#         ]
#         return {"matched_rows": fallback_controls}
    


from fastapi import FastAPI, Query
from typing import Optional
import pandas as pd
import numpy as np


from chatbot import summarize_user_excel  # adjust path

# @app.get("/api/dashboard")
# def get_dashboard(level: Optional[str] = Query("All")):
#     excel_file = "Data/Reports/merged_poam_assessment.xlsx"

#     try:
#         # Load Excel
#         df = pd.read_excel(excel_file)

#         # Standardize Assessment Status
#         df["Assessment Status"] = df["Assessment Status"].fillna("Not Assessed")

#         # Map statuses to match frontend expected values
#         def map_status(status):
#             if status == "Met":
#                 return "Met"
#             elif status == "Not Met":
#                 return "Not Met"
#             else:
#                 return "Pending"

#         df["status"] = df["Assessment Status"].apply(map_status)
#         df["level"] = df["Level"].fillna("Unknown").astype(str)
#         df["id"] = df["Sort-As"].fillna("").astype(str)
#         df["name"] = df["Assessment Objective"].fillna("").astype(str)

#         # Filter by level
#         if level != "All":
#             df = df[df["level"] == level]

#         # Prepare matched_rows for frontend
#         matched_rows = df[["id", "name", "level", "status"]].to_dict(orient="records")

#         # Call summarize_user_excel to get SPRS and POA&M
#         summary = summarize_user_excel(excel_file, level=level)
#         sprs_score = int(summary.get("SPRS_score", 0))

#         # Convert POA&M dict to list of label/value objects
#         poam_dict = summary.get("POAM_progress", {})
#         poam_list = [{"label": k, "value": int(v) if isinstance(v, (np.integer, int)) else v} for k, v in poam_dict.items()]

#         dashboard_metrics = [
#             {"label": "SPRS Score", "value": sprs_score},
#             {"label": "POA&M Progress", "value": poam_list}
#         ]

#         return {"matched_rows": matched_rows, "dashboard_metrics": dashboard_metrics}

#     except Exception as e:
#         print("Error fetching dashboard data:", e)

#         # Fallback static data
#         fallback_controls = [
#             {"id": "AC.L1-3.1.1", "name": "Limit information system access to authorized users.", "level": "Level 1", "status": "Met"},
#             {"id": "AC.L1-3.1.2", "name": "Limit use of devices to authorized users.", "level": "Level 1", "status": "Pending"},
#             {"id": "IA.L2-3.5.3", "name": "Use multifactor authentication.", "level": "Level 2", "status": "Not Met"},
#         ]
#         fallback_metrics = [
#             {"label": "SPRS Score", "value": 0},
#             {"label": "POA&M Progress", "value": []}
#         ]
#         return {"matched_rows": fallback_controls, "dashboard_metrics": fallback_metrics}

@app.get("/api/dashboard")
def get_dashboard(level: Optional[str] = Query("All")):
    excel_file = "Data/Reports/merged_poam_assessment.xlsx"

    try:
        # Load Excel
        df = pd.read_excel(excel_file)

        # Fill missing Assessment Status
        df["Assessment Status"] = df["Assessment Status"].fillna("Not Applicable")

        # Map statuses
        def map_status(row):
            status = row["Assessment Status"]
            weakness = str(row.get("Weakness Description", "")).strip()
            poam_status = row.get("POA&M Status","".strip())
            
            if status == "Met":
                return "Met"
            elif status == "Not Applicable":
                return "Not Applicable"
            elif status == "Not Met":
                return "Not Met"
    

        df["Assessment Status"] = df.apply(map_status, axis=1)
        df["Level"] = df["Level"].fillna("Unknown")
        df["SPRS"] = df["SPRS"].fillna(0)
        df["Family"] = df["Family"].fillna("")
        df["Framework"] = df["Framework"].fillna("")
        df["Control ID"] = df['Control ID_x']

        # Filter by level
        if level != "All":
            df = df[df["Level"] == level]

        # Only send selected columns
        columns_to_send = [
            "Sort-As", "Family", "Control ID", "Assessment Objective",
            "Assessment Status", "Level", "Framework", "SPRS"
        ]
        matched_rows = df[columns_to_send].to_dict(orient="records")

        # KPI metrics
        summary = summarize_user_excel(excel_file, level=level)
        sprs_score = int(summary.get("SPRS_score", 0))
        poam_dict = summary.get("POAM_progress", {})
        poam_list = [{"label": k, "value": int(v) if isinstance(v, (np.integer, int)) else v} for k, v in poam_dict.items()]

        dashboard_metrics = [
            {"label": "SPRS Score", "value": sprs_score},
            {"label": "POA&M Progress", "value": poam_list},
        ]
        print("data being sent is ", dashboard_metrics)

        return {"matched_rows": matched_rows, "dashboard_metrics": dashboard_metrics}

    except Exception as e:
        print("Error fetching dashboard data:", e)
        return {"matched_rows": [], "dashboard_metrics": []}

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from pathlib import Path

EXCEL_FILE = Path("Data/Reports/merged_poam_assessment.xlsx")

@app.get("/api/download-dashboard")
async def get_poam_excel():
    """
    Returns the Excel file for frontend and download.
    """
    if not EXCEL_FILE.exists():
        raise HTTPException(status_code=404, detail="POA&M Excel file not found")

    return FileResponse(
        path=EXCEL_FILE,
        filename="excel_merged.xlsx",
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )

@app.get("/api/poam-excel")
async def get_poam_excel():
    """
    Returns the Excel file for frontend and download.
    """
    if not EXCEL_FILE.exists():
        raise HTTPException(status_code=404, detail="POA&M Excel file not found")

    return FileResponse(
        path=EXCEL_FILE,
        filename="poam_data.xlsx",
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )



@app.get("/api/update-readiness")
async def update_readiness():
    pass




import os
import datetime
from readinessUpdate import update_excel_with_mapping


UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/api/map-file")
async def map_file(file: UploadFile = File(...)):
    print("hit an apis")
    try:
        # Save uploaded file
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as f:
            f.write(await file.read())

        # Update main Excel with new mappings
        df_updated = update_excel_with_mapping(file_path)
        print("df upadtyed ", df_updated.head())

        # Return all rows to frontend
        return {"mappedControls": df_updated.to_dict(orient="records")}

    except Exception as e:
        return {"error": str(e), "mappedControls": []}