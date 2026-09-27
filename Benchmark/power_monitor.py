"""Power sampling for run_benchmark.py (standard library only).

Power is sampled for the whole run in a background thread; the energy of a task is the
integral of the samples over that task's time window (each sample held until the next).

Backends
--------
nvidia-smi
    NVIDIA GPU board power (``power.draw``).
LibreHardwareMonitor (LHM)
    Any GPU LHM supports, including AMD Radeon cards such as the RX 9070 XT, read from
    LHM's Remote Web Server (``/data.json``). When LHM runs as administrator it also
    reports CPU package power, which covers the verifier (Pyright, claim extraction,
    Node) as well as the CPU share of inference.

Only the listed channels are measured, never the whole system: memory, storage,
motherboard and power-supply losses are not included. For whole-system energy use a
wall power meter together with the task timestamps.
"""
from __future__ import annotations

import json
import re
import shutil
import subprocess
import threading
import time
import urllib.error
import urllib.request

LHM_URL_DEFAULT = "http://localhost:8085/data.json"
# Preferred sensor names, most complete first. LHM names differ between versions and vendors.
GPU_SENSOR_PREFERENCE = ["GPU Package", "GPU Total", "Total Board Power", "GPU Board", "GPU Power", "Package", "GPU Core"]
CPU_SENSOR_PREFERENCE = ["Package", "CPU Package", "Cores"]
WATTS_RE = re.compile(r"^\s*(-?[\d.,]+)\s*W\s*$")


def parse_watts(value) -> float | None:
    """'45.2 W' or '45,2 W' (LHM uses the Windows number format) -> 45.2."""
    match = WATTS_RE.match(str(value or ""))
    if not match:
        return None
    try:
        return float(match.group(1).replace(",", "."))
    except ValueError:
        return None


def lhm_power_sensors(tree: dict) -> list:
    """Every power sensor in an LHM data.json tree, with the hardware it belongs to."""
    found = []

    def walk(node, path, hardware):
        image = str(node.get("ImageURL") or "").lower()
        kind = None
        if any(k in image for k in ("cpu.png",)):
            kind = "cpu"
        elif any(k in image for k in ("ati.png", "amd.png", "nvidia.png", "intel.png", "gpu")):
            kind = "gpu"
        if kind:
            hardware = {"name": node.get("Text"), "kind": kind}
        children = node.get("Children") or []
        watts = parse_watts(node.get("Value"))
        if not children and watts is not None and (node.get("Type") in (None, "Power")):
            sensor_id = node.get("SensorId") or ""
            sensor_kind = hardware["kind"] if hardware else None
            if sensor_id.startswith(("/amdcpu", "/intelcpu")):
                sensor_kind = "cpu"
            elif sensor_id.startswith(("/gpu", "/atigpu", "/amdgpu", "/nvidiagpu", "/intelgpu")):
                sensor_kind = "gpu"
            if sensor_kind:
                found.append({"kind": sensor_kind, "hardware": hardware["name"] if hardware else None,
                              "sensor": node.get("Text"), "sensor_id": sensor_id or None,
                              "path": path + [node.get("Text")], "watts": watts})
        for child in children:
            walk(child, path + [node.get("Text")], hardware)

    walk(tree, [], None)
    return found


def choose_sensor(sensors: list, kind: str, hardware_hint: str | None, sensor_hint: str | None) -> dict | None:
    """One sensor per kind. Several GPUs (e.g. a Ryzen's integrated graphics next to an
    RX 9070 XT): the hardware named by the hint, else the GPU drawing the most power now,
    which during a benchmark is the discrete card running the model."""
    candidates = [s for s in sensors if s["kind"] == kind]
    if hardware_hint:
        candidates = [s for s in candidates if hardware_hint.lower() in (s["hardware"] or "").lower()]
    if sensor_hint:
        candidates = [s for s in candidates if s["sensor"].lower() == sensor_hint.lower()]
    if not candidates:
        return None
    preference = GPU_SENSOR_PREFERENCE if kind == "gpu" else CPU_SENSOR_PREFERENCE
    by_hardware: dict = {}
    for s in candidates:
        by_hardware.setdefault(s["hardware"], []).append(s)
    best = []
    for items in by_hardware.values():
        ranked = sorted(items, key=lambda s: preference.index(s["sensor"]) if s["sensor"] in preference else len(preference))
        best.append(ranked[0])
    return max(best, key=lambda s: s["watts"])


