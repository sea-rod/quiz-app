from utils.pdf_vectorizer import PDFVectorizer
from utils.vector_operations import VectorDBOperations as db
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from generate_questions import generate_questions

if __name__ == "__main__":
    # pdf = PDFVectorizer()
    # chunks = pdf.pdf_vectorize_store()
    # signal.signal(signal.SIGINT, shutdown_handler)
    # signal.signal(signal.SIGTERM, shutdown_handler)

    try:
        with db.connect_weaviate() as client:
            # client.insert("pdf_chunks", chunks, "user_id")
            # client.delete("pdf_chunk")
            res = generate_questions(client)
            print(res)
        # del client
    except Exception as e:
        exit(0)
