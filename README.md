# HOMECORE — Smart Home API

## Description

HOMECORE is a smart home API developed with Python, FastAPI, SQLAlchemy and SQLite. It allows users to manage rooms, devices and events. The API supports listing devices, filtering results, retrieving devices by ID, viewing events, generating room summaries and creating new devices.

## Requirements

- Python 3.10 or later
- FastAPI
- Uvicorn
- SQLAlchemy

## Installation

1. Clone the repository:

```bash
git clone <repository-url>
```

2. Open the project folder:

```bash
cd HOMECORE
```

3. Create a virtual environment:

```bash
py -m venv .venv
```

4. Activate the virtual environment:

```bash
.venv\Scripts\activate
```

5. Install the dependencies:

```bash
pip install -r requirements.txt
```

## Database Setup

The project uses SQLite to store information about rooms, devices and events. The database contains three tables:

- `rooms`: stores room information.
- `devices`: stores device information and their associated rooms.
- `events`: stores events associated with devices.

To create the database tables and load the initial data, run:

```bash
py seed.py
```

The seed script loads the initial data and avoids duplicating the initial records when executed again.

## Run the Project

Start the API using Uvicorn:

```bash
py -m uvicorn main:app --reload
```

Once the server is running, the API is available at:

`http://127.0.0.1:8000`

The interactive API documentation is available at:

`http://127.0.0.1:8000/docs`

Keep the terminal open while using the API.

## Authentication

The API uses API key authentication through the `X-API-Key` HTTP header.

To access the protected endpoints through Swagger UI:

1. Open `http://127.0.0.1:8000/docs`.
2. Click **Authorize**.
3. Enter the configured API key.
4. Click **Authorize** and close the dialog.

Requests without a valid API key return HTTP `401 Unauthorized`.

For security reasons, API keys