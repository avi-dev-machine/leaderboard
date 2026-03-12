from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from .routers import leaderboard, teams, admin
from . import models, auth
from .database import SessionLocal

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Hack Among Us Leaderboard API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, replace with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(leaderboard.router, prefix="/api")
app.include_router(teams.router, prefix="/api")
app.include_router(admin.router, prefix="/api")

@app.on_event("startup")
def startup_populate():
    db = SessionLocal()
    try:
        # Remove default admin if it exists
        old_admin = db.query(models.User).filter(models.User.username == "admin").first()
        if old_admin:
            db.delete(old_admin)
            db.commit()

        # Check if admin users exist
        admin_users = [
            {"username": "mohitjena@dakshh", "password": "jenamohit"},
            {"username": "sayakghosh@dakshh", "password": "ghoshsayak"}
        ]
        
        for u in admin_users:
            existing_user = db.query(models.User).filter(models.User.username == u["username"]).first()
            if not existing_user:
                hashed_pwd = auth.get_password_hash(u["password"])
                db.add(models.User(username=u["username"], hashed_password=hashed_pwd))
        
        db.commit()
        # Check if rounds exist
        if db.query(models.Round).count() == 0:
            rounds_data = [
                {"number": 1, "name": "Round 1"},
                {"number": 2, "name": "Round 2"},
                {"number": 3, "name": "Round 3"},
                {"number": 4, "name": "FINAL PITCH (top5)"},
            ]
            for r in rounds_data:
                db_round = models.Round(round_number=r["number"], name=r["name"])
                db.add(db_round)
                db.commit()
                db.refresh(db_round)
                
                # Add criteria for each round
                if r["number"] == 1:
                    criteria_data = [
                        {"name": "Problem Relevance", "max": 8},
                        {"name": "Idea Innovation", "max": 10},
                        {"name": "Tech Feasibility", "max": 8},
                        {"name": "System Architecture", "max": 8},
                        {"name": "Early Progress", "max": 6}
                    ]
                    for c_data in criteria_data:
                        db.add(models.Criteria(round_id=db_round.id, name=c_data["name"], max_score=c_data["max"]))
                elif r["number"] == 2:
                    criteria_data = [
                        {"name": "Prototype Progress", "max": 15},
                        {"name": "Technical Depth", "max": 12},
                        {"name": "Practical Impact", "max": 10},
                        {"name": "UX Design", "max": 8},
                        {"name": "Tech Demo", "max": 5},
                        {"name": "Mentor Feedback", "max": 10}
                    ]
                    for c_data in criteria_data:
                        db.add(models.Criteria(round_id=db_round.id, name=c_data["name"], max_score=c_data["max"]))
                elif r["number"] in [3, 4]:
                    criteria_data = [
                        {"name": "—", "max": 10},
                        {"name": "— ", "max": 10},
                        {"name": "—  ", "max": 10},
                        {"name": "—   ", "max": 10}
                    ]
                    for c_data in criteria_data:
                        db.add(models.Criteria(round_id=db_round.id, name=c_data["name"], max_score=c_data["max"]))
                else:
                    # Placeholders for future rounds
                    pass
            db.commit()
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "Hack Among Us Leaderboard API is running"}
