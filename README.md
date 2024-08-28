# aibots-intern

## Overview

This backend component allows CRUD operations on conversations, integrates with OpenAI's GPT-3.5-turbo for generating responses, and stores conversation data in a MongoDB database. All data is anonymized before storage.

## Tech Stack
- Python 3.8+
- FastAPI
- Beanie (MongoDB ODM)
- MongoDB
- Docker
- OpenAI Python Client

## Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/ongbernice/aibots-intern.git
   cd aibots-intern

2. **Create and activate a virtual environment**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate

3. **Install dependencies**:
    ```bash
    pip install -r requirements.txt

4. **Start MongoDB using Docker**:
    ```bash
    docker-compose up -d

5. **Run the FastAPI app**:
    ```bash
    uvicorn app.main:app --reload

6. **Access the API documentation**: Open your browser and navigate to `http://127.0.0.1:8000/docs`.

## Docker Setup
1. **Build the Docker image**:
   ```bash
   docker build -t aibots-intern .

2. **Run the Docker container**:
    ```bash
    docker-compose up --build



