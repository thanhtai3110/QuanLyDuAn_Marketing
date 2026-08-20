from fastapi import FastAPI, Request,HTTPException
from fastapi.responses import JSONResponse
from datetime import datetime, timezone

def setup_exception_handlers(app: FastAPI):
    
    # 1. Bắt các lỗi cơ bản theo yêu cầu (400, 403, 404...)
    @app.exception_handler(HTTPException)
    async def bat_loi_http_co_ban(request: Request, exc: HTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "status": "error",
                "code": exc.status_code,
                "error": "Lỗi HTTP",
                "message": exc.detail,
                "data": None,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "path": str(request.url.path)
            }
        )