import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from pgmpy.inference import VariableElimination
from bayesian.model import model

infer = VariableElimination(model)

def show(title: str, evidence: dict):
    q = infer.query(variables=["C"], evidence=evidence)
    print("\n" + "=" * 80)
    print(title)
    print("Evidence:", evidence)
    for s, p in zip(q.state_names["C"], q.values):
        print(f"  P(C={s:<6}) = {p:.3f}")

# Route-specific scenarios: Bayshore -> Expo
# Requirement: >=5 scenarios, >=3 explicit Today vs Future tests (same evidence except M)
scenarios = [
    # Pair 1: Clear evening baseline, normal service
    ("1A Today: clear evening + normal (Bayshore→Expo baseline)",
     {"W":"clear","T":"evening","D":"weekday","M":"today","S":"normal"}),
    ("1B Future: clear evening + normal (same evidence except Mode)",
     {"W":"clear","T":"evening","D":"weekday","M":"future","S":"normal"}),

    # Pair 2: Rainy evening + reduced service
    ("2A Today: rainy evening + reduced",
     {"W":"rainy","T":"evening","D":"weekday","M":"today","S":"reduced"}),
    ("2B Future: rainy evening + reduced (same evidence except Mode)",
     {"W":"rainy","T":"evening","D":"weekday","M":"future","S":"reduced"}),

    # Pair 3: Weekend afternoon + normal service
    ("3A Today: weekend afternoon + normal",
     {"W":"clear","T":"afternoon","D":"weekend","M":"today","S":"normal"}),
    ("3B Future: weekend afternoon + normal (same evidence except Mode)",
     {"W":"clear","T":"afternoon","D":"weekend","M":"future","S":"normal"}),

    # Extra scenario: disrupted service near corridor
    ("4 Future: disrupted service near corridor",
     {"W":"clear","T":"evening","D":"weekday","M":"future","S":"disrupted"}),

    # Extra scenario: Clear morning weekday + normal service
    ("5 Today: clear morning weekday + normal",
     {"W":"clear","T":"morning","D":"weekday","M":"today","S":"normal"}),
]

if __name__ == "__main__":
    print("Starting scenarios...")
    print(f"Model loaded: {model}")
    print(f"Infer created: {infer}")
    print(f"Number of scenarios: {len(scenarios)}")
    for title, ev in scenarios:
        print(f"\nRunning: {title}")
        show(title, ev)
    print("\nAll scenarios complete!")

