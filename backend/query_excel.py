# # import pandas as pd
# # import json
# # from openai import OpenAI

# # client = OpenAI()

# # def run_user_query_on_excel(user_query, excel_path):
# #     """
# #     Given a user query and Excel report path, generate a pandas query using LLM
# #     based on the Excel column structure, execute it, and summarize results.
# #     """

# #     # Load Excel
# #     df = pd.read_excel(excel_path)

# #     # Provide Excel columns to LLM so it can generate a query
# #     columns = df.columns.tolist()
    
# #     # Step 1: Ask LLM to generate pandas filter
# #     prompt_query_generation = f"""
# #     You are an AI assistant. You know the structure of an assessment report Excel:
# #     Columns: {columns}

# #     User query: "{user_query}"

# #     Write a **pandas query expression** to filter this DataFrame that answers the query.
# #     Return only the pandas expression, do not execute anything.
# #     Example: df['Assessment Status'] == 'Not Met' & df['Family'] == 'Access Control'
# #     """

# #     response = client.chat.completions.create(
# #         model="gpt-4o",
# #         messages=[
# #             {"role": "system", "content": "You are an expert data analyst assistant."},
# #             {"role": "user", "content": prompt_query_generation}
# #         ]
# #     )
# #     print(response)

# #     pandas_query = response.choices[0].message.content.strip()

# #     # Step 2: Execute the query safely
# #     try:
# #         matched_df = df.query(pandas_query)
# #     except Exception as e:
# #         return {"error": f"Failed to apply query: {str(e)}", "pandas_query": pandas_query}

# #     # Step 3: Pass filtered data back to LLM for summary
# #     filtered_data_json = matched_df.to_dict(orient="records")

# #     prompt_summary = f"""
# #     You are given filtered assessment report data (JSON):
# #     {json.dumps(filtered_data_json[:50])}  # Send first 50 for context

# #     User asked: "{user_query}"

# #     Provide a concise natural language summary answering the user query.
# #     Include counts, key findings, and optionally suggest next steps.
# #     """

# #     summary_resp = client.chat.completions.create(
# #         model="gpt-4o",
# #         messages=[
# #             {"role": "system", "content": "You are an expert summarizer of assessment reports."},
# #             {"role": "user", "content": prompt_summary}
# #         ]
# #     )

# #     summary_text = summary_resp.choices[0].message["content"].strip()


# #     print(summary_text)

# #     return {
# #         "pandas_query": pandas_query,
# #         "matched_rows": filtered_data_json,
# #         "summary": summary_text
# #     }

# # # Example usage:
# # result = run_user_query_on_excel("List all weaknesses for non-met assessment objectives.", "Data/Reports/assessment.xlsx")
# # # print(result["summary"])
# # # print(len(result["matched_rows"]), "rows matched")
# # print(result)

# import os
# import pandas as pd
# import json
# from pydantic import BaseModel
# from llm import llm_structured
# from langchain_openai import ChatOpenAI
# import re
# # -----------------------------
# # Define the output schema
# # -----------------------------
# class PandasQuerySchema(BaseModel):
#     query: str


# def clean_pandas_query(query: str) -> str:
#     """
#     Ensures safe pandas query syntax:
#     - Adds parentheses around expressions joined by & or |
#     - Removes stray df. prefixes if present (for df.query)
#     """
#     if not query:
#         return ""

#     # Add parentheses around top-level & / | expressions
#     query = re.sub(
#         r"(?<!\()(\s*[A-Za-z0-9_'\[\]\.\s]+?\s*[=!><]=?\s*['\"A-Za-z0-9_\-\s]+)(?=\s*[&|])",
#         r"(\1)",
#         query,
#     )

#     # Add parentheses after & or | if not already wrapped
#     query = re.sub(
#         r"(?<=[&|])\s*(?!\()([A-Za-z0-9_'\[\]\.\s]+?\s*[=!><]=?\s*['\"A-Za-z0-9_\-\s]+)",
#         r"(\1)",
#         query,
#     )

#     return query.strip()
# # -----------------------------
# # Main function
# # -----------------------------
# def run_user_query_on_excel(user_query: str, excel_path: str,user_report_summary:str):
#     """
#     Given a user query and Excel report path, generate a pandas query using LLM,
#     execute it on the Excel, and summarize results.
#     """

#     # Load Excel
#     df = pd.read_excel(excel_path)
#     columns = df.columns.tolist()

