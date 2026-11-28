"""E006 (graph quality): writer-only extraction of the annotated segments, and its scoring.

    uv run python -m grace.cli.graph_quality extract \\
        --config configs/experiments/E006-graph-quality.yaml \\
        --writer-url http://localhost:8252/v1 [--compute "<reservation>"] \\
        [--segments-only KEY ...] [--workers 4]
    uv run python -m grace.cli.graph_quality score WRITER_RUN_DIR \\
        --config configs/experiments/E006-graph-quality.yaml \\
        [--judge-url http://localhost:8252/v1] [--experiment E007 --run-parent DIR] \\
        [--gold FILE ...] [--label TEXT]

`extract` (stage `probe`) writes every segment of the T024 sample on its own, its context messages
first (`grace.eval.runner.probes.extract`), into a new run directory under
`$PROJECT_ROOT/runs/E006/artifacts/w01-E006/E006/<run-id>/`: `run.json`, `resolved-config.yaml`,
`run.log`, `calls.jsonl`, `updates.jsonl` (one record per extraction unit, with its `segment`) and
`graphs/<segment graph ID>/` (claim store and writer state). `n_records`: segments written.

`score` (stage `score`) reads one writer run directory, the gold label files and the segment texts,
and writes `metrics.json`, `claims.jsonl` (every writer claim occurrence on a segment message with
its match), `gold.jsonl` (every gold claim with its match) and `judgements.jsonl` (LLM judge calls
of the predicate and entailment checks) into a new score run directory. It accepts any writer run
with `updates.jsonl` and `graphs/<id>/store/changesets.jsonl` + `graphs/<id>/writer.json`: a
segment run of `extract` (graph per segment) or a full-history run of `grace.cli.writer_smoke`
(graph per history). The scoring logic is `grace.eval.analysis.metrics.graph` (files only).
"""

from __future__ import annotations

import argparse
import json
import shlex
import sys
import traceback
from collections import Counter, defaultdict
from collections.abc import Sequence
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import yaml

from grace.config.paths import REPO_ROOT, project_root, shared_dir
from grace.eval.runner.harness import rundir

WORKER = "w01-E006"


def _load_config(path: Path) -> tuple[Path, dict]:
    path = path if path.is_absolute() else REPO_ROOT / path
    return path, yaml.safe_load(path.read_text(encoding="utf-8"))


def _client(model_config: Path, url: str, ledger_path: Path, run_id: str):
    from grace.llm.client import ChatClient, Endpoint
    from grace.llm.records import CallLedger
    from grace.llm.tokens import HFTokenCounter, TokenizerPin, locate_snapshot
    ledger = CallLedger(ledger_path, run_id)
    pin = TokenizerPin.from_file(model_config)
    counter = HFTokenCounter(pin, locate_snapshot(pin))
    raw = yaml.safe_load(model_config.read_text(encoding="utf-8"))
    return ChatClient(Endpoint.for_model(pin, url, raw["served_name"], timeout_s=300.0),
                      ledger, counter)


