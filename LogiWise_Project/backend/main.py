from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from database import create_db_and_tables, get_session, engine
from models import Order, Product, Shipment
from sqlmodel import select
from sqlalchemy import text
from datetime import date
import json

# ai_service dosyasından gerekli fonksiyonları çağırıyoruz
from ai_service import ask_gemini_sql, ask_gemini_recovery, ask_gemini_summary

app = FastAPI(title="SevkAI / LogiWise API")

# --- CORS AYARI (Frontend Bağlantısı İçin Şart) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/")
def read_root():
    return {"message": "SevkAI Backend Sistemi Online!"}

@app.get("/orders")
def get_orders(session=Depends(get_session)):
    statement = select(Order)
    results = session.exec(statement).all()
    return results

# --- 1. YAPAY ZEKA SORGULAMA UCU (Reaktif - Chat) ---
@app.get("/ask-ai")
def ask_ai(prompt: str, session=Depends(get_session)):
    try:
        enhanced_prompt = f"{prompt} (Önemli: SQLite kullandığımız için tablo isimlerini \"Order\" şeklinde çift tırnak içine al.)"
        sql_query = ask_gemini_sql(enhanced_prompt)
        
        result = session.execute(text(sql_query))
        data = result.mappings().all()
        
        return {
            "user_prompt": prompt,
            "generated_sql": sql_query,
            "results": data
        }
    except Exception as e:
        return {"error": "Bir hata oluştu", "details": str(e)}

# --- 2. GHOST SUPPORT: PROAKTİF AKSİYON UCU ---
@app.get("/ghost-support/auto-action")
def ghost_support_action(session=Depends(get_session)):
    """
    Sistemdeki riskli kargoları bulur ve Frontend ile uyumlu JSON döner.
    """
    try:
        # 1. Aşama: Risk tespiti için SQL üretimi
        risk_query = "2026-05-09 tarihinden önce teslim edilmesi gereken ama teslim edilmemiş kargoları bul."
        generated_sql = ask_gemini_sql(risk_query)
        
        # 2. Aşama: Veritabanında çalıştırma
        result = session.execute(text(generated_sql))
        results = result.mappings().all()
        
        if not results:
            return {
                "status": "Safe",
                "message": "Şu an operasyonel bir risk bulunamadı.",
                "ai_action": None
            }

        # 3. Aşama: Gemini'den Frontend uyumlu (reason/action) yanıt alma
        recovery_prompt = f"Şu kargolar gecikti: {list(results)}. Nedenini analiz et ve müşteriye 'SEVKAI20' kodlu bir özür mesajı hazırla."
        
        ai_response_raw = ask_gemini_recovery(recovery_prompt)
        # Gemini'den gelen JSON string'i Python objesine çeviriyoruz
        ai_action_data = json.loads(ai_response_raw)
        
        return {
            "status": "success",
            "risky_orders_count": len(results),
            "ai_action": ai_action_data # Frontend artık burada reason ve action bulabilecek
        }

    except Exception as e:
        return {"status": "Error", "message": str(e)}

# --- 3. YAPAY ZEKA GÜNLÜK ÖZETİ ---
@app.get("/ai-summary")
def get_ai_summary(session=Depends(get_session)):
    try:
        orders = session.exec(select(Order)).all()
        shipments = session.exec(select(Shipment)).all()
        
        # Daha detaylı veri gönderiyoruz ki özet daha iyi olsun
        data_context = f"Siparişler: {orders}, Sevkiyatlar: {shipments}"
        summary = ask_gemini_summary(data_context)
        
        return {"summary": summary}
    except Exception as e:
        return {"summary": "Özet şu an hazırlanamıyor.", "detail": str(e)}

# --- 4. DEMO VERİ SETİ OLUŞTURUCU (Gecikme Simülasyonu) ---
@app.get("/setup-demo-data")
def setup_demo_data(session=Depends(get_session)):
    """Gecikmiş bir kargo oluşturur (Ghost Support'u test etmek için)"""
    try:
        session.execute(text("DELETE FROM shipment"))
        session.execute(text("DELETE FROM \"order\""))
        session.commit()
        
        # 4 gün önce verilmiş bir sipariş
        o1 = Order(customer_name="Ahmet Yılmaz", order_date=date(2026, 5, 5), status="Hazırlanıyor", total_amount=1500.0)
        session.add(o1)
        session.commit()
        session.refresh(o1)
        
        # Teslim tarihi 2 gün önce geçmiş (Gecikmiş kargo)
        s1 = Shipment(order_id=o1.id, tracking_code="TRK-999", eta_date=date(2026, 5, 7), current_location="Depo Transfer Merkezi")
        session.add(s1)
        session.commit()
        
        return {"status": "Success", "message": "Gecikme senaryosu yüklendi. Ghost Support'u çalıştırabilirsiniz!"}
    except Exception as e:
        return {"status": "Error", "message": str(e)}