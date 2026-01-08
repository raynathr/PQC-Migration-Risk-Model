"""
Custom Migration Strategy Example

Demonstrates how to define and evaluate a custom migration strategy
with specific deployment characteristics.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import matplotlib.pyplot as plt
from core_logic import calculate_adversarial_capability, calculate_rqr, calculate_cas
import config

def custom_migration_strategy(t_array, strategy_type="phased"):
    """
    Define a custom migration coverage function.
    
    Args:
        t_array: Array of time points
        strategy_type: Type of custom strategy
    
    Returns:
        Array of coverage percentages for each time point
    """
    L_t = np.zeros_like(t_array, dtype=float)
    
    if strategy_type == "phased":
        # Phased approach: 30% immediate, then gradual
        immediate_coverage = 0.30
        remaining_rate = 0.12  # 12% per year for remaining 70%
        
        for i, t in enumerate(t_array):
            if t == 1:
                L_t[i] = immediate_coverage
            else:
                additional = remaining_rate * (t - 1)
                L_t[i] = min(1.0, immediate_coverage + additional)
    
    elif strategy_type == "budget_constrained":
        # Budget constraints cause periodic plateaus
        for i, t in enumerate(t_array):
            if t <= 3:
                L_t[i] = 0.15 * t
            elif t <= 6:
                L_t[i] = 0.45  # Budget plateau
            else:
                L_t[i] = min(1.0, 0.45 + 0.10 * (t - 6))
    
    return L_t

def main():
    print("Custom Migration Strategy Example")
    print("="*50)
    
    np.random.seed(42)
    
    # Setup simulation parameters
    years = 15
    t_array = np.arange(1, years + 1)
    
    # Calculate a representative adversarial capability
    g = 0.5
    noise = np.random.normal(0, config.SIGMA_EPSILON, years)
    adv_cap = calculate_adversarial_capability(t_array, g, noise)
    
    # Calculate Kyber-512 risk
    rqr_kyber = calculate_rqr(adv_cap, config.COST_KYBER_512)
    
    # Evaluate different custom strategies
    strategies = {
        "Phased": custom_migration_strategy(t_array, "phased"),
        "Budget Constrained": custom_migration_strategy(t_array, "budget_constrained")
    }
    
    # Calculate CAS for each strategy
    results = {}
    for name, coverage in strategies.items():
        cas = calculate_cas(rqr_kyber, coverage)
        tci = np.mean(cas)
        results[name] = {"coverage": coverage, "cas": cas, "tci": tci}
    
    # Display results
    print("\nCustom Strategy Comparison:")
    print("-"*50)
    for name, data in results.items():
        print(f"\n{name}:")
        print(f"  TCI Score: {data['tci']:.3f}")
        print(f"  Year 5 Coverage: {data['coverage'][4]:.1%}")
        print(f"  Year 10 Coverage: {data['coverage'][9]:.1%}")
        print(f"  Year 15 Coverage: {data['coverage'][-1]:.1%}")
    
    # Create visualization
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    # Plot coverage trajectories
    for name, data in results.items():
        ax1.plot(t_array, data['coverage'], marker='o', label=name, linewidth=2)
    
    ax1.set_xlabel('Years')
    ax1.set_ylabel('Migration Coverage')
    ax1.set_title('Custom Migration Coverage Trajectories')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    ax1.set_ylim(0, 1.1)
    
    # Plot CAS trajectories
    for name, data in results.items():
        ax2.plot(t_array, data['cas'], marker='s', 
                label=f"{name} (TCI={data['tci']:.2f})", linewidth=2)
    
    ax2.axhline(config.CAS_THRESHOLD, linestyle='--', color='red', 
                label='Threshold', alpha=0.7)
    ax2.set_xlabel('Years')
    ax2.set_ylabel('Composite Assurance Score')
    ax2.set_title('CAS Evolution for Custom Strategies')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    ax2.set_ylim(0, 1.1)
    
    plt.tight_layout()
    
    output_path = 'results/custom_migration_comparison.png'
    os.makedirs('results', exist_ok=True)
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"\nVisualization saved to: {output_path}")

if __name__ == "__main__":
    main()