def extract(args: argparse.Namespace) -> int:
    from grace.cli.retrieval_recall import benchmark_config
    from grace.context.pipeline.update.updater import WriterConfig, llm_writer
    from grace.eval.datasets.benchmarks.splits import load_split
    from grace.eval.runner.probes.extract import drive_segment

    config_path, config = _load_config(args.config)
    if config["experiment"] != args.experiment:
        raise SystemExit(f"config is for {config['experiment']!r}, not {args.experiment}")
    writer_config_path = REPO_ROOT / config["writer_config"]
    writer_config = WriterConfig.load(writer_config_path)
    sample = json.loads((REPO_ROOT / config["sample"]).read_text(encoding="utf-8"))
    segments = [s for s in sample["segments"]
                if not args.segments_only or s["key"] in args.segments_only]
    entries = config["benchmarks"]
    configs = {e["slug"]: benchmark_config(e) for e in entries}

    run_parent = (args.run_parent or shared_dir("runs_root") / args.experiment / "artifacts"
                  / WORKER)
    run_dir = rundir.create(run_parent, args.experiment, args.run_id)
    run_id = run_dir.name
    log = (run_dir / "run.log").open("a", encoding="utf-8")

    def say(text: str) -> None:
        print(text, flush=True)
        log.write(text + "\n")
        log.flush()

    model_config = REPO_ROOT / config["model_config"]
    resolved = {"experiment": config,
                "writer": {"config": config["writer_config"],
                           "sha256": rundir.file_sha256(writer_config_path),
                           "values": yaml.safe_load(writer_config_path.read_text("utf-8"))},
                "sample": {"path": config["sample"],
                           "sha256": rundir.file_sha256(REPO_ROOT / config["sample"]),
                           "segments": [s["key"] for s in segments]},
                "serving": {"writer_url": args.writer_url, "compute": args.compute or "none",
                            **config.get("serving", {})},
                "workers": args.workers}
    (run_dir / "resolved-config.yaml").write_text(yaml.safe_dump(resolved, sort_keys=False),
                                                  encoding="utf-8")
    code = rundir.code_state()
    root = project_root()
    data = [{"benchmark": slug, "version": bc.version, "manifest_sha256": bc.manifest_sha256,
             "split": e["split"], "path": bc.source_dir(root).as_posix()}
            for e, (slug, bc) in zip(entries, configs.items(), strict=True)]
    run = rundir.RunJson(run_dir, {
        "run_id": run_id, "experiment": args.experiment, "stage": "probe", "upstream": [],
        "code_sha": code.sha, "code_dirty": code.dirty,
        "config_path": config_path.relative_to(REPO_ROOT).as_posix(),
        "config_sha256": rundir.file_sha256(run_dir / "resolved-config.yaml"),
        "resources_sha256": rundir.resources_sha256(), "data": data,
        "project_root": root.as_posix(), "seed": int(config["seed"]),
        "command": " ".join(shlex.quote(a) for a in sys.argv),
        "environment": rundir.environment("cpu (writer model on the serving endpoint)"),
        "compute": args.compute or "none", "held_out_access": "none",
        "segment_mode": config.get("segment_mode", "context+segment")})
    n_done = 0
    try:
        client = _client(model_config, args.writer_url, run_dir / "calls.jsonl", run_id)
        histories, messages = {}, defaultdict(list)
        for entry in entries:
            slug, bc = entry["slug"], configs[entry["slug"]]
            records = load_split(slug, entry["split"], config=bc)
            wanted = {s["history_id"] for s in segments if s["benchmark"] == slug}
            for h in records.histories:
                if h.history_id in wanted:
                    histories[(slug, h.history_id)] = h
            for m in records.messages:
                if m.history_id in wanted:
                    messages[(slug, m.history_id)].append(m)
            say(f"{slug}: {len(wanted)} histories for "
                f"{sum(1 for s in segments if s['benchmark'] == slug)} segments")

        def one(segment):
            key = (segment["benchmark"], segment["history_id"])
            updates = drive_segment(histories[key], messages[key], segment,
                                    lambda info: llm_writer(writer_config, client, info),
                                    writer_config, run_dir)
            say(f"  {segment['key']}: {len(updates)} unit records")
            return updates

        with ThreadPoolExecutor(max_workers=max(1, args.workers)) as pool:
            results = list(pool.map(one, segments))
        all_updates = [u for part in results for u in part]
        with (run_dir / "updates.jsonl").open("w", encoding="utf-8") as f:
            for u in all_updates:
                f.write(json.dumps(u, ensure_ascii=False, sort_keys=True) + "\n")
        n_done = len(results)
        from grace.eval.analysis.metrics import writer as metric
        updates = metric.read_jsonl(run_dir / "updates.jsonl")
        calls = metric.read_jsonl(run_dir / "calls.jsonl")
        metrics = {"units": metric.unit_stats(updates), "calls": metric.call_stats(calls),
                   "model_calls": len(calls), "segments": n_done}
        (run_dir / "metrics.json").write_text(json.dumps(metrics, indent=2, sort_keys=True)
                                              + "\n", encoding="utf-8")
        say(json.dumps({"units": metrics["units"]["by_status"],
                        "calls": metrics["calls"]["by_status"]}, sort_keys=True))
        run.data["model_calls"] = len(calls)
        run.finish(n_done)
        say(f"run directory: {run_dir} status={run.data['status']}"
            + (f" failure={run.data['failure']}" if run.data["failure"] else ""))
    except BaseException as exc:
        say(traceback.format_exc())
        run.finish(n_done, f"{type(exc).__name__}: {exc}")
        raise
    finally:
        log.close()
    return 0 if run.data["status"] == "completed" else 1


