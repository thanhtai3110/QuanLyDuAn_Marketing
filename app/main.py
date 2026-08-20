from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.db.database import engine, Base
from app.models import user, campaign, campaign_member, campaign_task
from app.core.exceptions import (
    NotFoundException,
    BadRequestException,
    ForbiddenException
)
from app.core.exception_handlers import (
    not_found_exception_handler,
    bad_request_exception_handler,
    forbidden_exception_handler
)
from app.core.response import success_response
app = FastAPI(
    title="Manager Campaign"
)

Base.metadata.create_all(bind=engine)

app.add_exception_handler(
    NotFoundException,
    not_found_exception_handler
)

app.add_exception_handler(
    BadRequestException,
    bad_request_exception_handler
)
app.add_exception_handler(
    ForbiddenException,
    forbidden_exception_handler
)

@app.get("/")
def root(request: Request):
    return success_response(
        message="API đang được kết nối",
        data=None,
        request=request)

@app.get("/health")
def health_check(request: Request):
    return success_response(
        message="Hệ thống đang hoạt động",
        data={
            "status": "ok"
        },
        request=request
    )

# @app.get("/test/404")
# def test_not_found():

#     raise NotFoundException(
#         "Không tìm thấy chiến dịch"
#     )

# @app.get("/test/400")
# def test_bad_request():

#     raise BadRequestException(
#         "Dữ liệu yêu cầu không hợp lệ"
#     )

# @app.get("/test/403")
# def test_forbidden():

#     raise ForbiddenException(
#         "Bạn không có quyền thực hiện thao tác này"
#     )