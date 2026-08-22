from fastapi import FastAPI, Request, HTTPException
from app.db.database import engine, Base
from app.models import user, campaign, campaign_task
from app.core.exceptions import setup_exception_handlers
from app.router import users, auth

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Manager Campaign"
)
setup_exception_handlers(app)
app.include_router(auth.router)
app.include_router(users.router)
@app.get("/")
def root():
    return {
        "message": "API đang chạy"
    }

@app.get("/health")
def health_check():
    return {
        "message": "Hệ thống đang hoạt động bình thường!"
    }
