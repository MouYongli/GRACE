---
id: E007
title: "Ablation G: writer scale, thinking, granularity"
created: 2026-11-23
---

# E007 · Ablation G: writer scale, thinking, granularity

## Question

How much graph quality and answer accuracy does a larger writer or thinking recover, and what do the three extraction granularities cost? Serves RQ3. The granularity result fixes the main configuration (plan section 8.4).

## Design

| Item | Value |
| --- | --- |
| Benchmarks and splits | Controlled sequences (5 density-10 sequences of the T015 model-rendered development set, 1,000 messages); LoCoMo development histories (conv-26, conv-49, 928 messages); the 40 annotated T024 segments (578 messages, for E006 scoring) |
| Systems and baselines | Writer: primary versus larger same-family model; thinking off versus on; granularity per message, per segment, per session |
| Metrics | Writer tokens; graph quality as in E006; answer accuracy; parse-failure and repair rates |
| Seeds and budget | Seed 0, temperature 0 in every arm; max_tokens 4096 (message, segment-8), 12288 (session), 16384 (thinking) |
| Config | `configs/experiments/E007-ablation-g-writer.yaml` (driver `grace.cli.writer_ablation`); recall proxy `configs/experiments/E007-recall-locomo.yaml`; graph quality with E006's `grace.cli.graph_quality score` |

## Acceptance

- [ ] Every number traces to a run report.

## Runs

