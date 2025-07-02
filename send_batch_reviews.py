import requests
import time

reviews = [
    {
        "user_id": "usr1",
        "business_id": "bus1",
        "text": "The food was amazing!",
        "method": "custom"
    },
    {
        "user_id": "usr2",
        "business_id": "bus2",
        "text": "Service was slow but the staff were friendly.",
        "method": "better_prof"
    },
    {
        "user_id": "usr3",
        "business_id": "bus2",
        "text": "Buy now!!! Buy now!!! Limited offer!!!",
        "method": "ml"
    },
    {
        "user_id": "usr1",
        "business_id": "bus3",
        "text": "What a sh*tty place, worst experience ever.",
        "method": "better_prof"
    },
    {
        "user_id": "usr1",
        "business_id": "bus3",
        "text": "What a sh**ty place, worst experience ever.",
        "method": "tinybert"
    },
    {
        "user_id": "usr2",
        "business_id": "bus1",
        "text": "This place sucks, total scam!",
        "method": "tinybert"
    },
    {
        "user_id": "usr3",
        "business_id": "bus3",
        "text": "Great atmosphere and delicious drinks.",
        "method": "ml"
    },
    {
        "user_id": "usr1",
        "business_id": "bus2",
        "text": "Click this link for a prize: http://spam.com",
        "method": "custom"
    },
    {
        "user_id": "usr2",
        "business_id": "bus3",
        "text": "Absolutely loved the desserts here!",
        "method": "tinybert"
    },
    {
        "user_id": "usr3",
        "business_id": "bus1",
        "text": "F*** this place!",
        "method": "better_prof"
    },
    {
        "user_id": "usr1",
        "business_id": "bus1",
        "text": "Best service! Best service! Best service! Best service!",
        "method": ""  # No method, should use default (better_prof)
    }
]

base_url = "http://34.38.188.116:8080/reviews" # Using my VM's external API

for idx, review in enumerate(reviews, 1):
    method = review.pop("method")
    params = {"method": method} if method else {}
    try:
        response = requests.post(base_url, params=params, json=review)
        print(f"Review {idx} (method={method or 'default'}): {review}")
        print(f"Status: {response.status_code}, Response: {response.text}\n")
    except Exception as e:
        print(f"Error submitting review {idx}: {e}")
    time.sleep(1)  # Wait 1 second between each submission (for demo)