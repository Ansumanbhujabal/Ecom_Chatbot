# Chatbot Backend with FastAPI

## Features
- Dynamic product recommendations from FakeStore API.
- Simulated bargaining logic with dynamic discounts.
- Order tracking functionality.
- Multilingual support (English and Hindi).

## Prerequisites
- Python 3.8 or later
- Dialogflow account

## Setup
1. Clone this repository.
2. Install dependencies:
   ```bash
   pip install fastapi uvicorn requests
   pip install -r requirements.txt
   uvicorn main:app --reload --port 5000
   ngrok http 5000  (As Dialogflow only supports https)
