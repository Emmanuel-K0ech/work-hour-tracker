from fastapi import FastAPI, HTTPException
from datetime import datetime
from database import engine, SessionLocal
from models import Base, Shift
from fastapi import Query
from datetime import datetime, timedelta
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Check active shift
def get_active_shift(db):
    return db.query(Shift).filter(Shift.clock_out == None).first()

@app.get("/")
def home():
    return {"message": "Work Hour Tracker API running"}

# Clock In Endpoint
@app.post("/clock-in")
def clock_in():
    db = next(get_db())

    active_shift = get_active_shift(db)
    if active_shift:
        raise HTTPException(status_code=400, detail="Already clocked in")

    new_shift = Shift(clock_in=datetime.now())
    db.add(new_shift)
    db.commit()
    db.refresh(new_shift)

    return {"message": "Clocked in", "time": new_shift.clock_in}

# Clock Out Endpoint
@app.post("/clock-out")
def clock_out():
    db = next(get_db())

    shift = get_active_shift(db)
    if not shift:
        raise HTTPException(status_code=400, detail="No active shift")

    shift.clock_out = datetime.now()

    duration = shift.clock_out - shift.clock_in
    shift.hours_worked = round(duration.total_seconds() / 3600, 2)

    db.commit()

    return {
        "message": "Clocked out",
        "hours_worked": shift.hours_worked
    }

# Get Shift History Endpoint
@app.get("/shifts")
def get_shifts(start: str = None, end: str = None):

    db = next(get_db())

    query = db.query(Shift)

    if start:
        start_date = datetime.strptime(start, "%Y-%m-%d")
        query = query.filter(Shift.clock_in >= start_date)

    if end:
        end_date = datetime.strptime(end, "%Y-%m-%d") + timedelta(days=1)
        query = query.filter(Shift.clock_in < end_date)

    shifts = query.all()

    total_hours = sum(shift.hours_worked or 0 for shift in shifts)

    results = []

    for shift in shifts:
        results.append({
            "id": shift.id,
            "clock_in": shift.clock_in,
            "clock_out": shift.clock_out,
            "hours_worked": shift.hours_worked
        })

    return {
        "total_hours": round(total_hours, 2),
        "shifts": results
    }

# Get Active Shift Endpoint
@app.get("/active-shift")
def active_shift():
    db = next(get_db())

    shift = db.query(Shift).filter(Shift.clock_out == None).first()

    if not shift:
        return {"active": False}

    return {
        "active": True,
        "clock_in": shift.clock_in
    }

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Today's Shifts Endpoint
@app.get("/today-hours")
def today_hours():

    db = next(get_db())

    today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    tomorrow = today_start + timedelta(days=1)

    shifts = db.query(Shift).filter(
        Shift.clock_in >= today_start,
        Shift.clock_in < tomorrow
    ).all()

    total = sum(shift.hours_worked or 0 for shift in shifts)

    return {
        "today_hours": round(total, 2)
    }

# Weekly Hours Endpoint
@app.get("/weekly-hours")
def weekly_hours():

    db = next(get_db())

    today = datetime.now()
    start_of_week = today - timedelta(days=today.weekday())

    week_data = {}

    for i in range(7):
        day = start_of_week + timedelta(days=i)
        next_day = day + timedelta(days=1)

        shifts = db.query(Shift).filter(
            Shift.clock_in >= day,
            Shift.clock_in < next_day
        ).all()

        total = sum(shift.hours_worked or 0 for shift in shifts)

        week_data[day.strftime("%A")] = round(total, 2)

    return week_data
