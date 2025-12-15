import numpy as np
import simulation
import visualization

def main():
    # 1. Run Monte Carlo Simulation
    t_array, rqr_rsa, rqr_kyber = simulation.run_monte_carlo()
    
    # 2. Generate RQR Plot (Figure 1)
    visualization.save_rqr_plot(t_array, rqr_rsa, rqr_kyber)
    
    # 3. Calculate Scenarios
    # We use the mean Kyber risk to calculate CAS for the organization
    kyber_mean_risk = np.mean(rqr_kyber, axis=0)
    scenario_data = simulation.calculate_tci_scenarios(t_array, kyber_mean_risk)
    
    # 4. Generate CAS Plot (Figure 2)
    visualization.save_cas_plot(t_array, scenario_data)
    
    # 5. Print Summary Statistics for the Paper
    print("\n--- SIMULATION RESULTS FOR PAPER ---")
    print(f"RSA Risk at Year 5: {np.mean(rqr_rsa[:, 4]):.4f}")
    print(f"Kyber Risk at Year 5: {np.mean(rqr_kyber[:, 4]):.4f}")
    
    print("\n--- TRUST CONTINUITY INDEX (TCI) ---")
    for name, data in scenario_data.items():
        print(f"Scenario: {name} | TCI: {data['tci']:.3f}")

if __name__ == "__main__":
    main()
