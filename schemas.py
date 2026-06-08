from pydantic import BaseModel, ConfigDict

# =========================
# PLACES
# =========================

class PlaceBase(BaseModel):
    name: str
    description: str
    category: str
    latitude: float
    longitude: float


class PlaceCreate(PlaceBase):
    pass


class PlaceResponse(PlaceBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


# =========================
# HOTELS
# =========================

class Hotel(BaseModel):
    id: int
    name: str
    price: float
    rating: float

    model_config = ConfigDict(from_attributes=True)


# =========================
# RESTAURANTS
# =========================

class Restaurant(BaseModel):
    id: int
    name: str
    cuisine: str
    price: float

    model_config = ConfigDict(from_attributes=True)


# =========================
# MUSEUMS
# =========================

class Museum(BaseModel):
    id: int
    name: str
    ticket_price: float

    model_config = ConfigDict(from_attributes=True)


# =========================
# USERS
# =========================

class UserBase(BaseModel):
    username: str
    role: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class LoginRequest(BaseModel):
    username: str
    password: str