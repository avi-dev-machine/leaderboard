from app.database import SessionLocal
from app import models

def update_round_1_criteria():
    db = SessionLocal()
    
    round1 = db.query(models.Round).filter(models.Round.round_number == 1).first()
    if not round1:
        print("Round 1 not found!")
        return
        
    criteria = db.query(models.Criteria).filter(models.Criteria.round_id == round1.id).all()
    
    # Map old names to new details
    # Old names: "Innovation", "Technical Feasibility", "Problem Relevance", "Presentation"
    for c in criteria:
        if c.name == "Problem Relevance":
            c.max_score = 8
        elif c.name == "Innovation":
            c.name = "Idea Innovation"
            c.max_score = 10
        elif c.name == "Technical Feasibility":
            c.name = "Tech Feasibility"
            c.max_score = 8
        elif c.name == "Presentation":
            c.name = "System Architecture"
            c.max_score = 8
            
    # Check if the 5th criteria already exists
    early_progress = db.query(models.Criteria).filter(
        models.Criteria.round_id == round1.id, 
        models.Criteria.name == "Early Progress"
    ).first()
    
    if not early_progress:
        db.add(models.Criteria(round_id=round1.id, name="Early Progress", max_score=6))
        
    db.commit()
    db.close()
    print("Criteria updated successfully.")

if __name__ == "__main__":
    update_round_1_criteria()
