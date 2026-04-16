from datetime import datetime
import pandas as pd


def build_markdown(grouped):
    today = datetime.now().strftime("%d %B %Y")
    lines = [f"# Global News Wrap - {today}", ""]

    for section, stories in grouped.items():
        if not stories:
            continue

        lines.append(f"## {section}")
        lines.append("")

        for story in stories[:25]:
            source = story.get("source", "Unknown source")
            title = story.get("title", "Untitled")
            link = story.get("link", "")
            published_at = story.get("published_at", "")
            stamp = f" ({published_at})" if published_at else ""

            lines.append(f"- [{title}]({link}) — {source}{stamp}")

        lines.append("")

    return "\n".join(lines)


def save_outputs(stories, markdown):
    df = pd.DataFrame(stories)
    df.to_csv("output/latest.csv", index=False)

    with open("output/latest.md", "w", encoding="utf-8") as f:
        f.write(markdown)