class _Run:
    """A score-stage run directory with run.json, run.log and resolved-config.yaml."""

    def __init__(self, args: argparse.Namespace, config_path: Path, resolved: dict,
                 upstream: list[dict], data: list[dict], seed: int):
        parent = (args.run_parent or shared_dir("runs_root") / args.experiment / "artifacts"
                  / WORKER)
        self.dir = rundir.create(parent, args.experiment, args.run_id)
        self.id = self.dir.name
        self._log = (self.dir / "run.log").open("a", encoding="utf-8")
        (self.dir / "resolved-config.yaml").write_text(yaml.safe_dump(resolved, sort_keys=False),
                                                       encoding="utf-8")
        code = rundir.code_state()
        self.json = rundir.RunJson(self.dir, {
            "run_id": self.id, "experiment": args.experiment, "stage": "score",
            "upstream": upstream, "code_sha": code.sha, "code_dirty": code.dirty,
            "config_path": config_path.relative_to(REPO_ROOT).as_posix(),
            "config_sha256": rundir.file_sha256(self.dir / "resolved-config.yaml"),
            "resources_sha256": rundir.resources_sha256(), "data": data,
            "project_root": project_root().as_posix(), "seed": seed,
            "command": " ".join(shlex.quote(a) for a in sys.argv),
            "environment": rundir.environment("cpu (judge model on the serving endpoint)"),
            "compute": args.compute or "none", "held_out_access": "none",
            "label": args.label})

    def say(self, text: str) -> None:
        print(text, flush=True)
        self._log.write(text + "\n")
        self._log.flush()

    def close(self) -> None:
        self._log.close()


def _write_jsonl(path: Path, rows) -> None:
    with path.open("x", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False, sort_keys=True, default=sorted) + "\n")


def _parallel(workers: int):
    def run_many(fn, items):
        with ThreadPoolExecutor(max_workers=max(1, workers)) as pool:
            return list(pool.map(fn, items))
    return run_many


def _judges(config: dict, url: str | None, run: _Run, need_predicate: bool, need_entail: bool):
    from grace.eval.analysis.metrics import graph as g
    from grace.llm.prompts import load_pinned
    if not (need_predicate or need_entail):
        return None, None
    if not url:
        raise SystemExit("--judge-url is required for the judge predicate matcher or the "
                         "entailment check")
    jc = config["scoring"]["judge"]
    client = _client(REPO_ROOT / jc["model_config"], url, run.dir / "calls.jsonl", run.id)
    registry = REPO_ROOT / "configs" / "common" / "prompts.yaml"
    decoding = {"temperature": jc["temperature"], "max_tokens": jc["max_tokens"],
                "seed": jc["seed"]}
    pj = g.llm_judge(client, load_pinned(jc["prompt"], registry), decoding,
                     g.PREDICATE_VERDICTS) if need_predicate else None
    ej = g.llm_judge(client, load_pinned(jc.get("entailment_prompt", "entailment-judge"),
                                         registry), decoding,
                     g.ENTAILMENT_VERDICTS) if need_entail else None
    return pj, ej


def _gold_paths(args: argparse.Namespace, config: dict) -> list[Path]:
    paths = args.gold or [REPO_ROOT / p for p in config["scoring"]["gold"]]
    return [p if Path(p).is_absolute() else REPO_ROOT / p for p in map(Path, paths)]


def _segments_path(args: argparse.Namespace, config: dict) -> Path:
    return args.segments or shared_dir("runs_root") / config["scoring"]["segments"]


