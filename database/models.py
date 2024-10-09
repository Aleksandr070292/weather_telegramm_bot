from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


DATABASE_URL = "sqlite:///logs.db"
engine = create_engine(DATABASE_URL)
Base = declarative_base()


# Модель для логов
class Log(Base):
    __tablename__ = 'logs'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    command = Column(String)
    timestamp = Column(DateTime)
    response = Column(String)


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
