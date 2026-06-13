# ==========================================
# AION JUDGEMENT ENGINE v1
# ==========================================

NARRATIVE_STATES = [
    "Dormant",
    "Emerging",
    "Accelerating",
    "Polarising",
    "Institutionalising",
    "Crisis",
    "Normalising",
    "Resolution"
]

TRANSITION_MATRIX = {

    "Dormant": {
        "Emerging": 0.45,
        "Dormant": 0.40,
        "Resolution": 0.15
    },

    "Emerging": {
        "Accelerating": 0.55,
        "Polarising": 0.25,
        "Normalising": 0.20
    },

    "Accelerating": {
        "Polarising": 0.35,
        "Institutionalising": 0.30,
        "Crisis": 0.25,
        "Normalising": 0.10
    },

    "Polarising": {
        "Institutionalising": 0.40,
        "Crisis": 0.30,
        "Normalising": 0.20,
        "Resolution": 0.10
    },

    "Institutionalising": {
        "Resolution": 0.35,
        "Normalising": 0.35,
        "Crisis": 0.15,
        "Institutionalising": 0.15
    },

    "Crisis": {
        "Normalising": 0.35,
        "Institutionalising": 0.30,
        "Resolution": 0.20,
        "Crisis": 0.15
    },

    "Normalising": {
        "Resolution": 0.45,
        "Dormant": 0.30,
        "Emerging": 0.15,
        "Normalising": 0.10
    },

    "Resolution": {
        "Dormant": 0.60,
        "Normalising": 0.25,
        "Emerging": 0.15
    }
}


def get_markov_forecast(current_state):

    if current_state not in TRANSITION_MATRIX:

        return {
            "current_state": current_state,
            "next_state": "Unknown",
            "markov_score": 0
        }

    transitions = TRANSITION_MATRIX[current_state]

    next_state = max(
        transitions,
        key=transitions.get
    )

    return {
    "current_state": current_state,
    "most_plausible_next_state": next_state,
    "markov_score": transitions[next_state],
    "judgement": (
        f"The issue is currently in a '{current_state}' narrative state. "
        f"The most plausible short-term movement is toward '{next_state}', "
        f"with a Markov plausibility score of {transitions[next_state]}."
    )
}

# ==========================================
# TEST BLOCK
# ==========================================

if __name__ == "__main__":

    result = get_markov_forecast("Emerging")

    print(result)