import math


def rbc_score(profile: dict[str, float], alpha: float = 0.0) -> float:
    """Rule-Based Classifier score (paper, p. 214):

        RBC = ln( sum(rs) - alpha*sum(rs) + 1 ) / ( 1 + (N - ||theta||) )

    N        = number of relations in the profile
    ||theta|| = number of non-zero resonance scores
    Numerator rewards total similarity, denominator penalises empty relations.
    Paper labels a persona as resonating when RBC > 0.2 (tuned on training data)."""
    scores = list(profile.values())
    n = len(scores)
    theta = sum(1 for s in scores if s > 0)
    total = sum(scores)
    return math.log(total - alpha * total + 1) / (1 + (n - theta))
