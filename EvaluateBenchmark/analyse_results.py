import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import wilcoxon

# Set visualization style
sns.set_theme(style="whitegrid")
plt.rcParams.update({'font.size': 12})

def run_wilcoxon_tests(prompt_stats_path):
    print("--- PAIRED WILCOXON SIGNED-RANK TESTS ---")
    # Load raw prompt data
    df = pd.read_csv(prompt_stats_path)
    
    # Filter for the main Q4 run (avoiding the preliminary run without power data)
    main_run = df[(df['model_label'] == 'Qwen3.5-9B-Q4_K_M-full-run2') & (df['run_role'] == 'main')]
    
    metrics = [
        ('Duration (Seconds)', 'b_duration_s', 'i_duration_s'),
        ('Energy (Joules)', 'b_energy_j', 'i_energy_j'),
        ('Total Tokens', 'b_total_tokens', 'i_total_tokens')
    ]
    
    for name, base_col, int_col in metrics:
        # Drop rows where either value might be missing (e.g., undetermined errors)
        paired_data = main_run.dropna(subset=[base_col, int_col])
        
        # Perform Wilcoxon Signed-Rank Test
        stat, p_value = wilcoxon(paired_data[base_col], paired_data[int_col])
        
        b_median = paired_data[base_col].median()
        i_median = paired_data[int_col].median()
        
        print(f"\n{name}:")
        print(f"  Baseline Median: {b_median:.2f}")
        print(f"  Intervention Median: {i_median:.2f}")
        print(f"  Wilcoxon Statistic: {stat}")
        print(f"  P-value: {p_value:.2e}")
        if p_value < 0.05:
            print("  Conclusion: Statistically significant difference.")
        else:
            print("  Conclusion: No statistically significant difference.")

def plot_efficacy(quant_comp_path):
    # Load quantization comparison data
    df = pd.read_csv(quant_comp_path)
    
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
    ax1.set_ylabel('Hallucination Rate (%)')
    ax1.set_title('Hallucination Reduction by Model Quantization')
    ax1.set_xticks(x)
    ax1.set_xticklabels(labels)
    ax1.legend()

    # Correctness Plot
    ax2.bar(x - width/2, b_corr, width, label='Baseline', color='#A8DADC')
    ax2.bar(x + width/2, i_corr, width, label='Confident Agent', color='#457B9D')
    ax2.set_ylabel('Correct Answer Rate (%)')
    ax2.set_title('Correctness Improvement by Model Quantization')
    ax2.set_xticks(x)
    ax2.set_xticklabels(labels)
    ax2.legend()

    plt.tight_layout()
    plt.savefig('efficacy_chart.png', dpi=300)
    print("\nSaved 'efficacy_chart.png'")

def plot_tradeoffs(prompt_stats_path):
    df = pd.read_csv(prompt_stats_path)
    main_run = df[(df['model_label'] == 'Qwen3.5-9B-Q4_K_M-full-run2') & (df['run_role'] == 'main')]
    
    # Prepare data for Seaborn (melting into long format)
    time_df = pd.melt(main_run, value_vars=['b_duration_s', 'i_duration_s'], 
                      var_name='Mode', value_name='Duration (s)')
    time_df['Mode'] = time_df['Mode'].map({'b_duration_s': 'Baseline', 'i_duration_s': 'Confident Agent'})
    
    energy_df = pd.melt(main_run, value_vars=['b_energy_j', 'i_energy_j'], 
                        var_name='Mode', value_name='Energy (Joules)')
    energy_df['Mode'] = energy_df['Mode'].map({'b_energy_j': 'Baseline', 'i_energy_j': 'Confident Agent'})

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    # We use log-scale because LLM latency/energy usually has long right-tails (outliers)
    sns.boxplot(data=time_df, hue='Mode', y='Duration (s)', ax=ax1, palette=['#A8DADC', '#1D3557'], legend=False)
    ax1.set_yscale('log')
    ax1.set_title('Latency Distribution (Log Scale)')

    sns.boxplot(data=energy_df, hue='Mode', y='Energy (Joules)', ax=ax2, palette=['#E63946', '#1D3557'], legend=False)
    ax2.set_yscale('log')
    ax2.set_title('Energy Consumption Distribution (Log Scale)')

    plt.tight_layout()
    plt.savefig('tradeoff_chart.png', dpi=300)
    print("Saved 'tradeoff_chart.png'")

if __name__ == "__main__": #EvaluateBenchmark\stats\combined\prompt_stats.csv
    PROMPT_STATS_FILE = './stats/combined/prompt_stats.csv'
    QUANT_COMP_FILE = './stats/combined/quantization_comparison.csv'
    
    try:
        run_wilcoxon_tests(PROMPT_STATS_FILE)
        plot_efficacy(QUANT_COMP_FILE)
        plot_tradeoffs(PROMPT_STATS_FILE)
    except FileNotFoundError as e:
        print(f"Error: Could not find CSV file. Make sure they are in the same folder. {e}")