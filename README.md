
# URL Shortener Service

## Overview

This project is a URL Shortener Service built using FastAPI, SQLAlchemy, and Alembic for migrations. It allows users to shorten URLs, generate QR codes for the shortened URLs, and track the number of transitions for each URL.

## Installation

### Requirements

- Python 3.10+
- FastAPI
- SQLAlchemy
- Alembic
- qrcode
- python-dotenv

### Setup

1. Clone the repository:
```bash
git clone https://github.com/Rebel21/links_shorter.git
cd links_shorter
```
2. Create and activate virtual environment
```bash
python3 -m venv venv
```
On Windows, run:
```bash 
venv\Scripts\activate
```
On Unix or MacOS, run:
```bash 
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```


## Running the Application

### in Docker
To run an application in Docker, it must be installed - https://docs.docker.com/engine/install/
1. Build containers
```bash
docker compose build
```
2. Run containers
```bash
docker compose up
```


### Locally

This project uses Alembic for database migrations. To run migrations, run this command:

```bash
alembic upgrade head
```

Start the FastAPI server:
```bash
uvicorn main:app --reload
```

The service should now be running on `http://localhost:8000/` (or your configured host and port).