#     # Step 1: Ask LLM to generate pandas filter
#     prompt_query_generation = f"""
# You are an AI assistant. You know the structure of an assessment report Excel:
# Columns: {columns}

# User query: "{user_query}"

# Write a **pandas query expression** to filter this DataFrame that answers the query.
# Return only the pandas expression in JSON format matching schema {{ "query": "<expression>" }}.
# Example: df['Assessment Status'] == 'Not Met' & df['Family'] == 'Access Control'
# """
#     try:
#         structured_result = llm_structured(prompt_query_generation, PandasQuerySchema)
#         pandas_query = structured_result.query
#         pandas_query = clean_pandas_query(pandas_query)

#         print("panfas qury ", pandas_query)
#     except Exception as e:
#         return {"error": f"Failed to generate pandas query: {str(e)}"}

#     # Step 2: Execute the query safely
#     try:
#         print("matching dfkjvh")
#         # matched_df = df.query(pandas_query)
#         matched_df = df[eval(pandas_query)]

#         print("skjdn")
#         print("found ", matched_df)
#     except Exception as e:
#         return {"error": f"Failed to apply pandas query: {str(e)}", "pandas_query": pandas_query}

#     # Step 3: Summarize matched data using LLM
#     print("filter")
#     filtered_data_json = matched_df.to_dict(orient="records")
#     filtered_json_snippet = json.dumps(filtered_data_json[:50], indent=2, default=str)

#     # filtered_json_snippet = json.dumps(filtered_data_json[:50], indent=2)  # first 50 rows for context

#     prompt_summary = f"""
# You are an expert summarizer of assessment reports.
# You are given filtered assessment report data (JSON):
# {filtered_json_snippet}

# User asked: "{user_query}"

# Provide a concise natural language summary answering the user query.
# Include counts, key findings, and optionally suggest next steps.
# For reference this is user report summary too:
# {user_report_summary}
# """

#     try:
#         structured_summary = llm_structured(prompt_summary, BaseModel.parse_obj({"summary": ""}))
#         summary_text = structured_summary.summary
#     except Exception:
#         # fallback to normal chat completion
#         llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, openai_api_key=os.getenv("OPENAI_API_KEY"))
#         summary_resp = llm.predict(prompt_summary)
#         summary_text = summary_resp

#     print("returning")
#     return {
#         "pandas_query": pandas_query,
#         "matched_rows": filtered_data_json,
#         "summary": summary_text
#     }

# # -----------------------------
# # Example usage
# # -----------------------------
# if __name__ == "__main__":
#     excel_file = "Data/Reports/assessment.xlsx"
#     # user_question = "List all weaknesses for non-met assessment objectives."
#     user_question = "what are all non-met controls "
#     result = run_user_query_on_excel(user_question, excel_file,"")

#     print("Pandas Query:", result.get("pandas_query"))
#     print("Summary:", result.get("summary"))
#     print("Matched Rows:", len(result.get("matched_rows", [])))

import os
import pandas as pd
import json
import re
from pydantic import BaseModel
from llm import llm_structured
from langchain_openai import ChatOpenAI

# -----------------------------
# Define structured output schemas
# -----------------------------
class PandasQuerySchema(BaseModel):
    query: str

class SummarySchema(BaseModel):
    summary: str

# -----------------------------
# Clean pandas query
# -----------------------------
def clean_pandas_query(query: str) -> str:
    if not query:
        return ""

    q = query.strip()

    # Remove code block markers if present
    if q.startswith("```"):
        q = "\n".join(q.splitlines()[1:-1]).strip()

    # Normalize whitespace
    q = re.sub(r"\s+", " ", q)

    # Rewrite .str.contains for df.query/eval
    pattern = re.compile(r"(?P<col>[A-Za-z0-9 _\-]+)\.str\.contains\(")
    q = pattern.sub(lambda m: f"df['{m.group('col').strip()}'].str.contains(", q)

    # Add parentheses around top-level & / |
    q = re.sub(
        r"(?<!\()(\s*[A-Za-z0-9_'\[\] \-\.]+\s*(?:==|!=|>=|<=|>|<)\s*['\"A-Za-z0-9_\-\s\.]+)(?=\s*[&|])",
        r"(\1)",
        q,
    )
    q = re.sub(
        r"(?<=[&|])\s*(?!\()([A-Za-z0-9_'\[\] \-\.]+\s*(?:==|!=|>=|<=|>|<)\s*['\"A-Za-z0-9_\-\s\.]+)",
        r"(\1)",
        q,
    )

    return q.strip()

