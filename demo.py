"""Toy run: AQAP baseline vs. two forum users (values are illustrative, not from the paper)."""
from frame_resonance import Triple, FrameStore, frp, rbc_score

store = FrameStore()

# Baseline "drawer": triples that FDS would have extracted from AQAP propaganda
store.add(
    Triple("AQAP", "performLethalActAgainstPeople", "Mujahideen", "Crusaders"),
    Triple("AQAP", "performLethalActAgainstPeople", "Believers", "Zionists"),
    Triple("AQAP", "performLethalActAgainstPeople", "Afghans", "America"),
    Triple("AQAP", "occupies", "America", "Afghanistan"),
    Triple("AQAP", "occupies", "Crusaders", "Iraq"),
    Triple("AQAP", "hasEnemy", "enemy", "Crusaders"),
    Triple("AQAP", "hasEnemy", "enemy", "Apostates"),
    Triple("AQAP", "takeUpArmsAgainst", "Ummah", "West"),
)

# User A: writes in the same frames
store.add(
    Triple("user_A", "performLethalActAgainstPeople", "Mujahideen", "Zionists"),
    Triple("user_A", "performLethalActAgainstPeople", "Ummah", "Crusaders"),
    Triple("user_A", "occupies", "America", "Iraq"),
    Triple("user_A", "hasEnemy", "enemy", "Crusaders"),
    Triple("user_A", "takeUpArmsAgainst", "Muslims", "West"),
)

# User B: talks about something else (animal rights)
store.add(
    Triple("user_B", "economicallyExploits", "Corporations", "Animals"),
    Triple("user_B", "hasEnemy", "enemy", "Vivisectors"),
    Triple("user_B", "sabotage", "Liberationists", "Laboratories"),
)

for user in ["user_A", "user_B"]:
    profile = frp(store, baseline="AQAP", target=user)
    print(f"\nFRP(AQAP vs {user})")
    for rel, rs in profile.items():
        print(f"  {rel:32s} {rs:.3f}")
    print(f"  RBC = {rbc_score(profile):.3f}  ->", "resonates" if rbc_score(profile) > 0.2 else "no")
