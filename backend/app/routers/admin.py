from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas, database, auth

router = APIRouter(prefix="/admin", tags=["admin"])

@router.post("/login", response_model=schemas.Token)
def login(user_credentials: schemas.UserLogin, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.username == user_credentials.username).first()
    if not user or not auth.verify_password(user_credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = auth.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/verify")
def verify_token(current_user: models.User = Depends(auth.get_current_user)):
    return {"status": "ok", "user": current_user.username}

@router.post("/team", response_model=schemas.Team)
def add_team(team: schemas.TeamCreate, db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    db_team = models.Team(**team.dict())
    db.add(db_team)
    db.commit()
    db.refresh(db_team)
    return db_team

@router.delete("/team/{id}")
def delete_team(id: int, db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    db_team = db.query(models.Team).filter(models.Team.id == id).first()
    if not db_team:
        raise HTTPException(status_code=404, detail="Team not found")
    db.delete(db_team)
    db.commit()
    return {"message": "Team deleted"}

@router.post("/score")
def add_score(score: schemas.ScoreCreate, db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    # Calculate current ranks before update
    previous_ranks = get_current_ranks(db)
    
    # Check if score exists, if so update, else create
    db_score = db.query(models.Score).filter(
        models.Score.team_id == score.team_id,
        models.Score.criteria_id == score.criteria_id
    ).first()
    
    if db_score:
        db_score.score = score.score
    else:
        db_score = models.Score(**score.dict())
        db.add(db_score)
        
    db.commit()
    
    # Calculate new ranks after update
    new_ranks = get_current_ranks(db)
    
    # Save history for teams that changed rank or score
    for t_id, t_data in new_ranks.items():
        prev_data = previous_ranks.get(t_id, {"rank": -1, "score": 0})
        # If score or rank changed, record history
        if prev_data["rank"] != t_data["rank"] or prev_data["score"] != t_data["score"]:
            history = models.ScoreHistory(
                team_id=t_id,
                total_score=t_data["score"],
                rank=t_data["rank"]
            )
            db.add(history)
            
    db.commit()
    return {"message": "Score added successfully"}

def get_current_ranks(db: Session):
    from sqlalchemy import func
    results = db.query(
        models.Team.id,
        func.sum(models.Score.score).label("total_score")
    ).outerjoin(models.Score).group_by(models.Team.id).order_by(func.sum(models.Score.score).desc()).all()
    
    ranks = {}
    for i, res in enumerate(results):
        score = res.total_score if res.total_score else 0.0
        ranks[res.id] = {"rank": i + 1, "score": score}
    return ranks
    
from fastapi.responses import StreamingResponse
from ..services import excel_service

@router.get("/export")
def export_excel(db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    file_data = excel_service.generate_excel_report(db)
    return StreamingResponse(
        file_data,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=leaderboard.xlsx"}
    )
