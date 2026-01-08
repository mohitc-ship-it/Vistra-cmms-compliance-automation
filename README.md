# Vistra - AI-Driven Federal Compliance Platform

## Client
**Vistra** (Project coordinated by Shantanu, Marketer Shivani VS, and Ankit)

## Problem Statement
The main requirement was to build an AI-driven federal compliance platform focused on **CMMC (Cybersecurity Maturity Model Certification)** and **NIST 800-171** standards. The goal was to automate the compliance evaluation process, readiness scoring, and reporting — which were previously being handled manually through static dashboards and spreadsheets.

## Approach
The platform was designed to help federal contractors automatically assess their compliance readiness by analyzing documents such as policies, SOPs, logs, and architectural diagrams. Once uploaded, the AI extracts and maps relevant content to the respective CMMC and NIST controls, determines compliance levels (Met, Partial, or Not Met), and dynamically updates readiness scores across all control families.

## Architecture
The entire system was built with a **Next.js-based frontend** and a **FastAPI backend**, integrating **multimodal RAG** for efficient retrieval-augmented analysis of complex regulatory documents. It supports hybrid RAG search with metadata tagging (including page numbers and section references) to ensure precise traceability for every mapping.

The platform runs entirely within Vistra’s Microsoft environment, using **Azure AD authentication** and internal-only processing to ensure zero external data exposure.

## Tech Stack
*   **Frontend:** Next.js, React, Tailwind CSS
*   **Backend:** FastAPI, Python
*   **AI/LLM:** LangChain, OpenAI/Groq/Google GenAI (via LangChain), Multimodal RAG
*   **Database/Vector Store:** ChromaDB (for RAG), Excel (as a structured data store for reports)
*   **Document Processing:** Unstructured, PyMuPDF (fitz), python-docx, pandas
*   **Authentication:** Azure AD

## File-to-File Explanation

### Backend (`/backend`)
*   **`app.py`**: The main entry point for the FastAPI application. It defines API endpoints for the dashboard, file uploading, chat, and history.
*   **`chatbot.py`**: Contains the core logic for the AI chatbot. It routes user queries to either the RAG system (for general document Q&A) or the Excel query engine (for specific readiness status questions).
*   **`readinessUpdate.py`**: Handles the logic for mapping uploaded documents to compliance controls. It extracts text from files, identifies "Not Met" controls from the master Excel, uses an LLM to map the document content to these controls, and updates the Excel file with the results (status, weakness, mitigation).
*   **`retrieveContent.py`**: Implements the RAG (Retrieval-Augmented Generation) logic, creating retrievers for ChromaDB and executing RAG chains.
*   **`llm.py`**: Wrapper module for initializing and interacting with LLMs (Language Models).
*   **`extract.py`**: Helper script for extracting content from various file formats.
*   **`query_excel.py`**: Logic for querying the Excel report to answer specific questions about compliance status, gaps, and POA&M.
*   **`vectorStoring.py` / `vector_db_prep2.py` / `vectordb_prep.py`**: Scripts used to preprocess documents and populate the ChromaDB vector store with embeddings.
*   **`requirements.txt`**: Lists all Python dependencies.

### Frontend (`/frontend/cmmc-compliance-ai-dashboard`)
*   **`app/`**: Contains the Next.js application routes and pages.
*   **`components/`**: Reusable UI components for the dashboard, chat interface, and file uploaders.
*   **`lib/`**: Utility functions and shared logic.
*   **`public/`**: Static assets.

## Flow-Wise Explanation

### 1. Readiness Assessment Flow
1.  **User Action:** The user uploads a document (PDF, Excel, DOCX) via the frontend.
2.  **API Call:** The frontend sends the file to the `/api/map-file` endpoint in `app.py`.
3.  **Processing (`readinessUpdate.py`):**
    *   The system extracts text from the uploaded file.
    *   It reads the master Excel report (`merged_poam_assessment.xlsx`) to identify controls that are currently "Not Met".
    *   It constructs a prompt for the LLM, providing the document content and the list of "Not Met" controls.
    *   The LLM analyzes the document and determines if it satisfies any of the controls. It returns a structured mapping (Control ID, Status, Weakness, Mitigation).
4.  **Update:** The system updates the master Excel file with the new findings (setting status to "Met" or "In-Progress", adding mitigation details).
5.  **Response:** The updated mapping is returned to the frontend to display the results to the user.

### 2. Chatbot Flow
1.  **User Action:** The user asks a question in the chat interface.
2.  **API Call:** The frontend sends the query to the `/api/chat` endpoint in `app.py`.
3.  **Routing (`chatbot.py`):**
    *   The system uses an LLM to classify the query into one of two types:
        *   **`DOCUMENT_QNA`**: General questions about standards (e.g., "What is AC.L1-3.1.1?").
        *   **`READINESS_STATUS`**: Specific questions about the user's report (e.g., "What are my gaps?").
4.  **Execution:**
    *   **If `DOCUMENT_QNA`**: The system enhances the query, searches the ChromaDB vector store for relevant regulatory text, and generates an answer using RAG.
    *   **If `READINESS_STATUS`**: The system queries the master Excel report (using `query_excel.py` or direct pandas manipulation) to retrieve specific data points like SPRS scores, open POA&M items, or control statuses.
5.  **Response:** The answer is returned to the frontend.

### 3. Dashboard Reporting Flow
1.  **User Action:** The user views the main dashboard.
2.  **API Call:** The frontend requests data from `/api/dashboard`.
3.  **Processing:**
    *   The backend reads the master Excel file.
    *   It calculates key metrics: **SPRS Score**, **POA&M Progress**, **Compliance Percentage** (Met vs. Not Met).
    *   It extracts the list of controls and their current status.
4.  **Response:** The structured data is returned to the frontend for visualization (charts, progress bars, tables).

## Future Iterations
In future iterations, features such as real-time change detection, control version tracking, and advanced hybrid search with visual evidence mapping will be added — enabling auditors to verify each compliance decision effortlessly.
# Vistra-cmms-compliance-automation
