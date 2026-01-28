from typing import TypeVar, Generic, Type, Any
from datetime import date
from sqlalchemy.orm import Session
from models import Client, Employee, User, Admin, SuperAdmin, Bike, Reservation
from schemas import UserCreate, UserLogin, BikeCreate,BikeUpdate, ReservationData, UserChangePassword
from fastapi import HTTPException
class UserService:
    def __init__(self, db: Session):
        self.db = db

    def create_client(self, user_data: UserCreate):
        check = self.db.query(User).filter(User.email == user_data.email).first()
        if check:
            raise HTTPException(status_code=400, detail="Podany email jest zajęty. Uzyj innego.")
        new_client = Client(
            email=user_data.email,
            password=user_data.password,
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            type="client"
        )
        
        self.db.add(new_client)
        self.db.commit()
        self.db.refresh(new_client)
        
        return new_client
    
    def create_employee(self, user_data: UserCreate):
        check = self.db.query(User).filter(User.email == user_data.email).first()
        if check:
            raise HTTPException(status_code=400, detail="Podany email jest zajęty. Uzyj innego.")
        new_client = Employee(
            email=user_data.email,
            password=user_data.password,
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            type="employee"
        )
        
        self.db.add(new_client)
        self.db.commit()
        self.db.refresh(new_client)
        
        return new_client

    def create_admin(self, user_data: UserCreate):
        check = self.db.query(User).filter(User.email == user_data.email).first()
        if check:
            raise HTTPException(status_code=400, detail="Podany email jest zajęty. Uzyj innego.")
        new_client = Admin(
            email=user_data.email,
            password=user_data.password,
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            type="admin"
        )
        
        self.db.add(new_client)
        self.db.commit()
        self.db.refresh(new_client)
        
        return new_client
    
    def create_superadmin(self, user_data: UserCreate):
        check = self.db.query(User).filter(User.email == user_data.email).first()
        if check:
            raise HTTPException(status_code=400, detail="Podany email jest zajęty. Uzyj innego.")
        new_client = SuperAdmin(
            email=user_data.email,
            password=user_data.password,
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            type="super_admin"
        )
        
        self.db.add(new_client)
        self.db.commit()
        self.db.refresh(new_client)
        
        return new_client

    def login(self, credentials: UserLogin):
        user = self.db.query(User).filter(User.email == credentials.email).first()
        if not user:
            raise HTTPException(status_code=404, detail="Podany email nie istnieje")
        if user.password != credentials.password:
            raise HTTPException(status_code=401, detail="Nieprawidłowe hasło")
        return {
            "email": user.email,
            "type": user.type
        }
    
    def change_password(self, credentials: UserChangePassword):
        user = self.db.query(User).filter(User.email == credentials.email).first()
        if not user:
            raise HTTPException(status_code=404, detail="Podany email nie istnieje")
        if user.password != credentials.password:
            raise HTTPException(status_code=401, detail="Nieprawidłowe hasło")
        user.password = credentials.new_password
        try:
            self.db.commit()
            self.db.refresh(user)
            return {"message": "Hasło zostało zmienione pomyślnie"}
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=500, detail="Błąd podczas zapisywania hasła")
class BikeService:
    def __init__(self, db: Session):
        self.db = db

    def list_bikes(self):
        bikes = self.db.query(Bike).all()
        return bikes
        
    def create_bike(self, bike_data: BikeCreate):
        user = self.db.query(User).filter(User.email == bike_data.user_email).first()
        if user.type == "client":
            raise HTTPException(status_code=403, detail="Nie posiadasz uprawnień do wykonania tej operacji.")
        bike_model = Bike(
            model=bike_data.model,
            type=bike_data.type,
            description=bike_data.description,
            price=bike_data.price
        )

        self.db.add(bike_model)
        self.db.commit()
        self.db.refresh(bike_model)
        return f"Model pomyślnie utworzony: {bike_model}"

    def update_bike(self, bike_id: int, user_email: str, bike_data: BikeUpdate):
        user = self.db.query(User).filter(User.email == user_email).first()
        if user.type == "client":
            raise HTTPException(status_code=403, detail="Nie posiadasz uprawnień do wykonania tej operacji.")
    
        bike = self.db.query(Bike).filter(Bike.id == bike_id).first()
        if not bike:
            raise HTTPException(status_code=404, detail="Nie znaleziono roweru")

        bike.model = bike_data.model
        bike.type = bike_data.type
        bike.description = bike_data.description
        bike.price = bike_data.price

        self.db.commit()
        self.db.refresh(bike)
        return f"Model pomyślnie zaktualizowany: {bike}"

    def delete_bike(self, bike_id: int, user_email: str):
        user = self.db.query(User).filter(User.email == user_email).first()
        if user.type == "client":
            raise HTTPException(status_code=403, detail="Nie posiadasz uprawnień do wykonania tej operacji.")
        bike = self.db.query(Bike).filter(Bike.id == bike_id).first()

        if not bike:
            raise HTTPException(status_code=404, detail="Nie znaleziono roweru")

        self.db.delete(bike)
        self.db.commit()
        return f"Model pomyślnie usunięty. ID: {bike_id}"
    
