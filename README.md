# PQC Migration Risk Model

A comprehensive framework for assessing migration risks and security assurance in the post-quantum cryptography (PQC) transition. This research-based tool uses Monte Carlo simulation to model adversarial capability growth and evaluate different organizational migration strategies.

## Overview

The PQC Migration Risk Model implements a quantitative framework for evaluating the quantum threat to current cryptographic systems and assessing the effectiveness of migration strategies. The framework is based on the research paper:

**"Quantitative Risk Assessment Framework for Post-Quantum Cryptography Migration"**  
Authors: Rayyan Athar, Abdul Moiz, Noor ul Hassan  
Institution: Air University, Islamabad, Pakistan

### Key Features

- **Stochastic Risk Modeling**: Monte Carlo simulation of adversarial quantum computing capability growth
- **Multi-Algorithm Assessment**: Compare risk profiles for classical (RSA) and PQC (Kyber) algorithms
- **Migration Strategy Evaluation**: Analyze three distinct migration scenarios (Aggressive, Conservative, Late Start)
- **Quantitative Metrics**: Calculate RQR, CAS, and TCI for comprehensive risk assessment
- **Visualization Tools**: Generate publication-ready figures for research and presentations
- **Extensible Framework**: Easy to add custom algorithms, scenarios, and parameters

## Framework Metrics

The framework calculates three key metrics:

1. **RQR (Residual Quantum Risk)**: Probability that an adversary can break a cryptographic algorithm given their computational capability. Ranges from 0 (secure) to 1 (broken).

2. **CAS (Composite Assurance Score)**: Organizational security posture combining:
   - Algorithm Strength (M_AS)
   - Key Management (M_KM)
   - Deployment Coverage (M_DC)
   - Crypto-Agility Index (M_CAI)

3. **TCI (Trust Continuity Index)**: Time-averaged CAS over the simulation horizon, providing a single metric to compare migration strategies.

## Quick Start

### Installation

1. Clone the repository:
```bash
git clone https://github.com/raynathr/PQC-Migration-Risk-Model.git
cd PQC-Migration-Risk-Model
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

### Basic Usage

Run the default simulation (1000 iterations, 15-year horizon):
```bash
python main.py
```

Run with custom parameters:
```bash
python main.py --n-iterations 5000 --seed 42 --output-dir ./my_results
```

Run with verbose logging:
```bash
python main.py --verbose
```

### Using Docker

Build and run with Docker:
```bash
docker build -t pqc-simulator .
docker run -v $(pwd)/results:/app/results pqc-simulator
```

Or use docker-compose:
```bash
docker-compose up
```

## Repository Structure

```
PQC-Migration-Risk-Model/
├── .github/
│   └── workflows/
│       └── tests.yml           # CI/CD pipeline
├── data/
│   ├── attack_costs.csv        # Algorithm attack cost reference
│   └── quantum_roadmaps.csv    # Quantum capability projections
├── examples/
│   ├── basic_simulation.py     # Simple single-run example
│   ├── custom_migration.py     # Custom strategy definition
│   └── parameter_sensitivity.py # Parameter sensitivity analysis
├── notebooks/
│   └── interactive_demo.ipynb  # Interactive exploration notebook
├── tests/
│   └── test_core_logic.py      # Unit tests
├── config.py                   # Configuration parameters
├── core_logic.py               # Core mathematical functions
├── main.py                     # Main entry point
├── scenarios.py                # Migration scenario definitions
├── simulation.py               # Monte Carlo simulation engine
├── visualization.py            # Plotting functions
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Docker container setup
├── docker-compose.yml          # Docker Compose configuration
├── .gitignore                  # Git ignore rules
├── CONTRIBUTING.md             # Contribution guidelines
├── CHANGELOG.md                # Version history
├── LICENSE                     # MIT License
└── README.md                   # This file
```

## Configuration

All simulation parameters can be modified in `config.py`:

### Simulation Settings
- `N_SIMULATIONS`: Number of Monte Carlo iterations (default: 1000)
- `YEARS`: Simulation time horizon in years (default: 15)

### Adversarial Capability Parameters
- `A0_LOG`: Initial adversarial capability, log10 scale (default: 5.0, representing 10^5 operations)
- `MU_G`: Mean annual growth rate (default: 0.5 or 50%)
- `SIGMA_G`: Growth rate standard deviation (default: 0.1)
- `SIGMA_EPSILON`: Annual volatility/noise (default: 0.05)

### Risk Model Parameters
- `ALPHA`: Logistic sensitivity parameter (default: 2.0)
- Controls the steepness of the risk transition function

### Algorithm Attack Costs (log10 operations)
- `COST_RSA_2048`: RSA-2048 attack cost (default: 10.0)
- `COST_KYBER_512`: Kyber-512 attack cost (default: 18.0)

### CAS Weights
- `w_AS`: Algorithm Strength weight (default: 0.40)
- `w_KM`: Key Management weight (default: 0.25)
- `w_DC`: Deployment Coverage weight (default: 0.20)
- `w_CAI`: Crypto-Agility weight (default: 0.15)

## Example Results

After running the simulation, you'll see output like:

```
============================================================
SIMULATION RESULTS SUMMARY
============================================================

