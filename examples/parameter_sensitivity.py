"""
Parameter Sensitivity Analysis Example

Demonstrates how to test the impact of different parameter values on 
simulation outcomes, useful for understanding model behavior and uncertainty.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import matplotlib.pyplot as plt
from core_logic import calculate_adversarial_capability, calculate_rqr
import config

def test_growth_rate_sensitivity():
    """Test impact of different adversarial capability growth rates."""
    print("\n1. Growth Rate Sensitivity Analysis")
    print("-"*50)
    
    np.random.seed(42)
    years = 15
    t_array = np.arange(1, years + 1)
    
    # Test different growth rates
    growth_rates = [0.3, 0.5, 0.7]
    results = {}
    
    for g in growth_rates:
        noise = np.random.normal(0, config.SIGMA_EPSILON, years)
        adv_cap = calculate_adversarial_capability(t_array, g, noise)
        rqr = calculate_rqr(adv_cap, config.COST_RSA_2048)
        
        # Find year when risk exceeds 50%
        critical = np.where(rqr > 0.5)[0]
        critical_year = critical[0] + 1 if len(critical) > 0 else None
        
        results[g] = {"rqr": rqr, "critical_year": critical_year}
        
        print(f"Growth rate {g:.1f}: Critical year = {critical_year if critical_year else 'Beyond horizon'}")
    
    return results

def test_alpha_sensitivity():
    """Test impact of logistic sensitivity parameter alpha."""
    print("\n2. Alpha (Logistic Sensitivity) Analysis")
    print("-"*50)
    
    np.random.seed(42)
    years = 15
    t_array = np.arange(1, years + 1)
    
    # Generate base capability
    g = 0.5
    noise = np.random.normal(0, config.SIGMA_EPSILON, years)
    adv_cap = calculate_adversarial_capability(t_array, g, noise)
    
    # Test different alpha values
    alpha_values = [1.0, 2.0, 3.0]
    results = {}
    
    for alpha in alpha_values:
        # Temporarily override config
        original_alpha = config.ALPHA
        config.ALPHA = alpha
        
        rqr = calculate_rqr(adv_cap, config.COST_RSA_2048)
        results[alpha] = rqr
        
        config.ALPHA = original_alpha  # Restore
        
        print(f"Alpha {alpha:.1f}: Year 7 risk = {rqr[6]:.4f}")
    
    return results

def test_cost_threshold_sensitivity():
    """Test impact of different algorithm attack costs."""
    print("\n3. Attack Cost Threshold Analysis")
    print("-"*50)
    
    np.random.seed(42)
    years = 15
    t_array = np.arange(1, years + 1)
    
    # Generate base capability
    g = 0.5
    noise = np.random.normal(0, config.SIGMA_EPSILON, years)
    adv_cap = calculate_adversarial_capability(t_array, g, noise)
    
    # Test different security levels (attack costs)
    algorithms = {
        "RSA-1024": 8.0,
        "RSA-2048": 10.0,
        "RSA-4096": 12.0,
        "Kyber-512": 18.0
    }
    
    results = {}
    for name, cost in algorithms.items():
        rqr = calculate_rqr(adv_cap, cost)
        results[name] = rqr
        print(f"{name:12s} (cost={cost:4.1f}): Year 10 risk = {rqr[9]:.6f}")
    
    return results

def visualize_sensitivity_results(growth_results, alpha_results, cost_results):
    """Create comprehensive sensitivity analysis visualization."""
    fig = plt.figure(figsize=(15, 5))
    years = 15
    t_array = np.arange(1, years + 1)
    
    # Growth rate sensitivity
    ax1 = plt.subplot(131)
    for g, data in growth_results.items():
        ax1.plot(t_array, data['rqr'], marker='o', label=f'g = {g:.1f}', linewidth=2)
    ax1.axhline(0.5, linestyle='--', color='red', alpha=0.5, label='50% threshold')
    ax1.set_xlabel('Years')
    ax1.set_ylabel('RQR (RSA-2048)')
    ax1.set_title('Growth Rate Sensitivity')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    ax1.set_ylim(0, 1.0)
    
    # Alpha sensitivity
    ax2 = plt.subplot(132)
    for alpha, rqr in alpha_results.items():
        ax2.plot(t_array, rqr, marker='s', label=f'α = {alpha:.1f}', linewidth=2)
    ax2.axhline(0.5, linestyle='--', color='red', alpha=0.5)
    ax2.set_xlabel('Years')
    ax2.set_ylabel('RQR (RSA-2048)')
    ax2.set_title('Logistic Sensitivity (α) Impact')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    ax2.set_ylim(0, 1.0)
    
    # Cost threshold sensitivity
    ax3 = plt.subplot(133)
    colors = plt.cm.viridis(np.linspace(0, 1, len(cost_results)))
    for (name, rqr), color in zip(cost_results.items(), colors):
        ax3.plot(t_array, rqr, marker='^', label=name, linewidth=2, color=color)
    ax3.axhline(0.5, linestyle='--', color='red', alpha=0.5)
    ax3.set_xlabel('Years')
    ax3.set_ylabel('RQR')
    ax3.set_title('Algorithm Security Level Comparison')
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    ax3.set_ylim(0, 1.0)
    
    plt.tight_layout()
    
    output_path = 'results/parameter_sensitivity.png'
    os.makedirs('results', exist_ok=True)
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"\nVisualization saved to: {output_path}")

def main():
    print("="*50)
    print("Parameter Sensitivity Analysis")
    print("="*50)
    
    # Run sensitivity tests
    growth_results = test_growth_rate_sensitivity()
    alpha_results = test_alpha_sensitivity()
    cost_results = test_cost_threshold_sensitivity()
    
    # Create visualization
    visualize_sensitivity_results(growth_results, alpha_results, cost_results)
    
    print("\n" + "="*50)
    print("Analysis complete!")
    print("="*50)
    print("\nKey Takeaways:")
    print("  - Higher growth rates accelerate risk evolution")
    print("  - Alpha controls transition steepness in risk function")
    print("  - Higher security algorithms provide longer protection")

if __name__ == "__main__":
    main()