def score(args: argparse.Namespace) -> int:
    from grace.eval.analysis.annotation import graph_quality as gq
    from grace.eval.analysis.metrics import graph as g
    from grace.eval.analysis.metrics import writer as wm

    config_path, config = _load_config(args.config)
    sc = config["scoring"]
    writer_dir = args.writer_run.resolve()
    writer_json = json.loads((writer_dir / "run.json").read_text(encoding="utf-8"))
    if writer_json.get("status") != "completed" and not args.allow_incomplete:
        raise SystemExit(f"upstream run {writer_dir.name} is {writer_json.get('status')!r}, "
                         "not completed (contracts.md, Stages and upstream runs)")
    gold_paths = _gold_paths(args, config)
    segments_path = _segments_path(args, config)
    method = args.predicate_match or sc["predicate_match"]
    entail = sc.get("entailment_judge", False) and not args.no_entailment
    resolved = {"experiment": config, "writer_run": writer_dir.as_posix(),
                "gold": [{"path": p.as_posix(), "sha256": rundir.file_sha256(p)}
                         for p in gold_paths],
                "segments": {"path": segments_path.as_posix(),
                             "sha256": rundir.file_sha256(segments_path)},
                "predicate_match": method, "entailment_judge": entail,
                "judge_url": args.judge_url, "workers": args.workers,
                "benchmarks": args.benchmarks}
    upstream = [{"run_id": writer_json["run_id"], "stage": writer_json["stage"],
                 "path": writer_dir.as_posix(),
                 "run_json_sha256": rundir.file_sha256(writer_dir / "run.json")}]
    run = _Run(args, config_path, resolved, upstream, writer_json.get("data", []),
               int(config["seed"]))
    n = 0
    try:
        pj, ej = _judges(config, args.judge_url, run, method == "judge", entail)
        segments = gq.read_segments(segments_path)
        if args.benchmarks:
            segments = {k: v for k, v in segments.items() if v.benchmark in args.benchmarks}
        raw = {json.loads(line)["key"]: json.loads(line)
               for line in segments_path.read_text(encoding="utf-8").splitlines() if line}
        history_of = {k: raw[k]["history_id"] for k in segments}
        texts = {k: [m["text"] for m in raw[k]["messages"] + raw[k].get("context", [])]
                 + [m.get("speaker") or "" for m in raw[k]["messages"]]
                 + list(raw[k].get("participants") or []) for k in segments}
        files = [gq.read_jsonl(p) for p in gold_paths]
        units = g.gold_units(files, segments)
        units_by_id = {u.uid: u for us in units.values() for u in us}
        wrun = g.read_writer_run(writer_dir)
        matcher = g.PredicateMatcher(method, pj)
        run_many = _parallel(args.workers)
        metrics, claim_rows, gold_rows = g.score(wrun, segments, units, matcher, history_of,
                                                 run_many)
        spans = g.span_checks(claim_rows, segments, units_by_id,
                              (lambda xs: run_many(ej, xs)) if ej else None)
        metrics = {
            "claims": metrics,
            "per_predicate": g.per_predicate(claim_rows),
            "spans": spans["metrics"],
            "entity_labels": g.entity_labels(wrun, segments, claim_rows, units_by_id, texts),
            "ending_drops": g.ending_drops(wrun, segments, units, history_of),
            "restatements": g.restatements(claim_rows, units_by_id),
            "predicate_matcher": {"method": method, "judged_pairs": len(matcher.log),
                                  "verdicts": dict(sorted(
                                      Counter(
                                          x["verdict"] for x in matcher.log).items()))},
            "gold": {"files": [p.name for p in gold_paths],
                     "mode": "reference" if len(files) == 1 else "two annotators"},
            "writer_run": {"run_id": writer_json["run_id"], "units": wm.unit_stats(wrun.updates)
                           if wrun.updates else None},
        }
        calls_path = writer_dir / "calls.jsonl"
        if calls_path.exists():
            metrics["writer_run"]["calls"] = wm.call_stats(wm.read_jsonl(calls_path))
        (run.dir / "metrics.json").write_text(json.dumps(metrics, indent=2, sort_keys=True)
                                              + "\n", encoding="utf-8")
        _write_jsonl(run.dir / "claims.jsonl", claim_rows)
        _write_jsonl(run.dir / "gold.jsonl", gold_rows)
        _write_jsonl(run.dir / "judgements.jsonl", matcher.log + spans["log"])
        n = len(segments)
        c = metrics["claims"]["all"]
        run.say(json.dumps({"writer_claims": c["writer_claims"], "gold_core": c["gold_core"],
                            "gold_all": c["gold_all"], "loose": c["loose"]}, sort_keys=True))
        run.json.data["model_calls"] = sum(1 for _ in (run.dir / "calls.jsonl").open()) \
            if (run.dir / "calls.jsonl").exists() else 0
        run.json.finish(n)
        run.say(f"run directory: {run.dir} status={run.json.data['status']}"
                + (f" failure={run.json.data['failure']}" if run.json.data["failure"] else ""))
    except BaseException as exc:
        run.say(traceback.format_exc())
        run.json.finish(n, f"{type(exc).__name__}: {exc}")
        raise
    finally:
        run.close()
    return 0 if run.json.data["status"] == "completed" else 1


