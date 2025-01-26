from utils.vector_operations import VectorDBOperations as db
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
import json
from langchain_core.output_parsers import JsonOutputParser
from dotenv import load_dotenv


load_dotenv()


def generate_questions(client):
    parser = JsonOutputParser(
        pydantic_object={
            "type": "object",
            "properties": {
                "question_1": {"type": "string"},
                "question_2": {"type": "string"},
            },
            "required": ["question_1", "question_2"],
        }
    )

    # Create a simple prompt for generating questions
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """Based on the content provided, generate one or two relevant, thought-provoking and only important questions. 
            Return the output in this JSON format.
            NOTE:ONLY GIVE THE QUESTIONS AND NOTHING MORE THAN THAT:
            {{
                "question_1": "first question here",
                "question_2": "second question here"
                ...
            }}""",
            ),
            ("user", "{input}"),
        ]
    )

    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=1,
    )
    chain = prompt | llm | parser

    collection = db.read(client, "pdf_chunks")
    print("retrived:", len(collection))

    for id, item in enumerate(collection.iterator()):
        response = {}
        res = chain.invoke({"input": item.properties["content"]})
        print(res, end="\n\n")
        for key, value in res.items():
            response[f"{id}_{key}"] = value
            yield json.dumps(response)

    return response