# -----------------------------
# Execute pandas expression safely
# -----------------------------
def execute_pandas_expression(df: pd.DataFrame, expr: str):
    use_eval = False
    if "df[" in expr or ".str.contains(" in expr:
        use_eval = True

    if not use_eval:
        try:
            return df.query(expr), "query", None
        except Exception as e:
            use_eval = True
            query_error = e

    if use_eval:
        try:
            result = eval(expr, {"df": df, "pd": pd})
            if isinstance(result, pd.Series):
                return df[result], "eval_mask", None
            elif isinstance(result, pd.DataFrame):
                return result, "eval_df", None
            else:
                return pd.DataFrame(result), "eval_other", None
        except Exception as e_eval:
            err = f"eval error: {e_eval}"
            if 'query_error' in locals():
                err = f"query error: {query_error}; eval error: {e_eval}"
            return None, "eval_failed", err

# -----------------------------
# Main function
# -----------------------------
def run_user_query_on_excel(user_query: str, excel_path: str, user_report_summary: str):
    # Load Excel
    df = pd.read_excel(excel_path)
    columns = df.columns.tolist()
    columns = df.head(1)
    # print(columns)


    # Step 1: Generate pandas query using LLM structured output
    prompt_query_generation = f"""
You are an AI assistant. You know the structure of an assessment report Excel:
possible values if required:
    - Assessment Status: (possible values - Met, Not Met, Not Applicable)
    - POA&M Status: (possible values - In-Progress, Completed)
    -Level - Level 1 and Level 2

User query: "{user_query}"

Write a **pandas query expression** to filter this DataFrame that answers the query.
Return only the pandas expression in JSON format matching schema {{ "query": "<expression>" }}.
Example: df['Assessment Status'] == 'Not Met' & df['Family'] == 'Access Control'
"""
    try:
        structured_result = llm_structured(prompt_query_generation, PandasQuerySchema)
        pandas_query = clean_pandas_query(structured_result.query)
        print("Pandas Query:", pandas_query)
    except Exception as e:
        return {"error": f"Failed to generate pandas query: {str(e)}"}

    # Step 2: Execute query
    matched_df, method_used, err = execute_pandas_expression(df, pandas_query)
    print("mathced ", matched_df,method_used, err)
    if err:
        # return {"error": err, "method_used": method_used, "pandas_query": pandas_query}
        print("no found in excel ", err)
        filtered_data_json = {}
        filtered_json_snippet = ""
        pass
    else:
        # Step 3: Convert matched data to JSON (timestamps → ISO)
        filtered_data_json = json.loads(json.dumps(
            matched_df.to_dict(orient="records"),
            default=lambda o: o.isoformat() if hasattr(o, 'isoformat') else str(o)
        ))
        filtered_json_snippet = json.dumps(filtered_data_json[:50], indent=2)

    # Step 4: Generate summary using LLM structured output
    prompt_summary = f"""
You are an expert summarizer of assessment reports.
Don't write anything on your own , answer based on filtered assessment report data and user report summary.
You are given filtered assessment report data (JSON):
{filtered_json_snippet}

User asked: "{user_query}"

Provide a concise natural language summary answering the user query.
Include counts, key findings, and optionally suggest next steps.
For reference this is user report summary too:
{user_report_summary}
"""
    try:
        structured_summary = llm_structured(prompt_summary, SummarySchema)
        summary_text = structured_summary.summary
    except Exception:
        # fallback to regular LLM call
        llm_fallback = ChatOpenAI(model="gpt-4o-mini", temperature=0, openai_api_key=os.getenv("OPENAI_API_KEY"))
        summary_text = llm_fallback.predict(prompt_summary)

    return {
        "pandas_query": pandas_query,
        "method_used": method_used,
        "matched_rows": filtered_data_json,
        "summary": summary_text
    }

# -----------------------------
# Example usage
# -----------------------------
if __name__ == "__main__":
    excel_file = "Data/Reports/merged_poam_assessment.xlsx"
    user_question = "what are all non-met controls and there weakness with mitigations"
    user_question = "what are weakness of non-met controls in report"
    user_question = "what are list of non-applicable controls"
    result = run_user_query_on_excel(user_question, excel_file, "")

    print("Pandas Query:", result.get("pandas_query"))
    print("Method Used:", result.get("method_used"))
    print("Summary:", result.get("summary"))
    print("Matched Rows:", len(result.get("matched_rows", [])))