def predicate_check(args: argparse.Namespace) -> int:
    from grace.eval.analysis.annotation import graph_quality as gq
    from grace.eval.analysis.metrics import graph as g

    config_path, config = _load_config(args.config)
    gold_paths = _gold_paths(args, config)
    if len(gold_paths) != 2:
        raise SystemExit("predicate-check needs two label files")
    segments_path = _segments_path(args, config)
    reference_path = args.reference if args.reference.is_absolute() else REPO_ROOT / args.reference
    resolved = {"experiment": config, "check": "predicate matcher",
                "gold": [{"path": p.as_posix(), "sha256": rundir.file_sha256(p)}
                         for p in gold_paths],
                "reference": {"path": reference_path.as_posix(),
                              "sha256": rundir.file_sha256(reference_path)},
                "n_negative": args.n_negative, "judge_url": args.judge_url}
    run = _Run(args, config_path, resolved, [], [], int(config["seed"]))
    n = 0
    try:
        pj, _ = _judges(config, args.judge_url, run, True, False)
        segments = gq.read_segments(segments_path)
        a, b = (gq.read_jsonl(p) for p in gold_paths)
        pairs = g.predicate_check_pairs(a, b, segments, args.n_negative)
        reference = {r["pair_id"]: r["reference"] for r in gq.read_jsonl(reference_path)}
        verdicts = dict(zip([p["pair_id"] for p in pairs],
                            _parallel(args.workers)(pj, pairs), strict=True))
        result = g.predicate_check(pairs, reference, lambda p: verdicts[p["pair_id"]])
        (run.dir / "metrics.json").write_text(json.dumps(result["metrics"], indent=2,
                                                         sort_keys=True) + "\n",
                                              encoding="utf-8")
        _write_jsonl(run.dir / "judgements.jsonl", result["rows"])
        n = result["metrics"]["n"]
        run.say(json.dumps(result["metrics"], sort_keys=True))
        run.json.finish(n)
        run.say(f"run directory: {run.dir} status={run.json.data['status']}")
    except BaseException as exc:
        run.say(traceback.format_exc())
        run.json.finish(n, f"{type(exc).__name__}: {exc}")
        raise
    finally:
        run.close()
    return 0 if run.json.data["status"] == "completed" else 1


# ---- controlled sequences --------------------------------------------------------------------


def _sequence_config(config: dict):
    from grace.eval.datasets.benchmarks.base import BenchmarkConfig
    seq = config["sequences"]
    bc = BenchmarkConfig.from_dict(seq["dataset"])
    if bc.splits[seq["split"]].kind != "development":
        raise SystemExit("controlled sequences: development splits only")
    return seq, bc


