from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from .. import models, schemas, database

router = APIRouter(prefix="/leaderboard", tags=["leaderboard"])

@router.get("/", response_model=List[schemas.LeaderboardEntry])
def get_leaderboard(db: Session = Depends(database.get_db)):
    # Calculate total scores for all teams
    results = db.query(
        models.Team.id,
        models.Team.team_name,
        models.Team.team_lead,
        func.sum(models.Score.score).label("total_score")
    ).outerjoin(models.Score).group_by(models.Team.id).order_by(func.sum(models.Score.score).desc()).all()
    
    # Find the maximum round number that has scores
    max_round = db.query(func.max(models.Round.round_number)).join(models.Score, models.Score.round_id == models.Round.id).scalar()
    
    prev_ranks = {}
    if max_round and max_round > 1:
        # Calculate scores up to max_round - 1
        prev_scores = db.query(
            models.Score.team_id,
            func.sum(models.Score.score).label("score")
        ).join(models.Round).filter(
            models.Round.round_number < max_round
        ).group_by(models.Score.team_id).subquery()

        prev_results = db.query(
            models.Team.id,
            func.coalesce(prev_scores.c.score, 0).label("prev_score")
        ).outerjoin(prev_scores, models.Team.id == prev_scores.c.team_id).order_by(
            func.coalesce(prev_scores.c.score, 0).desc()
        ).all()
        
        for i, res in enumerate(prev_results):
            prev_ranks[res.id] = i + 1

    leaderboard = []
    for i, res in enumerate(results):
        current_rank = i + 1
        
        if max_round and max_round > 1 and res.id in prev_ranks:
            prev_rank = prev_ranks[res.id]
            rank_change = prev_rank - current_rank
        else:
            rank_change = None
            
        leaderboard.append(schemas.LeaderboardEntry(
            rank=current_rank,
            team_id=res.id,
            team_name=res.team_name,
            team_lead=res.team_lead,
            total_score=res.total_score if res.total_score else 0.0,
            rank_change=rank_change
        ))
    return leaderboard
