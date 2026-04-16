from pathlib import Path
import yaml

from fetch_news import fetch_feed
from dedupe import dedupe_stories
from classify import group_stories
from generate_wrap import build_markdown, save_outputs


BASE_DIR = Path(__file__).resolve().parents[1]
CONFIG_DIR = BASE_DIR / "config"
OUTPUT_DIR = BASE_DIR / "output"


def load_yaml(path):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def ensure_dirs():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def main():
    ensure_dirs()

    feeds_config = load_yaml(CONFIG_DIR / "feeds.yaml")
    topics_config = load_yaml(CONFIG_DIR / "topics.yaml")

    all_stories = []

    for feed in feeds_config["feeds"]:
        all_stories.extend(fetch_feed(feed["name"], feed["url"]))

    deduped = dedupe_stories(all_stories)
    grouped = group_stories(deduped, topics_config["sections"])
    markdown = build_markdown(grouped)
    save_outputs(deduped, markdown)

    print(f"Fetched {len(all_stories)} stories")
    print(f"Saved {len(deduped)} deduplicated stories")
    print("Done. Output written to output/latest.md and output/latest.csv")


if __name__ == "__main__":
    main()