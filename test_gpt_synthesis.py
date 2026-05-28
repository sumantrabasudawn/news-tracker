from src.gpt_synthesis import synthesize_aion_brief

sample_events = [
    {
        "title": "Oil prices rise amid renewed West Asia tensions",
        "theme": "Energy Security",
        "source": "Sample",
        "impact_score": 8
    },
    {
        "title": "India accelerates transmission investments for renewable integration",
        "theme": "Power Infrastructure",
        "source": "Sample",
        "impact_score": 9
    }
]

brief = synthesize_aion_brief(sample_events)

print("\n===== AION TEST BRIEF =====\n")
print(brief)