import feedparser
import pandas as pd
import re
import html
import urllib.parse
import sys
import os

from src.fetch_x import fetch_x_posts
from datetime import datetime
from dateutil import parser

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from judgement_engine import get_markov_forecast


POSITIVE_WORDS = [
    "growth", "profit", "surge", "wins", "record", "strong", "expansion",
    "investment", "partnership", "approval", "order", "launch", "positive",
    "rises", "gain", "boost", "robust", "opportunity"
]

NEGATIVE_WORDS = [
    "loss", "fraud", "probe", "raid", "fall", "decline", "risk", "concern",
    "delay", "controversy", "allegation", "negative", "crisis", "default",
    "warning", "penalty", "lawsuit", "complaint", "protest"
]


def clean_text(text):
    if not text:
        return ""
    text = re.sub(r"<.*?>", "", text)
    text = html.unescape(text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def classify_sentiment(text):
    text_l = text.lower()
    pos = sum(1 for w in POSITIVE_WORDS if w in text_l)
    neg = sum(1 for w in NEGATIVE_WORDS if w in text_l)

    if pos > neg:
        return "Positive"
    if neg > pos:
        return "Negative"
    return "Neutral"


def classify_narrative_state(score, total, negative, positive):
    if total == 0:
        return "Dormant"

    negative_ratio = negative / total
    positive_ratio = positive / total

    if total <= 3:
        return "Dormant"

    if score <= -50 and negative_ratio >= 0.5:
        return "Crisis"

    if score <= -30:
        return "Polarising"

    if total >= 20 and abs(score) < 30:
        return "Accelerating"

    if total >= 8:
        return "Emerging"

    if positive_ratio >= 0.5 and score >= 30:
        return "Normalising"

    return "Emerging"


def fetch_google_news(query, limit=20):
    encoded = urllib.parse.quote(query)
    url = f"https://news.google.com/rss/search?q={encoded}&hl=en-IN&gl=IN&ceid=IN:en"

    parsed = feedparser.parse(url)
    stories = []

    for entry in parsed.entries[:limit]:
        title = clean_text(entry.get("title", ""))
        summary = clean_text(entry.get("summary", ""))
        link = entry.get("link", "")
        published_raw = entry.get("published") or entry.get("updated") or ""

        try:
            published_at = parser.parse(published_raw).strftime("%d %b %Y, %H:%M")
        except Exception:
            published_at = ""

        text = f"{title} {summary}"
        sentiment = classify_sentiment(text)

        if title:
            stories.append({
                "title": title,
                "summary": summary[:250],
                "link": link,
                "published_at": published_at,
                "sentiment": sentiment,
                "source": "Google News"
            })

    return stories


def generate_sentiment_report(query):
    stories = fetch_google_news(query)
    x_posts = fetch_x_posts(query, limit=20)

    for post in x_posts:
        sentiment = classify_sentiment(post["text"])
        stories.append({
            "title": post["text"][:120],
            "summary": post["text"][:250],
            "link": "",
            "published_at": post.get("created_at", ""),
            "sentiment": sentiment,
            "source": "X",
            "engagement": post.get("engagement", 0)
        })

    total = len(stories)
    positive = sum(1 for s in stories if s["sentiment"] == "Positive")
    negative = sum(1 for s in stories if s["sentiment"] == "Negative")
    neutral = sum(1 for s in stories if s["sentiment"] == "Neutral")

    score = 0
    if total:
        score = round(((positive - negative) / total) * 100)

    if score >= 30:
        mood = "Positive"
        action = "Amplify the favourable narrative and identify credible proof points."
    elif score <= -30:
        mood = "Negative"
        action = "Escalate monitoring, prepare corrective messaging and identify reputational risk triggers."
    else:
        mood = "Mixed / Neutral"
        action = "Monitor the narrative and look for emerging directional signals."

    narrative_state = classify_narrative_state(score, total, negative, positive)
    markov = get_markov_forecast(narrative_state)

    report = {
        "query": query,
        "generated_at": datetime.now().strftime("%d %B %Y, %I:%M %p"),
        "total": total,
        "positive": positive,
        "negative": negative,
        "neutral": neutral,
        "score": score,
        "mood": mood,
        "narrative_state": narrative_state,
        "most_plausible_next_state": markov["most_plausible_next_state"],
        "markov_score": markov["markov_score"],
        "markov_judgement": markov["judgement"],
        "action": action,
        "stories": stories
    }

    return report