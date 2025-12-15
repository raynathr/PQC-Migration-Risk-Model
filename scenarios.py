import numpy as np

def get_migration_coverage(scenario_name, t_array):
    """
    Returns the percentage L(t) of systems migrated for each year.
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
