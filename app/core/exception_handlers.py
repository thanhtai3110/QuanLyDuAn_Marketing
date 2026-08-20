from fastapi import Request
from fastapi.responses import JSONResponse
from app.core.exceptions import NotFoundException,BadRequestException,ForbiddenException
from app.core.response import error_response

async def not_found_exception_handler(
    request: Request,
    exc: NotFoundException
):
    response = error_response(
        request=request,
        message=exc.message,
        error="Không tìm thấy tài nguyên",
        status_code=404
    )

    return JSONResponse(
        status_code=404,
        content=response.model_dump()
    )


async def bad_request_exception_handler(
    request: Request,
    exc: BadRequestException
):
    response = error_response(
        request=request,
        message=exc.message,
        error="Yêu cầu không hợp lệ",
        status_code=400
    )

    return JSONResponse(
        status_code=400,
        content=response.model_dump()
    )


async def forbidden_exception_handler(
    request: Request,
    exc: ForbiddenException
):
    response = error_response(
        request=request,
        message=exc.message,
        error="Bạn không có quyền thực hiện thao tác này",
        status_code=403
    )

    return JSONResponse(
        status_code=403,
        content=response.model_dump()
    )