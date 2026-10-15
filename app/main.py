import time
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from app import orders, metrics
import app.database as database

app = FastAPI()


class OrderRequest(BaseModel):
    item: str
    quantity: int


@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    elapsed = time.time() - start
    metrics.record_request(
        route=request.url.path,
        status_code=response.status_code,
        response_time=round(elapsed, 4),
    )
    return response


@app.post("/orders", status_code=201)
def create_order(payload: OrderRequest):
    try:
        database.get_db()
    except Exception:
        raise HTTPException(status_code=503, detail="Service unavailable")
    return orders.create_order(item=payload.item, quantity=payload.quantity)


@app.get("/orders")
def list_orders():
    try:
        database.get_db()
    except Exception:
        raise HTTPException(status_code=503, detail="Service unavailable")
    return orders.list_orders()


@app.get("/orders/{order_id}")
def get_order(order_id: int):
    try:
        database.get_db()
    except Exception:
        raise HTTPException(status_code=503, detail="Service unavailable")
    order = orders.get_order(order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@app.get("/health")
def health_check():
    try:
        database.get_db()
        return {"status": "ok"}
    except Exception:
        return JSONResponse(
            status_code=200,
            content={"status": "degraded", "db": "down"},
        )
