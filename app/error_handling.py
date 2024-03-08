from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from exceptions import PersistenceException


def error_handling(app: FastAPI):
    @app.exception_handler(PersistenceException.ResourceNotFoundException)
    def resource_not_found_exception(reqeust, exc: PersistenceException.ResourceNotFoundException):
        return JSONResponse(content={'msg': '일치하는 데이터를 찾을 수 없습니다'}, status_code=status.HTTP_404_NOT_FOUND)

    @app.exception_handler(PersistenceException.ConnectionException)
    def resource_not_found_exception(reqeust, exc: PersistenceException.ResourceNotFoundException):
        return JSONResponse(content={'msg': '서버 연결이 불안정하여 데이터를 가져올 수 없습니다. 잠시 후 다시 시도해주세요'}, status_code=status.HTTP_502_BAD_GATEWAY)

