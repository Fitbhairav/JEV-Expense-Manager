import requests

from app.config import JEV_API_KEY, MOCK_JEV


JEV_URL = "https://jevtypesafeai.com/api/v1/decide"


class JevClient:

    def __init__(self):
        if not MOCK_JEV and not JEV_API_KEY:
            raise RuntimeError(
                "JEV_API_KEY is not configured"
            )

        self.headers = {
            "Authorization": f"Bearer {JEV_API_KEY}",
            "Content-Type": "application/json",
        }

    def analyze_expense(
        self,
        description: str,
        amount: float
    ):
        if MOCK_JEV:
            return self._mock_analyze_expense(description, amount)

        state = {
            "expense_description": description,
            "amount": amount,
            "currency": "INR"
        }

        questions = {

            "category": {
                "type": "choice",

                "instructions": (
                    "What is the primary category "
                    "of this expense?"
                ),

                "criteria": {
                    "food": (
                        "Restaurants, groceries, "
                        "coffee, meals or food delivery"
                    ),

                    "transport": (
                        "Taxi, Uber, Ola, fuel, metro, "
                        "bus, train or transportation"
                    ),

                    "shopping": (
                        "Clothes, electronics, Amazon, "
                        "personal shopping or retail"
                    ),

                    "travel": (
                        "Flights, hotels, vacation or "
                        "travel-related expenses"
                    ),

                    "bills": (
                        "Electricity, internet, mobile, "
                        "rent or recurring bills"
                    ),

                    "health": (
                        "Medicine, doctor, hospital, "
                        "gym or healthcare"
                    ),

                    "entertainment": (
                        "Movies, games, subscriptions "
                        "or entertainment"
                    ),

                    "education": (
                        "Courses, books, training or "
                        "education"
                    ),

                    "other": (
                        "Anything that does not fit "
                        "the categories above"
                    ),
                }
            },

            "expense_type": {
                "type": "choice",

                "instructions": (
                    "Is this expense personal, "
                    "business, or uncertain?"
                ),

                "criteria": {
                    "personal": (
                        "Clearly for personal use"
                    ),

                    "business": (
                        "Clearly related to work, "
                        "business or professional activity"
                    ),

                    "uncertain": (
                        "Cannot confidently determine "
                        "the purpose"
                    ),
                }
            },

            "risk": {
                "type": "score",

                "instructions": (
                    "How unusual or uncertain is this "
                    "expense for automatic categorization?"
                ),

                "criteria": [
                    "Clearly identifiable and routine",
                    "Mostly clear",
                    "Some ambiguity",
                    "Highly ambiguous or unusual",
                ]
            },

            "needs_review": {
                "type": "noul",

                "instructions": (
                    "Should this expense be manually "
                    "reviewed before being accepted?"
                )
            }
        }

        response = requests.post(
            JEV_URL,
            headers=self.headers,
            json={
                "model": "jev-latest",
                "state": state,
                "questions": questions,
            },
            timeout=30,
        )

        response.raise_for_status()

        return response.json()

    def _mock_analyze_expense(self, description: str, amount: float) -> dict:
        desc_lower = description.lower()

        if any(w in desc_lower for w in ["dinner", "restaurant", "lunch", "coffee", "meal", "food", "burger", "pizza", "groceries", "grocery", "cafe"]):
            category = "food"
        elif any(w in desc_lower for w in ["taxi", "uber", "ola", "cab", "fuel", "petrol", "diesel", "metro", "bus", "train", "flight"]):
            category = "transport"
        elif any(w in desc_lower for w in ["hotel", "vacation", "resort", "airbnb", "trip", "travel"]):
            category = "travel"
        elif any(w in desc_lower for w in ["amazon", "clothes", "shoes", "electronics", "shopping", "store"]):
            category = "shopping"
        elif any(w in desc_lower for w in ["electricity", "internet", "wifi", "phone", "rent", "bill", "utility"]):
            category = "bills"
        elif any(w in desc_lower for w in ["medicine", "doctor", "hospital", "gym", "pharma", "health"]):
            category = "health"
        elif any(w in desc_lower for w in ["movie", "cinema", "netflix", "game", "entertainment", "ticket"]):
            category = "entertainment"
        elif any(w in desc_lower for w in ["course", "book", "training", "tuition", "education"]):
            category = "education"
        else:
            category = "other"

        if any(w in desc_lower for w in ["work", "office", "client", "business", "meeting"]):
            expense_type = "business"
        else:
            expense_type = "personal"

        if amount > 10000 or category == "other":
            risk_score = 3.0
            review_probability = 0.85
        elif amount > 3000:
            risk_score = 2.0
            review_probability = 0.50
        else:
            risk_score = 1.0
            review_probability = 0.15

        return {
            "answers": {
                "category": {
                    "choice": category
                },
                "expense_type": {
                    "choice": expense_type
                },
                "risk": {
                    "score": risk_score
                },
                "needs_review": {
                    "noul": review_probability
                }
            }
        }