Algorithm Risk Assessment (Year 5):
  RSA-2048:   0.0106
  Kyber-512:  0.0000

Trust Continuity Index (TCI) by Scenario:
  Aggressive      TCI: 0.874
  Conservative    TCI: 0.894
  Late_Start      TCI: 0.854

============================================================
```

### Interpretation

- **RSA-2048 Risk**: The probability that RSA-2048 can be broken in Year 5 is about 1%
- **Kyber-512 Risk**: Kyber-512 remains extremely secure (near-zero risk) throughout the horizon
- **TCI Values**: Conservative migration achieves the highest trust continuity (0.894), balancing security and operational stability

The framework generates two figures:
- `results/figure1_rqr_evolution.png`: RQR trajectories for RSA and Kyber
- `results/figure2_cas_scenarios.png`: CAS evolution under different migration strategies

## Examples

### Basic Simulation

See `examples/basic_simulation.py` for a minimal example:

```python
from core_logic import calculate_adversarial_capability, calculate_rqr
import numpy as np

t = np.arange(1, 11)
g = 0.5
noise = np.random.normal(0, 0.05, 10)

capability = calculate_adversarial_capability(t, g, noise)
rqr = calculate_rqr(capability, 10.0)  # RSA-2048 cost
```

### Custom Migration Strategy

See `examples/custom_migration.py` for defining custom migration scenarios:

```python
def custom_migration_strategy(t_array):
    # 30% immediate, then gradual
    coverage = np.minimum(1.0, 0.30 + 0.12 * (t_array - 1))
    return coverage
```

### Parameter Sensitivity

See `examples/parameter_sensitivity.py` for sensitivity analysis of growth rates, alpha values, and algorithm costs.

## Running Tests

Run the test suite:
```bash
pytest tests/ -v
```

Run a specific test:
```bash
pytest tests/test_core_logic.py::TestRQR::test_rqr_bounds -v
```

## Citation

If you use this framework in your research, please cite:

```bibtex
@article{athar2025pqc,
  title={Quantitative Risk Assessment Framework for Post-Quantum Cryptography Migration},
  author={Athar, Rayyan and Moiz, Abdul and Hassan, Noor ul},
  institution={Air University, Islamabad, Pakistan},
  year={2025}
}
```

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on:
- Reporting issues
- Submitting pull requests
- Code style requirements
- Testing standards

## Contact

For questions, suggestions, or collaboration inquiries:

- **Rayyan Athar** - [GitHub](https://github.com/raynathr)
- **Abdul Moiz** - Air University, Islamabad
- **Noor ul Hassan** - Air University, Islamabad

## Related Resources

- [NIST Post-Quantum Cryptography Standardization](https://csrc.nist.gov/projects/post-quantum-cryptography)
- [NIST SP 800-208: Recommendation for Stateful Hash-Based Signature Schemes](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-208.pdf)
- [Kyber Algorithm Specification](https://pq-crystals.org/kyber/)
- [Quantum Threat Timeline](https://globalriskinstitute.org/publications/quantum-threat-timeline-report-2020/)
- [Migration to Post-Quantum Cryptography (CISA)](https://www.cisa.gov/quantum)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

This research was conducted at Air University, Islamabad, Pakistan. We acknowledge the support of the faculty and research community in developing this framework.

## Version

Current version: 1.0.0 - See [CHANGELOG.md](CHANGELOG.md) for version history and planned features.

