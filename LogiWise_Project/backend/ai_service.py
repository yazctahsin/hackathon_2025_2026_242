from google import genai
from google.genai import types
import os
from dotenv import load_dotenv
import json

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

CURRENT_MODEL = "gemini-2.5-flash-lite"


# ---------------- SQL ----------------

def ask_gemini_summary(context: str):

    prompt = f"""
    Sen LogiWise Risk Detection Agent birimisin. 
    Sen LogiWise Risk Detection Agent birimisin.

    Tablolar:
    - Product (id, name, price, stock)
    - Order (id, customer_name, order_date, status, total_amount, product_name, quantity)
    - Shipment (id, order_id, tracking_code, eta_date, current_location)

    GÖREVİN:
    1. Kullanıcı talebine göre sadece saf SQLite kodu üret. 
    2. Bugünün tarihi: 2026-05-09.
    3. Markdown kullanma, açıklama yapma. Tablo adlarını "Order" şeklinde tırnaklı yaz. 
    Görev:
    - Sadece SQLite query üret
    - Açıklama yazma
    - Markdown kullanma

"""

    try:
        response = client.models.generate_content(
            model=CURRENT_MODEL,
            contents=prompt
        )

        return response.text.strip()

    except Exception as e:
        return f"SUMMARY_ERROR: {str(e)}"
# ---------------- RECOVERY ----------------

def ask_gemini_recovery(prompt: str):

    schema = {
        "type": "OBJECT",
        "properties": {
            "reason": {"type": "STRING"},
            "actions": {
                "type": "ARRAY",
                "items": {"type": "STRING"}
            },
            "priority": {"type": "STRING"}
        },
        "required": ["reason", "actions", "priority"]
    }

    try:
        response = client.models.generate_content(
            model=CURRENT_MODEL,
            contents=f"""
Sen lojistik AI karar motorusun.

Görev:
- Problemi analiz et
- 3-5 aksiyon üret
- JSON döndür

{prompt}
""",
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=schema
            )
        )

        return response.text

    except Exception as e:
        return json.dumps({
            "reason": "AI error",
            "actions": ["manual review required"],
            "priority": "HIGH"
        })


# ---------------- SUMMARY ----------------

def ask_gemini_summary(context: str):

    prompt = f"""
Sen LogiWise Operasyon Direktörüsün.

Bu veriyi analiz et ve 3 maddelik kısa yönetici özeti yaz:

{context}
"""

    try:
        response = client.models.generate_content(
            model=CURRENT_MODEL,
            contents=prompt
        )

        return response.text.strip()

    except Exception as e:
        return f"SUMMARY_ERROR: {str(e)}"