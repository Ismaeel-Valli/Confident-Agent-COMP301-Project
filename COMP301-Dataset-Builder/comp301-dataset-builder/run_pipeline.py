"""Rebuild and check the draft from the bundled source snapshots, offline."""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
COMMANDS = [
    ['build_dataset.py', '--pilot', '--output', 'pilot'],
    ['validate_dataset.py', 'pilot/rest_api_tasks_pilot.jsonl', '--report', 'pilot/validation_report.json', '--prompts', 'pilot/rest_api_prompts_pilot.jsonl'],
    ['build_dataset.py'],
    ['validate_dataset.py', '--prompts', 'output/rest_api_prompts_v1_DRAFT.jsonl'],
    ['-m', 'unittest', 'test_validation.py'],
    ['make_review_pack.py'],
]


if __name__ == '__main__':
    for command in COMMANDS:
        print('Running:', ' '.join(command), flush=True)
        subprocess.run([sys.executable, *command], cwd=ROOT, check=True)
    print('Done. The files are drafts; read DATASET_AUDIT.md before experimental use.')
