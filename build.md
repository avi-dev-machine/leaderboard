Autonomous Build Prompt — Hack Among Us Live Leaderboard

You are an expert full-stack software engineer tasked with building a complete production-ready web application.

The application is a live leaderboard system for a hackathon.

You must build the entire project from scratch including:

Backend

Frontend

Database models

APIs

Admin panel

UI theme

Deployment-ready structure

Follow the instructions exactly and step-by-step.

1. Project Name

Hack Among Us – Live Hackathon Leaderboard

2. Event Details

Hackathon Name
Hack Among Us

Venue
Heritage Institute of Technology

Date
13th – 14th March

3. Core Purpose

Create a live leaderboard platform where participants can:

View the current rankings

Search for teams

Click on a team to see detailed score breakdown

Admins should be able to:

Add teams

Remove teams

Enter judging scores

View analytics

Export Excel sheets

4. Tech Stack

Backend

Python
FastAPI
SQLAlchemy
PostgreSQL
JWT Authentication
Pydantic

Frontend

Next.js 14 (App Router)
TypeScript
TailwindCSS
ShadCN UI
Axios
Recharts

Other

Pandas
XLSX Export
Docker-ready
5. Project Structure

You must generate this exact structure.

Root
hack-among-us-leaderboard/
Backend
backend/

app/

main.py
database.py
models.py
schemas.py
auth.py
config.py

routers/
leaderboard.py
teams.py
scores.py
admin.py

services/
leaderboard_service.py
excel_service.py

requirements.txt
Frontend
frontend/

app/
page.tsx

leaderboard/
page.tsx

team/[id]/
page.tsx

admin/login/
page.tsx

admin/dashboard/
page.tsx

admin/teams/
page.tsx

admin/scores/
page.tsx

components/
LeaderboardTable.tsx
SearchBar.tsx
TeamDetails.tsx
AdminSidebar.tsx
ScoreEntryForm.tsx
ScoreGraph.tsx

lib/
api.ts
6. Database Design

Create SQLAlchemy models.

Teams Table

Fields

id (primary key)
team_name
team_lead
created_at
Rounds Table
id
round_number
name

There must be 4 rounds

Round 1
Round 2
Round 3
Round 4
Criteria Table

Each round has multiple criteria.

id
round_id
name
max_score

Example

Round 1 criteria

Innovation
Technical Feasibility
Problem Relevance
Presentation
Scores Table
id
team_id
round_id
criteria_id
score
7. Leaderboard Logic

Total score for a team

SUM(all scores across all rounds and criteria)

Ranking

ORDER BY total_score DESC
8. Backend APIs

Base path

/api
Public APIs
Get Leaderboard
GET /leaderboard

Return

rank
team_name
team_lead
total_score
Get Team Details
GET /teams/{team_id}

Return

team_name
team_lead
rounds
criteria
scores
Search Teams
GET /teams/search?q=
Admin APIs

Require JWT authentication

Admin Login
POST /admin/login

Body

username
password

Return

JWT Token
Add Team
POST /admin/team

Body

team_name
team_lead
Delete Team
DELETE /admin/team/{id}
Add Score
POST /admin/score

Body

team_id
round_id
criteria_id
score
Update Score
PUT /admin/score/{id}
Export Excel
GET /admin/export

Return

Excel sheet

Columns

Team Name
Round 1 Total
Round 2 Total
Round 3 Total
Round 4 Total
Grand Total

Use

pandas
xlsxwriter
9. Frontend Pages
Homepage (Leaderboard)

Route

/

Layout

Header
Search Bar
Leaderboard Table

Header text

Hack Among Us
Heritage Institute of Technology
13–14 March
Leaderboard Table

Columns

Rank
Team Name
Team Lead
Total Score

Clicking team name → open team details page

Team Details Page

Route

/team/[id]

Display

TEAM MAVERICKS
Lead : Alex Thompson

ROUND 1
Innovation : 8
Technical : 7
Problem Relevance : 9
Presentation : 8

ROUND 2
...

ROUND 3
...

ROUND 4
...
Admin Login

Route

/admin/login

Fields

username
password
login button
Admin Dashboard

Sidebar

Dashboard
Teams
Scores
Graphs
Export Excel
Manage Teams Page

Admins can

Add team
Delete team
View teams
Score Entry Page

Form

Select Team
Select Round
Select Criteria
Enter Score
Submit
Analytics Page

Graphs

Team vs Total Score
Round wise score comparison
Score distribution

Use

Recharts
10. Search Functionality

Search bar filters teams by:

team_name
11. Live Leaderboard Updates

Use polling every 10 seconds

API

/leaderboard
12. UI / UX Design Theme

The entire website must follow an Among Us inspired theme.

Design inspiration

spaceship dashboard
dark space background
neon UI panels
rounded boxes
Colors
Dark Space (#0B0F19)
Neon Cyan
Red
Purple
White text
Fonts
Orbitron
Inter
Background

Subtle

stars
space grid
futuristic panels
13. Security

Admin authentication must include:

JWT tokens
bcrypt password hashing
protected admin routes
14. Deployment

Make the project deployment-ready.

Backend

Railway / Render

Frontend

Vercel

Database

Supabase PostgreSQL
15. Expected Final Result

The completed system must support:

✓ Live leaderboard
✓ Search teams
✓ Clickable team details
✓ Admin login panel
✓ Score entry system
✓ Round-wise scoring
✓ Graph analytics
✓ Excel export

16. Important Instructions

While generating code:

Generate fully working code.

Ensure backend and frontend communicate correctly.

Add sample seed data.

Ensure leaderboard updates dynamically.

Write clean, modular code.

Final Instruction

Build the entire system end-to-end and output the complete project structure with all files and code.