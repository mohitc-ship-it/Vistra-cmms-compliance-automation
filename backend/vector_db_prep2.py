# # import json
# # import re
# # import fitz  # PyMuPDF

# # def pdf_to_text(pdf_path):
# #     """Read PDF and return full text."""
# #     text = ""
# #     doc = fitz.open(pdf_path)
# #     for page in doc:
# #         text += page.get_text("text") + "\n"
# #     return text

# # def normalize_text(s):
# #     """Normalize text: remove trailing punctuation, collapse spaces, replace line breaks."""
# #     s = s.replace("\n", " ").strip().rstrip(".;")
# #     s = re.sub(r'\s+', ' ', s)
# #     return s

# # def enrich_controls_with_pdf(controls_json_path, pdf_path, output_path):
# #     # Load existing JSON controls
# #     with open(controls_json_path, "r") as f:
# #         controls = json.load(f)

# #     # Read PDF text and normalize spaces
# #     pdf_text = pdf_to_text(pdf_path)
# #     pdf_text_norm = normalize_text(pdf_text)

# #     for control in controls:
# #         last_ao = control.get("last_ao_sentence", "")
# #         if not last_ao:
# #             continue

# #         last_ao_norm = normalize_text(last_ao)

# #         # Find the last AO sentence in PDF
# #         match_pos = pdf_text_norm.find(last_ao_norm)
# #         if match_pos == -1:
# #             # If not found, skip enrichment for this control
# #             print(f"AO not found in PDF for control {control['metadata']['cmmc_id']} which is {control.get("last_ao_sentence")}")
# #             continue

# #         # Start searching from end of AO
# #         search_start = match_pos + len(last_ao_norm)

# #         # Find DISCUSSION after AO
# #         discussion_pos = pdf_text_norm.find("DISCUSSION", search_start)
# #         if discussion_pos == -1:
# #             print(f"DISCUSSION not found for control {control['metadata']['cmmc_id']}")
# #             continue

# #         # Find KEY REFERENCES after DISCUSSION
# #         key_ref_pos = pdf_text_norm.find("KEY REFERENCES", discussion_pos)
# #         discussion_end = key_ref_pos if key_ref_pos != -1 else len(pdf_text_norm)

# #         # Extract discussion text
# #         discussion_text = pdf_text_norm[discussion_pos:discussion_end].strip()

# #         # Append discussion to main text
# #         control["text"] = control.get("text", "") + "\n\n" + discussion_text

# #         # Extract NIST SP references after KEY REFERENCES
# #         if key_ref_pos != -1:
# #             key_ref_text = pdf_text_norm[key_ref_pos:key_ref_pos + 100]  # next 500 chars
# #             print("key ref ", key_ref_text)
# #             nist_refs = re.findall(r"NIST SP 800-171*?\d+(\.\d+)*", key_ref_text, re.IGNORECASE)
# #             print("nist ref ,", nist_refs)
# #             if nist_refs:
# #                 control.setdefault("metadata", {})["nist_references"] = nist_refs

# #     # Save enriched JSON
# #     with open(output_path, "w") as f:
# #         json.dump(controls, f, indent=2)

# #     print(f"Enriched {len(controls)} controls with PDF discussion and NIST references.")

# import json
# import re
# import fitz  # PyMuPDF

# def pdf_to_text(pdf_path):
#     """Read PDF and return full text."""
#     text = ""
#     doc = fitz.open(pdf_path)
#     for page in doc:
#         text += page.get_text("text") + "\n"
#     return text

# def normalize_text(s):
#     """Normalize text: remove trailing punctuation, collapse spaces, replace line breaks."""
#     s = s.replace("\n", " ").strip().rstrip(".;")
#     s = re.sub(r'\s+', ' ', s)
#     return s

# def enrich_controls_with_pdfs(controls_json_path, pdf_paths, output_path):
#     """
#     Enrich controls JSON using one or more PDFs.
#     pdf_paths: list of PDF file paths.
#     """
#     # Load existing JSON controls
#     with open(controls_json_path, "r") as f:
#         controls = json.load(f)

