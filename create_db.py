from sqlalchemy import create_engine
from models import Base

# Database connection string
DATABASE_URL = "sqlite:///app.db"

def create_database():
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(engine)
    print("Database and tables created successfully.")

if __name__ == "__main__":
    create_database()
