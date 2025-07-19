# Haven-Backend (FastAPI + MongoDB)

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Make sure MongoDB is running and update your connection info in `util/db.py` if needed.

## Run the app

```bash
uvicorn main:app --reload
```

## API Endpoints

### Mood

```json
{
  "user_id": "user123",
  "mood": 7,
  "timestamp": "2024-06-07T15:30:00",
  "note": "Feeling pretty good today!"
}
```

### User

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

### Meditation

```json
{
  "user_id": "user123",
  "timestamp": "2024-06-07T15:30:00",
  "duration": "00:30:00",
  "comment": "Morning meditation session"
}
```

### NCS Music

```json
{
  "title": "NCS - Fade"
}
```

## Static Files

Static files in the `static/` folder are served at `/static/` path.

## Project Structure

```
Haven-Backend/
├── main.py              # FastAPI app entry point
├── util/db.py           # MongoDB connection
├── routes/              # API route handlers
│   ├── mood.py
│   ├── user.py
│   ├── meditation.py
│   └── ncsmusic.py
└── static/              # Static files
```
