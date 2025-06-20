# Review Moderation Microservice

This microservice provides a REST API to moderate incoming reviews for spam, profanity, and other policy violations.

## Features

- Accepts review submissions via POST `/reviews`
- Runs each review through simple moderation logic (banned words, length)
- Returns moderation decision: accept, flag, or reject

## How to Run Locally

1. Install dependencies:
    ```
    pip install -r requirements.txt
    ```

2. Run the API:
    ```
    uvicorn app.main:app --reload
    ```

3. Submit a review (example with `curl` or use Swagger UI at [http://localhost:8000/docs](http://localhost:8000/docs)):
    ```
    curl -X POST "http://localhost:8000/reviews" -H "Content-Type: application/json" -d '{"user_id": "u1", "business_id": "b1", "text": "This place is a scam!"}'
    ```
