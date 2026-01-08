import os
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage
from pydantic import BaseModel

# ---------- Normal text output ----------
def llm_query(query: str):
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, api_key=os.getenv("OPENAI_API_KEY"))
    message = HumanMessage(content=f"Answer this question:\n{query}")
    return llm([message]).content

# ---------- Structured output with schema ----------
def llm_structured(query: str, output_schema: BaseModel):
    """
    query: str -> user question
    output_schema: pydantic BaseModel -> defines structured output
    """
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, api_key=os.getenv("OPENAI_API_KEY"))
    
    # Bind the schema to the LLM
    llm_with_structure = llm.with_structured_output(output_schema)
    
    # Invoke the LLM
    return llm_with_structure.invoke(query)

