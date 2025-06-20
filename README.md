# Real-Time Review Ingestion & Moderation Microservice

## Project Overview

This microservice provides a REST API to moderate incoming reviews for spam, profanity, and other policy violations. It demonstrates systems/backend engineering, streaming, machine learning moderation, and microservices skills relevant to real-world platforms (e.g., Yelp, Trustpilot).

## Tools and Technologies

- Python 3
- FastAPI
- Uvicorn
- Docker (planned)
- Google Cloud Platform: Cloud Run, Pub/Sub, Firestore/BigQuery (planned)
- scikit-learn and other ML libraries (planned)
- Streamlit, Grafana, or similar for dashboards (planned)

## Features

### Implemented

- Accept reviews in real time via a REST API endpoint (`POST /reviews`).
    - Example review JSON payload:
      ```json
      {
        "user_id": "u1",
        "business_id": "b1",
        "text": "This place is a scam!"
      }
      ```
- Run each review through basic moderation logic (e.g., banned words, length checks).
- Return a moderation decision: **accept**, **flag**, or **reject**.

### Planned

- Add advanced automated checks for spam, fraud, sentiment, and hate speech using ML and external rules.
- Queue flagged reviews for human moderation.
- Store reviews and moderation outcomes in a database or search index.
- Expose review data for downstream services (e.g., search, analytics).
- Provide a real-time dashboard of moderation activity and health.
- Deploy service to Google Cloud Platform using Docker and Cloud Run.

## How to Run Locally

1. **Install dependencies:**
    ```
    pip install -r requirements.txt
    ```

2. **Run the API:**
    ```
    uvicorn app.main:app --reload
    ```

3. **Submit a review** (with `curl` or via Swagger UI at [http://localhost:8000/docs](http://localhost:8000/docs)):
    ```
    curl -X POST "http://localhost:8000/reviews" -H "Content-Type: application/json" -d '{"user_id": "u1", "business_id": "b1", "text": "This place is a scam!"}'
    ```

## Project Structure

```
review-moderation-microservice/
│
├── app/
│   ├── main.py
│   └── models.py
│   └── moderation.py
├── requirements.txt
├── README.md
├── .gitignore
└── tests/
```

## Roadmap

- [ ] Add machine learning-based profanity and spam detection
- [ ] Integrate with a queue for human moderation
- [ ] Store reviews and outcomes in a persistent database
- [ ] Deploy the service to Google Cloud Platform (Cloud Run)
- [ ] Add analytics and dashboard for moderation activity

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.