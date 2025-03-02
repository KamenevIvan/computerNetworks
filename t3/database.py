from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql://parser_user:password@localhost/avito_parser"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Ad(Base):
    __tablename__ = "ads"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    price = Column(String)
    link = Column(String)
    location = Column(String)

Base.metadata.create_all(bind=engine)