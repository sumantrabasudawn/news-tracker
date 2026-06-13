import os
import requests

token = os.getenv("X_BEARER_TOKEN")

headers = {
    "Authorization": f"Bearer {token}"
}

url = "https://api.x.com/2/tweets/search/recent"

params = {
    "query": "artificial intelligence lang:en -is:retweet",
    "max_results": 10,
    "tweet.fields": "created_at,public_metrics"
}

response = requests.get(
    url,
    headers=headers,
    params=params,
    timeout=30
)

print("STATUS:", response.status_code)
print(response.text[:1000])
