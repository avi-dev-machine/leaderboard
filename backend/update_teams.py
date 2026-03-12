import json
import os
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import models

def update_teams():
    # Load team.json
    team_json_path = os.path.join(os.path.dirname(__file__), '..', 'team.json')
    with open(team_json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    db = SessionLocal()
    teams_data = data.get("teams", [])
    
    for t_data in teams_data:
        team_name = t_data.get("team_name")
        leader = t_data.get("leader")
        
        # Check if team already exists
        existing_team = db.query(models.Team).filter(models.Team.team_name == team_name).first()
        if existing_team:
            existing_team.team_lead = leader
            print(f"Updated team: {team_name} with leader {leader}")
        else:
            new_team = models.Team(team_name=team_name, team_lead=leader)
            db.add(new_team)
            print(f"Added team: {team_name} with leader {leader}")
    
    db.commit()
    db.close()
    print("Database update complete.")

if __name__ == "__main__":
    update_teams()
