"""
PQC Migration Risk Model - Main Entry Point

This framework assesses migration risks in a post-quantum cryptography environment
by simulating adversarial capability growth and evaluating different migration
strategies through Monte Carlo analysis.

The implementation follows the mathematical framework described in the research
paper, calculating three key metrics:
- RQR (Residual Quantum Risk): Break probability for cryptographic algorithms
- CAS (Composite Assurance Score): Organizational security posture
- TCI (Trust Continuity Index): Time-averaged assurance measure

Usage:
    Basic simulation with default parameters:
        python main.py
    
    Custom number of iterations:
        python main.py --n-iterations 5000
    
    Reproducible results with seed:
        python main.py --seed 42
    
    Paper mode (generates publication figures):
        python main.py --paper-mode
    
    Custom output directory:
        python main.py --output-dir ./my_results
"""

import numpy as np
import simulation
import visualization
import argparse
import logging
import sys
import os
import config

def setup_logging(verbose=False):
    """
    Configure logging for the application.
    
    Args:
        verbose (bool): If True, set logging level to DEBUG
    """
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

def parse_arguments():
    """
    Parse command-line arguments.
    
    Returns:
        argparse.Namespace: Parsed command-line arguments
    """
    parser = argparse.ArgumentParser(
        description='PQC Migration Risk Model Simulator',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --n-iterations 5000
  python main.py --seed 42 --paper-mode
  python main.py --output-dir ./custom_results
        """
    )
    
    parser.add_argument(
        '--n-iterations',
        type=int,
        default=config.N_SIMULATIONS,
        help=f'Number of Monte Carlo iterations (default: {config.N_SIMULATIONS})'
    )
    
    parser.add_argument(
        '--seed',
        type=int,
        default=None,
        help='Random seed for reproducibility (default: None)'
    )
    
    parser.add_argument(
        '--paper-mode',
        action='store_true',
        help='Generate publication-ready figures with paper styling'
    )
    
    parser.add_argument(
        '--output-dir',
        type=str,
        default='results',
        help='Output directory for results and figures (default: results)'
    )
    
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose logging'
    )
    
    return parser.parse_args()

def ensure_output_directory(output_dir):
    """
    Create output directory if it doesn't exist.
    
    Args:
        output_dir (str): Path to output directory
    """
    os.makedirs(output_dir, exist_ok=True)
    logging.info(f"Output directory: {output_dir}")

def main():
    """
    Main execution function for the PQC Migration Risk Model.
    
    Orchestrates the simulation workflow:
    1. Parse command-line arguments
    2. Configure logging and random seed
    3. Run Monte Carlo simulation
    4. Calculate scenario-based metrics
    5. Generate visualizations
    6. Display summary statistics
    """
    args = parse_arguments()
    setup_logging(args.verbose)
    
    logging.info("Starting PQC Migration Risk Model Simulation")
    
    # Set random seed for reproducibility
    if args.seed is not None:
        np.random.seed(args.seed)
        logging.info(f"Random seed set to: {args.seed}")
    
    # Override config if needed
    if args.n_iterations != config.N_SIMULATIONS:
        config.N_SIMULATIONS = args.n_iterations
        logging.info(f"Using {args.n_iterations} Monte Carlo iterations")
    
    # Ensure output directory exists
    ensure_output_directory(args.output_dir)
    
    try:
        # 1. Run Monte Carlo Simulation
        logging.info("Running Monte Carlo simulation...")
        t_array, rqr_rsa, rqr_kyber = simulation.run_monte_carlo()
        logging.info("Monte Carlo simulation completed")
        
        # 2. Generate RQR Plot (Figure 1)
        logging.info("Generating RQR evolution plot...")
        visualization.save_rqr_plot(t_array, rqr_rsa, rqr_kyber)
        
        # 3. Calculate Scenarios
        logging.info("Calculating migration scenarios...")
        kyber_mean_risk = np.mean(rqr_kyber, axis=0)
        scenario_data = simulation.calculate_tci_scenarios(t_array, kyber_mean_risk)
        
        # 4. Generate CAS Plot (Figure 2)
        logging.info("Generating CAS trajectories plot...")
        visualization.save_cas_plot(t_array, scenario_data)
        
        # 5. Print Summary Statistics
        print("\n" + "="*60)
        print("SIMULATION RESULTS SUMMARY")
        print("="*60)
        print(f"\nAlgorithm Risk Assessment (Year 5):")
        print(f"  RSA-2048:   {np.mean(rqr_rsa[:, 4]):.4f}")
        print(f"  Kyber-512:  {np.mean(rqr_kyber[:, 4]):.4f}")
        
        print(f"\nTrust Continuity Index (TCI) by Scenario:")
        for name, data in scenario_data.items():
            print(f"  {name:15s} TCI: {data['tci']:.3f}")
        
        print("\n" + "="*60)
        logging.info("Simulation completed successfully")
        
    except Exception as e:
        logging.error(f"Simulation failed: {str(e)}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
