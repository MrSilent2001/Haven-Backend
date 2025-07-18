# Haven-Backend (FastAPI + MongoDB)

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Make sure MongoDB is running and update your connection info in `db.py` if needed.

## Run the app

```bash
uvicorn main:app --reload
```

## Sample mood item

```json
{
  "user_id": "user123",
  "mood": 7,
  "timestamp": "2024-06-07T15:30:00",
  "note": "Feeling pretty good today!"
}
```

## Sample user item

```json
{
  "user_id": "user123",
  "first_name": "John",
  "last_name": "Doe",
  "age": 30,
  "telephone": "123-456-7890",
  "city": "New York"
}
```
