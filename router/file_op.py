from fastapi import APIRouter, UploadFile, Depends
from typing import Annotated
import shutil
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Callable
from quiz_utils.utils import PDFVectorizer
import os
from .user import validate_token
from quiz_utils.utils import VectorDBOperations as db
import dotenv

dotenv.load_dotenv()

router = APIRouter()


# from fastapi import AP
def save_upload_file_tmp(upload_file: UploadFile, user_id) -> Path:
    try:
        suffix = Path(upload_file.filename).suffix
        path = Path(f"{os.environ['TMP_FOLDER']}{user_id}")
        path.mkdir(parents=True)

        with NamedTemporaryFile(dir=path, delete=False, suffix=suffix) as tmp:
            shutil.copyfileobj(upload_file.file, tmp)
            tmp_path = Path(tmp.name)
    finally:
        upload_file.file.close()
    return tmp_path


def handle_upload_file(
    upload_file: UploadFile, handler: Callable[[Path], None], user_id
) -> None:
    tmp_path = save_upload_file_tmp(upload_file, user_id)
    try:
        print(tmp_path)
        chunks = handler(tmp_path)
    finally:
        tmp_path.unlink()
        shutil.rmtree(tmp_path.parent)
    return chunks


@router.post("/uploadfile")
def create_upload_file(
    file: UploadFile, user_id: Annotated[str, Depends(validate_token)]
):
    pdf_vectorizer = PDFVectorizer()
    chunks = handle_upload_file(file, pdf_vectorizer.pdf_vectorize_store, user_id)
    client = db.connect_weaviate()
    db.insert(client,chunks,user_id)
    client.close()
    return {"filename": chunks}
