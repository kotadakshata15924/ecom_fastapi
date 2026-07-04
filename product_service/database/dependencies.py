from database.connection import Session
db =Session()
def get_db():
    try:
        yield db
    finally:
        db.close()
