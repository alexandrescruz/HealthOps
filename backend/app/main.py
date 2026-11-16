from fastapi import FastAPI
from .routers.estabelecimentos import router as estabelecimentos_router
from contextlib import asynccontextmanager
from app.database import pool   

@asynccontextmanager
async def lifespan(app: FastAPI):
    pool.open()    
    try:
        pool.wait()
        yield
    finally:
        pool.close()



app = FastAPI(title="healthOps", description="healthOps API", version="1.0.0",lifespan=lifespan)

app.include_router(estabelecimentos_router)
@app.get("/api/health")
def health_check():
    return {"status": "ok","Service": "healthOps API is running successfully."}

@app.get("/")
def root():
    return {"message": "Welcome to healthOps API!"}


