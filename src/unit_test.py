import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from fastapi import HTTPException
from services import UserService, BikeService, ReservationService
from schemas import UserCreate, UserLogin, BikeCreate, BikeUpdate, ReservationData
from models import User,Bike
from database import Base

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)

@pytest.fixture()
def db_session():
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)

# USERSERVICE UNIT TESTS
def test_create_client_success(db_session):
    repo = UserService(db_session)

    user_data = UserCreate(
        email="test@example.com",
        password="1234",
        first_name="Jan",
        last_name="Kowalski"
    )

    client = repo.create_client(user_data)

    assert client.id is not None
    assert client.email == "test@example.com"
    assert client.type == "client"

def test_create_client_duplicate_email(db_session):
    repo = UserService(db_session)
    user_data = UserCreate(
        email="test@example.com",
        password="1234",
        first_name="Jan",
        last_name="Kowalski"
    )

    repo.create_client(user_data)

    with pytest.raises(HTTPException) as excinfo:
        repo.create_client(user_data)

    assert excinfo.value.status_code == 400
    assert excinfo.value.detail == "Podany email jest zajęty. Uzyj innego."

def test_create_employee_success(db_session):
    repo = UserService(db_session)

    user_data = UserCreate(
        email="test@example.com",
        password="1234",
        first_name="Jan",
        last_name="Kowalski"
    )

    client = repo.create_employee(user_data)

    assert client.id is not None
    assert client.email == "test@example.com"
    assert client.type == "employee"

def test_create_employee_duplicate_email(db_session):
    repo = UserService(db_session)
    user_data = UserCreate(
        email="test@example.com",
        password="1234",
        first_name="Jan",
        last_name="Kowalski"
    )

    repo.create_employee(user_data)

    with pytest.raises(HTTPException) as excinfo:
        repo.create_employee(user_data)

    assert excinfo.value.status_code == 400
    assert excinfo.value.detail == "Podany email jest zajęty. Uzyj innego."

def test_create_admin_success(db_session):
    repo = UserService(db_session)

    user_data = UserCreate(
        email="test@example.com",
        password="1234",
        first_name="Jan",
        last_name="Kowalski"
    )

    client = repo.create_admin(user_data)

    assert client.id is not None
    assert client.email == "test@example.com"
    assert client.type == "admin"

def test_create_admin_duplicate_email(db_session):
    repo = UserService(db_session)
    user_data = UserCreate(
        email="test@example.com",
        password="1234",
        first_name="Jan",
        last_name="Kowalski"
    )

    repo.create_admin(user_data)

    with pytest.raises(HTTPException) as excinfo:
        repo.create_admin(user_data)

    assert excinfo.value.status_code == 400
    assert excinfo.value.detail == "Podany email jest zajęty. Uzyj innego."

def test_create_superadmin_success(db_session):
    repo = UserService(db_session)

    user_data = UserCreate(
        email="test@example.com",
        password="1234",
        first_name="Jan",
        last_name="Kowalski"
    )

    client = repo.create_superadmin(user_data)

    assert client.id is not None
    assert client.email == "test@example.com"
    assert client.type == "super_admin"

def test_create_superadmin_duplicate_email(db_session):
    repo = UserService(db_session)
    user_data = UserCreate(
        email="test@example.com",
        password="1234",
        first_name="Jan",
        last_name="Kowalski"
    )

    repo.create_superadmin(user_data)

    with pytest.raises(HTTPException) as excinfo:
        repo.create_superadmin(user_data)

    assert excinfo.value.status_code == 400
    assert excinfo.value.detail == "Podany email jest zajęty. Uzyj innego."

def test_login_success(db_session):
    repo = UserService(db_session)
    user_data = UserCreate(
        email="test@example.com",
        password="1234",
        first_name="Jan",
        last_name="Kowalski"
    )
    repo.create_client(user_data)
    response = repo.login(UserLogin(
        email="test@example.com",
        password="1234"
    ))
    assert response == "Zalogowany"

def test_login_wrong_email(db_session):
    repo = UserService(db_session)
    user_data = UserCreate(
        email="test@example.com",
        password="1234",
        first_name="Jan",
        last_name="Kowalski"
    )
    repo.create_client(user_data)

    with pytest.raises(HTTPException) as excinfo:
        response = repo.login(UserLogin(
            email="tes@example.com",
            password="1234"
        ))

    assert excinfo.value.status_code == 404
    assert excinfo.value.detail == "Podany email nie istnieje"

