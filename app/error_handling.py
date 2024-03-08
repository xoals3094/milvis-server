from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from exceptions import PersistenceException


def error_handling(app: FastAPI):
    @app.exception_handler(PersistenceException.ResourceNotFoundException)
    def resource_not_found_exception(reqeust, exc: PersistenceException.ResourceNotFoundException):
        return JSONResponse(content={'msg': '일치하는 데이터를 찾을 수 없습니다'}, status_code=status.HTTP_404_NOT_FOUND)