def extract_sequences(args: argparse.Namespace) -> int:
    """Writer-only extraction of whole controlled sequences (stage `probe`): every message of each
    sequence in order, `finish()` at the end (`eval/runner/probes/writer_extract`); writes
    `updates.jsonl` and `graphs/<sequence_id>/`. `n_records`: sequences written."""
    from grace.context.pipeline.update.updater import WriterConfig, llm_writer
    from grace.eval.datasets.benchmarks.splits import load_split
    from grace.eval.runner.probes.writer_extract import drive_history

    config_path, config = _load_config(args.config)
    seq, bc = _sequence_config(config)
    writer_config_path = REPO_ROOT / config["writer_config"]
    writer_config = WriterConfig.load(writer_config_path)
    run_parent = (args.run_parent or shared_dir("runs_root") / args.experiment / "artifacts"
                  / WORKER)
    run_dir = rundir.create(run_parent, args.experiment, args.run_id)
    log = (run_dir / "run.log").open("a", encoding="utf-8")

    def say(text: str) -> None:
        print(text, flush=True)
        log.write(text + "\n")
        log.flush()

    model_config = REPO_ROOT / config["model_config"]
    resolved = {"experiment": config,
                "writer": {"config": config["writer_config"],
                           "sha256": rundir.file_sha256(writer_config_path),
                           "values": yaml.safe_load(writer_config_path.read_text("utf-8"))},
                "serving": {"writer_url": args.writer_url, "compute": args.compute or "none",
                            **config.get("serving", {})},
                "workers": args.workers}
    (run_dir / "resolved-config.yaml").write_text(yaml.safe_dump(resolved, sort_keys=False),
                                                  encoding="utf-8")
    code = rundir.code_state()
    root = project_root()
    run = rundir.RunJson(run_dir, {
        "run_id": run_dir.name, "experiment": args.experiment, "stage": "probe", "upstream": [],
        "code_sha": code.sha, "code_dirty": code.dirty,
        "config_path": config_path.relative_to(REPO_ROOT).as_posix(),
        "config_sha256": rundir.file_sha256(run_dir / "resolved-config.yaml"),
        "resources_sha256": rundir.resources_sha256(),
        "data": [{"benchmark": bc.benchmark, "version": bc.version,
                  "manifest_sha256": bc.manifest_sha256, "split": seq["split"],
                  "path": bc.source_dir(root).as_posix()}],
        "project_root": root.as_posix(), "seed": int(config["seed"]),
        "command": " ".join(shlex.quote(a) for a in sys.argv),
        "environment": rundir.environment("cpu (writer model on the serving endpoint)"),
        "compute": args.compute or "none", "held_out_access": "none"})
    n_done = 0
    try:
        client = _client(model_config, args.writer_url, run_dir / "calls.jsonl", run_dir.name)
        records = load_split(bc.benchmark, seq["split"], config=bc)
        wanted = list(seq["ids"])
        histories = {h.history_id: h for h in records.histories if h.history_id in wanted}
        missing = sorted(set(wanted) - histories.keys())
        if missing:
            raise ValueError(f"sequences not in the dataset split: {missing}")
        messages = defaultdict(list)
        for m in records.messages:
            if m.history_id in histories:
                messages[m.history_id].append(m)
        say(f"{len(wanted)} sequences, {sum(len(v) for v in messages.values())} messages, "
            f"granularity={writer_config.granularity.name}")
        if args.workers > 1:   # pyshacl is not thread safe (E007 run E007-20261128T110034Z-b2de)
            from grace.cli.writer_ablation import serialise_shacl
            serialise_shacl()

        def one(sid):
            updates = drive_history(histories[sid], messages[sid],
                                    llm_writer(writer_config, client, histories[sid]),
                                    writer_config, run_dir)
            say(f"  {sid}: {len(updates)} unit records")
            return updates

        with ThreadPoolExecutor(max_workers=max(1, args.workers)) as pool:
            results = list(pool.map(one, wanted))
        with (run_dir / "updates.jsonl").open("w", encoding="utf-8") as f:
            for u in (u for part in results for u in part):
                f.write(json.dumps(u, ensure_ascii=False, sort_keys=True) + "\n")
        n_done = len(results)
        from grace.eval.analysis.metrics import writer as metric
        updates = metric.read_jsonl(run_dir / "updates.jsonl")
        calls = metric.read_jsonl(run_dir / "calls.jsonl")
        metrics = {"units": metric.unit_stats(updates), "calls": metric.call_stats(calls),
                   "model_calls": len(calls), "sequences": n_done}
        (run_dir / "metrics.json").write_text(json.dumps(metrics, indent=2, sort_keys=True)
                                              + "\n", encoding="utf-8")
        run.data["model_calls"] = len(calls)
        run.finish(n_done)
        say(f"run directory: {run_dir} status={run.data['status']}"
            + (f" failure={run.data['failure']}" if run.data["failure"] else ""))
    except BaseException as exc:
        say(traceback.format_exc())
        run.finish(n_done, f"{type(exc).__name__}: {exc}")
        raise
    finally:
        log.close()
    return 0 if run.data["status"] == "completed" else 1


