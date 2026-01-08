# 1st option
# will look user query
# ask llm does it ask about specific Sort-As	Framework	Family	Control ID	CMMC ID	CMMC Title
# or its an open ended question

# as per that it if case 1 -> then will extract search spefici field -> in all docs in metadata -> and get content through elastic
# if case 2 -> then will go for vector db search 


# 2nd option
# or best way would be -> an input to query breaker
# where llm break user input -> into different queries for db
# then we extract all those info one by one
# and provide as context to llm with original query  


# will go with 2nd option
# for that will store everything with metadata in vectordb 

from llm import llm_query,llm_structured
from retrieveContent import create_retriever, rag

import pandas as pd
from collections import defaultdict
from query_excel import run_user_query_on_excel

from pydantic import BaseModel
from enum import Enum


# def summarize_user_excel(file_path, level="all"):
#     """
#     Summarize assessment excel data in natural language.

#     Parameters:
#         file_path (str): Path to Excel file
#         level (str): "all", "Level 1", "Level 2", etc.
    
#     Returns:
#         summary_text (str): Natural language summary
#     """
#     df = pd.read_excel(file_path)

#     # Filter by level if needed
#     if level.lower() != "all":
#         df = df[df["CMMC Level 1"].fillna("").str.contains(level) | df["CMMC Level 2"].fillna("").str.contains(level)]

#     # Standardize Assessment Status
#     df["Assessment Status"] = df["Assessment Status"].fillna("Not Assessed")

#     # Count total controls
#     total_controls = df["Control ID"].nunique()
#     total_aos = len(df)

#     # Count by status
#     status_counts = df["Assessment Status"].value_counts().to_dict()

#     # Families completed / remaining
#     family_status = df.groupby("Family")["Assessment Status"].apply(lambda x: all(s=="Met" for s in x)).to_dict()
#     completed_families = [fam for fam, completed in family_status.items() if completed]
#     remaining_families = [fam for fam, completed in family_status.items() if not completed]

#     # POA&M info
#     poam_counts = df["POA&M Status"].value_counts().to_dict()

#     # Construct natural language summary
#     summary_lines = [
#         f"Assessment Summary for {level} controls:",
#         f"Total controls assessed: {total_controls}",
#         f"Total assessment objectives (AOs): {total_aos}",
#         "Assessment Status Counts:"
#     ]
#     for status, count in status_counts.items():
#         summary_lines.append(f"- {status}: {count}")

#     summary_lines.append(f"Completed families ({len(completed_families)}): {', '.join(completed_families) if completed_families else 'None'}")
#     summary_lines.append(f"Remaining families ({len(remaining_families)}): {', '.join(remaining_families) if remaining_families else 'None'}")

#     summary_lines.append("POA&M Status Counts:")
#     for status, count in poam_counts.items():
#         summary_lines.append(f"- {status}: {count}")

#     summary_text = "\n".join(summary_lines)
#     return summary_text


import pandas as pd

def summarize_user_excel(file_path, level="all"):
    """
    Summarize merged assessment Excel data (POA&M + Assessment + Control Info)
    in natural language and JSON with detailed insights.

    Parameters:
        file_path (str): Path to merged Excel file
        level (str): "all", "Level 1", "Level 2", etc.
    
    Returns:
        summary (dict): comprehensive summary with NLP + JSON metrics
    """
    df = pd.read_excel(file_path)

    # Filter by Level if requested
    if level.lower() != "all":
        df = df[df["Level"].fillna("").str.lower() == level.lower()]

    # Standardize Assessment Status
    df["Assessment Status"] = df["Assessment Status"].fillna("Not Assessed")

    # Total controls & unique assessment objectives
    total_controls = df["Sort-As"].nunique()
    total_aos = len(df)

    # Status counts
    status_counts = df["Assessment Status"].value_counts().to_dict()
    controls_met = status_counts.get("Met", 0)
    controls_not_met = status_counts.get("Not Met", 0)
    controls_na = status_counts.get("Not Applicable", 0)
    controls_pending = status_counts.get("Not Assessed", 0)

    # Compliance % 
    compliance_status = {
        "Met": round(controls_met / total_controls * 100, 1) if total_controls else 0,
        "Not Met": round(controls_not_met / total_controls * 100, 1) if total_controls else 0,
        "Pending": round(controls_pending / total_controls * 100, 1) if total_controls else 0
    }

    # SPRS Score
    df["SPRS"] = df["SPRS"].fillna(0)
    sprs_score = round(df["SPRS"].sum(), 1)

    # POA&M Progress
    df["POA&M Status"] = df["POA&M Status"].fillna("Not Assigned")
    poam_counts = df["POA&M Status"].value_counts().to_dict()

    # Level distribution
    levels_count = df["Level"].fillna("Unknown").value_counts().to_dict()

    # Family completion
    family_status = df.groupby("Family")["Assessment Status"].apply(lambda x: all(s=="Met" for s in x)).to_dict()
    completed_families = [fam for fam, completed in family_status.items() if completed]
    remaining_families = [fam for fam, completed in family_status.items() if not completed]
    family_completion_pct = df.groupby("Family")["Assessment Status"].apply(lambda x: (x=="Met").sum() / len(x) * 100).to_dict()

    # Weaknesses per family
    df["Weakness Description"] = df["Weakness Description"].fillna("")
    weaknesses_per_family = df[df["Assessment Status"] != "Met"].groupby("Family").size().to_dict()
    top_non_met_families = sorted(weaknesses_per_family.items(), key=lambda x: x[1], reverse=True)

    # Natural language summary
    summary_lines = [
        f"Assessment Summary for {level} controls:",
        f"Total controls: {total_controls}, Controls Met: {controls_met}, SPRS Score: {sprs_score}",
        "Compliance Status:"
    ]
    for status, pct in compliance_status.items():
        summary_lines.append(f"- {status}: {pct}%")
    summary_lines.append(f"Completed families ({len(completed_families)}): {', '.join(completed_families) if completed_families else 'None'}")
    summary_lines.append(f"Remaining families ({len(remaining_families)}): {', '.join(remaining_families) if remaining_families else 'None'}")
    summary_lines.append("POA&M Progress:")
    for poam_status, count in poam_counts.items():
        summary_lines.append(f"- {poam_status}: {count}")
    summary_lines.append("Level distribution:")
    for lvl, cnt in levels_count.items():
        summary_lines.append(f"- {lvl}: {cnt}")
    summary_text = "\n".join(summary_lines)

    return {
        "summary": summary_text,
        "total_controls": total_controls,
        "controls_met": controls_met,
        "SPRS_score": sprs_score,
        "POAM_progress": poam_counts,
        "compliance_status": compliance_status,
        "completed_families": completed_families,
        "remaining_families": remaining_families,
        "family_completion_pct": family_completion_pct,
        "weaknesses_per_family": weaknesses_per_family,
        "top_non_met_families": top_non_met_families,
        "levels_count": levels_count
    }

