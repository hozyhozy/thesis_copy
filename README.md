# frame-resonance

Etudo & Yoon (2024, *ISR*) "Ontology-Based Information Extraction for Labeling Radical Online Content
Using Distant Supervision"의 핵심 아이디어를 최소한의 파이썬으로 재구성한 것.
논문 코드는 공개돼 있지 않아 본문·보충자료의 설명과 식을 그대로 옮겼다.

```
frame_resonance/
  ontology.py   TBO  - (domain, relation, range) 트리플을 claimant별 서랍에 보관
  frp.py        FRDS - 관계별 문자 2-gram cosine의 가중평균 → Frame Resonance Profile 벡터
  rbc.py        FRDS - Rule-Based Classifier 점수
demo.py         AQAP 기준 vs 유저 두 명 비교 예시
tests/          pytest
```

구현하지 않은 것: FDS(NER + RE, 텍스트에서 트리플 뽑기). 트리플은 직접 넣는다.
논문에 없는 것: `Triple.timestamp` — 시퀀스 연구용으로 비워 둔 자리.

```bash
python demo.py
pytest
```

## 왜 이렇게 생겼나 (한 줄씩)

* 관계가 edge가 아니라 `Triple` 객체인 이유: 누가 말했는지(claimant)와 언제(timestamp)를 붙이려면
  주장 자체가 사물이어야 한다 (논문의 reification 결정).
* `FrameStore.instance(claimant)`가 논문의 "TBO instance" (SPARQL 결과)이다.
* `frp()`는 기준 서랍과 대상 서랍을 **같은 관계끼리** 비교한 점수 목록 = 해석 가능한 벡터.
* 가중치는 논문 Table D8 값 그대로 (직관으로 정한 값이라 학습된 것이 아님).
