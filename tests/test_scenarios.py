"""
Unit tests for scenarios module.

Tests the migration scenario functions ensuring correctness of
coverage trajectories and adherence to paper specifications.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import pytest
from scenarios import get_migration_coverage


class TestAggressiveScenario:
    """Tests for Aggressive migration scenario (Eq. 15)."""
    
    def test_aggressive_parameters(self):
        """Test that Aggressive scenario uses correct parameters."""
        # Test at midpoint t0=3
        t_array = np.array([3.0])
        L_t = get_migration_coverage("Aggressive", t_array)
        
        # At t=t0, logistic should be L_max/2 = 0.98/2 = 0.49
        expected = 0.98 / 2.0
        np.testing.assert_almost_equal(L_t[0], expected, decimal=2)
    
    def test_aggressive_asymptote(self):
        """Test that Aggressive scenario asymptotes to L_max=0.98."""
        t_array = np.array([10.0, 15.0, 20.0])
        L_t = get_migration_coverage("Aggressive", t_array)
        
        # Should approach 0.98
        assert all(L_t >= 0.97)
        assert all(L_t <= 0.98)
    
    def test_aggressive_monotonic(self):
        """Test that Aggressive coverage increases monotonically."""
        t_array = np.arange(0, 15, 0.5)
        L_t = get_migration_coverage("Aggressive", t_array)
        
        # Should be monotonically increasing
        assert np.all(np.diff(L_t) >= 0)
    
    def test_aggressive_bounds(self):
        """Test that Aggressive coverage stays in [0, 1] range."""
        t_array = np.arange(0, 20)
        L_t = get_migration_coverage("Aggressive", t_array)
        
        assert np.all(L_t >= 0.0)
        assert np.all(L_t <= 1.0)


class TestConservativeScenario:
    """Tests for Conservative migration scenario (Eq. 16)."""
    
    def test_conservative_linear_rate(self):
        """Test that Conservative scenario grows at 18% per year."""
        t_array = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
        L_t = get_migration_coverage("Conservative", t_array)
        
        expected = np.array([0.18, 0.36, 0.54, 0.72, 0.90])
        np.testing.assert_array_almost_equal(L_t, expected, decimal=10)
    
    def test_conservative_caps_at_one(self):
        """Test that Conservative scenario caps at 100% coverage."""
        t_array = np.array([6.0, 10.0, 15.0])
        L_t = get_migration_coverage("Conservative", t_array)
        
        # Should be capped at 1.0 after ~5.56 years
        assert np.all(L_t <= 1.0)
        assert L_t[0] > 0.99  # At t=6, should be at cap
    
    def test_conservative_zero_at_zero(self):
        """Test that Conservative coverage starts at 0."""
        t_array = np.array([0.0])
        L_t = get_migration_coverage("Conservative", t_array)
        
        assert L_t[0] == 0.0


class TestLateStartScenario:
    """Tests for Late_Start migration scenario (Eq. 17)."""
    
    def test_late_start_delay(self):
        """Test that Late_Start has 0 coverage before t=2."""
        t_array = np.array([0.0, 0.5, 1.0, 1.5, 1.99])
        L_t = get_migration_coverage("Late_Start", t_array)
        
        # Should be zero before t=2
        np.testing.assert_array_almost_equal(L_t, np.zeros(5), decimal=10)
    
    def test_late_start_linear_after_delay(self):
        """Test that Late_Start grows linearly at 18% per year after t=2."""
        t_array = np.array([2.0, 3.0, 4.0, 5.0, 6.0])
        L_t = get_migration_coverage("Late_Start", t_array)
        
        # After delay, should be 0.18 * (t - 2)
        expected = np.array([0.0, 0.18, 0.36, 0.54, 0.72])
        np.testing.assert_array_almost_equal(L_t, expected, decimal=10)
    
    def test_late_start_transition(self):
        """Test Late_Start transition at t=2."""
        t_array = np.array([1.9, 2.0, 2.1])
        L_t = get_migration_coverage("Late_Start", t_array)
        
        # Before t=2: should be 0
        assert L_t[0] == 0.0
        # At t=2: should start at 0
        assert L_t[1] == 0.0
        # After t=2: should be positive
        assert L_t[2] > 0.0
    
    def test_late_start_caps_at_one(self):
        """Test that Late_Start scenario caps at 100% coverage."""
        t_array = np.array([8.0, 10.0, 15.0])
        L_t = get_migration_coverage("Late_Start", t_array)
        
        # Should be capped at 1.0 after t=2+5.56=7.56 years
        assert np.all(L_t <= 1.0)
        assert L_t[0] > 0.99  # At t=8, should be at cap


class TestScenarioComparison:
    """Tests comparing different scenarios."""
    
    def test_aggressive_fastest_early(self):
        """Test that Aggressive achieves high coverage fastest in mid-range years."""
        # At year 4, aggressive should be significantly ahead
        t_array = np.array([4.0])
        
        aggressive = get_migration_coverage("Aggressive", t_array)
        late_start = get_migration_coverage("Late_Start", t_array)
        
        # Aggressive should be much higher than Late_Start at year 4
        assert aggressive[0] > 0.7
        assert late_start[0] < 0.4
        assert aggressive[0] > late_start[0]
    
    def test_late_start_slowest(self):
        """Test that Late_Start has lowest coverage in early years."""
        t_array = np.array([1.0, 2.0, 3.0])
        
        aggressive = get_migration_coverage("Aggressive", t_array)
        conservative = get_migration_coverage("Conservative", t_array)
        late_start = get_migration_coverage("Late_Start", t_array)
        
        # Late_Start should be lowest due to delay
        assert np.all(late_start <= conservative)
        assert np.all(late_start <= aggressive)
    
    def test_all_scenarios_reach_high_coverage(self):
        """Test that all scenarios eventually reach high coverage."""
        t_array = np.array([15.0])
        
        aggressive = get_migration_coverage("Aggressive", t_array)
        conservative = get_migration_coverage("Conservative", t_array)
        late_start = get_migration_coverage("Late_Start", t_array)
        
        # All should be at or near 100% by year 15
        assert aggressive[0] > 0.97
        assert conservative[0] > 0.99
        assert late_start[0] > 0.99


class TestEdgeCases:
    """Tests for edge cases and error handling."""
    
    def test_negative_time(self):
        """Test behavior with negative time values."""
        t_array = np.array([-1.0, 0.0, 1.0])
        
        # Should handle gracefully (extrapolation)
        aggressive = get_migration_coverage("Aggressive", t_array)
        conservative = get_migration_coverage("Conservative", t_array)
        late_start = get_migration_coverage("Late_Start", t_array)
        
        # All should return valid arrays
        assert len(aggressive) == 3
        assert len(conservative) == 3
        assert len(late_start) == 3
    
    def test_unknown_scenario(self):
        """Test behavior with unknown scenario name."""
        t_array = np.array([1.0, 2.0, 3.0])
        
        # Should return zeros for unknown scenario
        result = get_migration_coverage("Unknown", t_array)
        np.testing.assert_array_equal(result, np.zeros(3))
    
    def test_single_time_point(self):
        """Test with single time point."""
        t_array = np.array([5.0])
        
        aggressive = get_migration_coverage("Aggressive", t_array)
        conservative = get_migration_coverage("Conservative", t_array)
        late_start = get_migration_coverage("Late_Start", t_array)
        
        assert len(aggressive) == 1
        assert len(conservative) == 1
        assert len(late_start) == 1
        
        # All should be in valid range
        assert 0.0 <= aggressive[0] <= 1.0
        assert 0.0 <= conservative[0] <= 1.0
        assert 0.0 <= late_start[0] <= 1.0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
