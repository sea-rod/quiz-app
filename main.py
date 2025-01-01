import pymupdf4llm
import pathlib
import os
from dotenv import load_dotenv
import weaviate
from weaviate.classes.init import Auth
from weaviate.classes.config import Property, DataType
from transformers import AutoModel
from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

DATA_PATH = "./output_data"
load_dotenv()


def extract_from_pdf():
    md_text = pymupdf4llm.to_markdown("data/NaiveBayes.pdf")
    pathlib.Path("./output_data/output.md").write_bytes(md_text.encode())
    print("#"*10,"Extraction Done","#"*10)


def generate_data_store():
    documents = load_documents()
    chunks = split_text(documents)
    save_to_weviate(chunks)


def load_documents():
    loader = DirectoryLoader(DATA_PATH, glob="**/*.md", show_progress=True)
    documents = loader.load()
    return documents


def split_text(documents):
    print(len(documents),":len")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,
        chunk_overlap=100,
        length_function=len,
        add_start_index=True,
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Split {len(documents)} documents into {len(chunks)} chunks.")

    document = chunks[0]
    print(document.page_content)
    print(document.metadata)
    return chunks


def save_to_weviate(chunks):
    weaviate_url = os.environ["WEAVIATE_URL"]
    weaviate_api_key = os.environ["WEAVIATE_API_KEY"]
    with weaviate.connect_to_weaviate_cloud(
        cluster_url=weaviate_url,
        auth_credentials=Auth.api_key(weaviate_api_key),
    ) as client:
        # Load the embedding model
        embedding_model = AutoModel.from_pretrained(
            "jinaai/jina-embeddings-v2-base-en", trust_remote_code=True
        )

        # Define Weaviate schema if not already done
        class_name = "PDFChunk"
        if not client.collections.exists(class_name):
            # schema = {
            #     "class": class_name,
            #     "vectorizer": "none",  # Custom embeddings are provided
            #     "properties": [
            #         {"name": "content", "dataType": ["text"]},
            #         {"name": "chunk_index", "dataType": ["int"]},
            #         {"name": "user_id", "dataType": ["string"]},
            #         {"name": "pdf_id", "dataType": ["string"]},
            #     ],
            # }
            client.collections.create(
                class_name,
                properties=[
                    Property(name="content", data_type=DataType.TEXT),
                    Property(name="chunk_index", data_type=DataType.INT),
                    Property(name="user_id", data_type=DataType.TEXT),
                    Property(name="pdf_id", data_type=DataType.TEXT),
                ],
            )

            print(f"Schema created for class '{class_name}'")

        pdf_chunk = client.collections.get(class_name)
        for index, chunk in enumerate(chunks):
            # Generate the embedding
            embedding = embedding_model.encode(chunk.page_content)

            # Metadata for the chunk
            metadata = {
                "content": chunk.page_content,
                "chunk_index": index,
                "user_id": "user_id",  # Replace with actual user_id
                "pdf_id": "pdf_id",  # Replace with actual pdf_id
            }

            uuid = pdf_chunk.data.insert(metadata,vector=embedding)

        print("All chunks saved successfully!",uuid)


if __name__ == "__main__":
    # extract_from_pdf()
    # generate_data_store()
    embedding_model = AutoModel.from_pretrained(
        "jinaai/jina-embeddings-v2-base-en", trust_remote_code=True
    )
    print(embedding_model.encode("what is classication"))
