# Confident Agent (COMP301, UKZN)

A Confident Agent verifies the REST API calls in LLM-generated Python code before the code
reaches the user. Six verification layers, scored by EWCS, decide whether to deliver the
code, deliver it with a flag, or abstain. A benchmark compares a baseline LLM with
the Confident Agent on a 1,000-task dataset of REST API prompts.

Everything handed in is in **`COMP301 Project Final Submission/`**:

```
COMP301 Project Final Submission/
  Code Submission/
    confident-agent-toolbox/        the Confident Agent: LM Studio plugin, verifier, EWCS, prompt
    COMP301-Dataset-Builder/        builds and validates the 1,000-task dataset (the answer key)
  Findings/
    Benchmark/                      runs the dataset through LM Studio, baseline vs intervention
      Completed Runs/<model>/       the runs the findings use (zipped, one zip per mode)
      EVALUATION_PLAN.md            the scoring rules, fixed before the main runs
    EvaluateBenchmark/              scores the runs against the answer key; compiles the statistics
    Statistical Analysis/
      Unprocessed Data/             everything the evaluator and the stats compiler write
        evaluation/                 report.md, per-run scores, manual review queues
        stats/                      CSV tables for data processing (see STATS_README.md)
      analyse_results.py            statistical tests and charts (figures/)
      tempstats/                    cost statistics in Rand; report_figures/ for the final report
  Final Report and Documentation/   reports, practicals and supporting documentation
    Final Report/                   COMP301 The Skeptics Final Report (.docx, .pdf); build/ regenerates it
Archive/                            superseded code and runs, kept for reference only
```

## Reproducing the findings

```bat
cd "COMP301 Project Final Submission\Findings\EvaluateBenchmark"
python evaluate_benchmark.py
python compile_stats.py
cd "..\Statistical Analysis"
pip install -r requirements.txt
python analyse_results.py
```

The evaluator and the stats compiler need only Python 3.9+ (standard library). Running the
benchmark itself needs LM Studio and the toolbox's setup: see `Findings/Benchmark/README.md`.

On Windows, some generated paths are long. If a clone in a deep folder fails with
"Filename too long", run `git config core.longpaths true`, or clone to a shorter path.
