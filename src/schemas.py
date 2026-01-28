from pydantic import BaseModel, EmailStr
from datetime import datetime
from enum import Enum
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    first_name: str
    last_name: str

class UserLogin(BaseModel):
    email: str
    password: str
    
class UserChangePassword(BaseModel):
    email: str
    password: str
    new_password: str

class ClientResponse(BaseModel):
    id: int
    email: EmailStr
    first_name: str
    last_name: str
    created_at: datetime


    model_config = {
        "from_attributes": True
    }

class BikeCreate(BaseModel):
    model: str
    type: str
    description: str
    price: float
    user_email: str

class BikeUpdate(BaseModel):
    model: str
    type: str
    description: str
    price: float
    
class ReservationData(BaseModel):
    email: str
    bike_model: str
    start_date: datetime
    end_date: datetime

class TicketStatus(Enum):
    CREATED = "CREATED"   
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"

class InquiryStatus(Enum):
    NEW = "NEW"
    IN_PROGRESS = "IN_PROGRESS"
    ANSWERED = "ANSWERED"
    CLOSED = "CLOSED"