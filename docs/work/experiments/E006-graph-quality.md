---
id: E006
title: Graph quality
created: 2026-11-23
---

# E006 · Graph quality

## Question

How good is the extracted graph itself: claim precision, recall and F1, attribution and time fields, and how often a restatement counts as independent evidence? Serves all three research questions as the error source of the graph channel.

## Design

| Item | Value |
| --- | --- |
| Benchmarks and splits | Annotated segments from T024; controlled sequences with gold graphs |
| Systems and baselines | Primary writer at the main configuration |
| Metrics | Claim precision, recall, F1; shape conformance and retries; whether the cited span entails the claim; attribution and time accuracy; answer coverage upper bound |
| Seeds and budget | TBD in config |
| Config | `configs/experiments/E006-graph-quality.yaml` |

## Acceptance

- [ ] Every number traces to a run report.

## Runs

| Run ID | Date | Status | Code SHA | Report |
| --- | --- | --- | --- | --- |
| E006-20261128T001447Z-0046 | 2026-11-28 | completed (provisional; probe: segment-wise extraction, Qwen3-8B T022 writer) | `aaee362e54ca141efa3bb685e42cbf4fb0ebef65` | `runs/E006/artifacts/w01-E006/E006/E006-20261128T001447Z-0046/report.yaml` |
| E006-20261128T002555Z-50c6 | 2026-11-28 | completed (predicate-matcher check) | `f2b69d7b6de65607820c2b22afaa3a7db5192e52` | `runs/E006/artifacts/w01-E006/E006/E006-20261128T002555Z-50c6/report.yaml` |
| E006-20261128T002604Z-514e | 2026-11-28 | completed (provisional; score of E006-20261128T001447Z-0046) | `f2b69d7b6de65607820c2b22afaa3a7db5192e52` | `runs/E006/artifacts/w01-E006/E006/E006-20261128T002604Z-514e/report.yaml` |
| E006-20261128T002611Z-896e | 2026-11-28 | completed (comparison; score of T022-20261126T214758Z-613e, LoCoMo segments) | `f2b69d7b6de65607820c2b22afaa3a7db5192e52` | `runs/E006/artifacts/w01-E006/E006/E006-20261128T002611Z-896e/report.yaml` |
| E006-20261128T082608Z-21cb | 2026-11-28 | completed (ingest, main configuration, LoCoMo dev; upstream for read runs) | `684d15bbcc1904e76cb5ec7e5ccad7e4de84ffb7` | `runs/E006/artifacts/w02-E006/E006/E006-20261128T082608Z-21cb/report.yaml` |
| E006-20261128T083248Z-24b4 | 2026-11-28 | completed (read smoke, budget 1024, from 21cb; not scored) | `bd232a93a172881f6a49565ed4502ddddcd23e76` | `runs/E006/artifacts/w02-E006/E006/E006-20261128T083248Z-24b4/report.yaml` |
| E006-20261128T083416Z-afed | 2026-11-28 | completed (probe: segment-wise extraction, main writer, 40 segments) | `b0dc4f9d123332888536eef5687b05bebd99e27e` | `runs/E006/artifacts/w02-E006/E006/E006-20261128T083416Z-afed/report.yaml` |
| E006-20261128T083416Z-cef6 | 2026-11-28 | completed (formal: LoCoMo full-history score of 21cb) | `b0dc4f9d123332888536eef5687b05bebd99e27e` | `runs/E006/artifacts/w02-E006/E006/E006-20261128T083416Z-cef6/report.yaml` |
| E006-20261128T083924Z-ac34 | 2026-11-28 | completed (formal: segment-wise score of afed) | `0a90160acbdb0ab2564406bcaad39603c97aa661` | `runs/E006/artifacts/w02-E006/E006/E006-20261128T083924Z-ac34/report.yaml` |
| E006-20261128T083910Z-be52 | 2026-11-28 | completed (formal: answer coverage, LoCoMo, of 21cb) | `0a90160acbdb0ab2564406bcaad39603c97aa661` | `runs/E006/artifacts/w02-E006/E006/E006-20261128T083910Z-be52/report.yaml` |
| E006-20261128T083758Z-b04e | 2026-11-28 | completed (probe: controlled sequences, main writer, 5 sequences) | `5ef3c24fbb28287c67ac2988dc672cb92fcdb33e` | `runs/E006/artifacts/w02-E006/E006/E006-20261128T083758Z-b04e/report.yaml` |
| E006-20261128T084019Z-66ac | 2026-11-28 | completed (superseded by cda5) | `0a90160acbdb0ab2564406bcaad39603c97aa661` | `runs/E006/artifacts/w02-E006/E006/E006-20261128T084019Z-66ac/report.yaml` |
| E006-20261128T084058Z-cda5 | 2026-11-28 | completed (formal: controlled-sequence score of b04e) | `1615967a47c453e6ef812bfdc2cdacd90041ae9d` | `runs/E006/artifacts/w02-E006/E006/E006-20261128T084058Z-cda5/report.yaml` |
| E006-20261128T083145Z-6288 | 2026-11-28 | completed (ingest, main configuration, LongMemEval-S dev main-text strata, 67 histories) | `bd232a93a172881f6a49565ed4502ddddcd23e76` | `runs/E006/artifacts/w02-E006/E006/E006-20261128T083145Z-6288/report.yaml` |
| E006-20261128T084142Z-ee92 | 2026-11-28 | completed (ingest, main configuration, LongMemEval-S dev other 31 histories) | `bd232a93a172881f6a49565ed4502ddddcd23e76` | `runs/E006/artifacts/w02-E006/E006/E006-20261128T084142Z-ee92/report.yaml` |
| E006-20261128T093835Z-e4b6 | 2026-11-28 | completed (formal: answer coverage, LongMemEval-S main strata, of 6288) | `d3572cea5b9318770ca481545ed872d76822812e` | `runs/E006/artifacts/w02-E006/E006/E006-20261128T093835Z-e4b6/report.yaml` |
| E006-20261128T092653Z-6d20 | 2026-11-28 | completed (formal: answer coverage, LongMemEval-S other strata, of ee92) | `d3572cea5b9318770ca481545ed872d76822812e` | `runs/E006/artifacts/w02-E006/E006/E006-20261128T092653Z-6d20/report.yaml` |
| E006-20261128T111659Z-5f3a | 2026-11-28 | completed (superseded before scoring: controlled-sequence extraction with the rejected E007 iteration 3; never scored) | `f839d3ecfa7c04492892362ec9058f6406fd745a` | `runs/E006/artifacts/w02-E007/E006/E006-20261128T111659Z-5f3a/report.yaml` |
| E006-20261128T111659Z-824d | 2026-11-28 | completed (superseded before scoring: segment-wise extraction with the rejected E007 iteration 3; never scored) | `f839d3ecfa7c04492892362ec9058f6406fd745a` | `runs/E006/artifacts/w02-E007/E006/E006-20261128T111659Z-824d/report.yaml` |
| E006-20261128T112035Z-b09d | 2026-11-28 | completed (probe: controlled sequences, final writer prompt of the E007 ending round) | `511d851af5a416cd4c5ace83e0c1dae0a422dd58` | `runs/E006/artifacts/w02-E007/E006/E006-20261128T112035Z-b09d/report.yaml` |
| E006-20261128T112035Z-fa8b | 2026-11-28 | completed (probe: segment-wise extraction, final writer prompt, 40 segments) | `511d851af5a416cd4c5ace83e0c1dae0a422dd58` | `runs/E006/artifacts/w02-E007/E006/E006-20261128T112035Z-fa8b/report.yaml` |
| E006-20261128T112541Z-9386 | 2026-11-28 | completed (formal: controlled-sequence score of b09d, final writer prompt) | `511d851af5a416cd4c5ace83e0c1dae0a422dd58` | `runs/E006/artifacts/w02-E007/E006/E006-20261128T112541Z-9386/report.yaml` |
| E006-20261128T112541Z-d4d2 | 2026-11-28 | completed (formal: segment-wise score of fa8b, final writer prompt) | `511d851af5a416cd4c5ace83e0c1dae0a422dd58` | `runs/E006/artifacts/w02-E007/E006/E006-20261128T112541Z-d4d2/report.yaml` |
| E006-20261128T113433Z-87ea | 2026-11-28 | completed (formal: LoCoMo full-history score of ingest E007-20261128T112542Z-c8d3, final writer prompt) | `511d851af5a416cd4c5ace83e0c1dae0a422dd58` | `runs/E006/artifacts/w02-E007/E006/E006-20261128T113433Z-87ea/report.yaml` |
| E006-20261128T113435Z-aa0b | 2026-11-28 | completed (formal: answer coverage, LoCoMo, of ingest E007-20261128T112542Z-c8d3) | `511d851af5a416cd4c5ace83e0c1dae0a422dd58` | `runs/E006/artifacts/w02-E007/E006/E006-20261128T113435Z-aa0b/report.yaml` |

