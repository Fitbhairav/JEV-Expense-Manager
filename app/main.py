from fastapi import (
    FastAPI,
    Depends,
    HTTPException,
)

from sqlalchemy.orm import Session

from app.database import (
    Base,
    engine,
    get_db,
)

from app.models import Expense

from app.schemas import (
    ExpenseCreate,
    ExpenseResponse,
)

from app.services.expense_service import (
    analyze_and_create_expense,
)


Base.metadata.create_all(
    bind=engine
)


app = FastAPI(
    title="Jev Expense Intelligence",
    description=(
        "Expense categorization using "
        "Jev and Python"
    ),
    version="1.0.0",
)


@app.get("/")
def root():

    return {
        "message": "Jev Expense Intelligence API",
        "status": "running"
    }


@app.post(
    "/expenses",
    response_model=ExpenseResponse
)
def create_expense(
    expense: ExpenseCreate,
    db: Session = Depends(get_db)
):

    try:

        result = analyze_and_create_expense(
            db=db,
            description=expense.description,
            amount=expense.amount,
        )

        return result

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )


@app.get(
    "/expenses",
    response_model=list[ExpenseResponse]
)
def get_expenses(
    db: Session = Depends(get_db)
):

    return (
        db.query(Expense)
        .order_by(
            Expense.created_at.desc()
        )
        .all()
    )


@app.get(
    "/expenses/review",
    response_model=list[ExpenseResponse]
)
def get_review_expenses(
    db: Session = Depends(get_db)
):

    return (
        db.query(Expense)
        .filter(
            Expense.needs_review == True
        )
        .order_by(
            Expense.created_at.desc()
        )
        .all()
    )
