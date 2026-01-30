from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = (
    "mysql+mysqlconnector://"
    "mongouhd_evernorth:U*dgQkKRuEHe"
    "@cp-15.webhostbox.net:3306/"
    "mongouhd_evernorth"
    "?ssl_disabled=true&use_pure=true"
)

engine = create_engine(DATABASE_URL, pool_pre_ping=True)

SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()
