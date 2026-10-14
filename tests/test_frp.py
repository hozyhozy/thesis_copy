from frame_resonance import Triple, FrameStore, frp, rbc_score


def test_identical_claimants_score_one():
    s = FrameStore()
    for c in ("A", "B"):
        s.add(Triple(c, "occupies", "America", "Iraq"))
    assert abs(frp(s, "A", "B")["occupies"] - 1.0) < 1e-9


def test_missing_relation_is_zero():
    s = FrameStore()
    s.add(Triple("A", "occupies", "America", "Iraq"))
    s.add(Triple("B", "besieges", "Israel", "West Bank"))
    assert frp(s, "A", "B")["occupies"] == 0.0


def test_rbc_penalises_empty_relations():
    full = {"a": .6, "b": .6}
    half = {"a": .6, "b": .0}
    assert rbc_score(full) > rbc_score(half)
