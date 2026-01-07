"""
Migration scenario models for PQC adoption strategies.

This module defines different organizational migration strategies and their
deployment coverage trajectories. Each scenario implements a different
approach to transitioning from classical to post-quantum cryptography.
"""

import numpy as np

def get_migration_coverage(scenario_name, t_array):
    """
    Calculate the percentage of systems migrated to PQC over time.
    
    Implements Eq. 15-17 from the paper representing three distinct
    migration strategies:
    
    - Aggressive (Eq. 15): Logistic curve reaching ~98% coverage quickly,
      suitable for organizations with strong resources and urgency
    
    - Conservative (Eq. 16): Linear migration at 18% per year,
      suitable for risk-averse organizations with gradual adoption
    
    - Late_Start (Eq. 17): Delayed linear migration starting after 3 years,
      representing organizations that postpone migration decisions
    
    Args:
        scenario_name (str): Migration strategy type
            Options: "Aggressive", "Conservative", "Late_Start"
        t_array (np.ndarray): Time array (years from present)
    
    Returns:
        np.ndarray: Migration coverage percentage L(t) for each time step,
            values in range [0, 1]
    """
    L_t = np.zeros_like(t_array, dtype=float)
    
    if scenario_name == "Aggressive":
        # Eq. 15: Logistic curve
        # Parameters tuned to reach ~98% quickly
        L_max = 0.98
        k = 0.8
        t0 = 4  # Midpoint year
        L_t = L_max / (1 + np.exp(-k * (t_array - t0)))
        
    elif scenario_name == "Conservative":
        # Eq. 16: Linear migration (18% per year)
        L_t = np.minimum(1.0, 0.18 * t_array)
        
    elif scenario_name == "Late_Start":
        # Eq. 17: Delayed linear
        t_delay = 3
        # Apply delay logic
        mask = t_array >= t_delay
        L_t[mask] = np.minimum(1.0, 0.18 * (t_array[mask] - t_delay))
        
    return L_t
