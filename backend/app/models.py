from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

class Team(Base):
    __tablename__ = "teams"
    id = Column(Integer, primary_key=True, index=True)
    team_name = Column(String, unique=True, index=True)
    team_lead = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    scores = relationship("Score", back_populates="team")

class Round(Base):
    __tablename__ = "rounds"
    id = Column(Integer, primary_key=True, index=True)
    round_number = Column(Integer, unique=True)
    name = Column(String)
    
    criteria = relationship("Criteria", back_populates="round")
    scores = relationship("Score", back_populates="round")

class Criteria(Base):
    __tablename__ = "criteria"
    id = Column(Integer, primary_key=True, index=True)
    round_id = Column(Integer, ForeignKey("rounds.id"))
    name = Column(String)
    max_score = Column(Integer)
    
    round = relationship("Round", back_populates="criteria")
    scores = relationship("Score", back_populates="criteria")

class Score(Base):
    __tablename__ = "scores"
    id = Column(Integer, primary_key=True, index=True)
    team_id = Column(Integer, ForeignKey("teams.id"))
    round_id = Column(Integer, ForeignKey("rounds.id"))
    criteria_id = Column(Integer, ForeignKey("criteria.id"))
    score = Column(Float)
    
    team = relationship("Team", back_populates="scores")
    round = relationship("Round", back_populates="scores")
    criteria = relationship("Criteria", back_populates="scores")

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)

class ScoreHistory(Base):
    __tablename__ = "score_history"
    id = Column(Integer, primary_key=True, index=True)
    team_id = Column(Integer, ForeignKey("teams.id"))
    total_score = Column(Float)
    rank = Column(Integer)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    
    team = relationship("Team")
