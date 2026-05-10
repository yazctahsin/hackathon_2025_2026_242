from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from database import create_db_and_tables, get_session
from models import Order, Shipment
from sqlmodel import select
from datetime import datetime, date
import json
from notification import router as notification_router
from ai_service import (
    ask_gemini_recovery,
    ask_gemini_summary
)

app = FastAPI(title="SevkAI / LogiWise PRO API")

app.include_router(notification_router)

# ---------------- CORS ----------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- STATUS MAP ----------------

STATUS_MAP = {
    "Sipariş Alındı": 0,
    "Alındı": 0,
    "Hazırlanıyor": 1,
    "Kargoda": 2,
    "Teslim": 3,
    "Teslim Edildi": 3
}

# ---------------- RISK ENGINE ----------------

def calculate_risk_level(order_status, eta_date, total_amount, current_date=None):

    if current_date is None:
        current_date = datetime.now()

    try:

        if order_status in ["Teslim", "Teslim Edildi"]:
            return "LOW", 0

        if not eta_date:
            return "MEDIUM", 50

        if isinstance(eta_date, date) and not isinstance(eta_date, datetime):
            eta_date = datetime.combine(eta_date, datetime.min.time())

        delay_days = (current_date - eta_date).days

        risk = 0

        # gecikme
        if delay_days > 0:
            risk += 70
        if delay_days >= 7:
            risk += 50
        elif delay_days >= 3:
            risk += 30
        elif delay_days >= 1:
            risk += 15

        # status
        if order_status == "Kargoda":
            risk += 30
        elif order_status == "Hazırlanıyor":
            risk += 40

        # amount
        if total_amount >= 5000:
            risk += 25
        elif total_amount >= 2000:
            risk += 15

        # HARD RULE
        if delay_days >= 5 and order_status != "Teslim Edildi":
            risk = 100

        # 🔥 CLAMP (EN KRİTİK FIX)
        risk = max(0, min(100, risk))

        if risk >= 75:
            return "HIGH", risk
        elif risk >= 40:
            return "MEDIUM", risk
        else:
            return "LOW", risk

    except Exception as e:
        print("RISK ERROR:", e)
        return "LOW", 0


@app.on_event("startup")
def startup():
    create_db_and_tables()


@app.get("/orders")
def get_orders(session=Depends(get_session)):

    orders = session.exec(select(Order)).all()

    result = []

    for o in orders:

        shipment = session.exec(
            select(Shipment).where(Shipment.order_id == o.id)
        ).first()

        risk_level, risk_score = calculate_risk_level(
            o.status,
            shipment.eta_date if shipment else None,
            o.total_amount
        )

        result.append({
            "id": o.id,
            "customer_name": o.customer_name,
            "status": o.status,
            "current_step": STATUS_MAP.get(o.status, 0),
            "order_date": o.order_date,
            "total_amount": o.total_amount,
            "risk_level": risk_level,
            "risk_score": risk_score,
            "tracking_code": shipment.tracking_code if shipment else "N/A"
        })

    return result


@app.get("/ghost-support/auto-action")
def ghost_support(session=Depends(get_session)):

    orders = session.exec(select(Order)).all()

    high_risk = []

    for o in orders:

        shipment = session.exec(
            select(Shipment).where(Shipment.order_id == o.id)
        ).first()

        level, score = calculate_risk_level(
            o.status,
            shipment.eta_date if shipment else None,
            o.total_amount
        )

        if level == "HIGH":
            high_risk.append({
                "id": o.id,
                "customer": o.customer_name,
                "status": o.status,
                "risk_score": score
            })

    if not high_risk:

        return {
            "status": "Safe",
            "risky_orders_count": 0,
            "ml_risk_analysis": {
                "score": 0,
                "factors": ["Operasyon stabil"]
            }
        }

    score = min(100, 60 + len(high_risk) * 10)

    prompt = f"""
    {len(high_risk)} HIGH risk sipariş var.

    {high_risk}

    Aksiyon üret.
    """

    ai = ask_gemini_recovery(prompt)

    try:
        ai_data = json.loads(ai)
    except:
        ai_data = {
            "reason": "system fallback",
            "actions": ["manual check"],
            "priority": "HIGH"
        }

    return {
        "status": "success",
        "risky_orders_count": len(high_risk),
        "ai_action": ai_data,
        "ml_risk_analysis": {
            "score": score,
            "factors": [
                f"High Risk: {len(high_risk)}",
                "Delay detected",
                "Operational stress"
            ]
        }
    }


@app.get("/ai-summary")
def ai_summary(session=Depends(get_session)):

    orders = session.exec(select(Order)).all()
    shipments = session.exec(select(Shipment)).all()

    context = f"{orders}\n{shipments}"

    return {
        "summary": ask_gemini_summary(context)
    }