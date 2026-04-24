from fastapi import FastAPI
from app.core.config import settings
from app.core.redis import redis_client
from app.api.auth import router as auth_router
from app.api.contests import router as contest_router
from app.api.problems import router as problem_router
from app.api.test_cases import router as tc_router
from app.api.submissions import router as submission_router
from app.core.database import Base, engine
from app.models.user import User
from app.models.contest import Contest
from app.models.problem import Problem
from app.models.test_case import TestCase
from app.models.submission import Submission
from fastapi.middleware.cors import CORSMiddleware


async def lifespan(app: FastAPI):
    try:
        redis_client.ping()
        print("Redis is alive!")
    except Exception as e:
        print(f"Could not connect to Redis: {e}")
    yield
    try:
        redis_client.close()
    except Exception:
        pass


app = FastAPI(title="CodeContest")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(contest_router)
app.include_router(problem_router)
app.include_router(tc_router)
app.include_router(submission_router)


@app.get("/")
def root():
    return {"message": "CodeContest API Running"}


@app.get("/redis-health")
def check_redis():
    try:
        redis_client.ping()
        return {"status": "Redis is connected"}
    except Exception:
        return {"status": "Redis connection lost"}, 503


# Create database tables
Base.metadata.create_all(bind=engine)


@app.get("/health")
def health():
    return {"status": "ok"}