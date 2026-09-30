# Jev Expense Manager

An intelligent expense management and categorization API built with **FastAPI**, **SQLAlchemy**, and **Jev TypeSafe AI**.

---

## 📌 Features

- **Automated Expense Categorization**: Categorizes expenses into standard buckets (Food, Transport, Shopping, Travel, Bills, Health, Entertainment, Education, Other).
- **Expense Classification**: Identifies whether expenses are for `personal` or `business` use.
- **Risk Assessment & Review Flagging**: Computes risk scores and flags high-risk or high-value expenses that require manual review (`needs_review`).
- **Flexible Modes**:
  - **Live Mode**: Integrates with the Jev TypeSafe AI API (`https://jevtypesafeai.com/api/v1/decide`).
  - **Mock Mode (`MOCK_JEV=true`)**: Provides instant offline intelligence without requiring external API credits.

---

## 🛠️ Project Structure

```
jev-expense-manager/
│
├── app/
│   ├── jev/
│   │   └── client.py          # Jev API client with Mock mode support
│   ├── services/
│   │   └── expense_service.py # Business logic for expense analysis and storage
│   ├── config.py              # Environment configuration loader
│   ├── database.py            # SQLAlchemy database connection setup
│   ├── main.py                # FastAPI application endpoints
│   ├── models.py              # Database models (SQLite/PostgreSQL)
│   └── schemas.py             # Pydantic validation schemas
│
├── .env                       # Environment configuration file
├── expenses.db                # SQLite database file
├── requirements.txt           # Project dependencies
└── README.md                  # Project documentation
```

---

## 🚀 Quick Start

### 1. Prerequisites
- Python 3.10+
- Virtual environment (`venv`)

### 2. Setup Environment

Create and activate a virtual environment:

```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

### 3. Environment Configuration

Create or update the `.env` file in the root directory:

```env
JEV_API_KEY=jv_live_your_api_key_here
DATABASE_URL=sqlite:///./expenses.db
MOCK_JEV=true
```

> 💡 **Tip:** Set `MOCK_JEV=true` to test locally without incurring API costs. Set `MOCK_JEV=false` to use live Jev AI predictions.

---

## 🏃 Running the Application

Start the development server using **Uvicorn**:

```bash
uvicorn app.main:app --reload
```

The API server will run at `http://127.0.0.1:8000`.

---

## 📖 API Documentation

Once the server is running, access the interactive API docs:

- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 📡 API Endpoints

### 1. Root Status
- **`GET /`**
  - **Response**: `{ "message": "Jev Expense Intelligence API", "status": "running" }`

### 2. Create & Analyze Expense
- **`POST /expenses`**
  - **Request Body**:
    ```json
    {
      "description": "Dinner at a restaurant",
      "amount": 1200
    }
    ```
  - **Response (200 OK)**:
    ```json
    {
      "id": 1,
      "description": "Dinner at a restaurant",
      "amount": 1200.0,
      "category": "food",
      "expense_type": "personal",
      "risk_score": 1.0,
      "review_probability": 0.15,
      "needs_review": false
    }
    ```

### 3. List All Expenses
- **`GET /expenses`**
  - Returns a list of all recorded expenses ordered by newest first.

### 4. List Expenses Needing Review
- **`GET /expenses/review`**
  - Returns a list of expenses where `needs_review == true`.

---

## 🧪 Example Request

Using `curl`:

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/expenses' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "description": "Dinner at a restaurant",
  "amount": 1200
}'
```
