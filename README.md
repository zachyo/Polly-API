# Polly-API: FastAPI Poll Application

A simple poll application built with FastAPI, SQLite, and JWT authentication. Users can register, log in, create, retrieve, vote on, and delete polls. The project follows best practices with modular code in the `api/` directory.

## Features

- User registration and login (JWT authentication)
- Create, retrieve, and delete polls
- Add options to polls (minimum of two options required)
- Vote on polls (authenticated users only)
- View poll results with vote counts
- SQLite database with SQLAlchemy ORM
- Modular code structure for maintainability

## Project Structure

```
Polly-API/
├── api/
│   ├── __init__.py
│   ├── auth.py
│   ├── database.py
│   ├── models.py
│   ├── routes.py
│   └── schemas.py
├── main.py
├── requirements.txt
└── README.md
```

## Setup Instructions

1. **Clone the repository**

```bash
git clone <your-repo-url>
cd Polly-API
```

2. **Set up a Python virtual environment (recommended)**

A virtual environment helps isolate your project dependencies.

- **On Unix/macOS:**

  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

- **On Windows (cmd):**

  ```cmd
  python -m venv venv
  venv\Scripts\activate
  ```

- **On Windows (PowerShell):**

  ```powershell
  python -m venv venv
  .\venv\Scripts\Activate.ps1
  ```

To deactivate the virtual environment, simply run:

```bash
deactivate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Set environment variables (optional)**

Create a `.env` file in the project root to override the default secret key:

```
SECRET_KEY=your_super_secret_key
```

5. **Run the application**

```bash
uvicorn main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

## API Usage

### 1. Register a new user

- **Endpoint:** `POST /register`
- **Body:**

```json
{
  "username": "yourusername",
  "password": "yourpassword"
}
```

### 2. Login

- **Endpoint:** `POST /login`
- **Body (form):**
  - `username`: yourusername
  - `password`: yourpassword
- **Response:**

```json
{
  "access_token": "...",
  "token_type": "bearer"
}
```

### 3. Get all polls

- **Endpoint:** `GET /polls`
- **Query params:** `skip` (default 0), `limit` (default 10)
- **Authentication:** Not required

### 4. Create a poll

- **Endpoint:** `POST /polls`
- **Headers:** `Authorization: Bearer <access_token>`
- **Body:**

```json
{
  "question": "Your poll question",
  "options": ["Option 1", "Option 2"]
}
```

### 5. Get a specific poll

- **Endpoint:** `GET /polls/{poll_id}`
- **Authentication:** Not required

### 6. Vote on a poll

- **Endpoint:** `POST /polls/{poll_id}/vote`
- **Headers:** `Authorization: Bearer <access_token>`
- **Body:**

```json
{
  "option_id": 1
}
```

### 7. Get poll results

- **Endpoint:** `GET /polls/{poll_id}/results`
- **Authentication:** Not required
- **Response:**

```json
{
  "poll_id": 1,
  "question": "Your poll question",
  "results": [
    {
      "option_id": 1,
      "text": "Option 1",
      "vote_count": 3
    },
    {
      "option_id": 2,
      "text": "Option 2",
      "vote_count": 1
    }
  ]
}
```

### 8. Delete a poll

- **Endpoint:** `DELETE /polls/{poll_id}`
- **Headers:** `Authorization: Bearer <access_token>`

## Interactive API Docs

Visit [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) for the interactive Swagger UI.

## License

MIT License
