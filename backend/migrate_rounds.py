from app.database import SessionLocal
from app import models

def update_rounds():
    db = SessionLocal()
    
    round4 = db.query(models.Round).filter(models.Round.round_number == 4).first()
    if round4:
        round4.name = "FINAL PITCH (top5)"
        
    db.commit()
    db.close()
    print("Round 4 renamed successfully.")

if __name__ == "__main__":
    update_rounds()
