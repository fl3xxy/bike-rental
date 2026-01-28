from fastapi import FastAPI, Depends, HTTPException, status
from database import engine
from sqlalchemy.orm import Session
from database import SessionLocal
from datetime import datetime
import models
from models import User
from schemas import UserCreate, ClientResponse, UserLogin, BikeCreate, ReservationData, UserChangePassword
from services import UserService, BikeService, ReservationService
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
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

# Listowanie
@app.get("/bikes")
def get_bikes(db: Session = Depends(get_db)):
    service = BikeService(db)
    return service.list_bikes()

@app.get("/list-reservations/{user_email}")
def get_reservations_by_user(user_email: str, db: Session = Depends(get_db)):
    service = ReservationService(db)
    return service.list_reservations_by_user(user_email)

@app.get('/list-reservation')
def list_reservations(db: Session = Depends(get_db)):
    service = ReservationService(db)
    return service.list_reservations()

@app.delete("/remove-reservation/{reservation_id}")
def remove_reservation(reservation_id: int, db: Session = Depends(get_db)):
    service = ReservationService(db)
    return service.remove_reservation(reservation_id)

@app.put("/cancel-reservaiton/{reservation_id}")
def update_bike(reservation_id: int, db: Session = Depends(get_db)):
    service = ReservationService(db)
    return service.cancel_reservation(reservation_id)

@app.delete("/delete-bike/{bike_id}")
def delete_bike(bike_id: int, user_email: str, db: Session = Depends(get_db)):
    service = BikeService(db)
    return service.delete_bike(bike_id, user_email)