def score_sequences(args: argparse.Namespace) -> int:
    """Score a writer run over controlled sequences against their gold graphs (stage `score`):
    `metrics.json` (`grace.eval.analysis.metrics.graph_sequences`), `occurrences.jsonl` and
    `judgements.jsonl`. `n_records`: sequences scored."""
    from grace.eval.analysis.metrics import graph as g
    from grace.eval.analysis.metrics import graph_sequences as gs

    config_path, config = _load_config(args.config)
    seq, bc = _sequence_config(config)
    writer_dir = args.writer_run.resolve()
    writer_json = json.loads((writer_dir / "run.json").read_text(encoding="utf-8"))
    if writer_json.get("status") != "completed":
        raise SystemExit(f"upstream run {writer_dir.name} is not completed")
    method = args.predicate_match or config["scoring"]["predicate_match"]
    source = bc.source_dir(project_root())
    dirs = {sid: source / "sequences" / sid for sid in seq["ids"]}
    resolved = {"experiment": config, "writer_run": writer_dir.as_posix(),
                "predicate_match": method, "judge_url": args.judge_url,
                "gold_graphs": {sid: rundir.file_sha256(d / "graph" / "changesets.jsonl")
                                for sid, d in dirs.items()}}
    upstream = [{"run_id": writer_json["run_id"], "stage": writer_json["stage"],
                 "path": writer_dir.as_posix(),
                 "run_json_sha256": rundir.file_sha256(writer_dir / "run.json")}]
    run = _Run(args, config_path, resolved, upstream, writer_json.get("data", []),
               int(config["seed"]))
    n = 0
    try:
        pj, _ = _judges(config, args.judge_url, run, method == "judge", False)
        matcher = g.PredicateMatcher(method, pj)
        metrics, rows = gs.score_run(g.read_writer_run(writer_dir), dirs, matcher,
                                     _parallel(args.workers))
        metrics["predicate_matcher"] = {"method": method, "judged_pairs": len(matcher.log),
                                        "verdicts": dict(sorted(Counter(
                                            x["verdict"] for x in matcher.log).items()))}
        metrics["writer_run"] = {"run_id": writer_json["run_id"]}
        (run.dir / "metrics.json").write_text(json.dumps(metrics, indent=2, sort_keys=True)
                                              + "\n", encoding="utf-8")
        _write_jsonl(run.dir / "occurrences.jsonl", rows)
        _write_jsonl(run.dir / "judgements.jsonl", matcher.log)
        n = len(dirs)
        a = metrics["all"]
        run.say(json.dumps({"anchor": a["anchor"], "loose": a["loose"],
                            "endings": a["endings"], "ending_drops": a["ending_drops"]},
                           sort_keys=True))
        run.json.finish(n)
        run.say(f"run directory: {run.dir} status={run.json.data['status']}")
    except BaseException as exc:
        run.say(traceback.format_exc())
        run.json.finish(n, f"{type(exc).__name__}: {exc}")
        raise
    finally:
        run.close()
    return 0 if run.json.data["status"] == "completed" else 1


