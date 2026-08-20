from fastapi import FastAPI, Request

from app.db.database import engine, Base
from app.models import user, campaign, campaign_task
from app.core.exceptions import setup_exception_handlers


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Manager Campaign"
)


setup_exception_handlers(app)


@app.get("/")
def root():
    return {
        "message": "API đang chạy"
    }


@app.get("/health")
def health_check(request: Request):
    return {
        "message": "Hệ thống đang hoạt động bình thường!",
        "request": str(request.url)
    }