#     # Read and concatenate all PDF texts
#     pdf_text_norm = ""
#     for pdf_path in pdf_paths:
#         pdf_text = pdf_to_text(pdf_path)
#         pdf_text_norm += " " + normalize_text(pdf_text)

#     for control in controls:
#         last_ao = control.get("last_ao_sentence", "")
#         if not last_ao:
#             continue

#         last_ao_norm = normalize_text(last_ao)

#         # Find the last AO sentence in PDF
#         match_pos = pdf_text_norm.find(last_ao_norm)
#         if match_pos == -1:
#             print(f"AO not found in PDF for control {control['metadata']['cmmc_id']}")
#             continue

#         search_start = match_pos + len(last_ao_norm)

#         # Find DISCUSSION after AO
#         discussion_pos = pdf_text_norm.find("DISCUSSION", search_start)
#         print(control['metadata']['cmmc_id'])
#         if control['metadata']['cmmc_id'] == "CM.L2-3.4.4":
#             print("dis is ",discussion_pos )

#         if discussion_pos == -1:
#             print(f"DISCUSSION not found for control {control['metadata']['cmmc_id']}")
#             continue

#         # Find KEY REFERENCES after DISCUSSION
#         key_ref_pos = pdf_text_norm.find("KEY REFERENCES", discussion_pos)
#         discussion_end = key_ref_pos if key_ref_pos != -1 else len(pdf_text_norm)

#         # Extract discussion text
#         discussion_text = pdf_text_norm[discussion_pos:discussion_end].strip()

#         # Append discussion to main text
#         control["text"] = control.get("text", "") + "\n\n" + discussion_text

#         # Extract NIST SP references and revision IDs after KEY REFERENCES
#         if key_ref_pos != -1:
#             key_ref_text = pdf_text_norm[key_ref_pos:key_ref_pos + 100]  # read next 500 chars
#             # Extract NIST SP references with optional revision and section
#             nist_refs = re.findall(r"NIST SP 800-171(?: Rev\. \d+)?(?: \d+(?:\.\d+)*)?", key_ref_text, re.IGNORECASE)
#             print("nist ", nist_refs)

#             metadata = control.setdefault("metadata", {})
#             current_nist = metadata.get("framework", "")


#             # Store full NIST SP references
#             if(len(nist_refs)>0):
#                 metadata["framework"] = nist_refs[0]


#     # Save enriched JSON
#     with open(output_path, "w") as f:
#         json.dump(controls, f, indent=2)

#     print(f"Enriched {len(controls)} controls with PDF discussions and NIST references.")


# if __name__ == "__main__":
#     pdf_path = ["LevelDataPdfs/AssessmentGuideL1v2.pdf","LevelDataPdfs/AssessmentGuideL2v2.pdf","LevelDataPdfs/AssessmentGuideL3v2.pdf"]
#     output_path = "final_embedding_data.json"
#     enrich_controls_with_pdfs("embedding_data.json", pdf_path, output_path)

import json
import re
import fitz  # PyMuPDF

def pdf_to_text(pdf_path):
    """Read PDF and return full text."""
    text = ""
    doc = fitz.open(pdf_path)
    for page in doc:
        text += page.get_text("text") + "\n"
    return text

def normalize_text(s):
    """Normalize text: remove trailing punctuation, collapse spaces, replace line breaks."""
    s = s.replace("\n", " ").strip().rstrip(".;")
    s = re.sub(r'\s+', ' ', s)
    return s

