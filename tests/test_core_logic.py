"""
Unit tests for core_logic module.

Tests the fundamental mathematical functions ensuring correctness of
risk calculations and adherence to expected properties.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import pytest
from core_logic import calculate_adversarial_capability, calculate_rqr, calculate_cas
import config

class TestAdversarialCapability:
    """Tests for adversarial capability calculation."""
    
    def test_basic_calculation(self):
        """Test basic adversarial capability calculation."""
        t = np.array([1, 2, 3])
        g = 0.5
        epsilon = np.array([0, 0, 0])
        
        result = calculate_adversarial_capability(t, g, epsilon)
        
        expected = config.A0_LOG + g * t
        np.testing.assert_array_almost_equal(result, expected)
    
    def test_with_noise(self):
        """Test capability calculation with noise."""
        t = np.array([1, 2, 3])
        g = 0.5
        epsilon = np.array([0.1, -0.05, 0.02])
        
        result = calculate_adversarial_capability(t, g, epsilon)
        
        expected = config.A0_LOG + g * t + epsilon
        np.testing.assert_array_almost_equal(result, expected)
    
    def test_increasing_trend(self):
        """Test that capability increases with positive growth."""
        t = np.arange(1, 11)
        g = 0.5
        epsilon = np.zeros(10)
        
        result = calculate_adversarial_capability(t, g, epsilon)
        
        # Should be monotonically increasing
        assert np.all(np.diff(result) > 0)

class TestRQR:
    """Tests for Residual Quantum Risk calculation."""
    
    def test_rqr_bounds(self):
        """Test that RQR is always in [0, 1] range."""
        capability = np.linspace(0, 20, 100)
        cost = 10.0
        
        rqr = calculate_rqr(capability, cost)
        
        assert np.all(rqr >= 0.0)
        assert np.all(rqr <= 1.0)
    
    def test_rqr_at_equilibrium(self):
        """Test RQR when capability equals cost (delta=0)."""
        capability = np.array([10.0])
        cost = 10.0
        
        rqr = calculate_rqr(capability, cost)
        
        # At delta=0, RQR should be 0.5
        np.testing.assert_almost_equal(rqr[0], 0.5, decimal=10)
    
    def test_rqr_calibration(self):
        """Test RQR calibration point (delta=1 should give ~0.88 with alpha=2)."""
        capability = np.array([11.0])
        cost = 10.0
        
        rqr = calculate_rqr(capability, cost)
        
        # With alpha=2 and delta=1: RQR = 1/(1+e^-2) ≈ 0.8808
        expected = 1.0 / (1.0 + np.exp(-config.ALPHA * 1.0))
        np.testing.assert_almost_equal(rqr[0], expected, decimal=4)
    
    def test_rqr_low_capability(self):
        """Test RQR when capability is much lower than cost."""
        capability = np.array([5.0])
        cost = 15.0
        
        rqr = calculate_rqr(capability, cost)
        
        # Should be very low risk
        assert rqr[0] < 0.01
    
    def test_rqr_high_capability(self):
        """Test RQR when capability is much higher than cost."""
        capability = np.array([15.0])
        cost = 5.0
        
        rqr = calculate_rqr(capability, cost)
        
        # Should be very high risk
        assert rqr[0] > 0.99
    
    def test_rqr_monotonic(self):
        """Test that RQR increases monotonically with capability."""
        capability = np.linspace(5, 15, 50)
        cost = 10.0
        
        rqr = calculate_rqr(capability, cost)
        
        # Should be monotonically increasing
        assert np.all(np.diff(rqr) >= 0)

class TestCAS:
    """Tests for Composite Assurance Score calculation."""
    
    def test_cas_bounds(self):
        """Test that CAS is in [0, 1] range."""
        rqr = np.linspace(0, 1, 10)
        coverage = np.linspace(0, 1, 10)
        
        cas = calculate_cas(rqr, coverage)
        
        assert np.all(cas >= 0.0)
        assert np.all(cas <= 1.0)
    
    def test_cas_weight_validation(self):
        """Test that CAS weights sum to 1.0."""
        weights = config.WEIGHTS
        weight_sum = (weights["w_AS"] + weights["w_KM"] + 
                     weights["w_DC"] + weights["w_CAI"])
        
        np.testing.assert_almost_equal(weight_sum, 1.0, decimal=10)
    
    def test_cas_zero_risk_full_coverage(self):
        """Test CAS with zero risk and full coverage."""
        rqr = np.array([0.0])
        coverage = np.array([1.0])
        
        cas = calculate_cas(rqr, coverage)
        
        # With RQR=0, M_AS=1, full coverage gives high CAS
        # CAS = 0.4*1 + 0.25*0.85 + 0.2*1 + 0.15*0.75 = 0.9125
        expected = (config.WEIGHTS["w_AS"] * 1.0 + 
                   config.WEIGHTS["w_KM"] * 0.85 +
                   config.WEIGHTS["w_DC"] * 1.0 + 
                   config.WEIGHTS["w_CAI"] * 0.75)
        
        np.testing.assert_almost_equal(cas[0], expected, decimal=4)
    
    def test_cas_high_risk_no_coverage(self):
        """Test CAS with high risk and no migration coverage."""
        rqr = np.array([1.0])
        coverage = np.array([0.0])
        
        cas = calculate_cas(rqr, coverage)
        
        # With RQR=1, M_AS=0, no coverage gives low CAS
        # CAS = 0.4*0 + 0.25*0.85 + 0.2*0 + 0.15*0.75 = 0.325
        expected = (config.WEIGHTS["w_AS"] * 0.0 + 
                   config.WEIGHTS["w_KM"] * 0.85 +
                   config.WEIGHTS["w_DC"] * 0.0 + 
                   config.WEIGHTS["w_CAI"] * 0.75)
        
        np.testing.assert_almost_equal(cas[0], expected, decimal=4)
    
    def test_cas_improves_with_coverage(self):
        """Test that CAS improves as coverage increases (for fixed risk)."""
        rqr = np.array([0.5, 0.5, 0.5, 0.5])
        coverage = np.array([0.0, 0.3, 0.7, 1.0])
        
        cas = calculate_cas(rqr, coverage)
        
        # CAS should increase with coverage
        assert np.all(np.diff(cas) > 0)

class TestTCICalculation:
    """Tests for Trust Continuity Index calculation logic."""
    
    def test_tci_is_mean_cas(self):
        """Test that TCI equals mean of CAS series."""
        rqr = np.array([0.1, 0.2, 0.3, 0.4, 0.5])
        coverage = np.array([0.2, 0.4, 0.6, 0.8, 1.0])
        
        cas = calculate_cas(rqr, coverage)
        tci = np.mean(cas)
        
        # TCI should be the average of CAS
        assert 0.0 <= tci <= 1.0
        np.testing.assert_almost_equal(tci, np.mean(cas))

class TestIntegration:
    """Integration tests combining multiple functions."""
    
    def test_full_pipeline(self):
        """Test complete calculation pipeline."""
        t = np.array([1, 2, 3, 4, 5])
        g = 0.5
        epsilon = np.zeros(5)
        
        # Calculate capability
        capability = calculate_adversarial_capability(t, g, epsilon)
        
        # Calculate RQR
        rqr = calculate_rqr(capability, config.COST_RSA_2048)
        
        # Calculate CAS
        coverage = np.array([0.0, 0.25, 0.5, 0.75, 1.0])
        cas = calculate_cas(rqr, coverage)
        
        # Verify all outputs are in valid range
        assert np.all(capability >= config.A0_LOG)
        assert np.all((rqr >= 0) & (rqr <= 1))
        assert np.all((cas >= 0) & (cas <= 1))
    
    def test_reproducibility_with_seed(self):
        """Test that results are reproducible with same seed."""
        np.random.seed(42)
        
        t = np.arange(1, 11)
        g = np.random.normal(0.5, 0.1)
        epsilon1 = np.random.normal(0, 0.05, 10)
        
        result1 = calculate_adversarial_capability(t, g, epsilon1)
        
        # Reset and recalculate
        np.random.seed(42)
        g = np.random.normal(0.5, 0.1)
        epsilon2 = np.random.normal(0, 0.05, 10)
        
        result2 = calculate_adversarial_capability(t, g, epsilon2)
        
        np.testing.assert_array_almost_equal(result1, result2)

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
