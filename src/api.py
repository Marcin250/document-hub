import uuid
from datetime import datetime

from fastapi import FastAPI, HTTPException, Response, UploadFile
from fastapi_injector import Injected, attach_injector
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from gridfs import GridFS, GridFSBucket
from pymongo import MongoClient

from app.configuration import Configuration
from app.dependency_container import Container

document_router = InferringRouter(tags=["DocumentController"])
status_router = InferringRouter(tags=["StatusController"])

MAX_CHUNK_SIZE_IN_BYTES = 229376


@cbv(document_router)
class DocumentController:
    __configuration: Configuration = Injected(Configuration)

    def __db(self):
        client = MongoClient(self.__configuration.database.uri)
        return client[self.__configuration.database.database]

    def __files(self):
        return self.__db()["fs.files"]

    def __grid_fs(self) -> GridFS:
        return GridFS(self.__db())

    def __grid_fs_bucket(self) -> GridFSBucket:
        return GridFSBucket(self.__db())

    @document_router.put("/documents")
    async def upload(self, document: UploadFile):
        _id = str(uuid.uuid4())

        try:
            with self.__grid_fs().new_file(
                _id=_id,
                content_type=document.content_type,
                chunk_size=MAX_CHUNK_SIZE_IN_BYTES,
            ) as grid_file:
                while content := await document.read(MAX_CHUNK_SIZE_IN_BYTES):
                    grid_file.write(content)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

        return Response(content=None, status_code=202, headers={"documentId": _id})

    @document_router.get("/documents/{_id}")
    def download(self, _id: str):
        file = self.__files().find_one({"_id": _id})
        if not file:
            return Response(status_code=404)

        return Response(
            content=self.__grid_fs_bucket().open_download_stream(_id).read(),
            status_code=200,
        )


@cbv(status_router)
class StatusController:
    @status_router.get("/status")
    def index(self):
        return Response(
            content=datetime.now().strftime("%Y-%m-%d %H:%M:%S"), status_code=200
        )


class Application:
    app: FastAPI

    def __init__(self):
        self.app = FastAPI()
        self.app.include_router(status_router, prefix="/api/v1")
        self.app.include_router(document_router, prefix="/api/v1")
        self.app.state.injector = (application_injector := Container().injector())
        attach_injector(self.app, application_injector)

    @classmethod
    def initialize(cls) -> FastAPI:
        return cls().app


app = Application().initialize()
