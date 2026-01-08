# import os
# import time
# import json
# from langchain_chroma import Chroma
# from langchain.schema import HumanMessage
# from langchain_openai import ChatOpenAI, OpenAIEmbeddings
# from langchain.storage import InMemoryStore
# from langchain.retrievers.multi_vector import MultiVectorRetriever
# from langchain_google_genai import ChatGoogleGenerativeAI


# def create_retriever(db_name, collection_name):
#     """Initialize Chroma vectorstore and MultiVectorRetriever"""
#     os.makedirs(db_name, exist_ok=True)

#     vectorstore = Chroma(
#         persist_directory=db_name,
#         collection_name=collection_name,
#         embedding_function=OpenAIEmbeddings(model="text-embedding-3-large")
#     )

#     store = InMemoryStore()

#     retriever = MultiVectorRetriever(
#         vectorstore=vectorstore,
#         docstore=store,
#         id_key="doc_id",
#     )

#     return retriever


# def rag(query, retriever, k=5, llm_provider="openai", structure=None):
#     """
#     Simple RAG pipeline for text-only chunks with flat metadata.
#     """
#     try:
#         # Select LLM
#         if llm_provider == "openai":
#             llm = ChatOpenAI(
#                 model="gpt-4o-mini",
#                 temperature=0,
#                 max_retries=2,
#                 api_key=os.getenv("OPENAI_API_KEY"),
#             )
#         elif llm_provider == "gemini":
#             llm = ChatGoogleGenerativeAI(
#                 model="gemini-2.5-flash",
#                 temperature=0,
#                 max_retries=2,
#             )
#         else:
#             raise ValueError(f"Unsupported LLM provider: {llm_provider}")

#         # Similarity search
#         results = retriever.vectorstore.similarity_search(query, k=k)
#         print("similarity search got ", results)
#         print()
#         print()
#         retrieved_texts = [doc.page_content for doc in results]

#         if not retrieved_texts:
#             print("No relevant text chunks found in vectorstore.")
#             return None

#         context_text = "\n".join(retrieved_texts)
#         full_prompt = f"Context:\n{context_text}\n\nQuestion: {query}"
#         message_local = HumanMessage(content=full_prompt)

#         # Call LLM with retry
#         for attempt in range(2):
#             try:
#                 if structure:
#                     llm_structured = llm.with_structured_output(structure)
#                     response = llm_structured.invoke([message_local])
#                 else:
#                     response = llm.invoke([message_local])
#                 return response.content
#             except Exception as e:
#                 if attempt == 0:
#                     time.sleep(60)

#         return None

#     except Exception as e:
#         print("RAG pipeline exception:", e)
#         return None


# if __name__ == "__main__":
#     retriever = create_retriever("./chroma_db_vistra2", "cmms_rag")
#     response = rag("tell me about all assessment objectives of 3.1.1", retriever)
#     print("\nRAG Response:\n", response)


import os
import time
from langchain_chroma import Chroma
from langchain.schema import HumanMessage
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.storage import InMemoryStore
from langchain.retrievers.multi_vector import MultiVectorRetriever
from langchain_google_genai import ChatGoogleGenerativeAI


def create_retriever(db_name, collection_name):
    """Initialize Chroma vectorstore and MultiVectorRetriever"""
    os.makedirs(db_name, exist_ok=True)

    vectorstore = Chroma(
        persist_directory=db_name,
        collection_name=collection_name,
        embedding_function=OpenAIEmbeddings(model="text-embedding-3-large")
    )

    store = InMemoryStore()

    retriever = MultiVectorRetriever(
        vectorstore=vectorstore,
        docstore=store,
        id_key="doc_id",
    )

    print(f"Retriever initialized with collection '{collection_name}' in '{db_name}'")
    return retriever


def rag(query, retriever, k=5, llm_provider="openai", structure=None):
    """
    RAG pipeline for text-only chunks with beautiful logging.
    """
    try:
        print("\n--- RAG PIPELINE START ---")
        print(f"User query: {query}\n")

        # Select LLM
        if llm_provider == "openai":
            llm = ChatOpenAI(
                model="gpt-4o-mini",
                temperature=0,
                max_retries=2,
                api_key=os.getenv("OPENAI_API_KEY"),
            )
        elif llm_provider == "gemini":
            llm = ChatGoogleGenerativeAI(
                model="gemini-2.5-flash",
                temperature=0,
                max_retries=2,
            )
        else:
            raise ValueError(f"Unsupported LLM provider: {llm_provider}")

        # Similarity search
        results = retriever.vectorstore.similarity_search(query, k=k)
        print(f"Retrieved {len(results)} chunks from vectorstore.\n")

        if not results:
            print("No relevant text chunks found.")
            return None

        # Print all chunks beautifully
        print("--- Retrieved Chunks ---")
        for idx, doc in enumerate(results, start=1):
            print(f"\nChunk {idx}:")
            print("-" * 60)
            print(doc.page_content)
            print("-" * 60)
        print("\n--- End of Chunks ---\n")

        # Combine all text for LLM context
        retrieved_texts = [doc.page_content for doc in results]
        context_text = "\n".join(retrieved_texts)
        full_prompt = f"Context:\n{context_text}\n\nQuestion: {query}"
        message_local = HumanMessage(content=full_prompt)

        print("Sending combined context to LLM...")

        # Call LLM with retry
        for attempt in range(2):
            try:
                if structure:
                    llm_structured = llm.with_structured_output(structure)
                    response = llm_structured.invoke([message_local])
                else:
                    response = llm.invoke([message_local])

                print("--- LLM Response Received ---\n")
                return response.content
            except Exception as e:
                print(f"LLM call attempt {attempt + 1} failed: {e}")
                if attempt == 0:
                    print("Retrying in 60s...")
                    time.sleep(60)

        print("All LLM attempts failed.")
        return None

    except Exception as e:
        print("RAG pipeline exception:", e)
        return None


if __name__ == "__main__":
    retriever = create_retriever("./chroma_db_vistra", "cmms_rag")
    response = rag("tell me about all assessment objectives of control id CM.L2-3.4.4 ", retriever)
    print("\n--- Final RAG Response ---\n")
    print(response)
