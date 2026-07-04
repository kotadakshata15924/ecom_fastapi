from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# each microservice owns its own database
engine = create_engine("sqlite:///category_service.db")
Session = sessionmaker(bind=engine)
Base = declarative_base()
