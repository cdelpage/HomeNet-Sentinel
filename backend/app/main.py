from fastapi import FastAPI, HTTPException
from typing import Dict, Any

from app import models
from app.database import engine

# Create the database tables
models.Base.metadata.create_all(bind=engine)

from app.models import ScanPayload

app = FastAPI(
    title="HomeNet Sentinel",
    description="Lightweight SIEM + Wireless Threat Detection System API",
    version="0.1.0"
)

@app.get("/")
async def root() -> Dict[str, str]:
    return {"status": "ok", "message": "HomeNet Sentinel API is running"}

@app.post("/scan", response_model=Dict[str, Any])
async def receive_scan(payload: ScanPayload):
    # For Sprint 1, we just validate the payload and return a success message.
    # In Sprint 3, this will be passed to the Detection Engine.
    
    scan_count = len(payload.scans)
    
    return {
        "status": "success",
        "message": f"Successfully received {scan_count} scans from sensor {payload.sensor_id}",
        "sensor_id": payload.sensor_id
    }
