# Real-Time Review Ingestion & Moderation Microservice

## Project Overview

This microservice provides an end-to-end solution for real-time review ingestion and automated moderation, designed for platforms that handle user-generated content (e.g., Yelp, Trustpilot).

Key features and workflow include:

- **Data Sources & Preparation:**  
  The moderation models are trained on large-scale, real-world datasets: the [Jigsaw Toxic Comment Classification Challenge](https://www.kaggle.com/c/jigsaw-toxic-comment-classification-challenge) and the [YouTube Spam Collection Dataset](https://www.kaggle.com/datasets/uciml/youtube-spam-collection). Extensive data cleaning, unification, and splitting scripts are included to ensure high-quality, labeled data for supervised learning.

- **Machine Learning & Rule-Based Moderation:**  
  Multiple moderation backends are supported, including classic ML (TF-IDF + Logistic Regression), transformer-based moderation (TinyBERT), and rule-based profanity/spam detection. Models are trained and evaluated using the cleaned datasets and can be retrained using provided scripts.

- **End-to-End Moderation Pipeline:**  
  - **Ingestion:** Reviews are submitted in real-time via a REST API.
  - **Moderation:** Each review is processed using the selected moderation backend.
  - **Event Streaming:** Moderation decisions and metadata are published to Kafka for downstream analytics and processing.
  - **Persistence:** All reviews and moderation results are stored in a relational database (SQLite).
  - **Live Analytics:** A Streamlit dashboard visualizes moderation activity and system health in real-time, powered by live event and database updates.

- **DevOps & Portability:**  
  The microservice is containerized with Docker, supports rapid local development with a bundled `docker-compose.yml` for Kafka/Zookeeper, and is easily deployable to Google Cloud Run or other cloud environments.

This project demonstrates practical skills in backend and systems engineering, data science, machine learning operations, and real-time analytics, providing a reference architecture for scalable, production-grade content moderation pipelines.

## Tools and Technologies

- **Python 3**
- **FastAPI** (API framework)
- **Uvicorn** (ASGI server)
- **Docker** (containerization)
- **Google Cloud Platform**: Cloud Run, Artifact Registry, Compute Engine, Cloud Storage
- **scikit-learn** (ML), **TinyBERT** (transformer moderation), and other ML libraries
- **better_profanity** (rule-based moderation)
- **SQLAlchemy & SQLite** (database)
- **Streamlit** (real-time analytics dashboard)
- **Streamlit Autorefresh** (for live dashboard updates)
- **Matplotlib** (dashboard plots)

## Data & Model Preparation

The machine learning moderation models in this project were trained using data from both the [Jigsaw Toxic Comment Classification Challenge](https://www.kaggle.com/c/jigsaw-toxic-comment-classification-challenge) and the [YouTube Spam Collection Dataset](https://www.kaggle.com/datasets/uciml/youtube-spam-collection) (or similar).

**These raw datasets are NOT included in the repository due to licensing and size constraints. You must download them manually before running the preprocessing or training scripts.**

### Workflow to Prepare Data and Train Models

1. **Download datasets:**  
   - [Jigsaw Toxic Comment Classification Challenge (Kaggle)](https://www.kaggle.com/c/jigsaw-toxic-comment-classification-challenge/data)
   - [YouTube Spam Collection Dataset (Kaggle)](https://www.kaggle.com/datasets/uciml/youtube-spam-collection)

2. **Preprocess and split:**
   - Run `clean_and_split_jigsaw.py` to clean and split the Jigsaw dataset into train/val/test.
   - Run `combine_and_split_youtube.py` to process and split the YouTube dataset.
   - Run `merge_jigsaw_youtube.py` to merge the splits from both datasets for unified training.

3. **(Optional) Explore and analyze:**
   - Use `data_exploration.py` to understand label distributions and text statistics.

4. **Train moderation models:**
   - **TF-IDF + Logistic Regression model:**  
     Run `tfidf_logreg_moderator.py` to train and evaluate the classic ML moderation model. This will save the trained model as `app/ml_moderation_model.joblib` and produce reports and confusion matrix plots in the `docs/` directory.
   - **TinyBERT transformer model:**  
     Run `tinyBert_moderator.py` to train and evaluate the transformer-based moderation model. This will save the model and tokenizer to a directory such as `tinyBert_moderation_model_run2`, and output evaluation metrics and confusion matrices.

See the individual script files for parameter options and usage instructions.

> **Note:**  
> You must download the original CSV files and place them in the correct location as expected by the scripts.

## Features

- Accept reviews in real time via a REST API endpoint (`POST /reviews`).
    - Example review JSON payload:
      ```json
      {
        "user_id": "u1",
        "business_id": "b1",
        "text": "This place is a scam!"
      }
      ```
- Advanced moderation logic with multiple selectable backends:
    - **custom**: Rule-based spam/profanity detection.
    - **better_prof**: Uses the [better_profanity](https://github.com/suragch/better-profanity) library (extensive wordlist).
    - **ml**: Machine learning moderation (tf-idf + logistic regression).
    - **tinybert**: Transformer-based moderation using TinyBERT.
- Select moderation method via the `method` query param (default: `better_prof`).
    - Example: `POST /reviews?method=ml`
- Return a moderation decision: **accept**, **flag**, or **reject** (with reason).
- Store all reviews and moderation results in a SQL database (SQLite).
- Expose `/moderation-events` endpoint to list moderation events for analytics and downstream processing.
- Provide a real-time dashboard of moderation activity and health via Streamlit (`dashboard.py`). Auto-refreshes for live analytics.
- Publish moderation events to Kafka for downstream processing (optional).
- Containerized with Docker for portability.
- Deployable to Google Cloud Run.
- Export moderation events to CSV for downstream analysis or archival (see `export_to_csv.py`).

## Testing

This project includes unit and integration tests demonstrating both API reliability and custom moderation logic correctness.

- **tests/test_api.py:**  
  Uses FastAPI’s `TestClient` and dependency overrides to test API endpoints in-memory, mock the database and Kafka dependencies, and check core moderation decisions (`accept`, `flag`, `reject`) for different review texts.

- **tests/test_moderation.py:**  
  Contains unit tests for core moderation logic, including the spam detection functions and both custom and rule-based moderation backends.

Run all tests using [pytest](https://docs.pytest.org/en/stable/):
```bash
pytest tests/
```
You can use these tests to verify your changes or as examples for further test development.

## How to Run Locally

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Kafka Setup (Required for Event Streaming & Dashboard)

This app publishes moderation events to Kafka (by default) and expects a running Kafka broker at `localhost:9092`.

**You must start a local Kafka and Zookeeper instance before running the API and analytics.**

- **Using Docker Compose (recommended):**
    ```bash
    docker-compose up -d zookeeper kafka
    ```
    (A ready-to-use `docker-compose.yml` with `zookeeper` and `kafka` services is included in this repository.)

- **Or manually (if you have Kafka installed):**
    ```bash
    # Start Zookeeper (in one terminal)
    bin/zookeeper-server-start.sh config/zookeeper.properties

    # Start Kafka broker (in another terminal)
    bin/kafka-server-start.sh config/server.properties
    ```

> **To run without Kafka** (e.g., for quick testing), set the environment variable:
> ```bash
> export DISABLE_KAFKA=true
> ```

### 3. Initialize the database
```bash
python -m app.create_tables
```

### 4. Run the API
```bash
uvicorn app.main:app --reload
```

### 5. (Optional, but recommended) Run the Moderation Events Consumer

To process moderation events for analytics and dashboard updates, run:
```bash
python kafka_consumer.py
```
This will read moderation events from Kafka and update `stats.json`/`cumul_stats.json` for the real-time dashboard.

### 6. Submit a review
Use `curl` or Swagger UI ([http://localhost:8000/docs](http://localhost:8000/docs)):
```bash
curl -X POST "http://localhost:8000/reviews?method=ml" \
     -H "Content-Type: application/json" \
     -d '{"user_id": "u1", "business_id": "b1", "text": "This place is a scam!"}'
```
- Valid values for `method`: `custom`, `better_prof`, `ml`, `tinybert`

### 7. List moderation events
```bash
curl "http://localhost:8000/moderation-events?limit=10"
```

### 8. Run the real-time dashboard
```bash
streamlit run dashboard.py
```
- The dashboard auto-refreshes and displays live moderation analytics.
- Requires `stats.json` and `cumul_stats.json` to be updated by the Kafka consumer.

### 9. Export moderation events to CSV
```bash
python export_to_csv.py
```
- Exports all moderation events to `moderation_events_export.csv`.

## Running with Docker

1. **Build the Docker image:**
    ```bash
    docker build -t review-moderation-api:latest .
    ```

2. **Run the container:**
    ```bash
    docker run -p 8080:8080 review-moderation-api:latest
    ```
    The API will be available at [http://localhost:8080/docs](http://localhost:8080/docs).

## Deploying to Google Cloud Run

> **Note:** Ensure you have enabled the Artifact Registry and Cloud Run APIs, and configured gcloud for your project.

1. **Create an Artifact Registry repository** (once per project):
    ```bash
    gcloud artifacts repositories create REPO_NAME \
      --repository-format=docker \
      --location=REGION \
      --description="Docker repo for moderation API"
    ```
    Replace `REPO_NAME` and `REGION` as appropriate.

2. **Authenticate Docker to Artifact Registry** (once per workstation):
    ```bash
    gcloud auth configure-docker REGION-docker.pkg.dev
    ```

3. **Build, tag, and push the image:**
    ```bash
    docker build -t review-moderation-api:latest .
    docker tag review-moderation-api:latest REGION-docker.pkg.dev/PROJECT_ID/REPO_NAME/review-moderation-api:latest
    docker push REGION-docker.pkg.dev/PROJECT_ID/REPO_NAME/review-moderation-api:latest
    ```

4. **Deploy to Cloud Run:**
    ```bash
    gcloud run deploy review-moderation-api \
      --image REGION-docker.pkg.dev/PROJECT_ID/REPO_NAME/review-moderation-api:latest \
      --platform managed \
      --region REGION \
      --allow-unauthenticated
    ```

    Replace `PROJECT_ID`, `REPO_NAME`, and `REGION` with your actual values.

> **Environment variable:**  
> Set `DISABLE_KAFKA=true` if you want to disable Kafka integration during deployment.

## API Endpoints

- `POST /reviews`: Submit a review for moderation.
    - Query parameter: `method` (`custom`, `better_prof`, `ml`, `tinybert`)
- `GET /moderation-events`: List moderation events (for analytics/downstream processing).
    - Query parameter: `limit` (number of events)
- `GET /`: Health check / welcome message.

## Project Structure

```
.
├── Dockerfile
├── LICENSE
├── README.md
├── requirements.txt
├── docker-compose.yml
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── models.py
│   ├── custom_moderation.py
│   ├── better_prof_moderation.py
│   ├── tfidf_logreg_moderation.py
│   ├── tfidf_logreg_moderator.py
│   ├── tinyBert_moderation.py
│   ├── tinyBert_moderator.py
│   ├── bert_moderator.py
│   ├── database.py
│   ├── db_models.py
│   ├── db_session.py
│   ├── create_tables.py
│   ├── kafka_client.py
│   ├── text_preprocessing.py
│   ├── clean_and_split_jigsaw.py
│   ├── combine_and_split_youtube.py
│   ├── data_exploration.py
│   ├── merge_jigsaw_youtube.py
├── dashboard.py
├── export_to_csv.py
├── send_batch_reviews.py
├── kafka_consumer.py
├── docs/
│   ├── classification_report_test_tfidf_logreg.txt
│   ├── classification_report_tinyBert_2.txt
│   ├── classification_report_val_tfidf_logreg.txt
│   ├── config.json
│   ├── confusion_matrix_test_tfidf_logreg.png
│   ├── confusion_matrix_test_tinyBert_2.png
│   ├── confusion_matrix_val_tfidf_logreg.png
│   └── trainer_state.json
├── tests/
│   ├── __init__.py
│   ├── test_api.py
│   └── test_moderation.py
```
- **app/**: All backend code (API, models, moderation logic, DB, utilities)
- **dashboard.py**: Real-time moderation dashboard (Streamlit)
- **export_to_csv.py**: Export moderation DB to CSV
- **docs/**: Reports, confusion matrices, model artifacts
- **tests/**: Unit and integration tests

> **Note:**  
> - Large datasets (CSV files), trained model files/directories (e.g., `ml_moderation_model.joblib`, `tinyBert_moderation_model/`), SQLite databases, and Python cache directories are **not** included in the repository and are ignored via `.gitignore`.  
> - To use the project fully, see Setup instructions for how to generate or download these files as needed.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.