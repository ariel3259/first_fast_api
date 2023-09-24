from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

def get_db():
    engine = create_engine("mssql+pyodbc://sa:12345678@localhost:1433/f_db?driver=SQL+Server+Native+Client+11.0")
    SessionMaker = sessionmaker(autoflush=False, autocommit=False, bind=engine)
    session: Session = SessionMaker()
    try:
        yield session
    finally:
        session.close()