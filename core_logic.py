import numpy as np
import config

def calculate_adversarial_capability(t, g, epsilon_series):
    """
    Implements Eq. 6: log10 A(t) = log10 A0 + g*t + epsilon
    """
    return config.A0_LOG + (g * t) + epsilon_series

def calculate_rqr(capability_log, cost_log):
    """
    Implements Eq. 10: RQR(t) = 1 / (1 + e^(-alpha * Delta))
    """
    delta = capability_log - cost_log
    return 1.0 / (1.0 + np.exp(-config.ALPHA * delta))

def calculate_cas(rqr, coverage_pct):
    """
    Implements Eq. 12: CAS(t) = w_AS * M_AS + ...
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
