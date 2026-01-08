import json
def print_all_chunks(retriever, name="collection"):
    """
    Print all chunks stored in the retriever's Chroma vectorstore.
    """
    collection = retriever.vectorstore._collection  # Access the underlying Chroma collection
    print(f"\n--- Chunks in {name} ---")

    # Get all stored documents and metadata
    data = collection.get(include=["documents", "metadatas"])

    if not data["documents"]:
        print("⚠️ No documents found in this collection!")
        return

    for idx, (doc, metadata, doc_id) in enumerate(zip(data["documents"], data["metadatas"], data["ids"])):
        print(f"\nChunk {idx + 1}:")
        print(f"ID: {doc_id}")
        print(f"Document text: {doc}")
        # If control_metadata is JSON string, deserialize for readability
        # if "control_metadata" in metadata:
        #     try:
        #         control_meta = json.loads(metadata["control_metadata"])
        #     except:
        #         control_meta = metadata["control_metadata"]
        #     metadata["control_metadata"] = control_meta
        # print(f"Metadata: {metadata}")
        # print("-" * 60)
    print(len(data["documents"]))

from retrieveContent import create_retriever

# Load your retriever
retriever = create_retriever("chroma_db_vistra2", "cmms_rag")

# Print all chunks
print_all_chunks(retriever, name="cmms_rag")
