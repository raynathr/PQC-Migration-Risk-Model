"""
Core mathematical functions for risk assessment in PQC migration.

This module implements the fundamental equations from the research paper:
- Adversarial capability modeling (Eq. 6)
- Residual Quantum Risk calculation (Eq. 10)
- Composite Assurance Score calculation (Eq. 12)
"""

import numpy as np
import config

def calculate_adversarial_capability(t, g, epsilon_series):
    """
    Calculate adversarial computational capability over time.
    
    Implements Eq. 6 from the paper:
        log10(A(t)) = log10(A0) + g*t + epsilon(t)
    
    This models the exponential growth of quantum computing capabilities with
    stochastic noise representing technological uncertainties.
    
    Args:
        t (np.ndarray): Time array (years from present)
        g (float): Annual growth rate of quantum capability
        epsilon_series (np.ndarray): Stochastic noise series for each time step
    
    Returns:
        np.ndarray: Log10 of adversarial capability at each time step
    """
    return config.A0_LOG + (g * t) + epsilon_series

def calculate_rqr(capability_log, cost_log):
    """
    Calculate Residual Quantum Risk using logistic function.
    
    Implements Eq. 10 from the paper:
        RQR(t) = 1 / (1 + exp(-alpha * delta))
    where delta = log10(A(t)) - log10(C_attack)
    
    This quantifies the probability that an adversary with capability A(t)
    can break an algorithm with attack cost C_attack. The logistic function
    provides smooth transition from negligible to critical risk.
    
    Args:
        capability_log (np.ndarray): Log10 of adversarial capability
        cost_log (float): Log10 of algorithm attack cost
    
    Returns:
        np.ndarray: Risk probability in range [0, 1] for each time step
    """
    delta = capability_log - cost_log
    return 1.0 / (1.0 + np.exp(-config.ALPHA * delta))

def calculate_cas(rqr, coverage_pct):
    """
    Calculate Composite Assurance Score for organizational security posture.
    
    Implements Eq. 12 from the paper:
        CAS(t) = w_AS * M_AS + w_KM * M_KM + w_DC * M_DC + w_CAI * M_CAI
    
    This aggregates multiple security metrics weighted by their importance:
    - M_AS: Algorithm Strength (derived from RQR)
    - M_KM: Key Management quality
    - M_DC: Deployment Coverage (migration progress)
    - M_CAI: Crypto-Agility Index
    
    Args:
        rqr (np.ndarray): Residual Quantum Risk values over time
        coverage_pct (np.ndarray): Percentage of systems migrated at each time step
    
    Returns:
        np.ndarray: Composite assurance score in range [0, 1] for each time step
    """
    # Metric 1: Algorithm Strength M_AS = max(0, 1 - RQR)
    m_as = np.maximum(0, 1 - rqr)
    
    # Metric 2: Key Management (Fixed baseline)
    m_km = 0.85
    
    # Metric 3: Deployment Coverage (M_DC = L(t))
    m_dc = coverage_pct
    
    # Metric 4: Crypto Agility (Assumed moderate baseline)
    m_cai = 0.75

    w = config.WEIGHTS
    cas = (w["w_AS"] * m_as + 
           w["w_KM"] * m_km + 
           w["w_DC"] * m_dc + 
           w["w_CAI"] * m_cai)
    return cas
