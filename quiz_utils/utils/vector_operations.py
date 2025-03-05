import os
from dotenv import load_dotenv
import weaviate
import torch
from weaviate.classes.init import Auth
from weaviate.classes.config import Property, DataType
from weaviate.exceptions import WeaviateBaseError
from weaviate.classes.init import AdditionalConfig, Timeout
from transformers import AutoModel


class VectorDBOperations:
    @staticmethod
    def connect_weaviate():
        load_dotenv()
        weaviate_url = os.environ["WEAVIATE_URL"]
        weaviate_api_key = os.environ["WEAVIATE_API_KEY"]
        print(weaviate_api_key, weaviate_url)
        client = weaviate.connect_to_weaviate_cloud(
            cluster_url=weaviate_url,
            auth_credentials=Auth.api_key(weaviate_api_key),
            additional_config=AdditionalConfig(
                timeout=Timeout(init=300, query=60, insert=120) # Values in seconds
            ),
        )
        return client

    @staticmethod
    def create_schema(client, class_name):
        try:
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
        except WeaviateBaseError as e:
            print(e)

    @staticmethod
    def insert(client, chunks, user_id):
        try:
            if not client.collections.exists(user_id):
                VectorDBOperations.create_schema(client, user_id)

            embedding_model = AutoModel.from_pretrained(
                "./model", trust_remote_code=True
            )

            pdf_chunk = client.collections.get(user_id)
            for index, chunk in enumerate(chunks):
                device = "cuda" if torch.cuda.is_available() else "cpu"
                embedding = embedding_model.encode(chunk[0])

                metadata = {
                    "content": chunk,
                    "chunk_index": index,
                    "pdf_id": chunk[1],
                }

                uuid = pdf_chunk.data.insert(metadata, vector=embedding)

            print("All chunks saved successfully!", uuid)
        except WeaviateBaseError as e:
            print("hello")
            print(e)

    @staticmethod
    def read(client, class_name):
        try:
            return client.collections.get(class_name)
        except WeaviateBaseError as e:
            print(e)

    @staticmethod
    def delete(client, class_name):
        print("deleting began...")
        try:
            client.collections.delete(class_name)
            print("deleting done...")
        except WeaviateBaseError as e:
            print(e)


if "__main__" == __name__:
    client = VectorDBOperations.connect_weaviate()
    VectorDBOperations.delete(client, "pdf_chunk")
