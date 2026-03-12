from app.database import SessionLocal
from app import models

def update_round_3_criteria():
    db = SessionLocal()
    
    round3 = db.query(models.Round).filter(models.Round.round_number == 3).first()
    if not round3:
        print("Round 3 not found!")
        return
        
    criteria = db.query(models.Criteria).filter(models.Criteria.round_id == round3.id).all()
    
    # Needs to be slightly different to avoid uniqueness constraint issues if any
    dash_names = ["—", "— ", "—  ", "—   "]
    
    for i, c in enumerate(criteria):
        if i < len(dash_names):
            c.name = dash_names[i]
            c.max_score = 10
            
    db.commit()
    db.close()
    print("Round 3 Criteria updated to dashes successfully.")

if __name__ == "__main__":
    update_round_3_criteria()
