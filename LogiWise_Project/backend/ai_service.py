from google import genai
from google.genai import types
import os
from dotenv import load_dotenv

load_dotenv()

# Gemini Client Yapılandırması
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

# Seçtiğin en güncel model
CURRENT_MODEL = "gemini-2.5-flash-lite"

def ask_gemini_sql(user_query: str):    
    """Doğal dildeki soruyu SQLite sorgusuna çevirir."""
    schema_context = """
    Sen LogiWise Risk Detection Agent birimisin. 
    Tablolar:
    - Product (id, name, price, stock)
    - Order (id, customer_name, order_date, status, total_amount, product_name, quantity)
    - Shipment (id, order_id, tracking_code, eta_date, current_location)

    GÖREVİN:
    1. Kullanıcı talebine göre sadece saf SQLite kodu üret. 
    2. Bugünün tarihi: 2026-05-09.
    3. Markdown kullanma, açıklama yapma. Tablo adlarını "Order" şeklinde tırnaklı yaz.
    """   

    try:
        response = client.models.generate_content(
            model=CURRENT_MODEL,
            contents=f"{schema_context}\nSoru: {user_query}"
        )
        sql = response.text.strip().replace("```sql", "").replace("```", "").strip()
        return sql
    except Exception as e:
        raise Exception(f"Gemini API Hatası: {str(e)}")

def ask_gemini_recovery(recovery_prompt: str):
    """Gecikmeler için JSON formatında aksiyon planı üretir."""
    response_schema = {
        "type": "OBJECT",
        "properties": {
            "reason": {"type": "STRING"},
            "action": {"type": "STRING"}
        },
        "required": ["reason", "action"]
    }

    try:
        response = client.models.generate_content(
            model=CURRENT_MODEL,
            contents=f"Lojistik risk analizi yap ve JSON döndür: {recovery_prompt}",
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=response_schema
            )
        )
        return response.text
    except Exception as e:
        raise Exception(f"Gemini Recovery Hatası: {str(e)}")

def ask_gemini_summary(data_context: str):
    """Operasyon verilerini yönetici özetine çevirir."""
    prompt = f"Sen LogiWise Operasyon Direktörüsün. Bu verilere göre kısa, 3 maddelik bir yönetici özeti yaz: {data_context}"
    try:
        response = client.models.generate_content(
            model=CURRENT_MODEL, 
            contents=prompt
        )
        return response.text.strip()
    except Exception as e:
        return f"Özet oluşturulamadı: {str(e)}"