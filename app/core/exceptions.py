from datetime import datetime, timezone
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse


def setup_exception_handlers(app: FastAPI):

    @app.exception_handler(HTTPException)
    async def handle_http_exception(
        request: Request,
        exc: HTTPException
    ):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "status": "error",
                "code": exc.status_code,
                "error": "HTTP Error",
                "message": exc.detail,
                "data": None,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "path": request.url.path
            }
        )