"""
Monte Carlo simulation engine for quantum risk assessment.

This module implements the main simulation loop that generates multiple
stochastic realizations of adversarial capability growth and calculates
risk metrics across different cryptographic algorithms and migration scenarios.
"""

import numpy as np
import config
from core_logic import calculate_adversarial_capability, calculate_rqr, calculate_cas
from scenarios import get_migration_coverage

def run_monte_carlo():
    """
    Execute Monte Carlo simulation for quantum risk evolution.
    
    Generates multiple stochastic scenarios of adversarial capability growth
    and calculates RQR for both classical (RSA-2048) and PQC (Kyber-512)
    algorithms. The simulation accounts for uncertainty in quantum computing
    development through random growth rates and annual volatility.
    
    The function implements the stochastic modeling framework from the paper,
    combining Eq. 6 (adversarial capability), Eq. 9 (growth rate distribution),
    and Eq. 10 (RQR calculation).
    
    Returns:
        tuple: (t_array, rqr_rsa_all, rqr_kyber_all)
            - t_array (np.ndarray): Time points from 1 to YEARS
            - rqr_rsa_all (np.ndarray): RQR values for RSA-2048, 
              shape (N_SIMULATIONS, YEARS)
            - rqr_kyber_all (np.ndarray): RQR values for Kyber-512,
              shape (N_SIMULATIONS, YEARS)
    """
    print(f"Starting Monte Carlo Simulation ({config.N_SIMULATIONS} runs)...")
    
    # Time array: Year 1 to Year T
    t_array = np.arange(1, config.YEARS + 1)
    
    # Pre-allocate arrays for results
    # Shape: (Simulations, Years)
    rqr_rsa_all = np.zeros((config.N_SIMULATIONS, config.YEARS))
    rqr_kyber_all = np.zeros((config.N_SIMULATIONS, config.YEARS))
    
    # Generate random growth rates for all simulations (Eq. 9)
    g_rates = np.random.normal(config.MU_G, config.SIGMA_G, config.N_SIMULATIONS)
    
    for i in range(config.N_SIMULATIONS):
        # Generate noise for this timeline
        epsilon = np.random.normal(0, config.SIGMA_EPSILON, config.YEARS)
        
        # Calculate Adversarial Capability
        adv_cap = calculate_adversarial_capability(t_array, g_rates[i], epsilon)
        
        # Calculate RQR for RSA
        rqr_rsa_all[i, :] = calculate_rqr(adv_cap, config.COST_RSA_2048)
        
        # Calculate RQR for Kyber
        rqr_kyber_all[i, :] = calculate_rqr(adv_cap, config.COST_KYBER_512)

    return t_array, rqr_rsa_all, rqr_kyber_all

def calculate_tci_scenarios(t_array, rqr_kyber_mean):
    """
    Calculate CAS and TCI for different migration strategies.
    
    Implements Eq. 14 from the paper:
        TCI = (1/T) * sum(CAS(t))
    
    This function evaluates how different migration strategies affect the
    overall security assurance over the simulation horizon. Each strategy
    has a different deployment coverage trajectory L(t) which affects the
    CAS metric and ultimately the Trust Continuity Index.
    
    Args:
        t_array (np.ndarray): Time points from 1 to YEARS
        rqr_kyber_mean (np.ndarray): Mean RQR values for Kyber-512 across
            all Monte Carlo simulations
    
    Returns:
        dict: Dictionary mapping scenario names to results
            Each entry contains:
            - 'cas_series' (np.ndarray): CAS values over time
            - 'tci' (float): Trust Continuity Index (time-averaged CAS)
    """
    scenarios = ["Aggressive", "Conservative", "Late_Start"]
    results = {}
    
    for sc in scenarios:
        # Get L(t)
        coverage = get_migration_coverage(sc, t_array)
        
        # Calculate CAS using the Mean RQR of Kyber (assuming migration is to Kyber)
        # Note: In a real complex model, we would mix RSA and Kyber RQR based on L(t).
        # For this paper's simplicity, we use the migrated system's risk profile scaled by L(t).
        
        # Hybrid Risk Model: Risk = (1 - L(t)) * RSA_Risk + L(t) * Kyber_Risk
        # But to keep CAS Eq 12 pure, we pass the RQR of the *target* state for the strength metric
        # and penalize the score via the Deployment Coverage metric.
        
        cas_series = calculate_cas(rqr_kyber_mean, coverage)
        
        # Calculate TCI (Eq. 14)
        tci_score = np.mean(cas_series)
        
        results[sc] = {
            "cas_series": cas_series,
            "tci": tci_score
        }
        
    return results
