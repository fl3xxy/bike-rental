from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Numeric, Enum as SQLEnum
from database import Base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from schemas import TicketStatus, InquiryStatus


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String, nullable=False)
    first_name = Column(String)
    last_name = Column(String)
    created_at = Column(DateTime, server_default=func.now())
    type = Column(String(50))
    __mapper_args__ = {
        "polymorphic_identity": "user",
        "polymorphic_on": type,
    }

class Client(User):
    __tablename__ = "clients"

    id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    phone = Column(Integer)
    reservations = relationship(
        "Reservation",
        back_populates="client",
        cascade="all, delete-orphan"
    )

    __mapper_args__ = {
        "polymorphic_identity": "client",
    }

class Employee(User):
    __tablename__ = "employees"

    id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    employeeNo = Column(String)

    __mapper_args__ = {
        "polymorphic_identity": "employee",
    }
    
class Admin(User):
    __tablename__ = "admins"

    id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    admin_level = Column(Integer, default=1)

    __mapper_args__ = {
        "polymorphic_identity": "admin",
    }

class SuperAdmin(User):
    __tablename__ = "super_admins"

    id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    is_superadmin = Column(Boolean, default=1)

    __mapper_args__ = {
        "polymorphic_identity": "super_admin",
    }

class Reservation(Base):
    __tablename__ = "reservations"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    
    bike_id = Column(Integer, ForeignKey("bikes.id"), nullable=False)
    
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    price = Column(Numeric)
    client = relationship("Client", back_populates="reservations")
    
    bike = relationship("Bike", back_populates="reservations")


class Bike(Base):
    __tablename__ = "bikes"

    id = Column(Integer, primary_key=True, index=True)
    model = Column(String, nullable=False)
    type = Column(String, nullable=False)
    description = Column(String)
    price = Column(Numeric)
    is_reserved = Column(Boolean, default=False)

    reservations = relationship("Reservation", back_populates="bike")


class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    topic = Column(String(100))
    content = Column(String(255))
    status = Column(
        SQLEnum(TicketStatus, name="ticket_status"),
        nullable=False,
        default=TicketStatus.CREATED
    )
    priority = Column(Integer)
    resolution = Column(String)
    created_at = Column(DateTime, server_default=func.now())
    resolved_at = Column(DateTime)

class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)
    report_type = Column(String)
    generated_at = Column(DateTime, server_default=func.now())

class Inquiry(Base):
    __tablename__ = "inquiries"

    id = Column(Integer, primary_key=True, index=True)
    topic = Column(String(100))
    content = Column(String(255))
    status = Column(
        SQLEnum(InquiryStatus, name="inquiry_status"),
        nullable=False,
        default=InquiryStatus.NEW
    )
    created_at = Column(DateTime, server_default=func.now())
    answer = Column(String)
    answered_at = Column(DateTime)