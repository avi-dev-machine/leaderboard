import json
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import models

def check_db():
    db = SessionLocal()
    teams = db.query(models.Team).all()
    for t in teams:
        print(f"ID={t.id}, Name={t.team_name}, Lead={t.team_lead}")
    db.close()

if __name__ == "__main__":
    check_db()
