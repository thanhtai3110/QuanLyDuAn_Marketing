from datetime import datetime, timezone
from typing import Any
from fastapi import Request
from pydantic import BaseModel

class APIResponse(BaseModel):
    statusCode: int
    message: str
    data: Any 
    error: Any 
    timestamp: str
    path: str

def success_response(
    request: Request,
    message: str,
    data: Any,
    status_code: int = 200
):
    return APIResponse(
        statusCode=status_code,
        message=message,
        data=data,
        error=None,
        timestamp=datetime.now(timezone.utc).isoformat(),
        path=request.url.path
    )

def error_response(
    request: Request,
    message: str,
    error: Any,
    status_code: int = 400
):
    return APIResponse(
        statusCode=status_code,
        message=message,
        data=None,
        error=error,
        timestamp=datetime.now(timezone.utc).isoformat(),
        path=request.url.path
    )