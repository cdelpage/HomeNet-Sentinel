from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.sql import func
from app.database import Base

# ==========================================
# SQLAlchemy ORM Models
# ==========================================

class KnownDevice(Base):
    __tablename__ = "known_devices"
    id = Column(Integer, primary_key=True, index=True)
    bssid = Column(String, unique=True, index=True)
    ssid = Column(String)
    expected_encryption = Column(String)
    expected_channel = Column(Integer)
    first_seen = Column(DateTime(timezone=True), server_default=func.now())
    last_seen = Column(DateTime(timezone=True), onupdate=func.now())

class ScanResult(Base):
    __tablename__ = "scan_results"
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    sensor_id = Column(String, index=True)
    bssid = Column(String, index=True)
    ssid = Column(String, index=True)
    rssi = Column(Integer)
    channel = Column(Integer)
    encryption_type = Column(String)

class Alert(Base):
    __tablename__ = "alerts"
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    alert_type = Column(String) # e.g., EvilTwin, Downgrade
    description = Column(String)
    severity = Column(String) # e.g., HIGH, MEDIUM, LOW
    scan_id = Column(Integer, ForeignKey("scan_results.id"), nullable=True)
    resolved = Column(Boolean, default=False)


# ==========================================
# Pydantic Schemas
# ==========================================

class ScanItem(BaseModel):
    bssid: str = Field(..., description="MAC address of the access point")
    ssid: str = Field(..., description="SSID of the network")
    rssi: int = Field(..., description="Signal strength in dBm")
    channel: int = Field(..., description="Wi-Fi channel")
    encryption_type: str = Field(..., description="Encryption type (e.g., WPA2, WPA3, Open)")

class ScanPayload(BaseModel):
    sensor_id: str = Field(..., description="Unique ID of the reporting sensor")
    timestamp: Optional[datetime] = Field(default_factory=datetime.utcnow, description="Time of the scan")
    scans: List[ScanItem] = Field(..., description="List of access points detected in the scan")
