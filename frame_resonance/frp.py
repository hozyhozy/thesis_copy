import math
from collections import Counter
from .ontology import FrameStore, ALL_RELATIONS

# Domain / range weights from Appendix D, Table D8 (set "by intuition" in the paper).
WEIGHTS = {
    "isComplicitWith": (.5, .5), "besieges": (.5, .5), "colonizes": (.6, .4),
    "conductsLethalActAgainst": (.5, .5), "conductsViolenceAgainst": (.5, .5),
    "economicallyExploits": (.6, .4), "occupies": (.5, .5), "oppresses": (.6, .4),
    "slanders": (.6, .4), "terrorizes": (.6, .4), "unlawfullyDetains": (.4, .6),
    "unwantedlyPresent": (.6, .4), "hasEnemy": (.0, 1.0), "victoryOverEnemy": (.4, .6),
    "popularUprisingAgainst": (.5, .5), "takeUpArmsAgainst": (.4, .6),
    "performLethalActAgainstPeople": (.5, .5), "hasNegativeCharacteristic": (.6, .4),
}
DEFAULT_W = (.5, .5)


def char_ngrams(strings, n=2) -> Counter:
    """Term-frequency vector over character n-grams of all strings (paper: n = 2)."""
    c = Counter()
    for s in strings:
        s = s.lower()
        for i in range(len(s) - n + 1):
            c[s[i:i + n]] += 1
    return c


def cosine(a: Counter, b: Counter) -> float:
    if not a or not b:
        return 0.0
    dot = sum(a[k] * b[k] for k in a if k in b)
    na = math.sqrt(sum(v * v for v in a.values()))
    nb = math.sqrt(sum(v * v for v in b.values()))
    return dot / (na * nb)


def resonance_score(base: dict, other: dict, relation: str) -> float:
    """One element rs_i of the FRP: weighted cosine of domain and range vectors
    for one FrameRelation. 0 if either side has no instance of the relation."""
    if relation not in base or relation not in other:
        return 0.0
    wd, wr = WEIGHTS.get(relation, DEFAULT_W)
    d = cosine(char_ngrams(base[relation]["domain"]), char_ngrams(other[relation]["domain"]))
    r = cosine(char_ngrams(base[relation]["range"]), char_ngrams(other[relation]["range"]))
    return wd * d + wr * r


def frp(store: FrameStore, baseline: str, target: str, relations=None) -> dict[str, float]:
    """Frame Resonance Profile of `target` against `baseline`.
    Returns {relation: rs_i}; the values in a fixed order are the embedding vector."""
    base, other = store.instance(baseline), store.instance(target)
    rels = relations or sorted(base)           # N = relations active in the baseline
    return {rel: resonance_score(base, other, rel) for rel in rels}
