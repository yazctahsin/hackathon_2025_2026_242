from sqlmodel import create_engine, Session, SQLModel

# SQLite veritabanı dosyasının yolu ve adı
sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

# Veritabanı motorunu (engine) oluşturuyoruz
engine = create_engine(sqlite_url, echo=True)

# Bu fonksiyon çalıştırıldığında modellerimizdeki tablolar SQL'e dönüşür
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# Veritabanı ile konuşmak için her seferinde bir "oturum" açmamızı sağlar
def get_session():
    with Session(engine) as session:
        yield session