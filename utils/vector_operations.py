import os
from dotenv import load_dotenv
import weaviate
from weaviate.classes.init import Auth
from weaviate.classes.config import Property, DataType
from transformers import AutoModel


class VectorDBOperations:
    def __init__(self):
        load_dotenv()
        weaviate_url = os.environ["WEAVIATE_URL"]
        weaviate_api_key = os.environ["WEAVIATE_API_KEY"]
        self.client = weaviate.connect_to_weaviate_cloud(
            cluster_url=weaviate_url, auth_credentials=Auth.api_key(weaviate_api_key)
        )

    def create_schema(self, class_name):
        self.client.collections.create(
            class_name,
            properties=[
                Property(name="content", data_type=DataType.TEXT),
                Property(name="chunk_index", data_type=DataType.INT),
                Property(name="user_id", data_type=DataType.TEXT),
                Property(name="pdf_id", data_type=DataType.TEXT),
            ],
        )
        print(f"Schema created for class '{class_name}'")

    def insert(self, class_name, chunks, user_id):
        if not self.client.collections.exists(class_name):
            self.create_schema(class_name)

        embedding_model = AutoModel.from_pretrained(
            "jinaai/jina-embeddings-v2-base-en", trust_remote_code=True
        )

        pdf_chunk = self.client.collections.get(class_name)
        for index, chunk in enumerate(chunks):
            # Generate the embedding
            embedding = embedding_model.encode(chunk[0], device="cuda")

            # Metadata for the chunk
            metadata = {
                "content": chunk,
                "chunk_index": index,
                "user_id": user_id,  # Replace with actual user_id
                "pdf_id": chunk[1],  # Replace with actual pdf_id
            }

            uuid = pdf_chunk.data.insert(metadata, vector=embedding)

        print("All chunks saved successfully!", uuid)

    def read(self, class_name):
        collection = self.client.collections.get(class_name)

        for item in collection.iterator():
            print(f"{item.uuid} {item.properties}...")

    def delete(self, class_name):
        print("deleting began...")
        self.client.collections.delete(class_name)
        print("deleting done...")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.client.close()
        if exc_type:
            print(f"An exception occurred: {exc_value}")
        return False

    def __del__(self):
        self.client.close()


if "__main__" == __name__:
    a = VectorDBOperations()
    a.delete("pdf_chunk")
    del a
