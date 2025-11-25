from fastapi import FastAPI
from app.database.base import Base
from app.database.session import engine
from app.modules.users.router import router as users_router
from app.modules.products.router import router as products_router

app = FastAPI(title="Product Catalog API", version="1.0.0")

@app.on_event("startup")
def startup_event():
    Base.metadata.create_all(bind=engine)

app.include_router(users_router)
app.include_router(products_router)

@app.get("/")
def health_check():
    return {"status": "ok"}
