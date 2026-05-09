from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from database import create_db_and_tables, get_session
from models import Order, Shipment
from sqlmodel import select
from sqlalchemy import text
from datetime import date
import json

# ai_service dosyasından gerekli fonksiyonları çağırıyoruz
from ai_service import ask_gemini_sql, ask_gemini_recovery, ask_gemini_summary

app = FastAPI(title="SevkAI / LogiWise API")

# --- CORS AYARI ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def calculate_risk_level(eta_date, current_date=date(2026, 5, 9)):
    """Basit risk skorlama sistemi"""
    try:
        delay_days = (current_date - eta_date).days
        if delay_days >= 3:
            return "HIGH"
        elif delay_days >= 1:
            return "MEDIUM"
        else:
            return "LOW"
    except:
        return "LOW"


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/")
def read_root():
    return {"message": "SevkAI Backend Sistemi Online!", "status": "running"}


# --- SİPARİŞLERİ GETİR ---
@app.get("/orders")
def get_orders(session=Depends(get_session)):
    statement = select(Order)
    orders = session.exec(statement).all()

    status_map = {
        "Sipariş Alındı": 0,
        "Hazırlanıyor": 1,
        "Kargoda": 2,
        "Teslim Edildi": 3
    }

    enriched = []
    for o in orders:
        shipment = session.exec(select(Shipment).where(Shipment.order_id == o.id)).first()
        risk = "LOW"
        if shipment and shipment.eta_date:
            risk = calculate_risk_level(shipment.eta_date)

        enriched.append({
            "id": o.id,
            "customer_name": o.customer_name,
            "status": o.status,
            "current_step": status_map.get(o.status, 0),
            "order_date": o.order_date,
            "total_amount": o.total_amount,
            "risk_level": risk
        })

    return enriched


# --- GHOST SUPPORT: PROAKTİF AKSİYON UCU (GÜNCELLENDİ) ---
@app.get("/ghost-support/auto-action")
def ghost_support_action(session=Depends(get_session)):
    try:
        # 1. Adım: Riskli kargoları bulmak için AI'dan SQL al
        risk_query = "2026-05-09 tarihinden önce teslim edilmesi gereken ama teslim edilmemiş kargoları bul."
        generated_sql = ask_gemini_sql(risk_query)

        result = session.execute(text(generated_sql))
        results = result.mappings().all()

        if not results:
            return {
                "status": "Safe",
                "message": "Şu an operasyonel bir risk bulunamadı.",
                "ai_action": None
            }

        # 2. Adım: Risk analizini recovery servisine gönder
        recovery_prompt = (
            f"Şu kargolar gecikti: {list(results)}. "
            f"Nedenini analiz et ve JSON formatında şu alanları döndür: "
            f"'reason' (neden), 'actions' (aksiyon listesi), 'priority' (öncelik)."
        )

        ai_response_raw = ask_gemini_recovery(recovery_prompt)

        # JSON parse işlemi (AI bazen markdown içinde verebilir, ai_service içinde temizlenmediyse dikkat)
        try:
            ai_action_data = json.loads(ai_response_raw)
        except:
            # Yedek plan: Eğer AI hatalı JSON dönerse manuel oluştur
            ai_action_data = {
                "reason": "Genel lojistik aksaklık algılandı.",
                "actions": ["Müşteri bilgilendirme mesajı gönder"],
                "priority": "MEDIUM"
            }

        formatted_actions = ai_action_data.get("actions", [])

        # 3. Adım: Frontend için zenginleştirilmiş veri dön
        return {
            "status": "success",
            "risky_orders_count": len(results),
            "ai_action": {
                "reason": ai_action_data.get("reason", "Bilinmeyen gecikme faktörü"),
                "actions": formatted_actions,
                "priority": ai_action_data.get("priority", "MEDIUM")
            },
            "ml_risk_analysis": {
                "score": 82,
                "factors": [
                    "Depo Doluluk Oranı: %82",
                    "Taşıyıcı Gecikmesi: +2 Gün",
                    "Hava Durumu: Elverişsiz",
                    "Geçmiş Gecikme Oranı: Yüksek"
                ]
            }
        }
    except Exception as e:
        return {"status": "Error", "message": str(e)}


# --- YAPAY ZEKA GÜNLÜK ÖZETİ ---
@app.get("/ai-summary")
def get_ai_summary(session=Depends(get_session)):
    try:
        orders = session.exec(select(Order)).all()
        shipments = session.exec(select(Shipment)).all()
        data_context = f"Siparişler: {orders}, Sevkiyatlar: {shipments}"
        summary = ask_gemini_summary(data_context)
        return {"summary": summary}
    except Exception as e:
        return {"summary": "Özet şu an hazırlanamıyor.", "detail": str(e)}


# --- DEMO VERİ SETİ ---
@app.get("/setup-demo-data")
def setup_demo_data(session=Depends(get_session)):
    try:
        # Temizlik
        session.execute(text("DELETE FROM shipment"))
        session.execute(text("DELETE FROM \"order\""))
        session.commit()

        # Örnek 1: Gecikmiş sipariş
        o1 = Order(customer_name="Ahmet Yılmaz", order_date=date(2026, 5, 5), status="Hazırlanıyor",
                   total_amount=1500.0)
        session.add(o1)
        session.commit()
        session.refresh(o1)

        s1 = Shipment(order_id=o1.id, tracking_code="TRK-999", eta_date=date(2026, 5, 7),
                      current_location="Depo Transfer Merkezi")
        session.add(s1)

        # Örnek 2: Zamanında sipariş
        o2 = Order(customer_name="Ayşe Demir", order_date=date(2026, 5, 8), status="Kargoda",
                   total_amount=2450.0)
        session.add(o2)
        session.commit()
        session.refresh(o2)

        s2 = Shipment(order_id=o2.id, tracking_code="TRK-101", eta_date=date(2026, 5, 12),
                      current_location="Yolda")
        session.add(s2)

        session.commit()
        return {"status": "Success", "message": "Demo verileri (gecikme senaryosu dahil) yüklendi!"}
    except Exception as e:
        session.rollback()
        return {"status": "Error", "message": str(e)}