def test_login_wrong_password(db_session):
    repo = UserService(db_session)
    user_data = UserCreate(
        email="test@example.com",
        password="1234",
        first_name="Jan",
        last_name="Kowalski"
    )
    repo.create_client(user_data)

    with pytest.raises(HTTPException) as excinfo:
        response = repo.login(UserLogin(
            email="test@example.com",
            password="123"
        ))

    assert excinfo.value.status_code == 401
    assert excinfo.value.detail == "Nieprawidłowe hasło"


# BIKESERVICE UNIT TESTS

def test_create_bike_success(db_session):
    user_repo = UserService(db_session)
    bike_repo = BikeService(db_session)
    user_data = UserCreate(
        email="test@example.com",
        password="1234",
        first_name="Jan",
        last_name="Kowalski"
    )
    user_repo.create_employee(user_data)
    bike_model = BikeCreate(
        model="test_model",
        type="test_type",
        description="test_description",
        price=0.00,
        user_email="test@example.com"
    )
    response = bike_repo.create_bike(bike_model)
    
    response == f"Model pomyślnie utworzony: {bike_model}"
    
def test_create_bike_unauthorized(db_session):
    user_repo = UserService(db_session)
    bike_repo = BikeService(db_session)
    user_data = UserCreate(
        email="test@example.com",
        password="1234",
        first_name="Jan",
        last_name="Kowalski"
    )
    user_repo.create_client(user_data)
    bike_model = BikeCreate(
        model="test_model",
        type="test_type",
        description="test_description",
        price=0.00,
        user_email="test@example.com"
    )

    with pytest.raises(HTTPException) as excinfo:
        response = bike_repo.create_bike(bike_model)

    assert excinfo.value.status_code == 403
    assert excinfo.value.detail == "Nie posiadasz uprawnień do wykonania tej operacji."

def test_update_bike_success(db_session):
    user_repo = UserService(db_session)
    bike_repo = BikeService(db_session)
    user_data = UserCreate(
        email="test@example.com",
        password="1234",
        first_name="Jan",
        last_name="Kowalski"
    )
    bike_model = BikeCreate(
        model="test_model",
        type="test_type",
        description="test_description",
        price=0.00,
        user_email="test@example.com"
    )
    user_repo.create_employee(user_data)
    bike_repo.create_bike(bike_model)

    updated_bike_model = BikeUpdate(
        model="updated_model",
        type="updated_model",
        description="updated_model",
        price=5.00,
    )
    response = bike_repo.update_bike(1, user_data.email, updated_bike_model)

    updated_bike_in_db = db_session.query(Bike).filter(Bike.id == 1).first()

    assert updated_bike_in_db.model == "updated_model"
    assert updated_bike_in_db.price == 5.00
    assert "pomyślnie zaktualizowany" in response

def test_update_bike_unauthorized(db_session):
    user_repo = UserService(db_session)
    bike_repo = BikeService(db_session)
    employee_data = UserCreate(
        email="test_employee@example.com",
        password="1234",
        first_name="Jan",
        last_name="Kowalski"
    )
    client_data = UserCreate(
        email="test_client@example.com",
        password="1234",
        first_name="Jan",
        last_name="Kowalski"
    )
    bike_model = BikeCreate(
        model="test_model",
        type="test_type",
        description="test_description",
        price=0.00,
        user_email="test_employee@example.com"
    )
    user_repo.create_employee(employee_data)
    user_repo.create_client(client_data)

    bike_repo.create_bike(bike_model)

    updated_bike_model = BikeUpdate(
        model="updated_model",
        type="updated_model",
        description="updated_model",
        price=5.00,
    )
    
    with pytest.raises(HTTPException) as excinfo:
        bike_repo.update_bike(1, client_data.email, updated_bike_model)

    assert excinfo.value.status_code == 403
    assert "Nie posiadasz uprawnień" in excinfo.value.detail

def test_delete_bike_success(db_session):
    user_repo = UserService(db_session)
    bike_repo = BikeService(db_session)

    employee_data = UserCreate(
          email="test_employee@example.com",
          password="1234",
          first_name="Jan",
          last_name="Kowalski"
      )
    bike_model = BikeCreate(
        model="test_model",
        type="test_type",
        description="test_description",
        price=0.00,
        user_email="test_employee@example.com"
    )
    user_repo.create_employee(employee_data)
    bike_repo.create_bike(bike_model)

    response = bike_repo.delete_bike(1, employee_data.email)

    assert response == f"Model pomyślnie usunięty. ID: {1}"