## Results

Provisional only: the writer is the T022 configuration (Qwen3-8B), not the main configuration E007 will fix, and the gold is two agent annotators pending human review. Precision and recall are bounds (lower–upper): precision against core units (both agents) to all units, recall against all units to core units. Loose = same message, subject and object (T024 normalisation) and an equivalent predicate (lexical, then the Qwen3-8B judge). Scorer code `f2b69d7`.

| Run | Benchmark | Writer claims | Gold core / all | Level | Precision | Recall | F1 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| E006-20261128T002604Z-514e (segment-wise) | all | 611 | 426 / 675 | anchor | 0.311–0.365 | 0.330–0.446 | 0.320–0.402 |
| | | | | loose | 0.160–0.182 | 0.164–0.230 | 0.162–0.203 |
| | | | | strict | 0.048–0.052 | 0.047–0.068 | 0.047–0.059 |
| | LoCoMo | 343 | 182 / 262 | loose | 0.140–0.163 | 0.214–0.264 | 0.169–0.202 |
| | LongMemEval-S | 268 | 244 / 413 | loose | 0.187–0.205 | 0.133–0.205 | 0.155–0.205 |
| E006-20261128T002611Z-896e (T022 full-history run) | LoCoMo | 428 | 182 / 262 | anchor | 0.173–0.206 | 0.336–0.407 | 0.228–0.273 |
| | | | | loose | 0.068–0.077 | 0.126–0.159 | 0.088–0.104 |

