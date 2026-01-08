# Changelog

All notable changes to the PQC Migration Risk Model framework will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-01-07

### Added
- Initial release of the PQC Migration Risk Model framework
- Monte Carlo simulation engine for adversarial capability modeling (Eq. 6)
- Residual Quantum Risk (RQR) calculation using logistic risk function (Eq. 10)
- Composite Assurance Score (CAS) calculation with weighted metrics (Eq. 12)
- Trust Continuity Index (TCI) calculation across migration scenarios (Eq. 14)
- Three migration scenario strategies: Aggressive, Conservative, and Late Start
- Visualization tools for RQR evolution and CAS trajectories
- Configuration module for easy parameter tuning
- Example scripts demonstrating various use cases
- Comprehensive unit test suite
- Docker support for containerized execution
- GitHub Actions CI/CD pipeline
- Interactive Jupyter notebook for exploration
- Sample data files for quantum roadmaps and attack costs
- Complete documentation and contribution guidelines

### Features
- Support for comparing classical (RSA-2048) vs PQC (Kyber-512) algorithms
- Configurable adversarial capability growth modeling
- Multiple migration strategy evaluation
- Statistical analysis with confidence intervals
- Publication-ready figure generation

### Known Issues
- Simulation time increases linearly with number of iterations
- Memory usage can be high for very large iteration counts (>100,000)
- Current model assumes simplified key management and crypto-agility metrics

### Future Planned Features
- Support for additional PQC algorithms (Dilithium, SPHINCS+)
- Hybrid classical-quantum migration modeling
- Cost-benefit analysis module
- Integration with real-world quantum computing benchmarks
- Interactive web-based dashboard
- Sensitivity analysis automation tools
- Extended scenario modeling (network effects, partial failures)
