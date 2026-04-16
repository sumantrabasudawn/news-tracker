from collections import defaultdict


def classify_story(story, sections):
    text = f"{story.get('title', '')} {story.get('summary', '')}".lower()
    matched = []

    for section, keywords in sections.items():
        for keyword in keywords:
            if keyword.lower() in text:
                matched.append(section)
                break

    return matched if matched else ["Other"]


def group_stories(stories, sections):
    grouped = defaultdict(list)

    for story in stories:
        labels = classify_story(story, sections)
        for label in labels:
            grouped[label].append(story)

    return dict(grouped)