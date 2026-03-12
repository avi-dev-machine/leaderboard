import pandas as pd
from sqlalchemy.orm import Session
from .. import models
import io

def generate_excel_report(db: Session):
    teams = db.query(models.Team).all()
    rounds = db.query(models.Round).order_by(models.Round.round_number).all()
    
    data = []
    for team in teams:
        row = {"Team Name": team.team_name, "Team Lead": team.team_lead}
        grand_total = 0
        for r in rounds:
            round_total = db.query(models.func.sum(models.Score.score)).filter(
                models.Score.team_id == team.id,
                models.Score.round_id == r.id
            ).scalar() or 0
            row[f"{r.name} Total"] = round_total
            grand_total += round_total
        row["Grand Total"] = grand_total
        data.append(row)
    
    df = pd.DataFrame(data)
    
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Leaderboard')
    
    output.seek(0)
    return output
