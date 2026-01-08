"""
Visualization functions for generating publication-ready figures.

This module creates visualizations of simulation results including RQR evolution
curves and CAS trajectory comparisons across different migration scenarios.
"""

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import config

def save_rqr_plot(t_array, rqr_rsa, rqr_kyber):
    """
    Generate and save RQR evolution plot comparing algorithms.
    
    Creates Figure 1 from the paper showing the evolution of Residual Quantum
    Risk over time for classical (RSA-2048) and PQC (Kyber-512) algorithms.
    The plot includes mean trajectories and 95% confidence intervals from
    Monte Carlo simulations.
    
    Args:
        t_array (np.ndarray): Time points (years from present)
        rqr_rsa (np.ndarray): RQR values for RSA-2048,
            shape (N_SIMULATIONS, YEARS)
        rqr_kyber (np.ndarray): RQR values for Kyber-512,
            shape (N_SIMULATIONS, YEARS)
    
    Side Effects:
        Saves plot to 'results/figure1_rqr_evolution.png'
    """
    plt.figure(figsize=(10, 6))
    
    # Plot RSA
    rsa_mean = np.mean(rqr_rsa, axis=0)
    rsa_ci = 1.96 * np.std(rqr_rsa, axis=0) / np.sqrt(config.N_SIMULATIONS)
    plt.plot(t_array, rsa_mean, color='red', label='RSA-2048 (Classical)', linewidth=2)
    plt.fill_between(t_array, rsa_mean - rsa_ci, rsa_mean + rsa_ci, color='red', alpha=0.1)

    # Plot Kyber
    kyber_mean = np.mean(rqr_kyber, axis=0)
    kyber_ci = 1.96 * np.std(rqr_kyber, axis=0) / np.sqrt(config.N_SIMULATIONS)
    plt.plot(t_array, kyber_mean, color='blue', label='Kyber-512 (PQC Hybrid)', linewidth=2)
    plt.fill_between(t_array, kyber_mean - kyber_ci, color='blue', alpha=0.1)

    plt.title('Residual Quantum Risk (RQR) Evolution')
    plt.xlabel('Years from Present')
    plt.ylabel('Break Probability')
    plt.axhline(0.5, linestyle='--', color='gray', alpha=0.5)
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    plt.savefig('results/figure1_rqr_evolution.png')
    print("Saved results/figure1_rqr_evolution.png")

def save_cas_plot(t_array, scenario_results):
    """
    Generate and save CAS trajectories plot for migration scenarios.
    
    Creates Figure 2 from the paper showing how Composite Assurance Score
    evolves under different migration strategies. Includes TCI values in
    legend and highlights the minimum assurance threshold.
    
    Args:
        t_array (np.ndarray): Time points (years from present)
        scenario_results (dict): Dictionary mapping scenario names to their
            CAS series and TCI values. Each entry should have:
            - 'cas_series' (np.ndarray): CAS values over time
            - 'tci' (float): Trust Continuity Index
    
    Side Effects:
        Saves plot to 'results/figure2_cas_scenarios.png'
    """
    plt.figure(figsize=(10, 6))
    
    colors = {"Aggressive": "green", "Conservative": "orange", "Late_Start": "red"}
    
    for name, data in scenario_results.items():
        plt.plot(t_array, data["cas_series"], label=f"{name} (TCI={data['tci']:.2f})", color=colors[name], linewidth=2)

    plt.axhline(config.CAS_THRESHOLD, linestyle='--', color='black', label='Min Assurance Threshold')
    plt.title('Composite Assurance Score (CAS) Trajectories')
    plt.xlabel('Years')
    plt.ylabel('Assurance Score (0-1)')
    plt.ylim(0, 1.0)
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    plt.savefig('results/figure2_cas_scenarios.png')
    print("Saved results/figure2_cas_scenarios.png")
