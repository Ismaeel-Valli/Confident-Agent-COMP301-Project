"""Statistical analysis of the compiled stats: Wilcoxon tests on cost and the report's charts.

Reads Unprocessed Data/stats/combined/ (written by Findings/EvaluateBenchmark/compile_stats.py)
and writes the charts to figures/. Run from anywhere:  python analyse_results.py
Needs: pip install -r requirements.txt
"""
from pathlib import Path

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import wilcoxon

HERE = Path(__file__).resolve().parent
COMBINED = HERE / "Unprocessed Data" / "stats" / "combined"
FIGURES = HERE / "figures"

# Set visualization style
sns.set_theme(style="whitegrid")
plt.rcParams.update({'font.size': 12})


def main_runs(prompt_stats_path):
    """The main runs (one per quantization), pilot tasks excluded as in the evaluation plan."""
    df = pd.read_csv(prompt_stats_path)
    return df[(df['run_role'] == 'main') & (df['pilot'] == 0)]


def run_wilcoxon_tests(prompt_stats_path):
    print("--- PAIRED WILCOXON SIGNED-RANK TESTS ---")
    df = main_runs(prompt_stats_path)

    metrics = [
        ('Duration (Seconds)', 'b_duration_s', 'i_duration_s'),
        ('Energy (Joules)', 'b_energy_j', 'i_energy_j'),
        ('Total Tokens', 'b_total_tokens', 'i_total_tokens')
    ]

    for quantization, run in sorted(df.groupby('quantization')):
        print(f"\n=== {quantization} ({run['model_label'].iloc[0]})")
        for name, base_col, int_col in metrics:
            # Drop rows where either value might be missing (e.g., undetermined errors)
            paired_data = run.dropna(subset=[base_col, int_col])

            # Perform Wilcoxon Signed-Rank Test
            stat, p_value = wilcoxon(paired_data[base_col], paired_data[int_col])

            b_median = paired_data[base_col].median()
            i_median = paired_data[int_col].median()

            print(f"\n{name}:")
            print(f"  Baseline Median: {b_median:.2f}")
            print(f"  Intervention Median: {i_median:.2f}")
            print(f"  Median ratio (intervention / baseline): {i_median / b_median:.2f}")
            print(f"  Wilcoxon Statistic: {stat}")
            print(f"  P-value: {p_value:.2e}")
            if p_value < 0.05:
                print("  Conclusion: Statistically significant difference.")
            else:
                print("  Conclusion: No statistically significant difference.")


def plot_efficacy(quant_comp_path):
    # Load quantization comparison data
    df = pd.read_csv(quant_comp_path)

    # Sort so the chart goes Q4 -> Q6 -> Q8
    df = df.sort_values('quantization')

    # Set up the grouped bar chart data
    labels = df['quantization'].tolist()
    b_halluc = df['b_hallucination_rate'] * 100
    i_halluc = df['i_hallucination_rate'] * 100
    b_corr = df['b_correct_rate'] * 100
    i_corr = df['i_correct_rate'] * 100

    x = np.arange(len(labels))
    width = 0.35

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    # Hallucination Plot
    ax1.bar(x - width/2, b_halluc, width, label='Baseline', color='#E63946')
    ax1.bar(x + width/2, i_halluc, width, label='Confident Agent', color='#1D3557')
    ax1.set_ylabel('Hallucination reaching the user (%)')
    ax1.set_title('Hallucination Reduction by Model Quantization')
    ax1.set_xticks(x)
    ax1.set_xticklabels(labels)
    ax1.legend()

    # Correctness Plot
    ax2.bar(x - width/2, b_corr, width, label='Baseline', color='#A8DADC')
    ax2.bar(x + width/2, i_corr, width, label='Confident Agent', color='#457B9D')
    ax2.set_ylabel('Correct code reaching the user (%)')
    ax2.set_title('Correctness Improvement by Model Quantization')
    ax2.set_xticks(x)
    ax2.set_xticklabels(labels)
    ax2.legend()

    plt.tight_layout()
    plt.savefig(FIGURES / 'efficacy_chart.png', dpi=300)
    print(f"\nSaved {FIGURES / 'efficacy_chart.png'}")


def plot_tradeoffs(prompt_stats_path):
    df = main_runs(prompt_stats_path)
    modes = {'b': 'Baseline', 'i': 'Confident Agent'}

    # Prepare data for Seaborn (melting into long format), one box per quantization and mode
    def long(column, value_name):
        out = pd.melt(df, id_vars=['quantization'], value_vars=[f'b_{column}', f'i_{column}'],
                      var_name='Mode', value_name=value_name)
        out['Mode'] = out['Mode'].str[0].map(modes)
        return out

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    order = sorted(df['quantization'].unique())
    palette = {'Baseline': '#A8DADC', 'Confident Agent': '#1D3557'}

    # We use log-scale because LLM latency/energy usually has long right-tails (outliers)
    sns.boxplot(data=long('duration_s', 'Duration (s)'), x='quantization', y='Duration (s)', hue='Mode',
                order=order, ax=ax1, palette=palette)
    ax1.set_yscale('log')
    ax1.set_xlabel('Quantization')
    ax1.set_title('Latency per Prompt (Log Scale)')

    sns.boxplot(data=long('energy_j', 'Energy (Joules)'), x='quantization', y='Energy (Joules)', hue='Mode',
                order=order, ax=ax2, palette=palette)
    ax2.set_yscale('log')
    ax2.set_xlabel('Quantization')
    ax2.set_title('Energy per Prompt (Log Scale)')

    # one legend for both panels, above them, so it covers no data
    handles, labels = ax1.get_legend_handles_labels()
    ax1.get_legend().remove()
    ax2.get_legend().remove()
    fig.legend(handles, labels, loc='upper center', ncol=2, frameon=False)
    plt.tight_layout(rect=(0, 0, 1, 0.94))
    plt.savefig(FIGURES / 'tradeoff_chart.png', dpi=300)
    print(f"Saved {FIGURES / 'tradeoff_chart.png'}")


if __name__ == "__main__":
    PROMPT_STATS_FILE = COMBINED / 'prompt_stats.csv'
    QUANT_COMP_FILE = COMBINED / 'quantization_comparison.csv'
    FIGURES.mkdir(exist_ok=True)

    try:
        run_wilcoxon_tests(PROMPT_STATS_FILE)
        plot_efficacy(QUANT_COMP_FILE)
        plot_tradeoffs(PROMPT_STATS_FILE)
    except FileNotFoundError as e:
        print(f"Error: Could not find CSV file. Run evaluate_benchmark.py and compile_stats.py first. {e}")
