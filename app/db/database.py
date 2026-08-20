from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL ="mysql+pymysql://root:123456@localhost:3306/campaign_management_db"