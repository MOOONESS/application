from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

import models
import schemas
from database import engine, SessionLocal

# Create tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Database Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Root
@app.get("/")
def root():
    return {"message": "Tourism API is running 🚀"}


# =========================
# USERS
# =========================

@app.post("/register")
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):

    existing_user = (
        db.query(models.User)
        .filter(models.User.username == user.username)
        .first()
    )

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )

    new_user = models.User(
        username=user.username,
        password=user.password,  # Later we'll hash it
        role=user.role
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User created successfully",
        "user": new_user
    }


@app.post("/login")
def login(user: schemas.LoginRequest, db: Session = Depends(get_db)):

    db_user = (
        db.query(models.User)
        .filter(models.User.username == user.username)
        .first()
    )

    if not db_user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    if db_user.password != user.password:
        raise HTTPException(
            status_code=401,
            detail="Wrong password"
        )

    return {
        "id": db_user.id,
        "username": db_user.username,
        "role": db_user.role
    }


# =========================
# PLACES
# =========================

@app.post("/places/", response_model=schemas.PlaceResponse)
def create_place(
    place: schemas.PlaceCreate,
    db: Session = Depends(get_db)
):

    db_place = models.Place(**place.dict())

    db.add(db_place)
    db.commit()
    db.refresh(db_place)

    return db_place


@app.get("/places/", response_model=list[schemas.PlaceResponse])
def get_places(db: Session = Depends(get_db)):

    return db.query(models.Place).all()


@app.get("/places/{place_id}", response_model=schemas.PlaceResponse)
def get_place(place_id: int, db: Session = Depends(get_db)):

    place = (
        db.query(models.Place)
        .filter(models.Place.id == place_id)
        .first()
    )

    if not place:
        raise HTTPException(
            status_code=404,
            detail="Place not found"
        )

    return place


@app.delete("/places/{place_id}")
def delete_place(place_id: int, db: Session = Depends(get_db)):

    place = (
        db.query(models.Place)
        .filter(models.Place.id == place_id)
        .first()
    )

    if not place:
        raise HTTPException(
            status_code=404,
            detail="Place not found"
        )

    db.delete(place)
    db.commit()

    return {"message": "Place deleted successfully"}


# =========================
# ZONES
# =========================

@app.get("/zones/{zone_id}")
def get_zone(zone_id: int, db: Session = Depends(get_db)):

    zone = (
        db.query(models.Place)
        .filter(models.Place.id == zone_id)
        .first()
    )

    if not zone:
        raise HTTPException(
            status_code=404,
            detail="Zone not found"
        )

    return zone


@app.get("/zones/{zone_id}/hotels", response_model=list[schemas.Hotel])
def get_hotels(zone_id: int, db: Session = Depends(get_db)):

    return (
        db.query(models.Hotel)
        .filter(models.Hotel.zone_id == zone_id)
        .all()
    )


@app.get("/zones/{zone_id}/restaurants", response_model=list[schemas.Restaurant])
def get_restaurants(zone_id: int, db: Session = Depends(get_db)):

    return (
        db.query(models.Restaurant)
        .filter(models.Restaurant.zone_id == zone_id)
        .all()
    )


@app.get("/zones/{zone_id}/museums", response_model=list[schemas.Museum])
def get_museums(zone_id: int, db: Session = Depends(get_db)):

    return (
        db.query(models.Museum)
        .filter(models.Museum.zone_id == zone_id)
        .all()
    )