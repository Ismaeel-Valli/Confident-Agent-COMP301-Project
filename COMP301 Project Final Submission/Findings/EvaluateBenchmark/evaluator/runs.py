"""Discovers the benchmark's runs and reads their files, from run folders or from zipped
archives anywhere under Benchmark/. An archive holds `Baseline_Tests/<label>/...` (a zipped
mode folder), or `<label>/...` when the archive or the folder it is in is named after the
mode (`Completed Runs/<model>/Baseline_Tests.zip`, `Baseline_Tests/<label>.zip`).

Shared by evaluate_benchmark.py and compile_stats.py so both agree on what a run is:
its model, quantization, benchmark version, machine and role.

Role
  main         run with the newest benchmark version found; the runs compared with each
               other (quantizations, models) and the Holm family of EVALUATION_PLAN.md §6
  preliminary  run made with an older benchmark version (different measurements or
               verifier); scored and kept, but not part of the main comparison
"""
from __future__ import annotations

import json
import re
import zipfile
from pathlib import Path

MODE_DIRS = {"baseline": "Baseline_Tests", "intervention": "Intervention_Tests"}
KEEP = ("result.json", "run_manifest.json")


class BenchmarkFiles:
    """result.json and run_manifest.json of every run, from folders or zips (recursive)."""

    def __init__(self, root: Path):
        self.root = root
        self.index: dict = {}     # (mode dir, label, [task,] file) -> (archive path or None, member name)
        self._open: dict = {}     # archive path -> ZipFile, kept open (a run has thousands of members)
        modes = set(MODE_DIRS.values())
        for archive in sorted(root.rglob("*.zip")):
            implied = next((n for n in (archive.stem, archive.parent.name) if n in modes), None)
            with zipfile.ZipFile(archive) as z:
                for name in z.namelist():
                    parts = tuple(name.replace("\\", "/").split("/"))
                    if parts[0] not in modes and implied:
                        parts = (implied, *parts)
                    if len(parts) >= 3 and parts[0] in modes and parts[-1] in KEEP:
                        self.index.setdefault(parts, (archive, name))
        self.archives = sorted({a for a, _ in self.index.values()})

    def read(self, *parts: str) -> dict | None:
        path = self.root.joinpath(*parts)
        if path.exists():  # a run folder on disk wins over an archived copy
            return json.loads(path.read_text(encoding="utf-8"))
        hit = self.index.get(tuple(parts))
        if not hit:
            return None
        archive, name = hit
        if archive not in self._open:
            self._open[archive] = zipfile.ZipFile(archive)
        return json.loads(self._open[archive].read(name).decode("utf-8"))

    def result(self, mode: str, label: str, task: str) -> dict | None:
        return self.read(MODE_DIRS[mode], label, task, "result.json")

    def manifest(self, mode: str, label: str) -> dict:
        return self.read(MODE_DIRS[mode], label, "run_manifest.json") or {}

    def labels(self) -> set:
        found = {parts[1] for parts in self.index if parts[-1] == "run_manifest.json"}
        for folder in MODE_DIRS.values():
            base = self.root / folder
            if base.exists():
                found |= {p.name for p in base.iterdir() if p.is_dir()}
        return found

    def close(self):
        for z in self._open.values():
            z.close()
        self._open.clear()


def normalize(text: str) -> str:
    return re.sub(r"[^a-z0-9]", "", (text or "").lower())


def describe(files: BenchmarkFiles, label: str) -> dict:
    """Everything the manifests say about one run."""
    info: dict = {"label": label, "versions": [], "commits": [], "started": {}}
    for mode in ("baseline", "intervention"):
        m = files.manifest(mode, label)
        if not m:
            continue
        settings, model = m.get("settings") or {}, m.get("lmstudio_model_info") or {}
        invocations = m.get("invocations") or [{}]
        env = invocations[-1].get("environment") or {}
        power = invocations[-1].get("power") or {}
        info["versions"].append(settings.get("benchmark_version") or "before 2026-09-26.2")
        info["commits"] += [(i.get("git_commit") or "")[:7] for i in invocations]
        info["started"][mode] = (invocations[0].get("started") or "")[:19]
        gpus = power.get("gpus") or env.get("gpus") or []
        for key, value in (("model", settings.get("model")), ("quantization", model.get("quantization")),
                           ("architecture", model.get("arch")), ("context_length", m.get("context_limit")),
                           ("thinking", settings.get("thinking")), ("temperature", settings.get("temperature")),
                           ("max_tokens", settings.get("max_tokens")), ("seed", settings.get("seed")),
                           ("machine_cpu", env.get("cpu")), ("machine_gpu", ", ".join(g.get("name", "") for g in gpus) or None),
                           ("machine_ram_gb", env.get("ram_gb")), ("power_backend", power.get("backend")),
                           ("power_idle_w", json.dumps(power.get("idle_w")) if power.get("idle_w") else None)):
            info.setdefault(key, value)
        if mode == "intervention":
            info["max_turns"] = settings.get("max_turns")
            info["frozen_package_evidence"] = bool(settings.get("package_evidence_sha256"))
    info["benchmark_version"] = max(info["versions"]) if info["versions"] else None
    info["started_first"] = min(info["started"].values()) if info["started"] else None
    info["commits"] = sorted(set(c for c in info["commits"] if c))
    quant = normalize(info.get("quantization") or "")
    info["label_matches_quantization"] = bool(quant) and quant in normalize(label)
    return info


def discover(root: Path, labels: list | None = None) -> dict:
    """label -> run description, with a `role` for each (see the module docstring)."""
    files = BenchmarkFiles(root)
    try:
        wanted = sorted(labels if labels is not None else files.labels())
        runs = {label: describe(files, label) for label in wanted}
    finally:
        files.close()
    versions = [r["benchmark_version"] for r in runs.values() if r["benchmark_version"]]
    newest = max(versions) if versions else None
    for r in runs.values():
        if r["benchmark_version"] == newest and len(set(r["versions"])) == 1:
            r["role"], r["role_reason"] = "main", f"benchmark {newest}"
        elif len(set(r["versions"])) > 1:
            r["role"], r["role_reason"] = "preliminary", f"baseline and intervention used different benchmark versions {r['versions']}"
        else:
            r["role"] = "preliminary"
            r["role_reason"] = f"benchmark {r['benchmark_version']} is older than {newest}: earlier measurements and verifier"
    return runs