| Run ID | Date | Status | Code SHA | Report |
| --- | --- | --- | --- | --- |
| `E007-dry-seg-1` | 2026-11-28 | failed | `b7c62c3` | dry run (writer 32b-segment8, 2 T024 segments, uncommitted code); `runs/E007/artifacts/w01-E007/E007/E007-dry-seg-1/` |
| `E007-dry-think-1` | 2026-11-28 | completed | `d88d908` | dry run (writer 32b-segment8-think, 1 T024 segment, superseded mode); `runs/E007/artifacts/w01-E007/E007/E007-dry-think-1/` |
| `E007-20261128T001630Z-aed4` | 2026-11-28 | completed | `d88d908` | writer 32b-segment8 on t024-segments; superseded (segment-only mode, graphs not read by the E006 scorer); `runs/E007/artifacts/w01-E007/E007/E007-20261128T001630Z-aed4/report.yaml` |
| `E007-20261128T001630Z-da86` | 2026-11-28 | completed | `d88d908` | writer 8b-segment8 on locomo-dev; `runs/E007/artifacts/w01-E007/E007/E007-20261128T001630Z-da86/report.yaml` |
| `E007-20261128T001630Z-e513` | 2026-11-28 | completed | `d88d908` | writer 32b-segment8 on locomo-dev; `runs/E007/artifacts/w01-E007/E007/E007-20261128T001630Z-e513/report.yaml` |
| `E007-20261128T001937Z-22db` | 2026-11-28 | failed | `d88d908` | writer 32b-session on locomo-dev; aborted by the worker within a minute: started with an untracked test file (code_dirty true); relaunched under; `runs/E007/artifacts/w01-E007/E007/E007-20261128T001937Z-22db/report.yaml` |
| `E007-20261128T001937Z-59b7` | 2026-11-28 | failed | `d88d908` | writer 32b-message on t024-segments; aborted by the worker within a minute: started with an untracked test file (code_dirty true); relaunched under; `runs/E007/artifacts/w01-E007/E007/E007-20261128T001937Z-59b7/report.yaml` |
| `E007-20261128T001937Z-6b6b` | 2026-11-28 | failed | `d88d908` | writer 32b-session on t024-segments; aborted by the worker within a minute: started with an untracked test file (code_dirty true); relaunched under; `runs/E007/artifacts/w01-E007/E007/E007-20261128T001937Z-6b6b/report.yaml` |
| `E007-20261128T001937Z-c0e1` | 2026-11-28 | failed | `d88d908` | writer 32b-message on locomo-dev; aborted by the worker within a minute: started with an untracked test file (code_dirty true); relaunched under; `runs/E007/artifacts/w01-E007/E007/E007-20261128T001937Z-c0e1/report.yaml` |
| `E007-20261128T002008Z-1f87` | 2026-11-28 | completed | `1343fb6` | writer 32b-session on locomo-dev; `runs/E007/artifacts/w01-E007/E007/E007-20261128T002008Z-1f87/report.yaml` |
| `E007-20261128T002008Z-860d` | 2026-11-28 | completed | `1343fb6` | writer 32b-message on t024-segments; superseded (segment-only mode, graphs not read by the E006 scorer); `runs/E007/artifacts/w01-E007/E007/E007-20261128T002008Z-860d/report.yaml` |
| `E007-20261128T002008Z-9da7` | 2026-11-28 | failed | `1343fb6` | writer 32b-session on t024-segments; ParseException: Expected SelectQuery, found end of text  (at char 336), (line:9, col:14); `runs/E007/artifacts/w01-E007/E007/E007-20261128T002008Z-9da7/report.yaml` |
| `E007-20261128T002008Z-e01f` | 2026-11-28 | completed | `1343fb6` | writer 32b-message on locomo-dev; `runs/E007/artifacts/w01-E007/E007/E007-20261128T002008Z-e01f/report.yaml` |
| `E007-20261128T002410Z-581d` | 2026-11-28 | completed | `d6aec1d` | writer 32b-session on t024-segments; superseded (segment-only mode, graphs not read by the E006 scorer); `runs/E007/artifacts/w01-E007/E007/E007-20261128T002410Z-581d/report.yaml` |
| `E007-20261128T002410Z-8686` | 2026-11-28 | completed | `d6aec1d` | writer 8b-segment8 on t024-segments; superseded (segment-only mode, graphs not read by the E006 scorer); `runs/E007/artifacts/w01-E007/E007/E007-20261128T002410Z-8686/report.yaml` |
| `E007-20261128T002500Z-7946` | 2026-11-28 | completed | `d6aec1d` | writer 8b-session on locomo-dev; `runs/E007/artifacts/w01-E007/E007/E007-20261128T002500Z-7946/report.yaml` |
| `E007-20261128T002500Z-a973` | 2026-11-28 | completed | `d6aec1d` | writer 32b-session on changeseq-dev; `runs/E007/artifacts/w01-E007/E007/E007-20261128T002500Z-a973/report.yaml` |
| `E007-20261128T002500Z-e19f` | 2026-11-28 | failed | `d6aec1d` | writer 32b-segment8-think on t024-segments; aborted by the worker: superseded by the context+segment mode of E006 (commit 714577d); the segment-only graph; `runs/E007/artifacts/w01-E007/E007/E007-20261128T002500Z-e19f/report.yaml` |
| `E007-20261128T002500Z-ff7d` | 2026-11-28 | completed | `d6aec1d` | writer 32b-segment8 on changeseq-dev; `runs/E007/artifacts/w01-E007/E007/E007-20261128T002500Z-ff7d/report.yaml` |
| `E007-20261128T002505Z-e0e0` | 2026-11-28 | completed | `d6aec1d` | recall (graph channel) on `E007-20261128T001630Z-e513`; `runs/E007/artifacts/w01-E007/E007/E007-20261128T002505Z-e0e0/report.yaml` |
| `E007-20261128T002505Z-ff77` | 2026-11-28 | completed | `d6aec1d` | recall (graph channel) on `E007-20261128T001630Z-da86`; `runs/E007/artifacts/w01-E007/E007/E007-20261128T002505Z-ff77/report.yaml` |
| `E007-20261128T002721Z-7812` | 2026-11-28 | completed | `d6aec1d` | writer 32b-segment8-think on locomo-dev; `runs/E007/artifacts/w01-E007/E007/E007-20261128T002721Z-7812/report.yaml` |
| `E007-20261128T002721Z-8619` | 2026-11-28 | completed | `d6aec1d` | writer 32b-message on changeseq-dev; `runs/E007/artifacts/w01-E007/E007/E007-20261128T002721Z-8619/report.yaml` |
| `E007-20261128T002800Z-3c65` | 2026-11-28 | completed | `d6aec1d` | writer 8b-message on t024-segments; superseded (segment-only mode, graphs not read by the E006 scorer); `runs/E007/artifacts/w01-E007/E007/E007-20261128T002800Z-3c65/report.yaml` |
| `E007-20261128T002800Z-ac49` | 2026-11-28 | completed | `d6aec1d` | writer 8b-session on t024-segments; superseded (segment-only mode, graphs not read by the E006 scorer); `runs/E007/artifacts/w01-E007/E007/E007-20261128T002800Z-ac49/report.yaml` |
| `E007-20261128T002800Z-c019` | 2026-11-28 | completed | `d6aec1d` | recall (graph channel) on `E007-20261128T002008Z-1f87`; `runs/E007/artifacts/w01-E007/E007/E007-20261128T002800Z-c019/report.yaml` |
| `E007-20261128T002954Z-22c4` | 2026-11-28 | completed | `d6aec1d` | writer 8b-message on locomo-dev; `runs/E007/artifacts/w01-E007/E007/E007-20261128T002954Z-22c4/report.yaml` |
| `E007-20261128T002954Z-85cf` | 2026-11-28 | completed | `d6aec1d` | writer 8b-session on changeseq-dev; `runs/E007/artifacts/w01-E007/E007/E007-20261128T002954Z-85cf/report.yaml` |
| `E007-20261128T002954Z-9911` | 2026-11-28 | completed | `d6aec1d` | recall (graph channel) on `E007-20261128T002500Z-7946`; `runs/E007/artifacts/w01-E007/E007/E007-20261128T002954Z-9911/report.yaml` |
| `E007-20261128T002954Z-accd` | 2026-11-28 | completed | `d6aec1d` | writer 8b-segment8 on changeseq-dev; `runs/E007/artifacts/w01-E007/E007/E007-20261128T002954Z-accd/report.yaml` |
| `E007-20261128T003307Z-7735` | 2026-11-28 | completed | `4c209fe` | score (E006 scorer, segments) of `E007-20261128T001630Z-aed4`; upstream superseded, 0 writer claims found (graph IDs); `runs/E007/artifacts/w01-E007/E007/E007-20261128T003307Z-7735/report.yaml` |
| `E007-20261128T003307Z-a0ae` | 2026-11-28 | completed | `4c209fe` | score (E006 scorer, segments) of `E007-20261128T002410Z-8686`; upstream superseded, 0 writer claims found (graph IDs); `runs/E007/artifacts/w01-E007/E007/E007-20261128T003307Z-a0ae/report.yaml` |
| `E007-20261128T003308Z-842a` | 2026-11-28 | completed | `4c209fe` | score (E006 scorer, segments) of `E007-20261128T002008Z-860d`; upstream superseded, 0 writer claims found (graph IDs); `runs/E007/artifacts/w01-E007/E007/E007-20261128T003308Z-842a/report.yaml` |
| `E007-20261128T003308Z-a33d` | 2026-11-28 | completed | `4c209fe` | score (E006 scorer, segments) of `E007-20261128T002800Z-ac49`; upstream superseded, 0 writer claims found (graph IDs); `runs/E007/artifacts/w01-E007/E007/E007-20261128T003308Z-a33d/report.yaml` |
| `E007-20261128T003309Z-ad27` | 2026-11-28 | completed | `4c209fe` | score (E006 scorer, segments) of `E007-20261128T002410Z-581d`; upstream superseded, 0 writer claims found (graph IDs); `runs/E007/artifacts/w01-E007/E007/E007-20261128T003309Z-ad27/report.yaml` |
| `E007-20261128T003438Z-23eb` | 2026-11-28 | completed | `714577d` | writer 32b-segment8-think on t024-segments; `runs/E007/artifacts/w01-E007/E007/E007-20261128T003438Z-23eb/report.yaml` |
| `E007-20261128T003438Z-39d2` | 2026-11-28 | completed | `714577d` | writer 32b-segment8 on t024-segments; `runs/E007/artifacts/w01-E007/E007/E007-20261128T003438Z-39d2/report.yaml` |
| `E007-20261128T003438Z-4a4e` | 2026-11-28 | completed | `714577d` | writer 8b-segment8 on t024-segments; `runs/E007/artifacts/w01-E007/E007/E007-20261128T003438Z-4a4e/report.yaml` |
| `E007-20261128T003438Z-4f4f` | 2026-11-28 | completed | `714577d` | writer 32b-session on t024-segments; `runs/E007/artifacts/w01-E007/E007/E007-20261128T003438Z-4f4f/report.yaml` |
| `E007-20261128T003438Z-e1c8` | 2026-11-28 | completed | `714577d` | writer 8b-session on t024-segments; `runs/E007/artifacts/w01-E007/E007/E007-20261128T003438Z-e1c8/report.yaml` |
| `E007-20261128T003438Z-ee1d` | 2026-11-28 | completed | `714577d` | writer 32b-message on t024-segments; `runs/E007/artifacts/w01-E007/E007/E007-20261128T003438Z-ee1d/report.yaml` |
| `E007-20261128T003513Z-452d` | 2026-11-28 | completed | `714577d` | score (E006 scorer, full-history, LoCoMo segments) of `E007-20261128T001630Z-e513`; `runs/E007/artifacts/w01-E007/E007/E007-20261128T003513Z-452d/report.yaml` |
| `E007-20261128T003516Z-7132` | 2026-11-28 | completed | `714577d` | score (E006 scorer, full-history, LoCoMo segments) of `E007-20261128T001630Z-da86`; `runs/E007/artifacts/w01-E007/E007/E007-20261128T003516Z-7132/report.yaml` |
| `E007-20261128T003520Z-1b87` | 2026-11-28 | completed | `714577d` | score (E006 scorer, full-history, LoCoMo segments) of `E007-20261128T002008Z-1f87`; `runs/E007/artifacts/w01-E007/E007/E007-20261128T003520Z-1b87/report.yaml` |
| `E007-20261128T003523Z-908d` | 2026-11-28 | completed | `714577d` | score (E006 scorer, full-history, LoCoMo segments) of `E007-20261128T002500Z-7946`; `runs/E007/artifacts/w01-E007/E007/E007-20261128T003523Z-908d/report.yaml` |
| `E007-20261128T003540Z-7178` | 2026-11-28 | completed | `714577d` | score (E006 scorer, full-history, LoCoMo segments) of `T022-20261126T214758Z-c1fa`; `runs/E007/artifacts/w01-E007/E007/E007-20261128T003540Z-7178/report.yaml` |
| `E007-20261128T003544Z-c23b` | 2026-11-28 | completed | `714577d` | score (E006 scorer, full-history, LoCoMo segments) of `T022-20261126T214758Z-613e`; `runs/E007/artifacts/w01-E007/E007/E007-20261128T003544Z-c23b/report.yaml` |
| `E007-20261128T003731Z-0d06` | 2026-11-28 | completed | `714577d` | writer 8b-message on t024-segments; `runs/E007/artifacts/w01-E007/E007/E007-20261128T003731Z-0d06/report.yaml` |
| `E007-20261128T003855Z-e127` | 2026-11-28 | completed | `714577d` | score (E006 scorer, full-history, LoCoMo segments) of `E007-20261128T002008Z-e01f`; `runs/E007/artifacts/w01-E007/E007/E007-20261128T003855Z-e127/report.yaml` |
| `E007-20261128T003905Z-b458` | 2026-11-28 | completed | `714577d` | recall (graph channel) on `E007-20261128T002008Z-e01f`; `runs/E007/artifacts/w01-E007/E007/E007-20261128T003905Z-b458/report.yaml` |
| `E007-20261128T004158Z-79d3` | 2026-11-28 | completed | `714577d` | score (E006 scorer, segments) of `E007-20261128T003438Z-39d2`; `runs/E007/artifacts/w01-E007/E007/E007-20261128T004158Z-79d3/report.yaml` |
| `E007-20261128T004203Z-c002` | 2026-11-28 | completed | `714577d` | score (E006 scorer, segments) of `E007-20261128T003438Z-4f4f`; `runs/E007/artifacts/w01-E007/E007/E007-20261128T004203Z-c002/report.yaml` |
| `E007-20261128T004207Z-c26f` | 2026-11-28 | completed | `714577d` | score (E006 scorer, segments) of `E007-20261128T003438Z-ee1d`; `runs/E007/artifacts/w01-E007/E007/E007-20261128T004207Z-c26f/report.yaml` |
| `E007-20261128T004213Z-0520` | 2026-11-28 | completed | `714577d` | score (E006 scorer, segments) of `E007-20261128T003438Z-4a4e`; `runs/E007/artifacts/w01-E007/E007/E007-20261128T004213Z-0520/report.yaml` |
| `E007-20261128T004220Z-41aa` | 2026-11-28 | completed | `714577d` | score (E006 scorer, segments) of `E007-20261128T003438Z-e1c8`; `runs/E007/artifacts/w01-E007/E007/E007-20261128T004220Z-41aa/report.yaml` |
| `E007-20261128T004242Z-5779` | 2026-11-28 | completed | `714577d` | writer 8b-message on changeseq-dev; `runs/E007/artifacts/w01-E007/E007/E007-20261128T004242Z-5779/report.yaml` |
| `E007-20261128T004407Z-dc73` | 2026-11-28 | completed | `714577d` | score (E006 scorer, segments) of `E007-20261128T003731Z-0d06`; `runs/E007/artifacts/w01-E007/E007/E007-20261128T004407Z-dc73/report.yaml` |
| `E007-20261128T004411Z-13b9` | 2026-11-28 | completed | `714577d` | score (E006 scorer, full-history, LoCoMo segments) of `E007-20261128T002954Z-22c4`; `runs/E007/artifacts/w01-E007/E007/E007-20261128T004411Z-13b9/report.yaml` |
| `E007-20261128T004411Z-38af` | 2026-11-28 | completed | `714577d` | recall (graph channel) on `E007-20261128T002954Z-22c4`; `runs/E007/artifacts/w01-E007/E007/E007-20261128T004411Z-38af/report.yaml` |
| `E007-20261128T011144Z-2c97` | 2026-11-28 | completed | `e648679` | score (E006 scorer, segments) of `E007-20261128T003438Z-23eb`; `runs/E007/artifacts/w01-E007/E007/E007-20261128T011144Z-2c97/report.yaml` |
| `E007-20261128T011156Z-501d` | 2026-11-28 | completed | `e648679` | score (E006 scorer, segments) of `E007-20261128T003438Z-23eb`; `runs/E007/artifacts/w01-E007/E007/E007-20261128T011156Z-501d/report.yaml` |
| `E007-20261128T014112Z-e4b3` | 2026-11-28 | completed | `e648679` | score (E006 scorer, full-history, LoCoMo segments) of `E007-20261128T002721Z-7812`; `runs/E007/artifacts/w01-E007/E007/E007-20261128T014112Z-e4b3/report.yaml` |
| `E007-20261128T014114Z-87f8` | 2026-11-28 | completed | `e648679` | recall (graph channel) on `E007-20261128T002721Z-7812`; `runs/E007/artifacts/w01-E007/E007/E007-20261128T014114Z-87f8/report.yaml` |
| `E007-20261128T062349Z-3ea4` | 2026-11-28 | completed | `af0f87e` | system: configs/engines/grace-writer-segment8.yaml on LoCoMo dev, budget 1024; `runs/E007/artifacts/w01-E007/E007/E007-20261128T062349Z-3ea4/report.yaml` |
| `E007-20261128T062349Z-41ff` | 2026-11-28 | failed | `af0f87e` | system: configs/engines/grace-writer-8b.yaml on LoCoMo dev, budget 1024; aborted by the worker: the Qwen3-8B writer was sent to --writer-url (the Qwen3-32B server); fixed in the harne; `runs/E007/artifacts/w01-E007/E007/E007-20261128T062349Z-41ff/report.yaml` |
| `E007-20261128T062349Z-8899` | 2026-11-28 | completed | `af0f87e` | system: configs/engines/grace.yaml on LoCoMo dev, budget 1024; `runs/E007/artifacts/w01-E007/E007/E007-20261128T062349Z-8899/report.yaml` |
| `E007-20261128T062513Z-aa58` | 2026-11-28 | completed | `528b043` | system: configs/engines/grace-writer-8b.yaml on LoCoMo dev, budget 1024; `runs/E007/artifacts/w01-E007/E007/E007-20261128T062513Z-aa58/report.yaml` |
| `E007-20261128T062749Z-b374` | 2026-11-28 | failed | `46977f7` | T013 break-even with measured writer runs (write_budget estimate); ModuleNotFoundError: No module named 'matplotlib'; `runs/E007/artifacts/w01-E007/E007/E007-20261128T062749Z-b374/report.yaml` |
| `E007-20261128T062759Z-f620` | 2026-11-28 | completed | `42de3d5` | T013 break-even with measured writer runs (write_budget estimate); `runs/E007/artifacts/w01-E007/E007/E007-20261128T062759Z-f620/report.yaml` |
| `E007-20261128T062931Z-a884` | 2026-11-28 | completed | `3e5235a` | score (LoCoMo F1, grace.cli.locomo_score) of `E001-20261125T182212Z-2cd5`; `runs/E007/artifacts/w01-E007/E007/E007-20261128T062931Z-a884/report.yaml` |
| `E007-20261128T063748Z-9feb` | 2026-11-28 | completed | `f0f5c1e` | score (LoCoMo F1, grace.cli.locomo_score) of `E007-20261128T062349Z-8899`; `runs/E007/artifacts/w01-E007/E007/E007-20261128T063748Z-9feb/report.yaml` |
| `E007-20261128T063919Z-5126` | 2026-11-28 | completed | `f0f5c1e` | score (LoCoMo F1, grace.cli.locomo_score) of `E007-20261128T062513Z-aa58`; `runs/E007/artifacts/w01-E007/E007/E007-20261128T063919Z-5126/report.yaml` |
| `E007-20261128T064049Z-0d19` | 2026-11-28 | completed | `f0f5c1e` | score (LoCoMo F1, grace.cli.locomo_score) of `E007-20261128T062349Z-3ea4`; `runs/E007/artifacts/w01-E007/E007/E007-20261128T064049Z-0d19/report.yaml` |
| `E007-20261128T110034Z-b2de` | 2026-11-28 | failed | `f131e31` | ending round, tuning set, baseline prompt; pyshacl not thread safe under 10 parallel sequences (ParseException); relaunched as `2f7e`; `runs/E007/artifacts/w02-E007/E007/E007-20261128T110034Z-b2de/report.yaml` |
| `E007-20261128T110306Z-2f7e` | 2026-11-28 | completed | `191836f` | ending round, tuning set (10 sequences), prompt before the round (baseline); `runs/E007/artifacts/w02-E007/E007/E007-20261128T110306Z-2f7e/report.yaml` |
| `E007-20261128T110603Z-7f5b` | 2026-11-28 | completed | `050ad90` | ending round, tuning set, prompt iteration 1 (not judge-scored); `runs/E007/artifacts/w02-E007/E007/E007-20261128T110603Z-7f5b/report.yaml` |
| `E007-20261128T110903Z-e42d` | 2026-11-28 | completed | `51e25ee` | ending round, tuning set, prompt iteration 2 (final prompt); `runs/E007/artifacts/w02-E007/E007/E007-20261128T110903Z-e42d/report.yaml` |
| `E007-20261128T111356Z-94b8` | 2026-11-28 | completed | `f839d3e` | ending round, tuning set, prompt iteration 3 (closing reminder; rejected and reverted); `runs/E007/artifacts/w02-E007/E007/E007-20261128T111356Z-94b8/report.yaml` |
| `E007-20261128T111659Z-1642` | 2026-11-28 | completed | `f839d3e` | score (E006 sequence scorer) of `2f7e`; `runs/E007/artifacts/w02-E007/E007/E007-20261128T111659Z-1642/report.yaml` |
| `E007-20261128T111659Z-3b57` | 2026-11-28 | completed | `f839d3e` | score (E006 sequence scorer) of `94b8`; `runs/E007/artifacts/w02-E007/E007/E007-20261128T111659Z-3b57/report.yaml` |
| `E007-20261128T112034Z-ab5f` | 2026-11-28 | completed | `511d851` | score (E006 sequence scorer) of `e42d`; `runs/E007/artifacts/w02-E007/E007/E007-20261128T112034Z-ab5f/report.yaml` |
| `E007-20261128T112542Z-c8d3` | 2026-11-28 | completed | `511d851` | ingest, main configuration with the final prompt, LoCoMo dev (shared ingest; supersedes `E006-20261128T082608Z-21cb`); `runs/E007/artifacts/w02-E007/E007/E007-20261128T112542Z-c8d3/report.yaml` |
| `E007-20261128T112648Z-1453` | 2026-11-28 | completed | `511d851` | ingest, main configuration with the final prompt, LongMemEval-S dev main-text strata, 67 histories (shared ingest; supersedes `E006-20261128T083145Z-6288`); `runs/E007/artifacts/w02-E007/E007/E007-20261128T112648Z-1453/report.yaml` |
| `E007-20261128T112653Z-065d` | 2026-11-28 | completed | `511d851` | ingest, main configuration with the final prompt, LongMemEval-S dev other 31 histories (shared ingest; supersedes `E006-20261128T084142Z-ee92`); `runs/E007/artifacts/w02-E007/E007/E007-20261128T112653Z-065d/report.yaml` |

