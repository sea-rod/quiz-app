from utils.pdf_vectorizer import PDFVectorizer
from utils.vector_operations import VectorDBOperations

if __name__ == "__main__":
    pdf = PDFVectorizer()
    chunks = pdf.pdf_vectorize_store()
    with VectorDBOperations() as client:
        client.insert("pdf_chunks",chunks,"user_id")
        # client.delete("pdf_chunk")
    del client