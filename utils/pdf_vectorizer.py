from utils.sentence_text_splitter import SentenceTextSplitter
from langchain_community.document_loaders import DirectoryLoader
import pymupdf4llm
import pathlib
from utils.vector_operations import VectorDBOperations


class PDFVectorizer:
    def __init__(self):
        self.DATA_PATH = "./output_data"

    def extract_from_pdf(self):
        md_text = pymupdf4llm.to_markdown("data/NaiveBayes.pdf")
        pathlib.Path("./output_data/output.md").write_bytes(md_text.encode())
        print("#" * 10, "Extraction Done", "#" * 10)

    def load_documents(self):
        loader = DirectoryLoader(self.DATA_PATH, glob="**/*.md", show_progress=True)
        documents = loader.lazy_load()
        return documents

    def split_text(self, documents):
        text_splitter = SentenceTextSplitter(
            chunk_size=5,
            chunk_overlap=1,
        )
        chunks = text_splitter.split_documents(documents)
        return chunks

    def pdf_vectorize_store(self):
        documents = self.load_documents()
        chunks = self.split_text(documents)
        return chunks