def fuzzy_match_line(pdf_text, target_sentence, threshold=0.7):
    """
    Try to find a line in pdf_text containing at least `threshold` fraction of words from target_sentence.
    Removes leading 'determine' and 'if' from target_sentence.
    Returns the best matching line or None if no line meets threshold.
    """
    # Normalize and split words
    words = normalize_text(target_sentence).split()
    
    # Remove leading "determine" and/or "if"
    while words and words[0].lower() in {"determine", "if"}:
        words.pop(0)
    
    target_words = set(words)
    
    if not target_words:
        return None

    lines = pdf_text.splitlines()
    best_line = None
    best_ratio = 0

    for line in lines:
        line_words = set(normalize_text(line).split())
        if not line_words:
            continue
        common_words = target_words.intersection(line_words)
        ratio = len(common_words) / len(target_words)
        if ratio > best_ratio and ratio >= threshold:
            best_ratio = ratio
            best_line = line

    return normalize_text(best_line) if best_line else None


def enrich_controls_with_pdfs(controls_json_path, pdf_paths, output_path):
    """
    Enrich controls JSON using one or more PDFs.
    pdf_paths: list of PDF file paths.
    """
    # Load existing JSON controls
    with open(controls_json_path, "r") as f:
        controls = json.load(f)

    # Read and concatenate all PDF texts
    pdf_text = ""
    pdf_text_norm = ""
    for pdf_path in pdf_paths:
        text = pdf_to_text(pdf_path)
        pdf_text += text + "\n"
        pdf_text_norm += " " + normalize_text(text)

    for control in controls:
        last_ao = control.get("last_ao_sentence", "")
        if not last_ao:
            continue

        last_ao_norm = normalize_text(last_ao)

        # Find the last AO sentence in PDF
        match_pos = pdf_text_norm.find(last_ao_norm)
        if match_pos == -1:
            # Try fuzzy match line if exact not found
            fuzzy_line = fuzzy_match_line(pdf_text, last_ao, threshold=0.4)
            if fuzzy_line:
                print(f"Fuzzy match found for control {control['metadata']['cmmc_id']}")
                match_pos = pdf_text_norm.find(fuzzy_line)
                last_ao_norm = fuzzy_line
            else:
                print(f"AO not found in PDF for control {control['metadata']['cmmc_id']}")
                continue

        search_start = match_pos + len(last_ao_norm)

        # Find DISCUSSION after AO
        discussion_pos = pdf_text_norm.find("DISCUSSION", search_start)
        if discussion_pos == -1:
            print(f"DISCUSSION not found for control {control['metadata']['cmmc_id']}")
            continue

        # Find KEY REFERENCES after DISCUSSION
        key_ref_pos = pdf_text_norm.find("KEY REFERENCES", discussion_pos)
        discussion_end = key_ref_pos if key_ref_pos != -1 else len(pdf_text_norm)

        # Extract discussion text
        discussion_text = pdf_text_norm[discussion_pos:discussion_end].strip()

        # Append discussion to main text
        control["text"] = control.get("text", "") + "\n\n" + discussion_text

        # Extract NIST SP references and revision IDs after KEY REFERENCES
        if key_ref_pos != -1:
            key_ref_text = pdf_text_norm[key_ref_pos:key_ref_pos + 100]  # read next 100 chars
            # Extract NIST SP references with optional revision and section
            nist_refs = re.findall(r"NIST SP 800-171(?: Rev\. \d+)?(?: \d+(?:\.\d+)*)?", key_ref_text, re.IGNORECASE)

            metadata = control.setdefault("metadata", {})
            # Store first NIST SP reference if found
            if nist_refs:
                metadata["framework"] = nist_refs[0]

    # Save enriched JSON
    with open(output_path, "w") as f:
        json.dump(controls, f, indent=2)

    print(f"Enriched {len(controls)} controls with PDF discussions and NIST references.")


if __name__ == "__main__":
    pdf_paths = [
        "LevelDataPdfs/AssessmentGuideL1v2.pdf",
        "LevelDataPdfs/AssessmentGuideL2v2.pdf",
        "LevelDataPdfs/AssessmentGuideL3v2.pdf"
    ]
    output_path = "final_embedding_data.json"
    enrich_controls_with_pdfs("embedding_data.json", pdf_paths, output_path)
