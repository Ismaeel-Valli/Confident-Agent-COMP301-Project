# Archive

Earlier versions of the code and earlier benchmark runs. **Not part of the final
submission**: the final versions are in `COMP301 Project Final Submission/`. Kept so the
project's development can be traced; the full history is also in git (tag
`pre-final-cleanup` marks the repository before this reorganisation).

| Folder | What it is | Replaced by |
|---|---|---|
| `Toolbox/` | Confidence Agent built into the Beledarian LM Studio framework (third-party plugin with the verifier added) | `Code Submission/confident-agent-toolbox` (standalone 3.0.0, framework removed) |
| `Confidence-Agent-Toolbox/` | first toolbox prototype (System Prompt v2.2) | the same |
| `confident_agent/` | first Python design of the six layers and EWCS | the same (EWCS reference kept in its `docs/reference`) |
| `Testing/` | DeepSeek variant of the toolbox and the EWCS test package | the same |
| `Superseded Benchmark Runs/` | run 1 (pilot of the full dataset, Q4_K_M), run 2 (Q4_K_M), the first Q6_K and Q8_0 runs, the timing checks, run 1's console log, and the JSONL files with all of them | the final runs in `Findings/Benchmark/Completed Runs` (EVALUATION_PLAN.md §7 and its change of 2026-10-06) |

To score a superseded run again, copy its zips into a `Findings/Benchmark` folder of a
checkout together with the archived `complete_test_*.jsonl` files, and run the evaluator.
