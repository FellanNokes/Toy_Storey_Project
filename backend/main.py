from fastapi import FastAPI

from backend.routers import products, revenue, sales

app = FastAPI(title="Toy Storey API")
app.include_router(sales.router)
#app.include_router(revenue.router)
#app.include_router(products.router)


@app.get("/health")
def health():
    return {"status": "ok"}