Other measures of run E006-20261128T002604Z-514e (all segments): the cited span anchors in the message text for 523 of 611 claims (0.856); the Qwen3-8B judge finds the span entails the claim for 0.828 of 523 (0.941 of 101 loose-matched, 0.801 of 422 unmatched; 0 invalid); on loose matches with core units the fields agree for function 0.897 (n 97), certainty 0.891 (92), speaker 0.969 (98), polarity, report mode and derived 1.0, time expression 0.837 (92) but 0.444 of the 27 where the gold sets one, and the writer sets `valid_from` on none (gold sets it on 12). Catch-all predicates are 8 of 611 claims (precision 0.375); 152 distinct predicates. Entity labels: 2 of 507 are first-person (`my fam`, `my dad`), 34 (0.067) have a content word that is not in the segment or context text (mostly abstract nouns typed as entities); on loose matches the writer's subject equals the gold name in 0.937 (n 111) and an entity object in 0.743 (n 105). Ending-evidence check: 10 ending stances dropped on units with segment messages and no gold ending stance exists in the 40 segments, so the false-drop rate is 0 of 10 by construction and the check's recall cannot be measured on this sample. The full-history run (896e) has 44 `felt` claims (10% catch-all, precision 0) against 1.3% in the segment-wise run, and its span entailment rate is 0.655 (n 377).

### Formal run, main configuration (2026-11-28)

