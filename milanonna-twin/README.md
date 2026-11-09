# milanonna-twin — 밀라논나(장명숙) 디지털 트윈 데이터셋

유튜버 밀라논나의 공개 인터뷰·영상 발화를 질문–답(QA) 형태로 정리해, LLM 디지털 트윈을 만들고 평가하기 위한 데이터와 코드. (Celebrity Twin 연구 / 마케팅 인텔리전스 수업)

## 현재 상태 (2026-11-09)

| 항목 | 수치 |
|---|---|
| 처리한 영상 | 37편 (자기 채널 24 + 외부 인터뷰·방송 13) |
| QA 문항 | **665** |
| 최종 분할 | **Train 381 / Holdout 270 / Retest 14** |
| Holdout 중 2025년 이후(엄격) 부분집합 | 139 |
| 복원(오탈자 정리) 완료 | 24문항 (2편) — 나머지는 진행 예정 |
| 보류 | `l2gWsx7TolQ` (한국어 자막 대신 영어 번역 자막이 들어 있음) |

## 폴더

```
milanonna-twin/
├─ README.md                 이 문서
├─ WORKLOG.md                작업 일지 (날짜순, 앞으로 여기에 이어 적음)
├─ docs/
│  ├─ 분할기준_및_통합기록.md   Train/Holdout/Retest 분할 규칙과 근거, 필드 설명, 영상별 분할표
│  ├─ 영상별_분할표.csv         영상 ID·시기·근거·확신도·분할
│  └─ 참고자료/
│     ├─ 페르소나_사실_참고자료.md   트윈 프롬프트용 배경 사실 (생애 연표·가족·가치관·취향, 출처 표시)
│     └─ [최종]언론기사_모음.md      기사 4건 요약 (QA에서는 제외)
├─ data/
│  ├─ qa_merged/             통합 QA — [QA통합]전체 / Train / Holdout / Retest .json
│  └─ qa_by_video/           영상별 QA json (폴더는 시간 기준 Train/Holdout; 문항 단위 최종 분할은 통합 json의 split 필드)
└─ scripts/                  처리 코드 (아래 "재현" 참고)
```

영상 자막 정리본(`[최종]*.md`, 발화 전문)은 저장소에 올리지 않음. 로컬 `~/Desktop/밀라논나/최종데이터/`에만 보관.

## 데이터 형식

`data/qa_merged/*.json`의 각 문항:

| 필드 | 뜻 |
|---|---|
| `id`, `video_id`, `title`, `channel`, `year` | 출처 |
| `split` | 최종 분할: `Train` / `Holdout` / `Retest` |
| `split_time` | 시간 기준 분할 (복귀 2024-08 이후 = Holdout) |
| `split_strict` | 엄격 기준 분할 (2025-01-01 이후 = Holdout) |
| `overlap`, `overlap_detail` | 시간상 Holdout 후보가 Train과 겹치는지: `same_question` / `shared_anecdote` / `novel` |
| `type` | `interview` = 실제 질문(진행자·사연·자막), `derived` = 발언에서 도출한 질문 |
| `question`, `question_original` | 정리한 질문 / 실제 질문 원문 |
| `answer_raw` | 자동자막 원문 (오탈자 그대로, 수정하지 않음) |
| `answer`, `restored`, `restore_note` | 복원본과 근거. `restored=false`면 원문과 동일 |
| `start`, `end`, `topic` | 영상 내 구간(mm:ss), 주제 |
| `dup_group` | 여러 영상에서 반복된 같은 질문 묶음 |

## 분할 설계 요약

1. **시간 기준**: 활동 중단(2022-07)~복귀(2024-08) 공백을 단절점으로, 시즌 1 발화 = Train, 시즌 2 발화 = Holdout 후보.
2. **겹침 제거**: Holdout 후보 중 Train에 같은 질문이 있으면 `Retest`(본인 일관성 = human ceiling 계산 전용), Train에 이미 있는 인생 일화(삼풍, 86 아시안게임, 78년 유학, 돌체 동기, 명품 유치, 염색 중단 등 23개 패턴)가 답에 들어 있으면 `Train`으로 이동, 둘 다 아니면 `Holdout`.
3. **강건성**: `split_strict`(2025년 이후)로 Holdout의 부분집합을 잘라 같은 결과가 나오는지 확인. 누수 통제의 핵심은 날짜가 아니라 G0 베이스라인(페르소나 없이 "밀라논나라면"만 묻는 조건)과의 차이.

자세한 근거와 버린 대안은 `docs/분할기준_및_통합기록.md`.

## 재현

스크립트는 Mac의 Claude 작업 VM(`~/work`)에서 실행하며, 연결 폴더 `~/mnt/youtube_transcripts`(자막 .vtt/.md)와 `~/mnt/최종데이터`(출력)를 전제로 함.

```
dedup.py        VTT 롤링 자막 중복 제거 → lines/{vid}.json
dump.py         정리된 자막을 45초 단위로 출력 (화자 경계·QA 구간을 정할 때 읽음)
specs_*.py      영상별 설정: 화자 경계(bounds), QA 구간(qa), 채널·날짜·메모
run_specs.py    specs_x.py + specs/{vid}.skel.json → specs/{vid}.json → build2.py 실행
build2.py       [최종]md + [QA]json 생성 (답 구간 유일성·화자·겹침 검증)
merge_split.py  영상별 QA 통합, 시간 기준 분할, 분할표 CSV
apply_restore.py restore/*.json 의 복원본 반영
reassign.py     Train 겹침에 따라 Holdout 후보를 Train/Holdout/Retest로 재배정 (항상 마지막)
```

새 영상 추가 순서: 자막 md/vtt 넣기 → skel 생성 → `dump.py`로 읽고 `specs_X.py` 작성 → `run_specs.py specs_X` → `merge_split.py`의 `DATES`에 시기 추가 → `merge_split.py` → `apply_restore.py` → `reassign.py`.

## 화자 코드

M = 밀라논나 · H/I/K/P = 진행자·제작진·김미경·제작자 · R = 사연·질문 낭독 · S = 아들 · X = 예고·내레이션·기타. 답(answer)은 항상 M 발화에서만 뽑음.
