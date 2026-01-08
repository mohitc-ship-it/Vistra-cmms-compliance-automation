# from langchain.schema.document import Document
# import os
# import uuid
# import json


# def storing(json_file_path, retriever):
#     """
#     Reads JSON file containing embedding chunks and metadata, 
#     and stores each chunk in the vector DB.
#     """
#     print(f"Storing data from {json_file_path} into vector DB...")

#     # Load JSON
#     with open(json_file_path, "r") as f:
#         chunks = json.load(f)

#     id_key = retriever.id_key

#     for chunk in chunks:
#         print("going for ", chunk.get("metadata"))
#         doc_id = str(uuid.uuid4())

#         # Text to embed
#         text_to_embed = chunk.get("text", "")

#         # Metadata for vector DB
#         metadata = {
#             id_key: doc_id,
#             "file_name": os.path.basename(json_file_path),
#             "control_metadata": json.dumps(chunk.get("metadata", {}))
#         }

#         # Create Document object for LangChain retriever
#         doc = [Document(page_content=text_to_embed, metadata=metadata)]
#         # Add to vector store
#         retriever.vectorstore.add_documents(doc)

#         # Save mapping in docstore for retrieval
#         retriever.docstore.mset([(doc_id, {"content": text_to_embed, "metadata": metadata})])

#     print(f"Added {len(chunks)} chunks to vector DB.")
#     return retriever



# if __name__ == "__main__":
#     # Example usage (requires retriever and vectorstore to be defined)
#     #
#     from retrieveContent import create_retriever
#     retriver = create_retriever("chroma_db_vistra", "cmms_rag")
#     storing("final_embedding_data.json", retriver)  # Example call (replace None with actual retriever and vectorstore)

from langchain.schema.document import Document
import os
import uuid
import json

def storing(json_file_path, retriever):
    """
    Reads JSON file containing embedding chunks and metadata, 
    and stores each chunk in the vector DB.
    """
    print(f"Storing data from {json_file_path} into vector DB...")

    # Load JSON
    with open(json_file_path, "r") as f:
        chunks = json.load(f)

    id_key = "doc_id"  # fixed key

    for chunk in chunks:
        print("Processing metadata:", chunk.get("metadata"))
        doc_id = str(uuid.uuid4())
        text_to_embed = chunk.get("text", "")

        # Serialize nested metadata
        metadata = {
            id_key: doc_id,
            "file_name": os.path.basename(json_file_path),
            "control_metadata": json.dumps(chunk.get("metadata", {}))
        }

        # Create Document object for LangChain retriever
        doc = [Document(page_content=text_to_embed, metadata=metadata)]

        # Add to vector store
        retriever.vectorstore.add_documents(doc)

        # Save mapping in docstore (if exists)
        if hasattr(retriever, "docstore"):
            retriever.docstore.mset([(doc_id, {"content": text_to_embed, "metadata": metadata})])

    print(f"Added {len(chunks)} chunks to vector DB.")
    return retriever


if __name__ == "__main__":
    from retrieveContent import create_retriever
    retriever = create_retriever("chroma_db_vistra", "cmms_rag")
    storing("final_embedding_data.json", retriever)