class ReservationService:
    def __init__(self, db: Session):
        self.db = db

    def create_reservation(self, reservation_data: ReservationData):
        user = self.db.query(User).filter(User.email == reservation_data.email).first()
        
        if not user:
            raise HTTPException(status_code=404, detail="Podany email nie istnieje")
        bike = self.db.query(Bike).filter(Bike.model == reservation_data.bike_model).first()
        if not bike:
            raise HTTPException(status_code=404, detail="Podany model roweru nie istnieje")
        
        if bike.is_reserved:
            raise HTTPException(status_code=400, detail="Ten rower jest już zarezerwowany")
        reservation_model = Reservation(
            client_id=user.id,
            bike_id=bike.id,
            start_date=reservation_data.start_date,
            end_date=reservation_data.end_date,
            price=self._calculate_cost(bike.price, reservation_data.start_date.date(), reservation_data.end_date.date())
        )

        bike.is_reserved = True

        try:
            self.db.add(reservation_model)
            self.db.commit()
            self.db.refresh(reservation_model)
            return f"Pomyślnie utworzono rezerwacje na rower: {reservation_data.bike_model}"
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=500, detail=f"Błąd bazy danych: {str(e)}")

    def list_reservations_by_user(self, user_email: str):
        user = self.db.query(User).filter(User.email == user_email).first()
        
        if not user:
            raise HTTPException(status_code=404, detail="Podany email nie istnieje")
        
        reservations = self.db.query(Reservation).filter(Reservation.client_id == user.id).all()
        bikes = self.db.query(Bike).all()
        reservation_return_list = []
        for reservation in reservations:
            for bike in bikes:
                if reservation.bike_id == bike.id:
                    return_model = {
                        "id": reservation.id,
                        "bike_model": bike.model,
                        "price": reservation.price,
                        "start_date": reservation.start_date,
                        "end_date": reservation.end_date
                    }
                    reservation_return_list.append(return_model)
        return reservation_return_list
    def list_reservations(self):
        reservations = self.db.query(Reservation).all()
        return reservations
    def remove_reservation(self, id: int):
        reservation = self.db.query(Reservation)\
               .filter(Reservation.id == id).first()
        bike = self.db.query(Bike).filter(Bike.id == reservation.bike_id).first()

        bike.is_reserved=False
        self.db.query(Reservation).filter(Reservation.id == id).delete(synchronize_session=False)
        self.db.commit()

    @staticmethod
    def _calculate_cost(bike_price_per_day: float, date_from: date, date_to: date):
        return bike_price_per_day * max((date_to - date_from).days, 1)