# app/models.py
from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Date,
    DECIMAL,
    Text,
    TIMESTAMP,
)
from sqlalchemy.orm import relationship
from utils.database import Base
from datetime import datetime


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    role = Column(String(50), nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)


class CoachClientRelationship(Base):
    __tablename__ = "coach_client_relationships"

    relationship_id = Column(Integer, primary_key=True, index=True)
    coach_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    client_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    status = Column(String(50), nullable=False, default="pending")
    start_date = Column(Date)
    end_date = Column(Date)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

    coach = relationship("User", foreign_keys=[coach_id])
    client = relationship("User", foreign_keys=[client_id])


class WorkoutPlan(Base):
    __tablename__ = "workout_plans"

    plan_id = Column(Integer, primary_key=True, index=True)
    relationship_id = Column(
        Integer,
        ForeignKey("coach_client_relationships.relationship_id"),
        nullable=False,
    )
    workout_type = Column(String(100))
    workout_duration = Column(Integer)  # in minutes
    frequency_per_week = Column(Integer)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)


class NutritionPlan(Base):
    __tablename__ = "nutrition_plans"

    plan_id = Column(Integer, primary_key=True, index=True)
    relationship_id = Column(
        Integer,
        ForeignKey("coach_client_relationships.relationship_id"),
        nullable=False,
    )
    meal_plan = Column(Text)
    calories_per_day = Column(Integer)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)


class PaymentPlan(Base):
    __tablename__ = "payment_plans"

    plan_id = Column(Integer, primary_key=True, index=True)
    relationship_id = Column(
        Integer,
        ForeignKey("coach_client_relationships.relationship_id"),
        nullable=False,
    )
    payment_amount = Column(DECIMAL(10, 2))
    payment_frequency = Column(String(50))
    next_payment_due = Column(Date)
    payment_method = Column(String(50))
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
