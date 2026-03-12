from app.database import SessionLocal
from app import models

def update_round_2_criteria():
    db = SessionLocal()
    
    round2 = db.query(models.Round).filter(models.Round.round_number == 2).first()
    if not round2:
        print("Round 2 not found!")
        return
        
    criteria = db.query(models.Criteria).filter(models.Criteria.round_id == round2.id).all()
    
    for c in criteria:
        if c.name == "Innovation":
            c.name = "Prototype Progress"
            c.max_score = 15
        elif c.name == "Technical Feasibility":
            c.name = "Technical Depth"
            c.max_score = 12
        elif c.name == "Problem Relevance":
            c.name = "Practical Impact"
            c.max_score = 10
        elif c.name == "Presentation":
            c.name = "UX Design"
            c.max_score = 8
            
    # Check if the 5th and 6th criteria already exist
    tech_demo = db.query(models.Criteria).filter(
        models.Criteria.round_id == round2.id, 
        models.Criteria.name == "Tech Demo"
    ).first()
    
    if not tech_demo:
        db.add(models.Criteria(round_id=round2.id, name="Tech Demo", max_score=5))
        
    mentor_feedback = db.query(models.Criteria).filter(
        models.Criteria.round_id == round2.id, 
        models.Criteria.name == "Mentor Feedback"
    ).first()
    
    if not mentor_feedback:
        db.add(models.Criteria(round_id=round2.id, name="Mentor Feedback", max_score=10))
        
    db.commit()
    db.close()
    print("Round 2 Criteria updated successfully.")

if __name__ == "__main__":
    update_round_2_criteria()
