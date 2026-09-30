from sqlalchemy import (
    Column,
    Integer,
    Float,
    String,
    Boolean,
    DateTime,
)
from sqlalchemy.sql import func

from app.database import Base


class Expense(Base):

    __tablename__ = "expenses"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    description = Column(
        String,
        nullable=False
    )

    amount = Column(
        Float,
        nullable=False
    )

    category = Column(
        String,
        nullable=False
    )

    expense_type = Column(
        String,
        nullable=False
    )

    risk_score = Column(
        Float,
        nullable=False
    )

    review_probability = Column(
        Float,
        nullable=False
    )

    needs_review = Column(
        Boolean,
        default=False
    )

    created_at = Column(
        DateTime,
        server_default=func.now()
    )
