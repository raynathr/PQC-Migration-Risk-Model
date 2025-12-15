import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import config

def save_rqr_plot(t_array, rqr_rsa, rqr_kyber):
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
