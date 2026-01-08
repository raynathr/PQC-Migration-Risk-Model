"""
Basic Simulation Example

Demonstrates a simple single simulation run calculating RSA-2048 quantum risk.
This example shows the minimal code needed to use the framework.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
from core_logic import calculate_adversarial_capability, calculate_rqr
import config

def main():
    print("Basic PQC Risk Assessment Example")
    print("="*50)
    
    # Set a fixed seed for reproducibility
    np.random.seed(42)
    
    # Define time horizon
    years = 10
    t_array = np.arange(1, years + 1)
    
    # Generate a single adversarial capability trajectory
    growth_rate = 0.5  # 50% annual growth
    noise = np.random.normal(0, config.SIGMA_EPSILON, years)
    
    # Calculate adversarial capability
    adv_capability = calculate_adversarial_capability(t_array, growth_rate, noise)
    
    # Calculate RSA-2048 risk over time
    rqr_rsa = calculate_rqr(adv_capability, config.COST_RSA_2048)
    
    print("\nRSA-2048 Quantum Risk Assessment:")
    print("-"*50)
    print(f"{'Year':<8} {'Capability (log10)':<20} {'Break Probability':<20}")
    print("-"*50)
    
    for i, year in enumerate(t_array):
        print(f"{year:<8} {adv_capability[i]:<20.2f} {rqr_rsa[i]:<20.6f}")
    
    # Find when risk exceeds 50%
    critical_year = np.where(rqr_rsa > 0.5)[0]
    if len(critical_year) > 0:
        print(f"\nCritical threshold (50% break probability) reached at year {critical_year[0] + 1}")
    else:
        print(f"\nRisk remains below 50% throughout {years}-year horizon")
    
    print("\nKey Insights:")
    print(f"  - Initial risk (Year 1): {rqr_rsa[0]:.6f}")
    print(f"  - Final risk (Year {years}): {rqr_rsa[-1]:.6f}")
    print(f"  - Average annual risk increase: {np.mean(np.diff(rqr_rsa)):.6f}")

if __name__ == "__main__":
    main()
