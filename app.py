from fastapi import FastAPI, HTTPException, Request
import redis
import os

app = FastAPI()


# Redis configuration
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")


# Connect to Redis
r = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    password=REDIS_PASSWORD,
    decode_responses=True,
)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    print(f"Incoming request path: {request.url.path}")

    response = await call_next(request)

    return response


@app.get("/")
def root():
    return {"message": "FastAPI is working"}


@app.post("/cache")
def store_value(key: str, value: str):
    try:
        r.set(key, value)
    except redis.RedisError as exc:
        raise HTTPException(
            status_code=503,
            detail="Redis is unavailable",
        ) from exc

    return {"message": f"Stored key '{key}'"}


@app.get("/cache")
def get_value(key: str):
    try:
        value = r.get(key)
    except redis.RedisError as exc:
        raise HTTPException(
            status_code=503,
            detail="Redis is unavailable",
        ) from exc

    if value is None:
        raise HTTPException(
            status_code=404,
            detail="Key not found",
        )

    return {
        "key": key,
        "value": value,
    }


@app.get("/secret-test")
def show_secret():
    return {
        "password": os.getenv("REDIS_PASSWORD")
    }