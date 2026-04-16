from rapidfuzz import fuzz


def dedupe_stories(stories, threshold=88):
    unique = []

    for story in stories:
        is_duplicate = False

        for kept in unique:
            score = fuzz.ratio(story["title"].lower(), kept["title"].lower())

            if score >= threshold:
                is_duplicate = True
                break

        if not is_duplicate:
            unique.append(story)

    return unique