Writer Qwen3-32B with `configs/common/writer.yaml` (session units) and the default `grace` engine. Gold: the two T024 agent label files (human review pending), so precision and recall are bounds: precision against core units (both agents) up to all units, and recall against all units up to core units. Loose matching: same message, subject and object (T024 normalisation with the possessive head rule of 2026-11-28), and an equivalent predicate (lexical, then the Qwen3-8B judge). LoCoMo is scored on the full-history graph and LongMemEval-S segment-wise (decisions of PR #148). The provisional rows above use the earlier name matcher and are not rescored.

| Run | Benchmark (reading) | Writer claims | Gold core / all | Level | Precision | Recall | F1 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| E006-20261128T083416Z-cef6 | LoCoMo (full history, 16 segments) | 229 | 181 / 263 | anchor | 0.345–0.371 | 0.323–0.437 | 0.334–0.401 |
| | | | | loose | 0.214–0.236 | 0.205–0.271 | 0.210–0.252 |
| | | | | strict | 0.079–0.083 | 0.072–0.099 | 0.075–0.091 |
| E006-20261128T083924Z-ac34 | LongMemEval-S (segment-wise, optimistic bound, 24 segments) | 153 | 221 / 436 | anchor | 0.503–0.706 | 0.248–0.348 | 0.332–0.467 |
| | | | | loose | 0.353–0.477 | 0.167–0.244 | 0.227–0.323 |
| | LoCoMo (segment-wise, for the gap) | 199 | 181 / 263 | loose | 0.246–0.276 | 0.209–0.271 | 0.226–0.274 |

LoCoMo segment-vs-full gap with the main writer: reading segment-wise raises loose precision by 0.03–0.04 (0.246–0.276 against 0.214–0.236) and leaves recall unchanged (0.209–0.271 against 0.205–0.271). The gap is much smaller than with the provisional Qwen3-8B writer (0.140–0.163 against 0.068–0.077, earlier matcher). The LongMemEval-S segment-wise numbers are therefore an optimistic bound. If the LoCoMo gap carries over, they overstate precision by a few points.

Other measures:

- **LoCoMo full history (cef6), spans:** the cited span anchors in the message for 214 of 229 claims (0.935). The judge finds the span entails the claim for 0.729 of 214: 0.923 of 52 matched, 0.667 of 162 unmatched, 0 invalid.
- **LoCoMo full history (cef6), fields on 49 loose core matches:**
  - agreeing: function 0.939, certainty 0.938 (n 48), speaker 0.980, polarity, report mode and derived 1.0;
  - time expression 0.804 (n 46), but 0.579 of the 19 where the gold sets one;
  - `valid_from`: 0 of the 9 where the gold sets it.
- **LoCoMo full history (cef6), predicates and entities:**
  - 46 distinct predicates, 1 catch-all claim;
  - the most used predicates have low precision: `hasGoal` 26 claims, precision 0.038; `hasHabit` and `hasHobby` 16 each, 0.25;
  - entity labels: 0 pronouns; 23 of 125 (0.184) have a content word that is not in the segment text (mostly abstract nouns typed as entities, e.g. `safe space for self-expression`);
  - on loose matches the subject equals the gold name in 1.0 (n 54) and the object in 0.755 (n 49);
  - restatements: 7 of 20 gold stances are attributed by the writer (0.35).
- **Segment-wise, all 40 segments (ac34):** span anchored 0.932 (328 of 352); entailed 0.893 (0.960 matched, 0.853 unmatched). Fields on loose core matches: function 0.941 (n 101), time expression 0.885 (n 96), 0.655 where the gold sets one, `valid_from` 0 of 10. Entity labels not in text 0.060 (n 331).
- **Controlled sequences (cda5)** against their gold graphs: 5 sequences of the T015 model-rendered development set, one per family at rho 10, 1,000 messages; extraction run `E006-20261128T083758Z-b04e`.
  - Claim occurrences: anchor precision 0.771, recall 0.830; loose precision 0.729, recall 0.785, F1 0.756 (245 matched; 312 gold, 336 writer). Loose precision ranges from 0.581 (flight-travel) to 0.902 (hotel-stay).
  - Fields on loose matches: function 0.747, polarity 0.996.
  - Per gold predicate (recall): user facts are found well (`speaksLanguage` 0.929 of 70, `worksIn` 0.922 of 51, `livesIn` 0.839 of 56). Task and offer predicates are not: `selectedService` 0.267 of 30, `scheduledArrival`, `scheduledDeparture`, `pickupTime`, `viewingTime`, `seatPreference` and `apartmentSize` all 0 of 2–3.
  - Endings: 9 of 35 gold endings committed and matched (recall 0.257); 9 of 17 writer endings match (precision 0.529). Of the 26 missed endings, 20 have a negative writer attribution on the ended claim at the ending message but no supersession ("I don't speak Dutch anymore" becomes a negative stance, and the claim stays current in the store).
  - Ending-evidence check: 5 ending stances dropped (all `ended_without_evidence`), 1 of them a false drop. The false-drop rate is 0.2 (n 5, too small for an estimate), and 1 gold ending was lost to a drop.
- **Answer-coverage upper bound, LoCoMo (be52)**, on the full-history graph, 308 questions:
  - evidence messages: at least one carries a claim for 0.894 of 302 questions, all of them for 0.752;
  - every content word of the reference occurs in the claims of the evidence messages for 0.179 of 302, at least half of them for 0.305;
  - every content word occurs anywhere in the history's graph for 0.247 of 308;
  - the test is lexical, so restated dates or paraphrases count as not covered.
- **Answer-coverage upper bound, LongMemEval-S**, on the full-history ingest graphs:
  - main-text strata (`e4b6`, 67 questions): evidence messages carry a claim for 1.0 of 65 (all of them 0.892); answer words in the evidence claims 0.154 (at least half 0.262); anywhere in the graph 0.358. Per stratum (in evidence claims / anywhere): knowledge-update 0.286 / 0.400 (n 15), temporal-reasoning 0.231 / 0.385 (26), multi-session 0.0 / 0.308 (26; the answers are counts and aggregates).
  - other 31 histories (`6d20`): evidence messages carry a claim for 0.5 of 30. Per stratum: single-session-assistant 1 of 11 (the writer extracts little from assistant turns), preference 3 of 6, single-session-user 0.846 of 13.

### At the final writer prompt (E007 ending round, 2026-11-28)

The writer prompt was revised once more for endings (E007 Log and Results, "Ending round"); everything else as in the formal runs above. The rows below supersede them as E006's numbers at the final writer configuration; the earlier rows stay as the record of the previous prompt.

| Run | Benchmark (reading) | Writer claims | Level | Precision | Recall | F1 |
| --- | --- | --- | --- | --- | --- | --- |
| E006-20261128T113433Z-87ea (ingest `E007-20261128T112542Z-c8d3`) | LoCoMo (full history, 16 segments) | 205 | anchor | 0.322–0.3561 | 0.2776–0.3646 | 0.2982–0.3603 |
| | | | loose | 0.2146–0.2341 | 0.1825–0.2431 | 0.1973–0.2385 |
| | | | strict | 0.0683–0.0829 | 0.0646–0.0773 | 0.0664–0.08 |
| E006-20261128T112541Z-d4d2 | all 40 segments (segment-wise) | 409 | loose | 0.2836–0.335 | 0.196–0.2886 | 0.2318–0.3101 |
| | LoCoMo (segment-wise) | 213 | loose | 0.23–0.2441 | 0.1977–0.2707 | 0.2126–0.2567 |
| | LongMemEval-S (segment-wise, optimistic bound) | 196 | loose | 0.3418–0.4337 | 0.195–0.3032 | 0.2483–0.3569 |

- **Controlled sequences (`9386`, extraction `b09d`)**, same five sequences as `cda5`: endings 17 of 35 matched (recall 0.4857, was 0.2571), 17 of 50 writer endings match (precision 0.34, was 0.5294); negated only 12 (was 20). Ending-evidence check: 11 drops, 2 false (rate 0.1818), 2 gold endings lost to drops. Claim occurrences: loose precision 0.659, recall 0.6442 (201 matched; 312 gold, 305 writer), was 0.7292 / 0.7853; anchor 0.7607 / 0.7436. Fields on loose matches: function 0.7413, polarity 0.995. 33 of the 111 unmatched gold occurrences are `worksIn` (was 4 of 67): the writer uses `jobTitle` for a field of work.
- **Answer-coverage upper bound, LoCoMo (`aa0b`)**: evidence messages carry a claim for 0.8675 of 302 questions (all of them 0.7185); every content word of the reference in the evidence claims 0.1887, at least half 0.3146; anywhere in the graph 0.25 of 308.
- LongMemEval-S ingests at the final prompt: E007 runs `E007-20261128T112648Z-1453` and `E007-20261128T112653Z-065d` (E007 Runs); their answer coverage is not rescored here.

## Conclusion

Pending.

## Log

- 2026-11-23: created from the full project DAG.
- 2026-11-26: design inputs from the T022 writer smoke runs (PR #126, #129; runs under `runs/T022/artifacts/manager/T022/`), recorded by the integration owner on user decisions: measure both missed and spurious extraction against gold or human labels (writer scale trades precision for coverage: Qwen3-32B wrote 474 claims and left 45/136 units empty, Qwen3-8B wrote 957 with more noise); report quality per predicate, including catch-all predicates (no program-side blacklist is applied); measure the false-drop rate of the writer's evidence check on ended stances; separate writer errors from planner (T023) and fragment-selection errors in graph-channel misses (graph-channel R@20 was about 0.1 with either writer on LoCoMo dev); note that neither writer fills `valid_from`.
- 2026-11-27: design input recorded by the integration owner (user decision, T014 log of the same date): entity labels are immutable, so E006 also checks whether the writer's first-mention labels are correct surface names; a material error rate reopens the question of label correction.
- 2026-11-28: worker session `w01-E006` started on `task/E006-graph-quality` from `b7c62c3`; Issue #142. Scope of this round: the scorer and a provisional run; the formal run waits for the main writer configuration that E007 fixes.
- 2026-11-28: scorer `src/grace/eval/analysis/metrics/graph.py` (files only; reuses the T024 matching and normalisation of `eval/analysis/annotation/graph_quality.py`) and CLI `python -m grace.cli.graph_quality score <writer-run-dir>`, which takes any writer run directory with `updates.jsonl` and `graphs/<id>/` (a segment graph per sampled segment, or a graph per history as written by `grace.cli.writer_smoke`), writes a new `score` run with `metrics.json`, `claims.jsonl`, `gold.jsonl`, `judgements.jsonl` and `calls.jsonl`, and accepts `--experiment E007 --run-parent <dir>` for E007 arms. Gold: two label files give core units (claims both agents found, paired with the T024 matcher, identical to the merged review file) and uncertain units (one agent); precision and recall are reported as bounds (precision vs core to vs all units, recall vs all to vs core units). One label file (the human-reviewed reference) makes every claim core and the bounds coincide, without code change (`--gold FILE` or `scoring.gold`).
- 2026-11-28: predicate matching decision (run `E006-20261128T002555Z-50c6`). Three matchers were checked on 212 agent-agent predicate pairs: the 132 anchor pairs whose normalised predicates differ, and 80 seeded cross pairs (one pair's subject, object and quote with another pair's predicate), labelled same/different by the worker agent (`docs/research/annotations/graph-quality/predicate-check-reference.jsonl`; 130 same, 82 different; an agent's labels, not human). Normalised equality: accuracy 0.387 (accepts none of the differing pairs). Lexical (shared content stem after light words): accuracy 0.703, precision of SAME 0.986, recall 0.523. Lexical then the Qwen3-8B judge (`resources/prompts/predicate-judge`, through `grace.llm`, shared server): accuracy 0.882, precision 0.965, recall 0.838, 0 invalid. Chosen: lexical then judge as the `loose` level; `strict` (T024 strict) and `anchor` (no predicate condition) are reported with it as lower and upper references. The judge is conservative (it rejects, for example, wants/requires for a stated need), and the prompt examples were written after looking at these pairs, so the check is in-sample for the prompt. vLLM at temperature 0 is not bit-reproducible under batching (a dry run gave 0.887).
- 2026-11-28: deviation from a full-history reading (plan 6.7 does not fix how the writer sees a sampled segment): the provisional extraction writes each T024 segment on its own, with a fresh graph, its 6 context messages first (extracted, not scored) and the segment after (`eval/runner/probes/extract.py`, `segment_mode: context+segment`). Reason: cost; the LongMemEval-S segments sit in haystacks of about 50 sessions, and writing every prefix would cost the whole development histories for 578 scored messages; the segment-wise run made 132 calls. Effect measured on LoCoMo by scoring the T022 full-history Qwen3-8B run (same prompt, schema and writer config): loose precision 0.068–0.077 and recall 0.126–0.159 against 0.140–0.163 and 0.214–0.264 segment-wise; the full-history graph carries 10% catch-all claims (44 `felt`) against 1.3%. The segment-wise reading therefore overstates a full-history writer's graph quality; the formal E006 run should use full-history extraction at least for LoCoMo (both development histories are already written by any writer run) and decide for LongMemEval-S.
- 2026-11-28: provisional runs (not the formal E006 result): extraction `E006-20261128T001447Z-0046` (Qwen3-8B, T022 writer config, 40 segments, 132 calls, all schema-valid); score `E006-20261128T002604Z-514e`; comparison score `E006-20261128T002611Z-896e` of `T022-20261126T214758Z-613e`. Numbers in Results. Findings for the writer prompt round (E007): many conversational claims that the guideline excludes (`asks`, `askedAbout`, `contacted`, `expressedGratitude`, `feels`); speaker-as-subject claims where the gold describes an entity (`Caroline hasOrigin Sweden` for the necklace); `valid_from` never filled; 88 of 611 quotes do not anchor in the message text.
- 2026-11-28: not measurable or not done in this round: (1) the false-drop rate of the ending-evidence check: no gold ending stance exists in the 40 T024 segments (both agents), so all 10 drops on segment units are true drops by construction and the check's recall needs sequences with real endings (the controlled sequences); (2) the controlled sequences with gold graphs are not scored yet; (3) the separation of writer errors from planner (T023) and fragment-selection errors in graph-channel misses is not done (needs the retrieval traces of a T025-style run on the formal writer graph); (4) the answer-coverage upper bound. Contract note for the integration owner: a `score` run whose upstream is a `probe` run (writer-only extraction) is not in the stage table of contracts.md (Experiment run).
- 2026-11-28: worker session `w02-E006` on `task/E006-ingest-formal` (Part 1, PR #168) and `task/E006-formal-scoring` (Part 2), from `e23c68f`; Issue #142.
  - Part 1, the harness `ingest` and `read` stages. One ingest run serves several read runs; a read refuses an upstream that differs on the write side.
  - Main-configuration ingest run of LoCoMo dev: `E006-20261128T082608Z-21cb`, 928 messages, 481 claims. A read smoke run from it at budget 1024 (`E006-20261128T083248Z-24b4`) answered all 308 reads.
  - LongMemEval-S dev ingest runs: the three main-text strata (67 histories, 32,957 messages, 66 min with 8 workers) `E006-20261128T083145Z-6288`, and the other 31 histories (15,824 messages, 45 min) `E006-20261128T084142Z-ee92`. A read over all 98 histories takes one read run per ingest run.
- 2026-11-28: T024 matcher tightened (follow-up of PR #148). `same_name` now counts token containment only when the shorter name shares a token with the longer name's head, after its last possessive: `Caroline` no longer matches "Caroline's necklace".
  - Agent agreement re-reported in `agreement-agent-A-agent-B.json`: anchor Dice 0.774 -> 0.730 overall (LoCoMo 0.820 -> 0.815, LongMemEval-S 0.743 -> 0.673); strict 0.534 -> 0.532.
  - All 24 lost anchor pairs are `user` against "user's <task>" (23) or `Caroline` against "Caroline's close friends" (1), i.e. different subjects.
  - Core gold units fall from 426 to 402. The merged review file was not regenerated: it still pairs with the earlier matcher.
- 2026-11-28: formal scoring at the main configuration (numbers in Results):
  - LoCoMo full-history graph `cef6`; segment-wise extraction `afed` with score `ac34` (LongMemEval-S bound and LoCoMo gap);
  - controlled sequences: new commands `extract-sequences` and `score-sequences`, extraction `b04e`, score `cda5`;
  - answer-coverage upper bound: new command `coverage`; LoCoMo `be52`, LongMemEval-S `e4b6` and `6d20`.
  - Finding for the writer prompt and for T019/T014: on controlled sequences most changes and corrections ("I don't speak Dutch anymore") are written as a negative stance on the old claim, not as an ending, so the old claim stays current (20 of 35 gold endings).
  - Not done: the split of graph-channel misses into writer, planner (T023) and fragment-selection errors; human review of the gold.
- 2026-11-28: recorded done with a remark by the integration owner (s00-super): formal runs at the main configuration complete (PRs #168, #169). Remark: gold is the agent pair pending the human review, so precision and recall are bounds; writer, planner and fragment-selection errors are not yet separated. The merged review file was regenerated with the tightened matcher (699 rows; 24 former pairs are now two single claims each).
- 2026-11-28: rescored at the final writer prompt by worker session `w02-E007` (E007 ending round, Issue #141): controlled sequences `b09d`/`9386`, segment-wise `fa8b`/`d4d2`, LoCoMo full history `87ea` and answer coverage `aa0b` on the new shared ingest `E007-20261128T112542Z-c8d3` (numbers in Results, "At the final writer prompt"). The new shared ingests (`E007-20261128T112542Z-c8d3` LoCoMo, `E007-20261128T112648Z-1453` and `E007-20261128T112653Z-065d` LongMemEval-S) supersede `21cb`, `6288` and `ee92`. `5f3a` and `824d` were extracted with a prompt iteration that E007 rejected on its tuning set and were never scored.