def coverage(args: argparse.Namespace) -> int:
    """Answer-coverage upper bound of the graphs of one ingest run (stage `score`): per question
    of the run's benchmark split, whether its evidence messages carry claims and whether the
    reference answer's words occur in them (`graph_sequences.answer_coverage`). Writes
    `metrics.json` and `coverage.jsonl`. `n_records`: questions."""
    from grace.eval.analysis.metrics import graph as g
    from grace.eval.analysis.metrics import graph_sequences as gs
    from grace.eval.datasets.benchmarks.splits import load_split

    config_path, config = _load_config(args.config)
    ingest_dir = args.ingest_run.resolve()
    ingest_json = json.loads((ingest_dir / "run.json").read_text(encoding="utf-8"))
    if ingest_json.get("stage") != "ingest" or ingest_json.get("status") != "completed":
        raise SystemExit(f"{ingest_dir.name}: a completed ingest run is required")
    ingest_cfg = yaml.safe_load((ingest_dir / "resolved-config.yaml").read_text("utf-8"))
    resolved = {"experiment": config, "ingest_run": ingest_dir.as_posix(),
                "benchmark": ingest_cfg["benchmark"], "split": ingest_cfg["split"],
                "histories": ingest_cfg["histories"]}
    upstream = [{"run_id": ingest_json["run_id"], "stage": "ingest",
                 "path": ingest_dir.as_posix(),
                 "run_json_sha256": rundir.file_sha256(ingest_dir / "run.json")}]
    run = _Run(args, config_path, resolved, upstream, ingest_json.get("data", []),
               int(config["seed"]))
    n = 0
    try:
        records = load_split(ingest_cfg["benchmark"], ingest_cfg["split"])
        wanted = set(ingest_cfg["histories"])
        gold = []
        for r in records.gold:
            if r.history_id not in wanted:
                continue
            labels = r.labels or {}
            gold.append({"history_id": r.history_id, "task_id": r.task_id,
                         "reference": r.reference, "evidence_ids": list(r.evidence_ids),
                         "stratum": labels.get("question_type", labels.get("category"))})
        metrics, rows = gs.answer_coverage(g.read_writer_run(ingest_dir).graphs, gold)
        metrics["ingest_run"] = ingest_json["run_id"]
        (run.dir / "metrics.json").write_text(json.dumps(metrics, indent=2, sort_keys=True)
                                              + "\n", encoding="utf-8")
        _write_jsonl(run.dir / "coverage.jsonl", rows)
        n = len(rows)
        run.say(json.dumps(metrics["all"], sort_keys=True))
        run.json.finish(n)
        run.say(f"run directory: {run.dir} status={run.json.data['status']}")
    except BaseException as exc:
        run.say(traceback.format_exc())
        run.json.finish(n, f"{type(exc).__name__}: {exc}")
        raise
    finally:
        run.close()
    return 0 if run.json.data["status"] == "completed" else 1


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = parser.add_subparsers(dest="command", required=True)
    p_ext = sub.add_parser("extract", help="writer-only extraction of the sampled segments")
    p_ext.add_argument("--config", type=Path, required=True)
    p_ext.add_argument("--writer-url", required=True)
    p_ext.add_argument("--compute", default=None, help="reservation copied into run.json")
    p_ext.add_argument("--segments-only", nargs="*", default=None, help="segment keys")
    p_ext.add_argument("--workers", type=int, default=4, help="segments written in parallel")
    for p in (p_sco := sub.add_parser("score", help="score one writer run directory"),
              p_chk := sub.add_parser("predicate-check",
                                      help="check predicate matchers on two label files")):
        p.add_argument("--config", type=Path, required=True)
        p.add_argument("--judge-url", default=None)
        p.add_argument("--gold", type=Path, nargs="*", default=None,
                       help="gold label files (default: scoring.gold of the config)")
        p.add_argument("--segments", type=Path, default=None)
        p.add_argument("--compute", default=None)
        p.add_argument("--workers", type=int, default=8, help="parallel judge calls")
        p.add_argument("--label", default=None, help="free text stored in run.json")
    p_sco.add_argument("writer_run", type=Path)
    p_sco.add_argument("--predicate-match", choices=("normalised", "lexical", "judge"),
                       default=None)
    p_sco.add_argument("--no-entailment", action="store_true")
    p_sco.add_argument("--benchmarks", nargs="*", default=None,
                       help="score only the segments of these benchmarks")
    p_sco.add_argument("--allow-incomplete", action="store_true",
                       help="score a writer run that is not completed (dry runs only)")
    p_xs = sub.add_parser("extract-sequences",
                          help="writer-only extraction of whole controlled sequences")
    p_xs.add_argument("--config", type=Path, required=True)
    p_xs.add_argument("--writer-url", required=True)
    p_xs.add_argument("--compute", default=None, help="reservation copied into run.json")
    p_xs.add_argument("--workers", type=int, default=4, help="sequences written in parallel")
    p_ss = sub.add_parser("score-sequences",
                          help="score a sequence writer run against the gold graphs")
    p_ss.add_argument("writer_run", type=Path)
    p_ss.add_argument("--config", type=Path, required=True)
    p_ss.add_argument("--judge-url", default=None)
    p_ss.add_argument("--compute", default=None)
    p_ss.add_argument("--workers", type=int, default=8, help="parallel judge calls")
    p_ss.add_argument("--label", default=None, help="free text stored in run.json")
    p_ss.add_argument("--predicate-match", choices=("normalised", "lexical", "judge"),
                      default=None)
    p_cov = sub.add_parser("coverage", help="answer-coverage upper bound of an ingest run")
    p_cov.add_argument("ingest_run", type=Path)
    p_cov.add_argument("--config", type=Path, required=True)
    p_cov.add_argument("--compute", default=None)
    p_cov.add_argument("--label", default=None, help="free text stored in run.json")
    p_chk.add_argument("--reference", type=Path, default=Path(
        "docs/research/annotations/graph-quality/predicate-check-reference.jsonl"))
    p_chk.add_argument("--n-negative", type=int, default=80)
    for p in (p_ext, p_sco, p_chk, p_xs, p_ss, p_cov):
        p.add_argument("--experiment", default="E006")
        p.add_argument("--run-parent", type=Path, default=None)
        p.add_argument("--run-id", default=None)
    args = parser.parse_args(argv)
    return {"extract": extract, "score": score, "predicate-check": predicate_check,
            "extract-sequences": extract_sequences, "score-sequences": score_sequences,
            "coverage": coverage}[
        args.command](args)


if __name__ == "__main__":
    sys.exit(main())