def fetch_json(url: str, timeout: float = 3) -> dict:
    with urllib.request.urlopen(url, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


class PowerMonitor:
    def __init__(self, mode: str = "auto", interval_ms: int = 500, lhm_url: str = LHM_URL_DEFAULT,
                 lhm_gpu: str | None = None, lhm_gpu_sensor: str | None = None):
        self.samples: list = []  # (monotonic time, channel, watts)
        self.lock = threading.Lock()
        self.interval_ms = interval_ms
        self.backend = None
        self.reason = None
        self.channels: dict = {}  # channel -> description of the sensor
        self.gpus: list = []
        self.idle_w: dict = {}
        self._stop = threading.Event()
        self._proc = None
        self.lhm_url = lhm_url
        if mode == "none":
            self.reason = "disabled with --power none"
            return
        nvidia = shutil.which("nvidia-smi") if mode in ("auto", "nvidia") else None
        if nvidia:
            self._start_nvidia(nvidia)
        elif mode in ("auto", "lhm"):
            self._start_lhm(lhm_gpu, lhm_gpu_sensor, required=mode == "lhm")
        else:
            raise SystemExit("--power nvidia was requested but nvidia-smi is not available.")

    # ------------------------------------------------------------------ backends
    def _start_nvidia(self, exe: str) -> None:
        fields = "index,name,driver_version,memory.total,power.limit"
        out = subprocess.run([exe, f"--query-gpu={fields}", "--format=csv,noheader,nounits"],
                             capture_output=True, text=True, timeout=20).stdout
        for line in out.strip().splitlines():
            idx, name, driver, mem, limit = [x.strip() for x in line.split(",")]
            self.gpus.append({"index": idx, "name": name, "driver": driver, "memory_mib": mem, "power_limit_w": limit})
            self.channels[f"gpu{idx}"] = {"kind": "gpu", "hardware": name, "sensor": "power.draw"}
        self.backend = "nvidia-smi"
        self._proc = subprocess.Popen([exe, "--query-gpu=index,power.draw", "--format=csv,noheader,nounits",
                                       f"-lms={self.interval_ms}"], stdout=subprocess.PIPE,
                                      stderr=subprocess.DEVNULL, text=True, bufsize=1)

        def read():
            for line in self._proc.stdout:
                try:
                    idx, watts = [x.strip() for x in line.split(",")]
                    self._add(f"gpu{idx}", float(watts))
                except ValueError:
                    continue  # "[N/A]" or a partial line
        threading.Thread(target=read, daemon=True).start()

    def _start_lhm(self, gpu_hint, sensor_hint, required: bool) -> None:
        try:
            sensors = lhm_power_sensors(fetch_json(self.lhm_url))
        except (urllib.error.URLError, OSError, ValueError) as e:
            self.reason = (f"no nvidia-smi, and LibreHardwareMonitor's web server is not reachable at {self.lhm_url} "
                           f"({getattr(e, 'reason', e)}): power is not measured")
            if required:
                raise SystemExit(self.reason)
            return
        self.available = sensors
        for kind, hints in (("gpu", (gpu_hint, sensor_hint)), ("cpu", (None, None))):
            chosen = choose_sensor(sensors, kind, *hints)
            if chosen:
                self.channels[kind] = chosen
        if "gpu" not in self.channels:
            self.reason = "LibreHardwareMonitor is running but reports no GPU power sensor"
            if required:
                raise SystemExit(self.reason)
            return
        self.gpus = [{"name": self.channels["gpu"]["hardware"], "sensor": self.channels["gpu"]["sensor"]}]
        self.backend = "LibreHardwareMonitor"

        def poll():
            while not self._stop.is_set():
                started = time.monotonic()
                try:
                    now = {(s["hardware"], s["sensor"]): s["watts"] for s in lhm_power_sensors(fetch_json(self.lhm_url))}
                    for channel, sensor in self.channels.items():
                        watts = now.get((sensor["hardware"], sensor["sensor"]))
                        if watts is not None:
                            self._add(channel, watts)
                except (urllib.error.URLError, OSError, ValueError):
                    pass  # a missed poll only widens the gap between samples
                self._stop.wait(max(0.0, self.interval_ms / 1000 - (time.monotonic() - started)))
        threading.Thread(target=poll, daemon=True).start()

    def _add(self, channel: str, watts: float) -> None:
        with self.lock:
            self.samples.append((time.monotonic(), channel, watts))

    # ------------------------------------------------------------------ results
    @property
    def active(self) -> bool:
        return self.backend is not None

    def energy(self, t0: float, t1: float) -> dict:
        """Energy per kind (gpu, cpu) over [t0, t1]."""
        if not self.active:
            return {"measured": False, "reason": self.reason}
        with self.lock:
            # Samples ending well before the window are no longer needed (tasks run in sequence).
            self.samples = [s for s in self.samples if s[0] >= t0 - 60]
            samples = list(self.samples)
        seconds = max(t1 - t0, 1e-9)
        per_kind: dict = {}
        for channel, sensor in self.channels.items():
            series = [s for s in samples if s[1] == channel]
            joules, peak, count = 0.0, None, 0
            for (ta, _, wa), (tb, _, _) in zip(series, series[1:] + [(t1, channel, 0.0)]):
                overlap = min(tb, t1) - max(ta, t0)
                if overlap > 0:
                    joules += wa * overlap
                    count += 1
                    peak = wa if peak is None else max(peak, wa)
            k = per_kind.setdefault(sensor["kind"], {"joules": 0.0, "peak": None, "samples": 0})
            k["joules"] += joules
            k["samples"] += count
            if peak is not None:
                k["peak"] = peak if k["peak"] is None else max(k["peak"], peak)
        result = {"measured": any(k["samples"] for k in per_kind.values()), "source": self.backend,
                  "channels": {c: f"{s['hardware']}: {s['sensor']}" for c, s in self.channels.items()}}
        total = 0.0
        for kind, k in per_kind.items():
            result[f"{kind}_energy_j"] = round(k["joules"], 1)
            result[f"{kind}_mean_w"] = round(k["joules"] / seconds, 1)
            result[f"{kind}_peak_w"] = k["peak"]
            result[f"{kind}_samples"] = k["samples"]
            if kind in self.idle_w:
                result[f"{kind}_energy_above_idle_j"] = round(k["joules"] - self.idle_w[kind] * seconds, 1)
            total += k["joules"]
        result["measured_energy_j"] = round(total, 1)
        result["measured_energy_wh"] = round(total / 3600, 4)
        if self.idle_w and all(kind in self.idle_w for kind in per_kind):
            result["measured_energy_above_idle_j"] = round(total - sum(self.idle_w.values()) * seconds, 1)
        return result

    def measure_idle(self, seconds: float) -> None:
        if not self.active or seconds <= 0:
            return
        print(f"[setup] Measuring idle power for {seconds:.0f} s ...", flush=True)
        time.sleep(2 * self.interval_ms / 1000)  # let the first samples arrive, so the window starts covered
        t0 = time.monotonic()
        time.sleep(seconds)
        measured = self.energy(t0, time.monotonic())
        for kind in ("gpu", "cpu"):
            if measured.get(f"{kind}_samples"):
                self.idle_w[kind] = measured[f"{kind}_mean_w"]

    def describe(self) -> dict:
        return {"backend": self.backend, "reason": self.reason, "channels": self.channels, "gpus": self.gpus,
                "sample_interval_ms": self.interval_ms if self.active else None, "idle_w": self.idle_w,
                "lhm_url": self.lhm_url if self.backend == "LibreHardwareMonitor" else None,
                "scope": "only the listed channels (GPU; CPU package with LibreHardwareMonitor as administrator); "
                         "memory, storage, motherboard and power-supply losses are not included"}

    def summary_line(self) -> str:
        if not self.active:
            return self.reason
        return f"{self.backend}: " + "; ".join(f"{c} = {s['hardware']} / {s['sensor']}" for c, s in self.channels.items())

    def stop(self) -> None:
        self._stop.set()
        if self._proc:
            self._proc.terminate()


def power_check(monitor: PowerMonitor, seconds: float = 5) -> None:
    """Print what would be measured, then a few seconds of readings."""
    print("Power backend:", monitor.summary_line())
    for sensor in getattr(monitor, "available", []):
        print(f"  available: [{sensor['kind']}] {sensor['hardware']} / {sensor['sensor']} = {sensor['watts']} W")
    if not monitor.active:
        return
    t0 = time.monotonic()
    time.sleep(seconds)
    reading = monitor.energy(t0, time.monotonic())
    print(json.dumps(reading, indent=2))
