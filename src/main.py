from fastapi import FastAPI, Depends, HTTPException, status
from database import engine
from sqlalchemy.orm import Session
from database import SessionLocal
from datetime import datetime
import models
from models import User
from schemas import UserCreate, ClientResponse, UserLogin, BikeCreate, ReservationData, UserChangePassword
from services import UserService, BikeService, ReservationService
app = FastAPI()
models.Base.metadata.create_all(bind=engine)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Rejestracja
@app.post("/create-client", response_model=ClientResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    service = UserService(db)
    return service.create_client(user_data)

@app.post("/create-employee", response_model=ClientResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    service = UserService(db)
    return service.create_employee(user_data)

@app.post("/create-admin", response_model=ClientResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    service = UserService(db)
    return service.create_admin(user_data)


@app.post("/create-superadmin", response_model=ClientResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    service = UserService(db)
    return service.create_superadmin(user_data)


# Logowanie/Wylogowywanie
@app.post('/login')
def login(
    client_credentials: UserLogin,
    db: Session = Depends(get_db)
):
    service = UserService(db)
    return service.login(client_credentials)
@app.post('/logout')
def logout(
):
    return {"message": "Wylogowano"}
@app.post('/change-password')
def change_password(
    client_credentials: UserChangePassword,
    db: Session = Depends(get_db)
):
    service = UserService(db)
    return service.change_password(client_credentials)

@app.post('/create-bike')
def create_bike(
    bike_data: BikeCreate,
    db: Session = Depends(get_db)
):
    service = BikeService(db)
    return service.create_bike(bike_data)

@app.post('/create-reservation')
def create_reservation(
    reservation_data: ReservationData,
    db: Session = Depends(get_db)
):
    service = ReservationService(db)
    return service.create_reservation(reservation_data)