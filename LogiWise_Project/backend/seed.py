from sqlmodel import Session
from database import engine
from models import Order, Product, Shipment
from datetime import datetime, timedelta

def seed_data():

    with Session(engine) as session:

        # ---------------- ÜRÜNLER ----------------

        products = [
            Product(
                name="Zeytinyağı",
                price=1250.0,
                stock=50
            ),

            Product(
                name="Bal",
                price=3500.0,
                stock=20
            ),

            Product(
                name="Salça",
                price=2100.0,
                stock=15
            ),

            Product(
                name="Yumurta",
                price=18500.0,
                stock=5
            ),

            Product(
                name="Kuru Domates",
                price=9200.0,
                stock=8
            )
        ]

        session.add_all(products)
        session.commit()

        # ---------------- SİPARİŞLER ----------------

        orders = [

            # HIGH RISK
            Order(
                customer_name="Ahmet Kılsa",
                total_amount=7200.0,
                status="Kargoda"
            ),

            # MEDIUM RISK
            Order(
                customer_name="Ayşe Demir",
                total_amount=3200.0,
                status="Hazırlanıyor"
            ),

            # LOW RISK
            Order(
                customer_name="Melis Ak",
                total_amount=900.0,
                status="Teslim Edildi"
            ),

            # HIGH RISK
            Order(
                customer_name="Caner Öz",
                total_amount=12000.0,
                status="Kargoda"
            ),

            # LOW RISK
            Order(
                customer_name="Zeynep Kara",
                total_amount=1500.0,
                status="Sipariş Alındı"
            ),

            # MEDIUM
            Order(
                customer_name="Burak Yıldız",
                total_amount=2800.0,
                status="Hazırlanıyor"
            )
        ]

        session.add_all(orders)
        session.commit()

        # ---------------- SHIPMENTS ----------------

        shipments = [

            # HIGH RISK -> 5 gün gecikmiş
            Shipment(
                order_id=orders[0].id,
                tracking_code="LOGI-HIGH-001",
                eta_date=datetime.now() - timedelta(days=5),
                current_location="Ankara Transfer Merkezi"
            ),

            # MEDIUM -> 1 gün gecikmiş
            Shipment(
                order_id=orders[1].id,
                tracking_code="LOGI-MED-001",
                eta_date=datetime.now() - timedelta(days=1),
                current_location="İstanbul Depo"
            ),

            # LOW -> teslim edildi
            Shipment(
                order_id=orders[2].id,
                tracking_code="LOGI-LOW-001",
                eta_date=datetime.now() - timedelta(days=2),
                current_location="Teslim Edildi"
            ),

            # HIGH -> büyük tutarlı + çok gecikmiş
            Shipment(
                order_id=orders[3].id,
                tracking_code="LOGI-HIGH-002",
                eta_date=datetime.now() - timedelta(days=6),
                current_location="İzmir Aktarma"
            ),


            # LOW -> henüz yeni
            Shipment(
                order_id=orders[4].id,
                tracking_code="LOGI-LOW-002",
                eta_date=datetime.now() + timedelta(days=3),
                current_location="Hazırlık Merkezi"
            ),

            # MEDIUM
            Shipment(
                order_id=orders[5].id,
                tracking_code="LOGI-MED-002",
                eta_date=datetime.now(),
                current_location="Kargo Çıkış Noktası"
            )
        ]

        session.add_all(shipments)
        session.commit()

        print("Profesyonel demo verileri başarıyla yüklendi!")


if __name__ == "__main__":
    seed_data()