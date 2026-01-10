"""
Configuration parameters for the PQC Migration Risk Model framework.

This module centralizes all simulation parameters, adversarial capability modeling
parameters, algorithm attack costs, and risk assessment weights. These values are
based on the research framework and can be adjusted to explore different scenarios.

Parameters follow the notation from the research paper and implement the mathematical
models described in equations 6-17.
"""

# Simulation Settings
N_SIMULATIONS = 1000   # Number of Monte Carlo iterations
YEARS = 15             # Simulation horizon (T)

# Adversarial Capability Parameters (Table 1)
A0_LOG = 5.0           # Initial capability (10^5 operations)
MU_G = 0.5             # Mean annual growth rate
SIGMA_G = 0.1          # Growth rate standard deviation
SIGMA_EPSILON = 0.05   # Annual volatility (noise)

# Risk Model Parameters
ALPHA = 2.0            # Logistic sensitivity (Eq. 11)

# Algorithm Attack Costs (Log10 operations) - Table 2
COST_RSA_2048 = 10.0
COST_KYBER_512 = 18.0

# CAS Weights (Eq. 12)
WEIGHTS = {
    "w_AS": 0.40,  # Algorithm Strength
    "w_KM": 0.25,  # Key Management
    "w_DC": 0.20,  # Deployment Coverage
    "w_CAI": 0.15  # Crypto-Agility
}

# Thresholds
CAS_THRESHOLD = 0.70

# Default configuration dictionary for parameterized simulations
DEFAULT_CONFIG = {
    'n_simulations': N_SIMULATIONS,
    'years': YEARS,
    'a0_log': A0_LOG,
    'mu_g': MU_G,
    'sigma_g': SIGMA_G,
    'sigma_epsilon': SIGMA_EPSILON,
    'alpha': ALPHA,
    'cost_rsa_2048': COST_RSA_2048,
    'cost_kyber_512': COST_KYBER_512,
    'weights': {
        'AS': WEIGHTS['w_AS'],
        'KM': WEIGHTS['w_KM'],
        'DC': WEIGHTS['w_DC'],
        'CAI': WEIGHTS['w_CAI']
    },
    'cas_threshold': CAS_THRESHOLD
}
