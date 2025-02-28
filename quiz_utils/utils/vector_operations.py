import os
from dotenv import load_dotenv
import weaviate
from weaviate.classes.init import Auth
from weaviate.classes.config import Property, DataType
from weaviate.exceptions import WeaviateBaseError
from transformers import AutoModel


class VectorDBOperations:
    @staticmethod
    def connect_weaviate():
        load_dotenv()
        weaviate_url = os.environ["WEAVIATE_URL"]
        weaviate_api_key = os.environ["WEAVIATE_API_KEY"]
        client = weaviate.connect_to_weaviate_cloud(
            cluster_url=weaviate_url, auth_credentials=Auth.api_key(weaviate_api_key)
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
    def insert(client, class_name, chunks, user_id):
        try:
            if not client.collections.exists(class_name):
                VectorDBOperations.create_schema(client, class_name)

            embedding_model = AutoModel.from_pretrained(
                "./model", trust_remote_code=True
            )

            pdf_chunk = client.collections.get(class_name)
            for index, chunk in enumerate(chunks):
                embedding = embedding_model.encode(chunk[0], device="cuda")

                metadata = {
                    "content": chunk,
                    "chunk_index": index,
                    "user_id": user_id,
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
