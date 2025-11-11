import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

from database import db, create_document, get_documents
from schemas import Order, Testimonial

app = FastAPI(title="Boosting Service API", description="API for game boosting services", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Boosting Service API running"}

@app.get("/api/hello")
def hello():
    return {"message": "Hello from the backend API!"}

@app.get("/test")
def test_database():
    """Test endpoint to check if database is available and accessible"""
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }
    
    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Configured"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
            
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"
    
    # Check environment variables
    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"
    
    return response

# Request model for price calculation
class PriceRequest(BaseModel):
    service: str
    quantity: int = 1
    priority: bool = False
    streaming: bool = False

class PriceResponse(BaseModel):
    base_price: float
    addons: float
    total: float

# Basic pricing table (can be extended)
PRICES = {
    "exploration": 5.0,      # per 10% map or zone
    "spiral_abyss": 12.0,    # per floor
    "leveling": 3.5,         # per level
    "farming": 8.0,          # per hour
    "boss_runs": 6.0,        # per run
}

PRIORITY_MULT = 1.25
STREAMING_FEE = 3.0

@app.post("/api/calculate", response_model=PriceResponse)
def calculate_price(req: PriceRequest):
    service_key = req.service.lower()
    if service_key not in PRICES:
        raise HTTPException(status_code=400, detail="Unknown service")
    base_unit = PRICES[service_key]
    base_price = base_unit * max(1, req.quantity)
    addons = 0.0
    if req.priority:
        base_price *= PRIORITY_MULT
    if req.streaming:
        addons += STREAMING_FEE
    total = round(base_price + addons, 2)
    return PriceResponse(base_price=round(base_price, 2), addons=round(addons, 2), total=total)

@app.post("/api/orders")
def create_order(order: Order):
    try:
        order_id = create_document("order", order)
        return {"id": order_id, "status": "received"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/testimonials", response_model=List[Testimonial])
def list_testimonials(limit: int = 10):
    try:
        docs = get_documents("testimonial", {}, limit)
        # Convert ObjectId and extraneous fields
        normalized = []
        for d in docs:
            d.pop("_id", None)
            normalized.append(Testimonial(**d))
        return normalized
    except Exception:
        # Provide a few seed testimonials if DB not available
        seed = [
            Testimonial(name="Alex R.", game="Genshin Impact", rating=5, comment="Fast, safe, and super friendly. Cleared Abyss 36★ in one evening!"),
            Testimonial(name="Mina K.", game="HSR", rating=5, comment="Efficient farming package. Account felt so much stronger next day."),
            Testimonial(name="Neo", game="Multiple", rating=5, comment="Professional team. Great communication and fair pricing."),
        ]
        return seed[:limit]

# Expose schemas for the viewer
@app.get("/schema")
def get_schema_info():
    return {
        "order": Order.model_json_schema(),
        "testimonial": Testimonial.model_json_schema(),
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
