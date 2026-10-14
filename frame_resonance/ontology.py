from dataclasses import dataclass
from collections import defaultdict

# FrameRelation classes from TBO (Appendix D). Four kinds:
#   Practice  - what the enemy does      (diagnostic frames)
#   Action    - what adherents are told to do (prognostic / motivational)
#   Forecast  - predictions
#   Label     - characterisations
RELATIONS = {
    "Practice": ["besieges", "colonizes", "conductsLethalActAgainst", "conductsViolenceAgainst",
                 "economicallyExploits", "isComplicitWith", "occupies", "oppresses", "slanders",
                 "terrorizes", "unlawfullyDetains", "unwantedlyPresent"],
    "Action":   ["assassinate", "boycottCountry", "forciblyExpelPeople", "generateAnxiety",
                 "inflictEconomicHarm", "performLethalActAgainstPeople", "popularUprisingAgainst",
                 "sabotage", "takeUpArmsAgainst"],
    "Forecast": ["demiseOfProtectedGroup", "victoryOverEnemy"],
    "Label":    ["hasEnemy", "hasNegativeCharacteristic"],
}
ALL_RELATIONS = {r for rs in RELATIONS.values() for r in rs}


@dataclass(frozen=True)
class Triple:
    """One frame = one 'card'. The relation is reified (it is a thing, not an edge),
    so it can carry who said it (claimant) and, if you extend it, when (timestamp)."""
    claimant: str
    relation: str
    domain: str   # left argument  (who does it)
    range: str    # right argument (to whom / what)
    timestamp: str | None = None   # not in the paper - add it for sequence work

    def __post_init__(self):
        if self.relation not in ALL_RELATIONS:
            raise ValueError(f"unknown FrameRelation: {self.relation}")


class FrameStore:
    """The 'drawer': triples grouped by claimant. A claimant's drawer is the
    paper's 'TBO instance' (baseline if it is an organisation, ephemeral if a user)."""

    def __init__(self):
        self._by_claimant: dict[str, list[Triple]] = defaultdict(list)

    def add(self, *triples: Triple):
        for t in triples:
            self._by_claimant[t.claimant].append(t)

    def claimants(self):
        return list(self._by_claimant)

    def instance(self, claimant: str) -> dict[str, dict[str, list[str]]]:
        """{relation: {'domain': [...], 'range': [...]}} for one claimant.
        This is what the paper's SPARQL query returns."""
        out: dict[str, dict[str, list[str]]] = defaultdict(lambda: {"domain": [], "range": []})
        for t in self._by_claimant.get(claimant, []):
            out[t.relation]["domain"].append(t.domain)
            out[t.relation]["range"].append(t.range)
        return dict(out)
