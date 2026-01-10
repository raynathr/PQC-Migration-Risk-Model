"""
Visualization functions for generating publication-ready figures.

This module creates visualizations of simulation results including RQR evolution
curves and CAS trajectory comparisons across different migration scenarios.
"""

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import config
from simulation import run_simulation
from config import DEFAULT_CONFIG


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


# Added: Figure 3 - Sensitivity analysis heatmap

def generate_sensitivity_heatmap():
    """
    Generate Figure 3: Sensitivity analysis heatmap.
    Tests TCI across growth rate (mu_g) and Algorithm Strength weight (w_AS).
    """
    # Define parameter ranges
    mu_g_range = np.linspace(0.3, 0.7, 10)  # 10 values from 0.3 to 0.7
    w_as_range = np.linspace(0.30, 0.50, 10)  # 10 values from 0.30 to 0.50
    
    # Initialize TCI matrix
    tci_matrix = np.zeros((len(w_as_range), len(mu_g_range)))
    
    # Run simulations for each parameter combination
    print("Running sensitivity analysis...")
    for i, w_as in enumerate(w_as_range):
        for j, mu_g in enumerate(mu_g_range):
            # Adjust weights (must sum to 1.0)
            w_km = 0.25
            w_dc = 0.20
            w_cai = 1.0 - w_as - w_km - w_dc
            
            # Run simulation with these parameters
            config_local = DEFAULT_CONFIG.copy()
            config_local['mu_g'] = mu_g
            config_local['weights'] = {
                'AS': w_as,
                'KM': w_km,
                'DC': w_dc,
                'CAI': w_cai
            }
            
            results = run_simulation(config_local, n_iterations=100)  # Reduced for speed
            tci_matrix[i, j] = results['tci']
            
        print(f"Progress: {(i+1)/len(w_as_range)*100:.1f}%")
    
    # Create heatmap
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Use seaborn for better aesthetics
    sns.heatmap(
        tci_matrix,
        xticklabels=[f'{x:.2f}' for x in mu_g_range],
        yticklabels=[f'{y:.2f}' for y in w_as_range],
        cmap='RdYlGn',  # Red-Yellow-Green colormap
        vmin=0.70,      # Min TCI (red)
        vmax=0.95,      # Max TCI (green)
        annot=True,     # Show values in cells
        fmt='.3f',      # Format: 3 decimal places
        cbar_kws={'label': 'Trust Continuity Index (TCI)'},
        ax=ax
    )
    
    # Formatting
    ax.set_xlabel('Growth Rate ($\\mu_g$)', fontsize=14)
    ax.set_ylabel('Algorithm Strength Weight ($w_{AS}$)', fontsize=14)
    ax.set_title('Sensitivity Analysis: TCI Across Parameter Space', fontsize=16, fontweight='bold')
    
    # Add threshold line (optional baseline reference)
    ax.axhline(y=0, color='black', linewidth=2)
    
    plt.tight_layout()
    plt.savefig('results/figure3_sensitivity_analysis.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    print(f"Figure 3 saved to: results/figure3_sensitivity_analysis.png")
    print(f"TCI range: {tci_matrix.min():.3f} - {tci_matrix.max():.3f}")


if __name__ == '__main__':
    generate_sensitivity_heatmap()
