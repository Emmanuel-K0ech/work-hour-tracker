from fastapi import FastAPI, HTTPException
from datetime import datetime
from .database import engine, SessionLocal
from .models import Base, Shift, Role
from fastapi import Query
from datetime import datetime, timedelta
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

Base.metadata.create_all(bind=engine)

app = FastAPI()

# Pydantic models for request bodies
class RoleCreate(BaseModel):
    name: str
    hourly_rate: float

class ClockInRequest(BaseModel):
    role_id: int
    location: str

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
def clock_in(request: ClockInRequest):
    db = next(get_db())

    active_shift = get_active_shift(db)
    if active_shift:
        raise HTTPException(status_code=400, detail="Already clocked in")

    # Verify role exists
    role = db.query(Role).filter(Role.id == request.role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")

    new_shift = Shift(clock_in=datetime.now(), role_id=request.role_id, location=request.location)
    db.add(new_shift)
    db.commit()
    db.refresh(new_shift)

    return {"message": "Clocked in", "time": new_shift.clock_in, "role": role.name, "location": request.location}

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

    # Calculate pay if role is assigned
    if shift.role_id:
        role = db.query(Role).filter(Role.id == shift.role_id).first()
        if role:
            shift.pay = round(shift.hours_worked * role.hourly_rate, 2)

    db.commit()

    return {
        "message": "Clocked out",
        "hours_worked": shift.hours_worked,
        "pay": shift.pay
    }

# Get Shift History Endpoint
@app.get("/shifts")
def get_shifts(start: str = None, end: str = None, role_id: int = None):

    db = next(get_db())

    query = db.query(Shift)

    if start:
        start_date = datetime.strptime(start, "%Y-%m-%d")
        query = query.filter(Shift.clock_in >= start_date)

    if end:
        end_date = datetime.strptime(end, "%Y-%m-%d") + timedelta(days=1)
        query = query.filter(Shift.clock_in < end_date)

    if role_id:
        query = query.filter(Shift.role_id == role_id)

    shifts = query.all()

    total_hours = sum(shift.hours_worked or 0 for shift in shifts)
    total_pay = sum(shift.pay or 0 for shift in shifts)

    results = []

    for shift in shifts:
        role_name = shift.role_obj.name if shift.role_obj else "Unknown"
        results.append({
            "id": shift.id,
            "clock_in": shift.clock_in,
            "clock_out": shift.clock_out,
            "hours_worked": shift.hours_worked,
            "location": shift.location,
            "role": role_name,
            "pay": shift.pay
        })

    return {
        "total_hours": round(total_hours, 2),
        "total_pay": round(total_pay, 2),
        "shifts": results
    }

# Get Active Shift Endpoint
@app.get("/active-shift")
def active_shift():
    db = next(get_db())

    shift = db.query(Shift).filter(Shift.clock_out == None).first()

    if not shift:
        return {"active": False}

    role_name = shift.role_obj.name if shift.role_obj else "Unknown"
    return {
        "active": True,
        "clock_in": shift.clock_in,
        "role": role_name,
        "location": shift.location
    }

# Create Role Endpoint
@app.post("/roles")
def create_role(role: RoleCreate):
    db = next(get_db())

    existing_role = db.query(Role).filter(Role.name == role.name).first()
    if existing_role:
        raise HTTPException(status_code=400, detail="Role already exists")

    new_role = Role(name=role.name, hourly_rate=role.hourly_rate)
    db.add(new_role)
    db.commit()
    db.refresh(new_role)

    return {"id": new_role.id, "name": new_role.name, "hourly_rate": new_role.hourly_rate}

# Get All Roles Endpoint
@app.get("/roles")
def get_roles():
    db = next(get_db())
    roles = db.query(Role).all()
    return [{"id": r.id, "name": r.name, "hourly_rate": r.hourly_rate} for r in roles]

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

# Pay Breakdown Endpoint
@app.get("/pay-breakdown")
def pay_breakdown(start: str = None, end: str = None):
    db = next(get_db())

    query = db.query(Shift)

    if start:
        start_date = datetime.strptime(start, "%Y-%m-%d")
        query = query.filter(Shift.clock_in >= start_date)

    if end:
        end_date = datetime.strptime(end, "%Y-%m-%d") + timedelta(days=1)
        query = query.filter(Shift.clock_in < end_date)

    shifts = query.all()

    # Group by role
    role_breakdown = {}
    for shift in shifts:
        if shift.role_obj:
            role_name = shift.role_obj.name
            if role_name not in role_breakdown:
                role_breakdown[role_name] = {"hours": 0, "pay": 0}
            role_breakdown[role_name]["hours"] += shift.hours_worked or 0
            role_breakdown[role_name]["pay"] += shift.pay or 0

    total_pay = sum(sum(data["pay"] for data in role_breakdown.values()) for _ in [1])

    result = []
    for role_name, data in role_breakdown.items():
        result.append({
            "role": role_name,
            "hours": round(data["hours"], 2),
            "pay": round(data["pay"], 2)
        })

    return {
        "breakdown": result,
        "total_pay": round(total_pay, 2)
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
