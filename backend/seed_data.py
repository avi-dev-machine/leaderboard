from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app import models

def seed_teams():
    db = SessionLocal()
    try:
        # Check if teams exist
        if db.query(models.Team).count() == 0:
            teams = [
                {"name": "Team Mavericks", "lead": "Alex Thompson"},
                {"name": "Cyber Phantoms", "lead": "Sarah Chen"},
                {"name": "Space Voyagers", "lead": "John Doe"},
            ]
            for t_data in teams:
                team = models.Team(team_name=t_data["name"], team_lead=t_data["lead"])
                db.add(team)
                db.commit()
                db.refresh(team)
                
                # Add some scores for Round 1
                round1 = db.query(models.Round).filter(models.Round.round_number == 1).first()
                if round1:
                    criteria = db.query(models.Criteria).filter(models.Criteria.round_id == round1.id).all()
                    import random
                    for c in criteria:
                        score = models.Score(
                            team_id=team.id,
                            round_id=round1.id,
                            criteria_id=c.id,
                            score=random.uniform(5, 10)
                        )
                        db.add(score)
            db.commit()
            print("Seeded teams and sample scores.")
    finally:
        db.close()

if __name__ == "__main__":
    seed_teams()