## Results

Partial: thinking on was run for Qwen3-32B at segment-8 only; Qwen3-8B with thinking was not run (see Log). All numbers below are from completed runs listed in Runs; each row names its writer run, its score run (E006 scorer, T024 agent labels, loose level, lower-upper bounds from the two label files) and, for LoCoMo, its recall run. Code: writer runs at `d88d908`, `1343fb6`, `d6aec1d` (LoCoMo, controlled sequences; the writer, prompt and schema are the same at all three) and `714577d` (T024 segments); score runs at `714577d`; recall runs at `d6aec1d` or `714577d` (each report names its SHA).

Extraction modes, compared only within a mode: **LoCoMo dev** = full-history writing (every message of both histories in order; the score covers the 16 LoCoMo T024 segments, read from the history graphs); **T024 segments** = each of the 40 segments written on its own with its 6 context messages first (E006's `context+segment` mode; message counts include the 228 context messages, which are extracted but not scored); **controlled sequences** = full-history writing, no graph-quality score yet (no scorer for the gold graphs).

Token columns are per message of history (calls x tokens / messages). "Cached" is the prompt prefix the server reported as cached; "n/r" = not reported: the shared Qwen3-8B server runs without `--enable-prompt-tokens-details`, so its cached count is unknown, not zero (both models share one tokenizer and the same prompts, so the Qwen3-32B cached share at the same granularity is a close estimate). Output tokens of thinking arms include the thinking.

#### LoCoMo dev (full history)

| Arm | Writer run | Messages | Calls | Input / msg | Cached / msg | Uncached / msg | Output / msg | Parse failures (rate); repaired splits | Empty patches | Claims | Loose P | Loose R | Loose F1 | Score run | Graph R@20 / RRF-all R@20 (recall run) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 8b-message | `E007-20261128T002954Z-22c4` | 928 | 928 | 4806 | n/r | n/r | 311.8 | 26 (0.028); 0/0 | 28/902 (0.031) | 1389 | 0.069-0.074 | 0.187-0.253 | 0.101-0.114 | `E007-20261128T004411Z-13b9` | 0.071 / 0.730 (`E007-20261128T004411Z-38af`) |
| 8b-segment8 | `E007-20261128T001630Z-da86` | 928 | 142 | 776 | n/r | n/r | 146.3 | 4 (0.0282); 2/2 | 7/138 (0.0507) | 1187 | 0.050-0.058 | 0.111-0.137 | 0.069-0.082 | `E007-20261128T003516Z-7132` | 0.071 / 0.734 (`E007-20261128T002505Z-ff77`) |
| 8b-session | `E007-20261128T002500Z-7946` | 928 | 44 | 285 | n/r | n/r | 97.5 | 0 (0.0); 0/0 | 0/44 (0.0) | 806 | 0.089-0.093 | 0.115-0.159 | 0.101-0.117 | `E007-20261128T003523Z-908d` | 0.081 / 0.741 (`E007-20261128T002954Z-9911`) |
| 32b-message | `E007-20261128T002008Z-e01f` | 928 | 928 | 4621 | 3824 | 796 | 87.3 | 0 (0.0); 0/0 | 389/928 (0.4192) | 688 | 0.136-0.158 | 0.221-0.275 | 0.169-0.201 | `E007-20261128T003855Z-e127` | 0.099 / 0.747 (`E007-20261128T003905Z-b458`) |
| 32b-segment8 | `E007-20261128T001630Z-e513` | 928 | 136 | 743 | 541 | 202 | 55.2 | 0 (0.0); 0/0 | 38/136 (0.2794) | 621 | 0.195-0.215 | 0.210-0.275 | 0.202-0.241 | `E007-20261128T003513Z-452d` | 0.105 / 0.741 (`E007-20261128T002505Z-e0e0`) |
| 32b-session | `E007-20261128T002008Z-1f87` | 928 | 44 | 274 | 173 | 101 | 40.0 | 0 (0.0); 0/0 | 0/44 (0.0) | 462 | 0.250-0.273 | 0.225-0.297 | 0.237-0.284 | `E007-20261128T003520Z-1b87` | 0.117 / 0.743 (`E007-20261128T002800Z-c019`) |
| 32b-segment8-think | `E007-20261128T002721Z-7812` | 928 | 170 | 920 | 685 | 236 | 555.3 | 17 (0.1); 12/12 | 25/153 (0.1634) | 419 | 0.253-0.263 | 0.199-0.275 | 0.222-0.269 | `E007-20261128T014112Z-e4b3` | 0.082 / 0.736 (`E007-20261128T014114Z-87f8`) |

#### T024 segments (context+segment)

| Arm | Writer run | Messages | Calls | Input / msg | Cached / msg | Uncached / msg | Output / msg | Parse failures (rate); repaired splits | Empty patches | Claims | Loose P | Loose R | Loose F1 | Score run | Graph R@20 / RRF-all R@20 (recall run) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 8b-message | `E007-20261128T003731Z-0d06` | 806 | 806 | 4359 | n/r | n/r | 355.4 | 24 (0.0298); 0/0 | 148/782 (0.1893) | 1827 | 0.080-0.094 | 0.206-0.279 | 0.116-0.141 | `E007-20261128T004407Z-dc73` | - |
| 8b-segment8 | `E007-20261128T003438Z-4a4e` | 806 | 140 | 840 | n/r | n/r | 109.9 | 4 (0.0286); 3/3 | 25/136 (0.1838) | 837 | 0.169-0.202 | 0.200-0.265 | 0.183-0.229 | `E007-20261128T004213Z-0520` | - |
| 8b-session | `E007-20261128T003438Z-e1c8` | 806 | 79 | 523 | n/r | n/r | 77.7 | 0 (0.0); 0/0 | 19/79 (0.2405) | 706 | 0.209-0.246 | 0.203-0.272 | 0.206-0.259 | `E007-20261128T004220Z-41aa` | - |
| 32b-message | `E007-20261128T003438Z-ee1d` | 806 | 806 | 4154 | 3698 | 455 | 86.6 | 1 (0.0012); 0/0 | 488/805 (0.6062) | 752 | 0.168-0.189 | 0.179-0.254 | 0.174-0.216 | `E007-20261128T004207Z-c26f` | - |
| 32b-segment8 | `E007-20261128T003438Z-39d2` | 806 | 142 | 842 | 698 | 144 | 59.1 | 5 (0.0352); 3/3 | 53/137 (0.3869) | 504 | 0.304-0.342 | 0.212-0.298 | 0.250-0.319 | `E007-20261128T004158Z-79d3` | - |
| 32b-session | `E007-20261128T003438Z-4f4f` | 806 | 83 | 547 | 380 | 167 | 40.2 | 2 (0.0241); 2/2 | 29/81 (0.358) | 480 | 0.349-0.395 | 0.216-0.303 | 0.267-0.343 | `E007-20261128T004203Z-c002` | - |
| 32b-segment8-think | `E007-20261128T003438Z-23eb` | 806 | 188 | 1107 | 873 | 234 | 802.5 | 30 (0.1596); 17/19 | 25/158 (0.1582) | 854 | 0.204-0.233 | 0.227-0.315 | 0.214-0.267 | `E007-20261128T011144Z-2c97` | - |

#### Controlled sequences (full history)

| Arm | Writer run | Messages | Calls | Input / msg | Cached / msg | Uncached / msg | Output / msg | Parse failures (rate); repaired splits | Empty patches | Claims | Loose P | Loose R | Loose F1 | Score run | Graph R@20 / RRF-all R@20 (recall run) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 8b-message | `E007-20261128T004242Z-5779` | 1000 | 1000 | 3910 | n/r | n/r | 40.5 | 0 (0.0); 0/0 | 677/1000 (0.677) | 202 | - | - | - | - | - |
| 8b-segment8 | `E007-20261128T002954Z-accd` | 1000 | 158 | 651 | n/r | n/r | 24.5 | 1 (0.0063); 1/1 | 54/157 (0.3439) | 183 | - | - | - | - | - |
| 8b-session | `E007-20261128T002954Z-85cf` | 1000 | 65 | 285 | n/r | n/r | 23.8 | 1 (0.0154); 1/1 | 10/64 (0.1562) | 182 | - | - | - | - | - |
| 32b-message | `E007-20261128T002721Z-8619` | 1000 | 1000 | 3900 | 3731 | 168 | 38.5 | 0 (0.0); 0/0 | 661/1000 (0.661) | 176 | - | - | - | - | - |
| 32b-segment8 | `E007-20261128T002500Z-ff7d` | 1000 | 158 | 651 | 582 | 68 | 24.1 | 1 (0.0063); 1/1 | 40/157 (0.2548) | 166 | - | - | - | - | - |
| 32b-session | `E007-20261128T002500Z-a973` | 1000 | 67 | 296 | 246 | 50 | 23.0 | 2 (0.0299); 2/2 | 3/65 (0.0462) | 171 | - | - | - | - | - |

#### Answer accuracy per writer arm (main configuration)

Default GRACE (planner, retrieval, views, assembly as in `configs/engines/grace.yaml`), LoCoMo dev, native end-of-history reads (308), memory budget 1,024 tokens; planner, rendering and answering on Qwen3-8B, embeddings Qwen3-Embedding-0.6B; registered rule-based LoCoMo F1 (`grace.cli.locomo_score`, categories 1-4; the 308 development reads hold no category 5). Reference: the T003 `rrf` baseline at 1,024 from E001.

| System | System run | Score run | F1 all (308) | cat 1 (69) | cat 2 (70) | cat 3 (26) | cat 4 (143) | Outputs answer / unknown / invalid |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| GRACE, Qwen3-32B writer, session (main) | `E007-20261128T062349Z-8899` | `E007-20261128T063748Z-9feb` | 0.293 | 0.238 | 0.071 | 0.150 | 0.453 | 251 / 56 / 1 |
| GRACE, Qwen3-8B writer, session | `E007-20261128T062513Z-aa58` | `E007-20261128T063919Z-5126` | 0.271 | 0.235 | 0.071 | 0.120 | 0.412 | 237 / 70 / 1 |
| GRACE, Qwen3-32B writer, segment-8 | `E007-20261128T062349Z-3ea4` | `E007-20261128T064049Z-0d19` | 0.283 | 0.240 | 0.071 | 0.148 | 0.433 | 249 / 56 / 3 |
| rrf baseline (E001) | `E001-20261125T182212Z-2cd5` | `E007-20261128T062931Z-a884` | 0.347 | 0.292 | 0.081 | 0.200 | 0.530 | 264 / 44 / 0 |

Read-side calls of the main arm (from its `calls.jsonl`): 350 `plan` calls (997,424 input, 32,366 output tokens) and 143 `repair` calls (437,082 / 14,644) next to 310 `answer` calls (453,637 / 10,435); the writer made 44 `extract` calls on Qwen3-32B (254,253 input of which 158,336 cached, 37,659 output). The Qwen3-8B server does not report cached tokens.

#### T013 break-even with measured writer tokens (D007)

Run `E007-20261128T062759Z-f620` (`write_budget estimate`, config `configs/experiments/E007-break-even.yaml`: T013's config with the E007 writer runs as reference writers, each priced at c from its own call records). c* = smallest c at which payback falls within the history's own reads (conv-26 152, conv-49 156). Read side as in T013: the cached full-history run and the `rrf` answer calls at 1,024 as GRACE's answer call, central planner (1 call per read); c marks measured on Qwen3-8B (warm-read 0.130, pooled 0.191).

| Writer | Weight | c* conv-26 / conv-49 | M* at c = 0.130 (conv-26 / conv-49) | M* at c = 0.191 |
| --- | --- | --- | --- | --- |
| T013 paper model, session, central | 1 | 0.075 / 0.061 | 47 / 38 | 27 / 24 |
| measured Qwen3-32B session (`1f87`) | 1 | 0.072 / 0.057 | 40 / 32 | 24 / 21 |
| measured Qwen3-32B segment-8 (`e513`) | 1 | 0.092 / 0.072 | 83 / 62 | 51 / 41 |
| measured Qwen3-32B message (`e01f`) | 1 | 0.338 / 0.218 | 373 / 243 (no payback) | 239 / 172 (no payback) |
| measured Qwen3-32B segment-8, thinking (`7812`) | 1 | 0.175 / 0.131 | 233 / 158 (no payback) | 136 / 99 |
| measured Qwen3-8B session (`7946`; input priced in full) | 1 | 0.102 / 0.081 | 98 / 72 | 55 / 43 |
| measured Qwen3-32B session, compute-weighted | 4.0 | 0.134 / 0.112 | 159 (no payback) / 128 | 94 / 81 |
| measured Qwen3-32B segment-8, compute-weighted | 4.0 | 0.253 / 0.198 | 332 / 245 (no payback) | 203 / 162 (no payback) |

Weight 4.0: assumption that compute per token, prefill and decode alike, scales with the parameter count (Qwen3-32B 32.8 B / Qwen3-8B 8.2 B); the read side stays on Qwen3-8B.

Verdict (as stated to s00-super): token-based, as T013 defines it, the LoCoMo token-savings claim survives with session units on the Qwen3-32B writer (c* 0.057-0.072 below the measured warm-read c of 0.13; payback within 32-40 of 152-156 reads). Compute-weighted at x4 it is at or beyond break-even: c* 0.11-0.13 against a measured c of 0.13 that is an upper bound (conv-26 does not pay back at 0.13, conv-49 does). Limits: the read side is T013's `rrf` proxy, not GRACE's measured read calls; the measured main arm spends about 4,650 planner input tokens per read (plan and repair, above) against T013's central assumption of one call of about 2,645 input tokens (2,265 prompt + 300 vocabulary + 80 request), so the proxy understates GRACE's read cost; c was measured on Qwen3-8B.

Prompt round (one round, user decision of 2026-11-26), scored once on the 16 LoCoMo T024 segments from the full-history graphs (the segments were not used to write the prompt), segment-8:

| Writer | Prompt | Writer run | Empty patches | Claims | Loose P | Loose R | Score run |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Qwen3-32B | T022 | `T022-20261126T214758Z-c1fa` | 44/136 | 474 | 0.172-0.179 | 0.183-0.253 | `E007-20261128T003540Z-7178` |
| Qwen3-32B | E007 | `E007-20261128T001630Z-e513` | 38/136 | 621 | 0.195-0.215 | 0.210-0.275 | `E007-20261128T003513Z-452d` |
| Qwen3-8B | T022 | `T022-20261126T214758Z-613e` | 6/136 | 957 | 0.068-0.077 | 0.126-0.159 | `E007-20261128T003544Z-c23b` |
| Qwen3-8B | E007 | `E007-20261128T001630Z-da86` | 7/138 | 1187 | 0.050-0.058 | 0.111-0.137 | `E007-20261128T003516Z-7132` |

(T022 counted 45 empty units for `c1fa`: units with nothing committed; 44 returned an empty patch.)

#### Ending round (user decision of 2026-11-28, follow-up of E006)

One writer-prompt round targeted at endings and changes, the same prompt for every writer arm. Tuned on 10 controlled development sequences that E006 did not score (`*-rho10-L200-001` and `*-rho30-L200-000`, one of each per family; 140 gold endings, 814 gold claim occurrences; config `configs/experiments/E007-ending-round.yaml`), then confirmed once with the E006 scorer on E006's five `*-rho10-L200-000` sequences and on the 40 T024 segments. Writer Qwen3-32B, session units, `configs/common/writer.yaml`. Endings: a gold supersession matched by a committed writer supersession on the same message with the same subject and object (E006 matcher; kind not compared). "Negated only": an unmatched gold ending whose message carries a negative writer attribution on the ended claim. Occurrences: loose and anchor matching of `grace.eval.analysis.metrics.graph_sequences`.

Tuning set (scored with the Qwen3-8B predicate judge):

| Prompt | Writer run | Score run | Endings matched / gold (recall) | Writer endings (precision) | Negated only | Ending drops (false) | Loose P | Loose R | Anchor P | Anchor R |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| before the round (`0ca40b38`) | `E007-20261128T110306Z-2f7e` | `E007-20261128T111659Z-1642` | 32 / 140 (0.2286) | 81 (0.3951) | 57 | 31 (7) | 0.6491 | 0.7273 | 0.6908 | 0.774 |
| iteration 2, final (`d2461141`) | `E007-20261128T110903Z-e42d` | `E007-20261128T112034Z-ab5f` | 56 / 140 (0.4) | 126 (0.4444) | 35 | 82 (8) | 0.6329 | 0.6376 | 0.7439 | 0.7494 |
| iteration 3, rejected | `E007-20261128T111356Z-94b8` | `E007-20261128T111659Z-3b57` | 59 / 140 (0.4214) | 147 (0.4014) | 32 | 74 (12) | 0.5933 | 0.5897 | 0.6972 | 0.6929 |

Confirmation, scored once (E006 runs; before = E006's formal runs at the earlier prompt):

| Set | Before (score run) | After: writer run, score run | Measure | Before | After |
| --- | --- | --- | --- | --- | --- |
| E006 controlled sequences (5, 35 gold endings) | `E006-20261128T084058Z-cda5` | `E006-20261128T112035Z-b09d`, `E006-20261128T112541Z-9386` | endings recall | 0.2571 (9/35) | 0.4857 (17/35) |
| | | | endings precision | 0.5294 (17 writer endings) | 0.34 (50) |
| | | | negated only | 20 | 12 |
| | | | ending drops (false; gold endings lost) | 5 (1; 1) | 11 (2; 2) |
| | | | loose occurrences P / R | 0.7292 / 0.7853 | 0.659 / 0.6442 |
| | | | anchor occurrences P / R | 0.7708 / 0.8301 | 0.7607 / 0.7436 |
| T024 segments, segment-wise (40) | `E006-20261128T083924Z-ac34` | `E006-20261128T112035Z-fa8b`, `E006-20261128T112541Z-d4d2` | loose P (all) | 0.2926-0.3636 | 0.2836-0.335 |
| | | | loose R (all) | 0.1831-0.2562 | 0.196-0.2886 |
| | | | loose P / R, LoCoMo | 0.2462-0.2764 / 0.2091-0.2707 | 0.23-0.2441 / 0.1977-0.2707 |
| | | | loose P / R, LongMemEval-S | 0.3529-0.4771 / 0.1674-0.2443 | 0.3418-0.4337 / 0.195-0.3032 |
| LoCoMo full history (16 T024 segments) | `E006-20261128T083416Z-cef6` (ingest `E006-20261128T082608Z-21cb`) | ingest `E007-20261128T112542Z-c8d3`, `E006-20261128T113433Z-87ea` | loose P / R | 0.214-0.2358 / 0.2053-0.2707 | 0.2146-0.2341 / 0.1825-0.2431 |
| | | | writer claims on the segments | 229 | 205 |

T024 bounds as in E006 (precision against core to all units, recall against all to core units; two agent label files). Each row is one writer run; writer output varies between runs at temperature 0, and no rerun of the same prompt was made, so differences of a few points are within unmeasured noise.

## Conclusion

Main configuration (decided 2026-11-28, Log): Qwen3-32B writer (user decision, D006 amendment) at session units (s00-super). What the completed runs support, each comparison within one extraction mode:

- Granularity: session units give the highest claim precision for both writers in both modes (Qwen3-32B loose P 0.250-0.273 full-history and 0.349-0.395 on segments; Qwen3-8B 0.089-0.093 and 0.209-0.246) at about the same recall as segment-8, and the fewest writer tokens per message (Qwen3-32B on LoCoMo: input 274 vs 743 for segment-8 and 4,621 for message; output 40 vs 55 and 87). Per-message units have the lowest precision and about six times the input tokens (the fixed prompt is resent per message; most of it is a cached prefix). Recommended main configuration: session granularity (proposal; s00-super decides). Not measured: the cost of read-triggered flushes inside an open session (no reads in these runs), which session units make more frequent under per-turn reading.
- Scale: Qwen3-32B is about four times as precise as Qwen3-8B in full-history writing (segment-8 0.195-0.215 vs 0.050-0.058) and about 1.7 times on segments, at similar recall, with fewer output tokens.
- Thinking (Qwen3-32B, segment-8): output tokens per message grow about tenfold (LoCoMo 555 vs 55; segments 803 vs 59) and parse failures rise to 0.10-0.16 (thinking cut at max_tokens 16384 at temperature 0; 2 of 19 split units on the segments were not repaired). Precision rises in full-history writing (0.253-0.263 vs 0.195-0.215) but falls on the segments (0.204-0.233 vs 0.304-0.342); recall is within the bounds of thinking off in both modes. Session units without thinking reach the same full-history precision (0.250-0.273) at 40 output tokens per message, so thinking does not pay for the writer here.
- Answer accuracy (LoCoMo dev, budget 1,024): the main configuration reaches F1 0.293 against 0.271 with the Qwen3-8B writer and 0.283 with Qwen3-32B segment-8, so the writer ordering follows graph quality; every GRACE arm is below the `rrf` baseline (0.347), and category 2 (temporal) is 0.071 in all three arms. Not explained from these runs.
- Break-even (D007): token-based the LoCoMo savings claim survives; compute-weighted it does not robustly (Results).
- The one prompt round helped Qwen3-32B (full history: P 0.172-0.179 to 0.195-0.215, R 0.183-0.253 to 0.210-0.275, empty patches 44 to 38 of 136) but not Qwen3-8B in full-history writing (P 0.068-0.077 to 0.050-0.058, R 0.126-0.159 to 0.111-0.137), where emotion and mention predicates the prompt forbids grew (`hasEmotionalImpact` 339, `mentions` 293 claims).
- Ending round (2026-11-28, Results): on the confirmation sequences ending recall rises from 0.257 to 0.486, but ending precision falls from 0.53 to 0.34. On the controlled sequences claim-occurrence recall falls (loose 0.785 to 0.644; tuning set 0.727 to 0.638), largely through predicate choice: the writer now uses `jobTitle` for a field of work where the gold has `worksIn` (unmatched gold `worksIn` occurrences 4 of 67 unmatched before and 33 of 111 after on the confirmation sequences; 26 of 222 and 60 of 295 on the tuning set). A likely cause, not tested, is the job example in the new Changes rule ("I'm a nurse now, not a teacher"). On the T024 segments claim P/R do not change materially (segment-wise loose P 0.29-0.36 to 0.28-0.34, R 0.18-0.26 to 0.20-0.29; LoCoMo full history P unchanged, R 0.21-0.27 to 0.18-0.24). The main remaining loss is in the program, not the prompt: when the writer emits both a negative claim and an ending stance for the same known claim in one message, the updater keeps the claim's attribution and discards the stance as `duplicate_in_message`, so nothing is superseded.

## Log

- 2026-11-23: created from the full project DAG.
- 2026-11-26: design inputs from the T022 writer smoke comparison (PR #129), recorded by the integration owner on user decisions: one prompt round on development data to raise Qwen3-32B extraction coverage (45/136 empty units in the smoke run), before the configuration lock (D012), with the same prompt then used for every writer arm; report empty-patch rate and output tokens next to quality (Qwen3-32B used about 2.7 times fewer output tokens than Qwen3-8B on the same input); session granularity needs larger schema array bounds (claims 32, stances 16, same_as 8 are sized for segment-8) and a re-pinned schema.
- 2026-11-28: worker session `w01-E007` (no manager layer; directed by `s00-super`) on `task/E007-ablation-g-writer`; Issue #141. Qwen3-32B server (revision `9216db5781bf21249d130ec9da846c4624c16137`, vLLM with `--reasoning-parser qwen3` for the thinking arms) on GPU 0, port 8253, reserved in `runs/compute.yaml`; Qwen3-8B on the shared server of `s00-super` (port 8252, started without `--enable-prompt-tokens-details`, so its cached tokens are not reported).
- 2026-11-28: prompt round (one round, before D012). Inputs: the empty units of the Qwen3-32B smoke run `T022-20261126T214758Z-c1fa` outside the T024 sessions (facts inside chit-chat missed: a childhood book, a family hobby, a diet, an incident at a supermarket). Changes to `extract-claims` (re-pinned): facts wrapped in chit-chat are kept, a list of easily missed kinds of facts, a per-message check, feelings only through what they are about, `hasEmotionalImpact`, `felt`, `mentions` named as catch-all predicates; all examples are invented, none is taken from benchmark text. Schema bounds widened for session units to 96 claims, 48 stances, 16 same_as (re-pinned; one schema for every arm); session arms use max_tokens 12288. Same prompt, schema and settings in every arm.
- 2026-11-28: driver `grace.cli.writer_ablation` (one arm on one target; `extractions.jsonl` with every raw writer item anchored to its message, graphs per history or segment); writer statistics gained empty patches, empty commits and the repair of invalid outputs by splitting (`eval/analysis/metrics/writer.py`); `metrics.json` has `writer_tokens` per message and call (D007). pyshacl is not thread safe: run `E007-20261128T002008Z-9da7` failed with a ParseException in SHACL validation under 8 parallel segments; validation is serialised in the driver since `d6aec1d`. Four runs started with an untracked test file (code_dirty) were aborted within a minute and relaunched.
- 2026-11-28: the first T024 arm runs wrote each segment from an empty graph without extracting its context and named graphs by a sanitised key; the E006 scorer (merged from main, PR #148) found no graphs in them (5 score runs with 0 writer claims). The T024 target now uses E006's probe (`context+segment`, `714577d`) and all T024 arms were rerun; the earlier runs are superseded (Runs).
- 2026-11-28: results of the scale and granularity arms (thinking off) on LoCoMo dev, the controlled sequences and the T024 segments, with E006 scores and the graph-channel recall proxy: Results. Answer accuracy was not run (no answering pipeline over extracted graphs exists yet); the T025 recall probe on each arm's graphs stands in as a proxy (graph R@20 0.071-0.117, fused R@20 0.730-0.747 across arms; fusion moves by about one point). D007 request (s00-super): writer tokens per granularity, model and thinking setting per message of history, input split into cached prefix and rest, are in the Results tables and in each writer run's `report.yaml` (`metrics.writer_tokens`).
- 2026-11-28: not run or not finished in this session: thinking on for Qwen3-8B (needs a Qwen3-8B server with a reasoning parser; the shared server has none); thinking on for Qwen3-32B at message and session granularity and on the controlled sequences; graph quality on the controlled sequences (no scorer against their gold graphs yet).
- 2026-11-28: thinking on, Qwen3-32B, segment-8: LoCoMo dev `E007-20261128T002721Z-7812` (score `E007-20261128T014112Z-e4b3`, recall `E007-20261128T014114Z-87f8`) and T024 segments `E007-20261128T003438Z-23eb` (score `E007-20261128T011144Z-2c97`); results in Results and Conclusion. The Qwen3-32B server on GPU 0 was stopped and its `runs/compute.yaml` entry removed.
- 2026-11-28: decisions recorded (s00-super, 2026-11-28). User decision: the main writer is Qwen3-32B (D006 amendment, PR #158); planning, rendering and answering stay Qwen3-8B; the Qwen3-8B writer stays as the small-writer arm; one prompt for all arms, no second prompt round. Decision of s00-super: main granularity session units. The Qwen3-8B thinking arm is not run: thinking does not pay for the writer on Qwen3-32B (the same full-history precision at about a tenth of the output tokens without it). The slot-table arms of ablation B also use the Qwen3-32B writer, so the representations are compared with one writer.
- 2026-11-28: main configuration on branch `task/E007-main-config`: engine config key `writer_model` (a model config reached at `--writer-url`; the writer and writer-side extensions use the port's `writer_client`, planner, views and answering the run's client); `configs/common/writer.yaml` session units with max_tokens 12288 (`writer-segment8.yaml` keeps the segment-8 settings); `grace.yaml` and all T027 variants on `writer_model: configs/models/qwen3-32b.yaml`; arms `grace-writer-8b.yaml` and `grace-writer-segment8.yaml`. The first small-writer run `E007-20261128T062349Z-41ff` sent the Qwen3-8B writer to the Qwen3-32B endpoint and was aborted; since `528b043` a writer model equal to the run's model is always reached at `--base-url`.
- 2026-11-28: answer accuracy per writer arm with `grace.cli.locomo_score` (new: score stage of a LoCoMo system run with the registered rule-based metrics of `configs/common/scorers.yaml`), and the T013 break-even with measured writer tokens (`write_budget` gained weighted reference writers and `--no-plot`; the first estimate `E007-20261128T062749Z-b374` failed on the missing matplotlib): Results. E001's LoCoMo table lists 0.310 for `rrf`: that column is the answer calls' prefix-cache hit ratio ("A hit ratio"; the table counts outputs, not scores), not an F1; E001 reports judge accuracy for `rrf` on LoCoMo (0.3929 / 0.4583) and no rule-based F1, so 0.347 here is the first F1 of run `E001-20261125T182212Z-2cd5` and no scorer differs.
- 2026-11-28: recorded done with a remark by the integration owner (s00-super): main configuration fixed (Qwen3-32B writer, session units, one prompt for all arms). Remark: not run are Qwen3-8B thinking (thinking does not pay for the writer), Qwen3-32B thinking at message and session granularity, and graph quality on the controlled sequences (no gold-graph scorer yet; E006). GRACE scores below rrf on LoCoMo dev answer F1; the diagnosis is the first step of E013.
- 2026-11-28: user decision: one additional writer-prompt round targeted only at endings and changes (E006 found 20 of 26 missed endings written as bare negative stances), tuned on controlled sequences E006 did not score, the same prompt then used for every writer arm; new shared ingest runs follow. Work on `task/E007-ending-round`.
- 2026-11-28: worker session `w02-E007` on `task/E007-ending-round` from `d276860` (Issue #141), directed by s00-super: one additional writer-prompt round targeted at endings (user decision of 2026-11-28 after E006, PR #169), then new shared main-configuration ingest runs.
  - Diagnosis (E006 extraction `E006-20261128T083758Z-b04e`, which E006 had already reported; then the tuning baseline `2f7e`): most missed endings are not missing stances. The writer emits the ended claim again as a claim with polarity negative *and* an ending stance on its handle; the updater applies the claim first (a repeated mention with a negative attribution) and drops the stance as `duplicate_in_message` (`pipeline/update/updater.py`, `_stance`), so the old claim stays current. Further causes: only a negative claim and no stance; an ending quote without the old value ("I don't anymore"), dropped by the ending-evidence check; a requirement ended with function `inform` instead of the `request` of its earlier stance, blocked by the guard (`speaker_or_function`); a change whose new claim uses another predicate, so nothing replaces the old claim.
  - Prompt change (`extract-claims`, re-pinned `d2461141...` in `configs/common/prompts.yaml`; schema unchanged): an ending is written only as a negative stance with `ends`, never also as a negative claim; `polarity: negative` on a claim only for something that is not a known claim; `ends: change` or `correction` with cues; the stance takes the function of the claim's earlier stance (request for a requirement); the handle must be the claim with the old value; the quote must contain the old value; on a change that names the old value, the new claim keeps the old subject and predicate and the old claim also gets an ending stance (this replaces "do not add an ending stance for it as well"). One invented example (tennis/squash correction, rowing/climbing change, a hotel room requirement). No contract change: the stance with `ends` and the G2(ii) removal already express everything.
  - Iterations on the tuning set only: 1 (`7f5b`, the Endings and Changes bullets and the example; 51 of 140 endings by the scorer's matcher run offline, not judge-scored), 2 (`e42d`, the polarity rule and the handle check; final), 3 (`94b8`, a closing reminder in `user.txt`; reverted because occurrence recall fell, anchor R 0.749 to 0.693). Two confirmation extractions made with iteration 3 (`E006-20261128T111659Z-5f3a`, `-824d`) were superseded before scoring: they were never scored or inspected, and the choice of iteration 2 rests on the tuning set alone. The confirmation was then run once with iteration 2.
  - `graph_quality extract-sequences` now serialises SHACL validation when sequences run in parallel (pyshacl is not thread safe; run `b2de` failed on it).
  - Results: Results, "Ending round". Shared ingest runs with the final prompt (main configuration, `configs/engines/grace.yaml`; they supersede the E006 ingests `E006-20261128T082608Z-21cb`, `-083145Z-6288` and `-084142Z-ee92`): LoCoMo dev `E007-20261128T112542Z-c8d3`, LongMemEval-S dev main-text strata `E007-20261128T112648Z-1453`, other 31 histories `E007-20261128T112653Z-065d`. All three completed: LoCoMo 928 messages, 511 claims, 1 supersession (8 min); LongMemEval-S main strata 32,957 messages, 12,232 claims, 44 supersessions (50 min, 8 workers); other 31 histories 15,824 messages, 5,071 claims, 18 supersessions (33 min, 6 workers).
  - Not done: a rerun of the same prompt to measure writer noise on these measures; a program-side fix of the duplicate rule (outside the prompt round; proposed to s00-super: apply an ending stance even when the same message already attributed the claim).
