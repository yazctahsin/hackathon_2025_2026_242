from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

# Ürünler Tablosu
class Product(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    price: float
    stock: int

# Siparişler Tablosu
class Order(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    customer_name: str
    order_date: datetime = Field(default_factory=datetime.now)
    status: str  # Örn: 'Hazırlanıyor', 'Kargoda', 'Teslim Edildi'
    total_amount: float

# Kargo/Sevkiyat Detayları Tablosu
class Shipment(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    order_id: int = Field(foreign_key="order.id")
    tracking_code: str
    eta_date: datetime
    current_location: str