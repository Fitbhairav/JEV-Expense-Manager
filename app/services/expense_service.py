from sqlalchemy.orm import Session

from app.models import Expense
from app.jev.client import JevClient


jev = JevClient()


def analyze_and_create_expense(
    db: Session,
    description: str,
    amount: float
):

    # Ask Jev to analyze the expense
    result = jev.analyze_expense(
        description=description,
        amount=amount
    )

    answers = result["answers"]

    # Extract typed Jev answers
    category = answers["category"]["choice"]

    expense_type = answers[
        "expense_type"
    ]["choice"]

    risk_score = answers[
        "risk"
    ]["score"]

    review_probability = answers[
        "needs_review"
    ]["noul"]

    # Our application decides the threshold.
    needs_review = review_probability >= 0.70

    expense = Expense(
        description=description,
        amount=amount,
        category=category,
        expense_type=expense_type,
        risk_score=risk_score,
        review_probability=review_probability,
        needs_review=needs_review,
    )

    db.add(expense)
    db.commit()
    db.refresh(expense)

    return expense
