from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class TeamBase(BaseModel):
    team_name: str
    team_lead: str

class TeamCreate(TeamBase):
    pass

class Team(TeamBase):
    id: int
    created_at: datetime
    class Config:
        from_attributes = True

class ScoreBase(BaseModel):
    team_id: int
    round_id: int
    criteria_id: int
    score: float

class ScoreCreate(ScoreBase):
    pass

class Score(ScoreBase):
    id: int
    class Config:
        from_attributes = True

class LeaderboardEntry(BaseModel):
    rank: int
    team_id: int
    team_name: str
    team_lead: str
    total_score: float
    rank_change: Optional[int] = None

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class UserLogin(BaseModel):
    username: str
    password: str
