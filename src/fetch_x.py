import os
import requests

def fetch_x_posts(query, limit=20):
    token = os.getenv("X_BEARER_TOKEN")

    if not token:
        return []

    url = "https://api.x.com/2/tweets/search/recent"

    headers = {
        "Authorization": f"Bearer {token}"
    }

    params = {
        "query": f'{query} lang:en -is:retweet',
        "max_results": min(limit, 100),
        "tweet.fields": "created_at,public_metrics,lang"
    }

    try:
        r = requests.get(url, headers=headers, params=params, timeout=30)

        if r.status_code != 200:
            print("X API error:", r.status_code, r.text[:500])
            return []

        data = r.json().get("data", [])

        posts = []

        for item in data:
            metrics = item.get("public_metrics", {})

            engagement = (
                metrics.get("like_count", 0)
                + metrics.get("retweet_count", 0) * 2
                + metrics.get("reply_count", 0) * 2
                + metrics.get("quote_count", 0) * 3
            )

            posts.append({
                "source": "X",
                "text": item.get("text", ""),
                "created_at": item.get("created_at", ""),
                "likes": metrics.get("like_count", 0),
                "retweets": metrics.get("retweet_count", 0),
                "replies": metrics.get("reply_count", 0),
                "quotes": metrics.get("quote_count", 0),
                "engagement": engagement
            })

        return posts

    except Exception as e:
        print("X fetch failed:", e)
        return []
