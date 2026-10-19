"""Architecture and UML diagrams for the final report (matplotlib only, no Graphviz needed).

  D01 experimental pipeline        D05 activity: decision policy
  D02 deployment / components      D06 how the six layers read a candidate
  D03 class diagram (core)         D07 evaluator: independent classification
  D04 sequence: one task

Run:  python -X utf8 build_diagrams.py     -> figures/D*.png
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Polygon, Rectangle, FancyArrowPatch, Circle

OUT = Path(__file__).resolve().parent / "figures"
OUT.mkdir(exist_ok=True)

INK, INK2, MUTED, LINE, SURF = "#0b0b0b", "#52514e", "#898781", "#8a8880", "#fcfcfb"
BLUE, ORANGE, GREEN, PURPLE, RED, AMBER, GREY = "#2a78d6", "#eb6834", "#1baf7a", "#6250d6", "#d03b3b", "#e8a200", "#c4c2bb"
TINT = {BLUE: "#e6eefa", ORANGE: "#fdebe2", GREEN: "#e2f5ee", PURPLE: "#ebe8fa", RED: "#f8e4e4", AMBER: "#fcf1d9", GREY: "#f1f0ec"}
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9.5, "text.color": INK})


def canvas(w, h):
    fig = plt.figure(figsize=(w, h))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, w)
    ax.set_ylim(0, h)
    ax.axis("off")
    fig.patch.set_facecolor(SURF)
    return fig, ax


def save(fig, name):
    fig.savefig(OUT / name, dpi=220, facecolor=SURF)
    plt.close(fig)
    print("wrote", name)


def box(ax, x, y, w, h, title, lines=(), color=GREY, stereo=None, fs=9.2, title_fs=10, rounded=True, align="left", fill=None):
    """A labelled box; (x, y) is the lower-left corner. Returns its centre and edges."""
    style = "round,pad=0.02,rounding_size=0.08" if rounded else "square,pad=0"
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=style, fc=fill or TINT.get(color, "#f4f4f2"), ec=color, lw=1.4))
    ty = y + h - 0.12
    if stereo:
        ax.text(x + w / 2, ty, f"«{stereo}»", ha="center", va="top", fontsize=fs - 0.8, color=INK2, style="italic")
        ty -= 0.2
    ax.text(x + w / 2, ty, title, ha="center", va="top", fontsize=title_fs, fontweight="bold", color=INK)
    ty -= 0.27
    for ln in lines:
        if align == "center":
            ax.text(x + w / 2, ty, ln, ha="center", va="top", fontsize=fs, color=INK2)
        else:
            ax.text(x + 0.12, ty, ln, ha="left", va="top", fontsize=fs, color=INK2)
        ty -= 0.2 * fs / 9.2 + 0.02
    return {"l": x, "r": x + w, "b": y, "t": y + h, "cx": x + w / 2, "cy": y + h / 2}


def arrow(ax, p, q, label=None, color=LINE, ls="-", head="->", lw=1.3, lpos=0.5, loff=(0, 0.12), lfs=8.3, rad=0.0, lcolor=None, lha="center"):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle=head, mutation_scale=12, color=color, lw=lw, ls=ls,
                                 connectionstyle=f"arc3,rad={rad}", shrinkA=2, shrinkB=2))
    if label:
        mx, my = p[0] + (q[0] - p[0]) * lpos + loff[0], p[1] + (q[1] - p[1]) * lpos + loff[1]
        ax.text(mx, my, label, ha=lha, va="center", fontsize=lfs, color=lcolor or INK2,
                bbox=dict(boxstyle="round,pad=0.12", fc=SURF, ec="none", alpha=0.9))


def diamond_end(ax, at, towards, filled=True, color=INK2, size=0.13):
    """UML aggregation (hollow) or composition (filled) diamond at `at`, pointing at `towards`."""
    import math
    dx, dy = towards[0] - at[0], towards[1] - at[1]
    d = math.hypot(dx, dy) or 1
    ux, uy = dx / d, dy / d
    px, py = -uy, ux
    pts = [at, (at[0] + ux * size + px * size * 0.55, at[1] + uy * size + py * size * 0.55),
           (at[0] + 2 * ux * size, at[1] + 2 * uy * size), (at[0] + ux * size - px * size * 0.55, at[1] + uy * size - py * size * 0.55)]
    ax.add_patch(Polygon(pts, closed=True, fc=color if filled else SURF, ec=color, lw=1.1, zorder=5))
    return (at[0] + 2 * ux * size, at[1] + 2 * uy * size)


def title(ax, w, h, text, sub=None):
    ax.text(0.2, h - 0.2, text, fontsize=14, fontweight="bold", va="top")
    if sub:
        ax.text(0.2, h - 0.55, sub, fontsize=9.5, va="top", color=INK2)


# --------------------------------------------------------------------------- D01
def d01():
    W, H = 15, 8.3
    fig, ax = canvas(W, H)
    title(ax, W, H, "Experimental pipeline: one dataset, two conditions, an independent judge",
          "Solid arrows: data flow. Dashed: the answer key, which only the evaluator reads. Everything to the right of the runs is offline and repeatable.")
    ds = box(ax, 0.3, 3.4, 2.9, 2.6, "Dataset Builder", ["1,000 Python tasks, 6 REST APIs", "142 operation families", "provider specs frozen 21 Sep 2026", "(SHA-256 per file and task)", "", "prompt-only file  ->  model", "task file = answer key"], color=PURPLE)
    hn = box(ax, 4.0, 1.2, 4.3, 5.1, "Benchmark harness", ["run_benchmark.py (benchmark 2026-09-27.2)", "same tasks, model and sampling settings"], color=GREY)
    bl = box(ax, 4.2, 4.15, 3.9, 1.1, "Baseline condition", ["Qwen3.5-9B + 2-line system prompt", "reply's code block is what the user gets"], color=BLUE, title_fs=9.5, fs=8.6)
    iv = box(ax, 4.2, 2.6, 3.9, 1.3, "Intervention condition", ["Qwen3.5-9B + Confident Agent prompt", "+ verify_candidate tool (function calling)", "decision of the tool on the last candidate"], color=ORANGE, title_fs=9.5, fs=8.6)
    tb = box(ax, 4.2, 1.35, 3.9, 1.0, "Confident Agent toolbox 3.0.0", ["6 layers · EWCS · decision policy", "frozen evidence selected by host"], color=ORANGE, title_fs=9.2, fs=8.4, fill="#fff7f2")
    lm = box(ax, 4.0, 6.5, 4.3, 0.55, "LM Studio: Qwen3.5-9B GGUF (Q4_K_M / Q6_K / Q8_0)", [], color=GREY, title_fs=8.8)
    pw = box(ax, 4.0, 0.3, 4.3, 0.65, "LibreHardwareMonitor: GPU + CPU power, 0.5 s", [], color=GREY, title_fs=8.8)
    rn = box(ax, 9.0, 3.4, 1.9, 2.6, "Completed runs", ["per task:", "replies, tool calls,", "every verified", "candidate, timing,", "tokens, energy", "", "zipped per model"], color=GREY)
    ev = box(ax, 11.55, 3.4, 3.15, 2.6, "Evaluate Benchmark", ["runs each candidate in a", "sandbox (python -I -S) with a", "recording stand-in for requests", "3 scenarios: ok / 204 / 500", "classes: correct, A, B,", "runtime failure, undetermined", "self-check: 1,000/1,000 refs"], color=GREEN)
    mr = box(ax, 11.55, 1.75, 3.15, 1.2, "Manual review and human audits", ["396 undetermined; 46 re-reviewed (kappa 0.88)", "answer-key audit: 100 tasks", "evaluator audit: 102 decisions, 2 reviewers"], color=GREEN, fs=8.0, title_fs=9.0)
    st = box(ax, 9.0, 0.3, 5.7, 1.05, "Stats compiler -> Statistical analysis -> report", ["CSV per prompt, group and run; McNemar, bootstrap, Holm;", "time, tokens and energy priced in Rand"], color=PURPLE, fs=8.5, title_fs=9.3)
    arrow(ax, (ds["r"], 5.0), (bl["l"], 4.7), "prompts only", lpos=0.45)
    arrow(ax, (ds["r"], 4.6), (iv["l"], 3.25), "same prompts", lpos=0.45)
    arrow(ax, (7.9, lm["b"]), (7.9, bl["t"]), None)
    arrow(ax, (iv["cx"], iv["b"]), (tb["cx"], tb["t"]), "verify_candidate(code)", loff=(0.95, 0))
    arrow(ax, (pw["cx"], pw["t"]), (pw["cx"], hn["b"]), None)
    arrow(ax, (hn["r"], 4.7), (rn["l"], 4.7), None)
    arrow(ax, (rn["r"], 4.7), (ev["l"], 4.7), None)
    arrow(ax, (ev["cx"], ev["b"]), (mr["cx"], mr["t"]), None)
    arrow(ax, (mr["cx"], mr["b"]), (mr["cx"], st["t"]), None)
    yk = 7.35
    ax.plot([ds["cx"], ds["cx"]], [ds["t"], yk], color=GREEN, lw=1.3, ls="--")
    ax.plot([ds["cx"], ev["cx"]], [yk, yk], color=GREEN, lw=1.3, ls="--")
    arrow(ax, (ev["cx"], yk), (ev["cx"], ev["t"]), None, color=GREEN, ls="--")
    ax.text((ds["cx"] + ev["cx"]) / 2, yk + 0.05, "answer key: expected request + pinned spec (never shown to the model or the agent)",
            fontsize=8.4, color=GREEN, ha="center", va="bottom", bbox=dict(boxstyle="round,pad=0.12", fc=SURF, ec="none"))
    save(fig, "D01_pipeline.png")


# --------------------------------------------------------------------------- D02
def d02():
    W, H = 15, 8.4
    fig, ax = canvas(W, H)
    title(ax, W, H, "Deployment and components (UML)", "Everything runs on one workstation; the evaluator shares no code with the toolbox.")
    ax.add_patch(Rectangle((0.3, 0.3), 14.4, 7.0, fc="#fbfbf9", ec=INK2, lw=1.2))
    ax.add_patch(Polygon([(0.3, 7.3), (0.55, 7.55), (14.95, 7.55), (14.7, 7.3)], fc="#efeee9", ec=INK2, lw=1.2))
    ax.add_patch(Polygon([(14.7, 7.3), (14.95, 7.55), (14.95, 0.55), (14.7, 0.3)], fc="#efeee9", ec=INK2, lw=1.2))
    ax.text(0.45, 7.12, "«device»  Workstation: Windows 11 · AMD Ryzen 7 5700X3D · AMD Radeon RX 9070 XT · 32 GB RAM (Durban Central)", fontsize=9.5, fontweight="bold", va="top")
    lm = box(ax, 0.6, 4.9, 3.2, 1.75, "LM Studio server", ["OpenAI-compatible API :1234", "artifact: Qwen3.5-9B (GGUF)", "Q4_K_M · Q6_K · Q8_0", "context 30,208 · tool use"], color=GREY, stereo="component", fs=8.6)
    hn = box(ax, 5.2, 4.9, 3.4, 1.75, "Benchmark harness", ["run_benchmark.py (Python 3.13)", "temperature 0.2 · thinking off", "max 4 turns · 4,096 tokens", "records timing, tokens, energy"], color=BLUE, stereo="component", fs=8.6)
    lh = box(ax, 9.4, 5.4, 2.4, 1.25, "LibreHardwareMonitor", ["web server :8085", "GPU and CPU Package"], color=GREY, stereo="component", fs=8.4)
    br = box(ax, 5.2, 3.35, 3.4, 1.15, "Tool bridge", ["tool_bridge.cjs (Node.js 24)", "one verify_candidate per call"], color=BLUE, stereo="component", fs=8.6)
    pl = box(ax, 0.6, 3.35, 3.2, 1.15, "LM Studio plugin", ["tools provider (demonstrations)", "same toolbox, chat UI"], color=GREY, stereo="component", fs=8.6)
    ax.add_patch(FancyBboxPatch((0.6, 0.55), 11.2, 2.45, boxstyle="round,pad=0.02,rounding_size=0.08", fc="#fff7f2", ec=ORANGE, lw=1.5))
    ax.text(0.75, 2.9, "«subsystem»  Confident Agent toolbox 3.0.0 (TypeScript, compiled dist/)", fontsize=9.5, fontweight="bold", va="top")
    parts = [("Claim extractor", ["Python ast, embedded,", "sent over stdin"]), ("Evidence registry", ["frozen OpenAPI snapshots", "selected by host"]),
             ("Package evidence", ["frozen PyPI record,", "stdlib inventory"]), ("Pyright runner", ["1.1.414, standard mode", "toolbox .venv (3.12)"]),
             ("OpenAPI verifier", ["layers 3-6: access point,", "input, output, context"]), ("EWCS + decision", ["policy 2026-09-25.1", "report bound to SHA-256"])]
    for i, (n, ls) in enumerate(parts):
        box(ax, 0.8 + i * 1.82, 0.72, 1.7, 1.75, n, ls, color=ORANGE, stereo="component", fs=7.6, title_fs=8.6, fill="#fdebe2")
    ev = box(ax, 12.1, 0.72, 2.4, 4.0, "Evaluate Benchmark", ["evaluate_benchmark.py", "compile_stats.py", "", "sandbox:", "python -I -S; sockets,", "subprocess and file", "writes blocked; 10 s", "", "reads: zipped runs,", "task file (answer key)"], color=GREEN, stereo="component", fs=8.2)
    arrow(ax, (hn["l"], 5.75), (lm["r"], 5.75), "chat + tools", lpos=0.5, loff=(0, 0.17))
    arrow(ax, (lh["l"], 6.0), (hn["r"], 6.0), "power", loff=(0, 0.16))
    arrow(ax, (hn["cx"], hn["b"]), (br["cx"], br["t"]), "tool call", loff=(0.45, 0))
    arrow(ax, (br["cx"], br["b"]), (br["cx"], 3.0), "require(dist)", loff=(0.62, 0.02))
    arrow(ax, (pl["cx"], pl["b"]), (pl["cx"], 3.0), "createConfidenceAgentTools", loff=(1.05, 0.02))
    arrow(ax, (lm["cx"], lm["b"]), (pl["cx"], pl["t"]), "loads plugin", loff=(0.62, 0))
    arrow(ax, (hn["r"], 5.2), (ev["cx"], ev["t"]), "results (offline)", ls="--", rad=-0.15, loff=(0.5, 0.25))
    save(fig, "D02_deployment_components.png")


# --------------------------------------------------------------------------- D03
def classbox(ax, x, y_top, w, name, attrs, ops=(), stereo=None, color=ORANGE, fs=8.2):
    lh = 0.205
    h_name = 0.42 + (0.2 if stereo else 0)
    h = h_name + lh * max(1, len(attrs)) + 0.12 + (lh * len(ops) + 0.12 if ops else 0)
    y = y_top - h
    ax.add_patch(Rectangle((x, y), w, h, fc="white", ec=color, lw=1.3))
    ax.add_patch(Rectangle((x, y_top - h_name), w, h_name, fc=TINT.get(color, "#f4f4f2"), ec=color, lw=1.3))
    ty = y_top - 0.08
    if stereo:
        ax.text(x + w / 2, ty, f"«{stereo}»", ha="center", va="top", fontsize=fs - 0.6, style="italic", color=INK2)
        ty -= 0.19
    ax.text(x + w / 2, ty, name, ha="center", va="top", fontsize=fs + 1, fontweight="bold")
    ty = y_top - h_name - 0.06
    for a in attrs:
        ax.text(x + 0.08, ty, a, ha="left", va="top", fontsize=fs, family="DejaVu Sans Mono")
        ty -= lh
    if ops:
        sep = y_top - h_name - lh * max(1, len(attrs)) - 0.12
        ax.plot([x, x + w], [sep, sep], color=color, lw=1)
        ty = sep - 0.06
        for o in ops:
            ax.text(x + 0.08, ty, o, ha="left", va="top", fontsize=fs, family="DejaVu Sans Mono")
            ty -= lh
    return {"l": x, "r": x + w, "t": y_top, "b": y, "cx": x + w / 2, "cy": y + h / 2}


def d03():
    W, H = 15.5, 10.2
    fig, ax = canvas(W, H)
    title(ax, W, H, "Class diagram: verification core (toolbox 3.0.0)",
          "Module functions are shown as «module» operations. Filled diamond = composition; dashed arrow = dependency (uses). Verification also\n"
          "composes six LayerResult objects and one EWCSReport (typed attributes, drawn without lines for legibility).")
    c1, c2, c3, cw = 0.3, 5.45, 10.6, 4.6
    ctl = classbox(ax, c1, 9.05, cw, "verificationController", [], ["+verifyCandidate(req, deps): Verification", "+runIntervention(req, deps): Outcome"], stereo="module")
    lay = classbox(ax, c2, 9.05, cw, "LayerVerifier", ["(claims, frozen spec) -> LayerResult"], ["verifyInterface      PyPI record, stdlib", "verifyIdentifier     Pyright", "verifyAccessPoint    OpenAPI paths", "verifyInputContract  OpenAPI parameters", "verifyOutputContract response schema", "verifyContextual     OpenAPI security"], stereo="interface")
    reg = classbox(ax, c3, 9.05, cw, "EvidenceRegistry", ["registry.json: host -> snapshot", "snapshots/*.openapi.json + SHA-256"], ["+evidenceFor(hosts, spec?): {spec, source}"], stereo="module")
    ver = classbox(ax, c1, 6.45, cw, "Verification", ["candidate_hash: sha256", "spec_hash: sha256", "extraction: Extraction", "layers: LayerResult[6]", "ewcs_report: EWCSReport", "decision: Decision"], stereo="interface")
    pol = classbox(ax, c2, 6.45, cw, "DecisionPolicy", ["uncertainty_gate = true", "deliver_threshold = 0.85", "flag_threshold = 0.60", "POLICY_VERSION = 2026-09-25.1"], ["+makeDecision(report, attempts): Decision", "+presentReport(code, report, d): Report"], stereo="module")
    lr = classbox(ax, c3, 6.45, cw, "LayerResult", ["layer: LayerName", "state: VerificationState", "tier: EvidenceTier", "weight: 1..4 (fixed per layer)", "evidence_source: string", "evidence_detail: string", "hallucination_type: string | null"], stereo="interface")
    ext = classbox(ax, c1, 3.95, cw, "Extraction", ["claims: Claim[]", "complete: boolean", "issues: {line, reason, affects}[]", "candidate_hash: sha256"], stereo="interface")
    acc = classbox(ax, c2, 3.95, cw, "EWCSAccumulator", ["-results: Map<LayerName, LayerResult>", "-report: EWCSReport | null"], ["+record(r: LayerResult)", "+finalise(): EWCSReport"])
    rep = classbox(ax, c3, 3.95, cw, "EWCSReport", ["ewcs, signed_score: number | null", "has_incorrect_layer: boolean", "contributions: LayerContribution[6]", "missing/failed/unverifiable_layers", "extraction_complete: boolean", "candidate_hash: sha256"], stereo="interface")
    clm = classbox(ax, c1, 1.95, cw, "Claim", ["type: import | method_call | endpoint", "      | input_field | output_field", "id, line, host, path, method, value"], stereo="interface")
    en = classbox(ax, c2, 1.75, cw, "VerificationState · EvidenceTier · Decision",
                  ["verified_correct | verified_incorrect |", "  unverifiable | not_applicable", "tier_1 1.0 | tier_2 0.8 | tier_3 0.9 | tier_4 0.5", "deliver | deliver_with_flag | correct | abstain"], stereo="enumeration", color=GREY, fs=7.6)
    end = diamond_end(ax, (ctl["cx"], ctl["b"]), (ver["cx"], ver["t"]), filled=False)
    arrow(ax, end, (ver["cx"], ver["t"]), "creates", loff=(0.45, 0), head="-")
    end = diamond_end(ax, (ext["cx"], ver["b"]), (ext["cx"], ext["t"]))
    arrow(ax, end, (ext["cx"], ext["t"]), "1", loff=(0.15, 0), head="-")
    end = diamond_end(ax, (clm["cx"], ext["b"]), (clm["cx"], clm["t"]))
    arrow(ax, end, (clm["cx"], clm["t"]), "0..*", loff=(0.25, 0), head="-")
    arrow(ax, (ctl["r"], 8.4), (lay["l"], 8.4), "runs 6 layers", ls="--", loff=(0, 0.13))
    arrow(ax, (lay["r"], 8.4), (reg["l"], 8.4), "spec for host", ls="--", loff=(0, 0.13))
    arrow(ax, (ctl["r"], 7.95), (pol["l"], 5.9), "decide", ls="--", loff=(0.05, 0.1))
    arrow(ax, (lay["r"], 6.9), (lr["l"], 6.1), "returns", ls="--", loff=(0.05, 0.13))
    arrow(ax, (pol["cx"], pol["b"]), (acc["cx"], acc["t"]), "recomputes EWCS", ls="--", loff=(0.75, 0))
    arrow(ax, (acc["r"], 3.0), (lr["l"], 4.6), "records 6", ls="--", loff=(-0.05, 0.12))
    arrow(ax, (acc["r"], 2.75), (rep["l"], 2.75), "finalise()", ls="--", loff=(0, 0.13))
    save(fig, "D03_class_diagram.png")


# --------------------------------------------------------------------------- D04
def d04():
    W, H = 15, 11.0
    fig, ax = canvas(W, H)
    title(ax, W, H, "Sequence diagram: one intervention task",
          "The model controls the conversation; the tool decides. The harness only relays, records, and asks for a reply if the turn limit is reached.")
    actors = [("Harness", "", 1.2, BLUE), ("LM Studio", "(Qwen3.5-9B)", 4.3, GREY), ("Tool bridge", "", 7.2, BLUE),
              ("Toolbox core", "", 10.1, ORANGE), ("Pyright /", "extractor", 13.1, ORANGE)]
    top = 9.55
    xs = {}
    for name, sub, x, c in actors:
        box(ax, x - 1.0, top, 2.0, 0.62, name, [sub] if sub else [], color=c, title_fs=9.2, fs=8, align="center")
        ax.plot([x, x], [0.4, top], color=MUTED, lw=1, ls=(0, (4, 3)))
        xs[name] = x
    H_, L, T, C, P = (xs[a[0]] for a in actors)

    def msg(y, a, b, text, ret=False):
        arrow(ax, (a, y), (b, y), None, color=INK2, ls="--" if ret else "-")
        ax.text((a + b) / 2, y + 0.07, text, ha="center", va="bottom", fontsize=8.4,
                bbox=dict(boxstyle="round,pad=0.08", fc=SURF, ec="none"))

    def act(x, y0, y1, c=GREY):
        ax.add_patch(Rectangle((x - 0.08, y0), 0.16, y1 - y0, fc=TINT.get(c, "#eee"), ec=c, lw=1, zorder=3))
    act(H_, 0.6, 9.35, BLUE)
    act(L, 8.45, 9.15)
    act(L, 4.95, 5.6)
    act(L, 1.85, 2.45)
    msg(9.0, H_, L, "system prompt (Confident Agent) + task text; tools = [verify_candidate]")
    msg(8.5, L, H_, "tool_call verify_candidate({code})", ret=True)
    msg(8.05, H_, T, "request.json (code only)")
    act(T, 6.05, 8.05, BLUE)
    msg(7.75, T, C, "runIntervention(code, spec by host, frozen PyPI)")
    act(C, 6.35, 7.75, ORANGE)
    msg(7.4, C, P, "extract claims (AST), run Pyright")
    act(P, 7.0, 7.4, ORANGE)
    msg(7.03, P, C, "claims, diagnostics", ret=True)
    ax.text(C + 0.15, 6.85, "6 layers -> EWCS -> policy\n-> report bound to SHA-256", fontsize=8, color=INK2, va="top")
    msg(6.4, C, T, "decision, report, layers, ewcs_report", ret=True)
    msg(6.1, T, H_, "result (saved as verification_N.json)", ret=True)
    ax.add_patch(Rectangle((0.5, 2.95), 13.9, 2.9, fc="none", ec=INK2, lw=1.1))
    ax.add_patch(Polygon([(0.5, 5.85), (1.35, 5.85), (1.35, 5.65), (1.2, 5.5), (0.5, 5.5)], fc="#efeee9", ec=INK2, lw=1))
    ax.text(0.58, 5.68, "alt", fontsize=9, fontweight="bold", va="center")
    ax.text(1.5, 5.7, "[a layer is verified_incorrect and this was the first candidate]", fontsize=8.6, va="center", color=INK2)
    msg(5.35, H_, L, "tool result (contradiction in evidence_detail)")
    msg(4.98, L, H_, "tool_call verify_candidate({corrected code})  (at most once)", ret=True)
    msg(4.6, H_, C, "same path: bridge -> toolbox -> layers -> policy")
    msg(4.25, C, H_, "second result: the decision that counts", ret=True)
    ax.plot([0.5, 14.4], [3.95, 3.95], color=INK2, lw=1, ls=(0, (5, 3)))
    ax.text(1.5, 3.8, "[deliver, deliver_with_flag, or abstain without a contradiction]", fontsize=8.6, va="top", color=INK2)
    msg(3.2, H_, L, "tool result (final)")
    ax.add_patch(Rectangle((0.5, 1.55), 13.9, 1.2, fc="none", ec=INK2, lw=1.1))
    ax.add_patch(Polygon([(0.5, 2.75), (1.35, 2.75), (1.35, 2.55), (1.2, 2.4), (0.5, 2.4)], fc="#efeee9", ec=INK2, lw=1))
    ax.text(0.58, 2.58, "opt", fontsize=9, fontweight="bold", va="center")
    ax.text(1.5, 2.6, "[4 turns used without a reply]", fontsize=8.6, va="center", color=INK2)
    msg(2.1, H_, L, "fixed message, tool_choice = none: reply with the last report")
    msg(1.2, L, H_, "final reply: the report verbatim (code only if the tool approved it)", ret=True)
    ax.text(H_ + 0.15, 0.75, "records decision, shown code, protocol notes, time, tokens, energy", fontsize=8.2, color=INK2)
    save(fig, "D04_sequence_task.png")


# --------------------------------------------------------------------------- D05
def node(ax, x, y, w, h, text, color=GREY, fs=9):
    ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h, boxstyle="round,pad=0.02,rounding_size=0.18", fc=TINT.get(color, "#f4f4f2"), ec=color, lw=1.4))
    ax.text(x, y, text, ha="center", va="center", fontsize=fs)


def decision(ax, x, y, text, w=2.9, h=1.0):
    ax.add_patch(Polygon([(x, y + h / 2), (x + w / 2, y), (x, y - h / 2), (x - w / 2, y)], fc="white", ec=INK2, lw=1.3))
    ax.text(x, y, text, ha="center", va="center", fontsize=8.5)


def poly_arrow(ax, pts, label=None, lpos=None, ls="-"):
    for a, b in zip(pts[:-2], pts[1:-1]):
        ax.plot([a[0], b[0]], [a[1], b[1]], color=LINE, lw=1.3, ls=ls)
    arrow(ax, pts[-2], pts[-1], None, ls=ls)
    if label:
        ax.text(lpos[0], lpos[1], label, fontsize=8.3, color=INK2, bbox=dict(boxstyle="round,pad=0.1", fc=SURF, ec="none"))


def d05():
    W, H = 12, 12.4
    fig, ax = canvas(W, H)
    title(ax, W, H, "Activity diagram: the decision policy (policy 2026-09-25.1)",
          "Hard rules come before the score: a contradiction or an unresolved critical check withholds code whatever the EWCS.")
    ax.add_patch(Circle((4.6, 11.35), 0.17, color=INK))
    node(ax, 4.6, 10.6, 4.6, 0.62, "Six layer results recorded (EWCSAccumulator)")
    decision(ax, 4.6, 9.45, "any layer\nverified_incorrect?")
    decision(ax, 9.2, 9.45, "first candidate?", w=2.4)
    node(ax, 9.2, 7.95, 3.4, 0.85, "CORRECT\nagent rewrites once;\nthe new code is verified", color=AMBER, fs=8.5)
    decision(ax, 4.6, 7.75, "missing or failed layer,\nor extraction incomplete?", w=3.3, h=1.1)
    decision(ax, 4.6, 6.0, "any applicable layer\nunverifiable?\n(uncertainty gate)", w=3.3, h=1.2)
    node(ax, 4.6, 4.65, 4.4, 0.75, "EWCS = Σ w·t (verified correct) / Σ w (applicable)", color=PURPLE, fs=8.6)
    decision(ax, 4.6, 3.45, "EWCS ≥ 0.85?", w=2.5, h=0.9)
    decision(ax, 4.6, 2.05, "EWCS ≥ 0.60?", w=2.5, h=0.9)
    node(ax, 1.55, 3.45, 2.0, 0.6, "DELIVER", color=BLUE)
    node(ax, 1.55, 2.05, 2.0, 0.75, "DELIVER\nWITH FLAG", color=BLUE)
    node(ax, 9.7, 3.75, 3.4, 2.6, "ABSTAIN\ncode withheld; the report\nstates which check failed\n(an abstain without a\ncontradiction is final)", color=RED, fs=8.6)
    node(ax, 4.6, 0.75, 6.6, 0.75, "presentReport: code is included only if the report's candidate_hash\nequals SHA-256 of the code and the recomputed decision allows delivery", color=GREY, fs=8.3)
    arrow(ax, (4.6, 11.18), (4.6, 10.92))
    arrow(ax, (4.6, 10.29), (4.6, 9.95))
    arrow(ax, (6.05, 9.45), (8.0, 9.45), "yes", loff=(0, 0.13))
    arrow(ax, (9.2, 8.95), (9.2, 8.38), "yes", loff=(0.25, 0))
    poly_arrow(ax, [(7.5, 7.95), (7.1, 7.95), (7.1, 10.6), (6.9, 10.6)], "re-verify", (6.55, 9.95), ls="--")
    poly_arrow(ax, [(10.4, 9.45), (11.2, 9.45), (11.2, 5.06)], "no (second\ncandidate)", (11.25, 8.9))
    arrow(ax, (4.6, 8.95), (4.6, 8.3), "no", loff=(0.25, 0))
    arrow(ax, (6.25, 7.75), (8.3, 5.05), "yes", loff=(0.1, 0.15))
    arrow(ax, (4.6, 7.2), (4.6, 6.6), "no", loff=(0.25, 0))
    arrow(ax, (6.25, 6.0), (8.0, 4.6), "yes", loff=(0.1, 0.15))
    arrow(ax, (4.6, 5.4), (4.6, 5.03), "no", loff=(0.25, 0))
    arrow(ax, (4.6, 4.27), (4.6, 3.9))
    arrow(ax, (3.35, 3.45), (2.55, 3.45), "yes", loff=(0, 0.13))
    arrow(ax, (4.6, 3.0), (4.6, 2.5), "no", loff=(0.25, 0))
    arrow(ax, (3.35, 2.05), (2.55, 2.05), "yes", loff=(0, 0.13))
    arrow(ax, (5.85, 2.05), (8.0, 2.9), "no", loff=(0.1, 0.12))
    poly_arrow(ax, [(0.55, 3.45), (0.3, 3.45), (0.3, 0.75), (1.3, 0.75)])
    arrow(ax, (1.55, 1.67), (2.4, 1.13))
    arrow(ax, (9.7, 2.45), (7.4, 1.13))
    save(fig, "D05_activity_decision.png")


# --------------------------------------------------------------------------- D06
def d06():
    W, H = 15, 7.4
    fig, ax = canvas(W, H)
    title(ax, W, H, "How the six layers read one candidate",
          "Each claim the extractor finds is checked by one layer against one kind of evidence. Weight = the layer's share of the score; tier = strength of its evidence.")
    code = ['import requests                                   # L1', '',
            'def solve(inputs):',
            '    url = f"https://api.github.com/orgs/{inputs[\'organization\']}"   # L3',
            '    headers = {"Authorization": f"Bearer {inputs[\'credential\']}",   # L6',
            '               "X-GitHub-Api-Version": "2026-03-10"}',
            '    r = requests.patch(url, headers=headers,          # L2  L3 (method)',
            '                       json={"description": inputs["new_description"]})  # L4',
            '    if r.status_code == 204:',
            '        return None',
            '    r.raise_for_status()',
            '    return r.json()["description"]                    # L5']
    ax.add_patch(FancyBboxPatch((0.3, 0.45), 7.9, 5.95, boxstyle="round,pad=0.02,rounding_size=0.08", fc="#f6f5f1", ec=GREY, lw=1.2))
    ax.text(0.45, 6.25, "candidate (illustrative task: update an organisation's description)", fontsize=8.6, color=INK2, va="top")
    for i, ln in enumerate(code):
        ax.text(0.45, 5.75 - i * 0.43, ln, family="DejaVu Sans Mono", fontsize=7.6, va="top")
    layers = [("L1 Interface", "do the imports exist?", "PyPI record, stdlib list", "3", "tier 2 (0.8)", BLUE),
              ("L2 Identifier", "do called names exist?", "Pyright 1.1.414", "3", "tier 4 (0.5)", BLUE),
              ("L3 Access point", "host, path, method declared?", "frozen OpenAPI", "4", "tier 1 / 2", ORANGE),
              ("L4 Input contract", "params, body, types, required", "frozen OpenAPI", "2", "tier 1 / 2", ORANGE),
              ("L5 Output contract", "response fields documented?", "OpenAPI schema (+Pyright)", "1", "tier 1 / 2", ORANGE),
              ("L6 Contextual", "credential in documented form?", "OpenAPI security", "2", "tier 1 / 2", ORANGE)]
    for x, t in ((8.6, "layer"), (10.55, "evidence"), (12.85, "weight"), (13.75, "tier")):
        ax.text(x, 6.25, t, fontsize=8.6, color=INK2, va="top", fontweight="bold")
    for i, (n, q, ev, wgt, tier, c) in enumerate(layers):
        y = 5.55 - i * 0.78
        ax.add_patch(FancyBboxPatch((8.55, y - 0.3), 6.15, 0.62, boxstyle="round,pad=0.02,rounding_size=0.06", fc=TINT[c], ec=c, lw=1.1))
        ax.text(8.65, y + 0.11, n, fontsize=9, fontweight="bold", va="center")
        ax.text(8.65, y - 0.14, q, fontsize=7.8, color=INK2, va="center")
        ax.text(10.55, y, ev, fontsize=8, va="center")
        ax.text(13.0, y, wgt, fontsize=10, fontweight="bold", va="center", ha="center")
        ax.text(13.75, y, tier, fontsize=8, va="center")
    ax.text(8.6, 0.45, "Weights 4:3:3:2:2:1 sum to 15. Tier 1 = official provider specification (GitHub, Petstore,\n"
            "Open-Meteo); tier 2 = curated partial specification, registry or stdlib inventory;\ntier 4 = absence of a Pyright error.",
            fontsize=8, color=INK2, va="bottom")
    save(fig, "D06_layers_anatomy.png")


# --------------------------------------------------------------------------- D07
def d07():
    W, H = 15, 5.6
    fig, ax = canvas(W, H)
    title(ax, W, H, "Evaluator: independent classification of the code that reaches the user",
          "It shares no code with the toolbox, executes candidates only in an isolated sandbox, and reads the answer key the agent never sees.")
    a = box(ax, 0.3, 1.2, 2.4, 3.0, "Candidate", ["baseline code block,", "or code delivered /", "shown by the agent,", "or the agent's final", "verified candidate"], color=GREY)
    b = box(ax, 3.1, 1.2, 2.9, 3.0, "Sandbox (python -I -S)", ["recording stand-in for", "requests (real names", "and signatures); task", "test inputs bound;", "network, subprocess and", "file writes blocked"], color=GREEN)
    c = box(ax, 6.4, 1.2, 2.5, 3.0, "3 scenarios", ["documented success", "response (schema-", "built), empty 204,", "server error 500", "", "-> behaviour checks"], color=GREEN)
    d = box(ax, 9.3, 1.2, 2.7, 3.0, "Compare", ["exact requests vs", "expected_request and", "the pinned spec", "($refs resolved);", "response fields read", "vs response schema"], color=GREEN)
    e = box(ax, 12.4, 1.2, 2.3, 3.0, "Class", ["A  API hallucination", "B  valid call, wrong task", "correct (incl. class C", "    equivalences)", "runtime failure", "undetermined", "    -> manual review"], color=PURPLE, fs=8.1)
    for p, q in ((a, b), (b, c), (c, d), (d, e)):
        arrow(ax, (p["r"], 2.7), (q["l"], 2.7))
    ax.text(7.5, 0.55, "Self-check before scoring: all 1,000 reference solutions classify as correct and meet the behaviour checks.", ha="center", fontsize=8.6, color=INK2)
    save(fig, "D07_evaluator.png")


if __name__ == "__main__":
    for f in (d01, d02, d03, d04, d05, d06, d07):
        f()
