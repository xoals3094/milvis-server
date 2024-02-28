from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from exceptions import PersistenceException


def error_handling(app: FastAPI):
    @app.exception_handler(PersistenceException.ResourceNotFoundException)
    def resource_not_found_exception(reqeust, exc: PersistenceException.ResourceNotFoundException):
        return JSONResponse(content=exc.msg, status_code=status.HTTP_404_NOT_FOUND)