def test_delete_bike_unauthorized(db_session):
    user_repo = UserService(db_session)
    bike_repo = BikeService(db_session)
    employee_data = UserCreate(
        email="test_employee@example.com",
        password="1234",
        first_name="Jan",
        last_name="Kowalski"
    )
    client_data = UserCreate(
        email="test_client@example.com",
        password="1234",
        first_name="Jan",
        last_name="Kowalski"
    )
    bike_model = BikeCreate(
        model="test_model",
        type="test_type",
        description="test_description",
        price=0.00,
        user_email="test_employee@example.com"
    )
    user_repo.create_employee(employee_data)
    user_repo.create_client(client_data)
    
    bike_repo.create_bike(bike_model)


    with pytest.raises(HTTPException) as excinfo:
        bike_repo.delete_bike(1, client_data.email)

    assert excinfo.value.status_code == 403
    assert "Nie posiadasz uprawnień" in excinfo.value.detail

# RESERVATIONSERVICE UNIT TESTS

def test_create_reservation_success(db_session):
    user_repo = UserService(db_session)
    bike_repo = BikeService(db_session)
    reservation_repo = ReservationService(db_session)

    employee_data = UserCreate(
        email="test_employee@example.com",
        password="1234",
        first_name="Jan",
        last_name="Kowalski"
    )
    bike_model = BikeCreate(
        model="test_model",
        type="test_type",
        description="test_description",
        price=0.00,
        user_email="test_employee@example.com"
    )

    user_repo.create_employee(employee_data)
    bike_repo.create_bike(bike_model)

    reservation_model = ReservationData(
        email = employee_data.email,
        bike_model = bike_model.model,
        start_date = "2026-02-10T11:15:30.456789",
        end_date = "2026-02-12T11:15:30.456789"
    )

    response = reservation_repo.create_reservation(reservation_model)
    assert response == f"Pomyślnie utworzono rezerwacje na rower: {reservation_model.bike_model}"

def test_create_reservation_bike_not_found(db_session):
    user_repo = UserService(db_session)
    bike_repo = BikeService(db_session)
    reservation_repo = ReservationService(db_session)

    employee_data = UserCreate(
        email="test_employee@example.com",
        password="1234",
        first_name="Jan",
        last_name="Kowalski"
    )
    bike_model = BikeCreate(
        model="test_model",
        type="test_type",
        description="test_description",
        price=0.00,
        user_email="test_employee@example.com"
    )

    user_repo.create_employee(employee_data)
    bike_repo.create_bike(bike_model)

    reservation_model = ReservationData(
        email = employee_data.email,
        bike_model = "test_model_1",
        start_date = "2026-02-10T11:15:30.456789",
        end_date = "2026-02-12T11:15:30.456789"
    )

    with pytest.raises(HTTPException) as excinfo:
        reservation_repo.create_reservation(reservation_model)

    assert excinfo.value.status_code == 404
    assert excinfo.value.detail == "Podany model roweru nie istnieje"

def test_create_reservation_bike_reserved(db_session):
    user_repo = UserService(db_session)
    bike_repo = BikeService(db_session)
    reservation_repo = ReservationService(db_session)

    employee_data = UserCreate(
        email="test_employee@example.com",
        password="1234",
        first_name="Jan",
        last_name="Kowalski"
    )
    bike_model = BikeCreate(
        model="test_model",
        type="test_type",
        description="test_description",
        price=0.00,
        user_email="test_employee@example.com"
    )

    user_repo.create_employee(employee_data)
    bike_repo.create_bike(bike_model)
    bike = db_session.query(Bike).filter(Bike.id == 1).first()
    bike.is_reserved = True
    reservation_model = ReservationData(
        email = employee_data.email,
        bike_model = bike_model.model,
        start_date = "2026-02-10T11:15:30.456789",
        end_date = "2026-02-12T11:15:30.456789"
    )

    with pytest.raises(HTTPException) as excinfo:
        reservation_repo.create_reservation(reservation_model)

    assert excinfo.value.status_code == 400
    assert excinfo.value.detail == "Ten rower jest już zarezerwowany"