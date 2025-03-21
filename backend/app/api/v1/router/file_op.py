from fastapi import APIRouter, Depends, UploadFile
from typing import Annotated
from task.file_processing import process_file
from .user import validate_token
import shutil
from pathlib import Path
from tempfile import NamedTemporaryFile
import os

router = APIRouter()


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
    return tmp.name


@router.post("/uploadfile")
def create_upload_file(
    file: UploadFile, user_id: Annotated[str, Depends(validate_token)]
):
    path = save_upload_file_tmp(file,user_id)
    task = process_file.delay(path, user_id)
    return {"task_id": task.id, "status": "processing"}
