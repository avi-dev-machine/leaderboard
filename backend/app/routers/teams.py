from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from .. import models, schemas, database

router = APIRouter(prefix="/teams", tags=["teams"])

@router.get("/{team_id}")
def get_team_details(team_id: int, db: Session = Depends(database.get_db)):
    team = db.query(models.Team).filter(models.Team.id == team_id).first()
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    
    rounds = db.query(models.Round).all()
    
    response_data = {
        "team_name": team.team_name,
        "team_lead": team.team_lead,
        "rounds": []
    }
    
    for r in rounds:
        round_data = {
            "round_number": r.round_number,
            "name": r.name,
            "criteria": []
        }
        criteria = db.query(models.Criteria).filter(models.Criteria.round_id == r.id).all()
        for c in criteria:
            score = db.query(models.Score).filter(
                models.Score.team_id == team_id,
                models.Score.criteria_id == c.id
            ).first()
            round_data["criteria"].append({
                "id": c.id,
                "name": c.name,
                "score": score.score if score else 0,
                "max_score": c.max_score
            })
        response_data["rounds"].append(round_data)
        
    return response_data

@router.get("/search", response_model=List[schemas.Team])
def search_teams(q: str = Query(...), db: Session = Depends(database.get_db)):
    teams = db.query(models.Team).filter(models.Team.team_name.ilike(f"%{q}%")).all()
    return teams
