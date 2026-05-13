# LogiWise AI

## Yapay Zeka Destekli Akıllı Operasyon ve Lojistik Yönetim Sistemi

LogiWise AI; KOBİ’ler, kooperatifler ve küçük ölçekli e-ticaret işletmeleri için geliştirilmiş yapay zeka destekli operasyon yönetim platformudur.

Sistem; sipariş takibi, kargo yönetimi, risk analizi, operasyon otomasyonu ve AI destekli karar mekanizmalarını tek platform altında birleştirir.

---

# Problem Tanımı

KOBİ’ler ve kooperatifler günlük operasyonlarını çoğunlukla:

* Excel tabloları
* Manuel takip süreçleri
* Telefon ve WhatsApp mesajları
* Dağınık sipariş sistemleri

üzerinden yönetmektedir.

Bu durum:

* Operasyonel verimsizlik
  ❌ İnsan kaynaklı hata
  ❌ Kargo gecikmeleri
  ❌ Müşteri memnuniyetsizliği
  ❌ Ölçeklenme problemleri

oluşturmaktadır.

LogiWise AI bu problemleri yapay zeka destekli otomasyon sistemleriyle çözmeyi hedefler.

---

# Çözümümüz

LogiWise AI klasik operasyon panellerinden farklı olarak yalnızca veri göstermez.

Sistem:

* Riskleri analiz eder
  ✅ Gecikmeleri tahmin eder
  ✅ AI destekli aksiyon önerileri üretir
  ✅ Operasyonel süreçleri otomatikleştirir
  ✅ Gerçek zamanlı operasyon yönetimi sağlar

---

# Temel Özellikler

## Sipariş Yönetimi

* Sipariş listeleme
* Sipariş durumu takibi
* Gerçek zamanlı operasyon görünürlüğü

## Kargo Süreç Yönetimi

* Teslimat durumu takibi
* Gecikme tespiti
* Risk analizi
* Proaktif bildirim sistemi

## AI Risk Analysis Engine

Sistem aşağıdaki verilere göre risk puanı üretir:

* Sipariş durumu
* Gecikme süresi
* Sipariş tutarı
* Operasyon yoğunluğu

## AI Recovery Agent

Gemini AI destekli sistem:

* Problemleri analiz eder
* Operasyonel çözüm önerileri üretir
* Öncelik seviyeleri belirler
* Yöneticiye aksiyon önerir

## AI Summary System

Yapay zeka destekli operasyon özeti:

* Günlük operasyon analizi
* Kritik siparişler
* Gecikmeli kargolar
* Operasyonel içgörü üretimi

---

# Sistem Mimarisi

```text
Frontend (Next.js)
        ↓
FastAPI Backend
        ↓
SQLite Database
        ↓
AI Services (Gemini API)
        ↓
Risk Analysis Engine
        ↓
Notification System
```

---

# Kullanılan Teknolojiler

## Backend

* Python
* FastAPI
* SQLModel
* SQLite

## Frontend

* Next.js
* React
* TypeScript

## AI & Automation

* Gemini API
* AI Risk Engine
* AI Recovery Agent
* NLP Summary System

---

# Proje Yapısı

```bash
LogiWise_Project/
│
├── backend/
│   ├── main.py
│   ├── ai_service.py
│   ├── database.py
│   ├── models.py
│   ├── notification.py
│   ├── notification_service.py
│   ├── seed.py
│   └── requirements.txt
│
├── frontend/
│   ├── app/
│   ├── public/
│   ├── package.json
│   └── next.config.ts
│
└── README.md
```

---

# Kurulum

## 1. Repository Clone

```bash
git clone <repo-url>
cd LogiWise_Project
```

---

## 2. Backend Kurulumu

```bash
cd backend
pip install -r requirements.txt
```

### Backend Çalıştırma

```bash
uvicorn main:app --reload
```

Backend:

```text
http://127.0.0.1:8000
```

Swagger Docs:

```text
http://127.0.0.1:8000/docs
```

---

## 3. Frontend Kurulumu

```bash
cd frontend
npm install
npm run dev
```

Frontend:

```text
http://localhost:3000
```

---

# Yapay Zeka Kullanımı

LogiWise AI içerisinde yapay zeka:

* Risk tahmini
* Operasyon analizi
* Otomatik aksiyon üretimi
* NLP tabanlı özetleme
* Karar destek sistemi

amaçlarıyla kullanılmaktadır.

Bu yapı klasik CRUD sistemlerinden farklı olarak:

* Aksiyon alabilen
* Proaktif çalışan
* Operasyon yöneten
* Karar destek sağlayan

bir AI operasyon asistanı oluşturur.

---

# Neden LogiWise AI?

| Klasik Sistemler      | LogiWise AI                 |
| --------------------- | --------------------------- |
| Manuel veri girişi    | AI destekli otomasyon       |
| Reaktif yaklaşım      | Proaktif risk analizi       |
| Sınırlı raporlama     | Akıllı operasyon içgörüleri |
| İnsan hatalarına açık | Otomatik karar desteği      |
| Gecikmeli müdahale    | Gerçek zamanlı analiz       |

---

# Demo Senaryosu

### Örnek Akış

1. Yeni sipariş oluşur
2. Kargo süreci başlar
3. Sistem gecikme riskini tespit eder
4. Risk Engine HIGH risk üretir
5. Gemini AI aksiyon önerisi oluşturur
6. Yönetici dashboard üzerinden bilgilendirilir

---

# Gelecek Planları

* WhatsApp entegrasyonu
* Gerçek kargo API entegrasyonu
* AI stok tahmin sistemi
* Mobil uygulama
* Çok kullanıcılı yönetim paneli
* Gelişmiş analitik ekranları

---

# Literatür ve İlham Kaynakları

* AI-powered logistics systems
* Predictive logistics
* Smart operations management
* Agent-based AI systems
* NLP-based customer support systems

---

# Hackathon Uyum Noktaları

✅ Yapay zeka kullanımı
✅ Agent-based yaklaşım
✅ Veri ile etkileşim
✅ Operasyon otomasyonu
✅ AI destekli aksiyon sistemi
✅ Gerçek kullanım senaryosu
✅ Modern kullanıcı deneyimi

---

# Takım

Hayrunnisa Kartal
Tahsin Yazıcı

---

# Final Mesajı

> “Biz yalnızca veri gösteren bir panel değil, aksiyon alabilen yapay zeka destekli operasyon sistemi geliştiriyoruz.”

---

# LogiWise AI

### AI-Powered Smart Operations for SMEs
