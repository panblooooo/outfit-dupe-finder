from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import Base, engine
from .routers import products

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Outfit Dupe Finder API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(products.router)

@app.get("/health")
def health():
    return {"status": "ok"}