# Example usage:
# summary = summarize_user_excel("assessment.xlsx", level="Level 1")
# print(summary)


def chat(user_input):
    # query elaboration for domain is 100% required


    class QueryType(str, Enum):
        DOCUMENT_QNA = "DOCUMENT_QNA"
        READINESS_STATUS = "READINESS_STATUS"

    class Classification(BaseModel):
        """
        Classifies a user query into document Q&A or readiness/status Q&A
        """
        type: QueryType


    query_type_prompt = """You are an intelligent assistant that classifies user queries related to cybersecurity compliance. 
The goal is to determine whether a user's query is about:

1. DOCUMENT_QNA: General questions about CMMC documents, standards, or policies.
2. READINESS_STATUS: Specific questions about the user's own CMMS report, POA&M items, gaps, or readiness.

Output must be strict JSON in the format:
{
  "type": "<DOCUMENT_QNA or READINESS_STATUS>"
}

### Examples:

User Query: "What is CUI Enclave and how does it relate to NIST controls?"
Output: {"type": "DOCUMENT_QNA"}

User Query: "What gaps do I have in my POA&M for level 2 assessment?"
Output: {"type": "READINESS_STATUS"}

User Query: "Which documents should I upload for IA.L2-3.5.3?"
Output: {"type": "READINESS_STATUS"}

now classify below one

"""
    query_type_prompt = query_type_prompt + user_input

    print("final propt ", query_type_prompt)

    query_type = llm_structured(query_type_prompt, Classification)
    print("query type , ", query_type)
    user_summary_report = summarize_user_excel("Data/Reports/merged_poam_assessment.xlsx","all")
    print("user ", user_summary_report)


    if(query_type.type=="DOCUMENT_QNA"):
        query_enhancer_prompt = f"""
        You are an expert AI query enhancer. 

        Your task is to take a user's natural language question about compliance, assessments, or security controls, and convert it into a structured format optimized for searching a vector database of controls, assessment objectives (AOs), and documentation. 

        Follow these instructions:

        1. Extract entities:
        - Control IDs (e.g., AC.L1-3.1.1, AC.L1-3.1.2)
        - Assessment Objectives (AO IDs, e.g., 3.1.1[a], 3.1.2[b])
        - Levels (Level 1, Level 2, etc.)
        - Topics, keywords, or actions (e.g., "access control", "limit users", "transactions")

        2. Split complex queries:
        - If the user asks multiple questions in one sentence, break them into individual query parts.

        3. Return structured output:
        - Format as JSON with the following fields:
            {{
            "queries": [
                {{
                "control_ids": [list of control IDs],
                "ao_ids": [list of AO IDs],
                "levels": [list of levels],
                "keywords": [list of relevant keywords],
                "original_query": "text of the sub-query"
                }},
                ...
            ]
            }}

        4. Notes:
        - If a field is not present in the user query, leave it as an empty list.
        - Preserve the meaning of the original query.
        - Make it ready for vector similarity search (concise, focused on entities and keywords).

        Now process the following user input and output the structured queries in JSON:

        User Input: "{user_input}"
        """

        enhanced_query = llm_query(query_enhancer_prompt)
        retriever = create_retriever("./chroma_db_vistra", "cmms_rag")
        return rag(enhanced_query, retriever)
    else:
        # retriver = user_data based retiriever vector data
        print("going for readiness ")
        temp_data = run_user_query_on_excel(user_input,"Data/Reports/merged_poam_assessment.xlsx",user_summary_report.get("summary"))
        return temp_data.get('summary')
        
        # return llm_query(enhanced_query)


    # router -> ask about current readiness and evaluation based question
    # direct llm with current_json of user reeadiness stuff

    # if asked generally 
    # llm_structured("")

    # normal qna
    # make a prompt with general overview of how many are in level 1 what are domains and all -> overall prompt which was on that github 
    # so it has basic general details too


# EXAMPLE QUESTIONS
# TELL ABOUT AC.L1-3.1.1
# what are non-applicable controls in report
# WHAT are weakness and mitigation of non-met compliance
# summarize our report 
# # have we cleared level 1

# Overall completion % of controls

# Per-family completion percentage

# Weaknesses per family

# Top families with most non-met controls

# POA&M “Not Assigned” handling

# More robust handling for missing data