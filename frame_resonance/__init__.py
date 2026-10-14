"""Minimal re-implementation of the TBO / FDS / FRDS idea from
Etudo & Yoon (2024), Information Systems Research 35(1).

Only the part that matters for ontology-embedding work is implemented:
  ontology.py  - triples (domain, relation, range) indexed by claimant   (TBO)
  frp.py       - Frame Resonance Profile: per-relation cosine similarity (FRDS step 1)
  rbc.py       - Rule-Based Classifier score                            (FRDS step 2)
The text-extraction part (FDS: NER + RE) is NOT implemented; triples are given directly.
"""
from .ontology import Triple, FrameStore
from .frp import frp, resonance_score
from .rbc import rbc_score
