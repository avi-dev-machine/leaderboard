from app.database import SessionLocal
from app import models

def remove_old_teams():
    db = SessionLocal()
    teams_to_remove = ["Space Voyagers", "Cyber Phantoms", "Team Mavericks", "Team Maverick", "Space Voyager", "Cyber Phantom"]
    
    for team_name in teams_to_remove:
        team = db.query(models.Team).filter(models.Team.team_name == team_name).first()
        if team:
            print(f"Removing scores for {team_name}...")
            db.query(models.Score).filter(models.Score.team_id == team.id).delete()
            
            print(f"Removing team {team_name}...")
            db.delete(team)
            
    db.commit()
    db.close()
    print("Done removing old teams.")

if __name__ == "__main__":
    remove_old_teams()
