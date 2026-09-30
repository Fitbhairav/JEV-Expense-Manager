from pydantic import BaseModel, Field


class ExpenseCreate(BaseModel):

    description: str = Field(
        min_length=3
    )

    amount: float = Field(
        gt=0
    )


class ExpenseResponse(BaseModel):

    id: int
    description: str
    amount: float
    category: str
    expense_type: str
    risk_score: float
    review_probability: float
    needs_review: bool

    class Config:
        from_attributes = True
