from sqlmodel import Session
from database import engine
from models import Order, Product, Shipment
from datetime import datetime, timedelta

def seed_data():
    with Session(engine) as session:
        # 1. Örnek Ürünler
        p1 = Product(name="Kablosuz Kulaklık", price=1250.0, stock=50)
        p2 = Product(name="Akıllı Saat", price=3500.0, stock=20)
        p3 = Product(name="Mekanik Klavye", price=2100.0, stock=15)
        
        session.add_all([p1, p2, p3])
        
        # 2. Örnek Siparişler
        # Biri teslim edilmiş, biri yolda, biri gecikmiş senaryosu
        o1 = Order(customer_name="Ahmet Yılmaz", total_amount=1250.0, status="Teslim Edildi")
        o2 = Order(customer_name="Ayşe Demir", total_amount=3500.0, status="Kargoda")
        o3 = Order(customer_name="Mehmet Can", total_amount=2100.0, status="Kargoda") # Gecikme adayı
        
        session.add_all([o1, o2, o3])
        session.commit() # ID'lerin oluşması için önce bunları kaydet
        
        # 3. Kargo Bilgileri
        s1 = Shipment(order_id=o2.id, tracking_code="LOGI123", eta_date=datetime.now() + timedelta(days=2), current_location="İstanbul Aktarma")
        # Bu kargonun ETA'sını (tahmini varış) DÜN yapalım ki sistem GECİKMİŞ desin:
        s2 = Shipment(order_id=o3.id, tracking_code="LOGI456", eta_date=datetime.now() - timedelta(days=1), current_location="Ankara Şube")
        
        session.add_all([s1, s2])
        session.commit()
        print("Veriler başarıyla yüklendi!")

if __name__ == "__main__":
    seed_data()