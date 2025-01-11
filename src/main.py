import csv
import json
import logging

from pathlib import Path

from src.simulation import Simulation
from src.utils import plot_performance

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)

def get_path(*args):
    return Path(__file__).resolve().parents[1].joinpath(*args)


def get_employee_setups(setups_path):
    """Returns the list of employee setups from the setup.json file."""
    setups_path = get_path('src', setups_path)
    if not Path(setups_path).exists():
        logging.error(f"Employee setups file not found at: {setups_path}")
        return {}

    with open(setups_path, "r") as file:
        employee_setups = json.load(file)

    return employee_setups


def run_simulations_with_setup(name, setup, iterations, config_path, verbose=False):
    """
    Run multiple simulations for a specific setup and return the results.

    :param name: Name of the simulation setup.
    :param setup: The configuration for employees and deanery.
    :param iterations: Number of iterations for the simulation.
    :param config_path: Path to the base configuration JSON file.
    :param verbose: Whether to print detailed results for each iteration.
    :return: List of dictionaries containing results for each iteration.
    """
    results = []
    for i in range(iterations):
        logging.info(f"Running iteration {i + 1} for setup {name}")
        simulation = Simulation(config_path=config_path, setup=setup, verbose=verbose)
        simulation.run()
        results.append({
            "name": name,
            "lambda": simulation.lambda_rate,
            "mu": simulation.service_rate,
            "iteration": i + 1,
            "average_waiting_time": simulation.get_average_wait_time(),
            "average_service_time": simulation.get_average_service_time()
        })
        if verbose:
            simulation.report()
    return results


def main():
    setups = get_employee_setups(setups_path="setups.json")
    results_path = get_path('results')
    config_path = get_path('src', 'config.json')
    iterations = 10  # Number of iterations per setup

    # Prepare CSV file
    csv_file = results_path.joinpath("results.csv")
    with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=[
            "name", "iteration", "lambda", "mu", "average_waiting_time", "average_service_time"
        ])
        writer.writeheader()

        # Run simulations for each setup
        for name, setup in setups.items():
            logging.info(f"Starting simulations for setup: {name}")
            results = run_simulations_with_setup(name, setup, iterations, config_path)
            writer.writerows(results)

    plot_performance(csv_file, output_dir=results_path.joinpath("plots"))

    logging.info(f"All results saved to {csv_file}")


if __name__ == "__main__":
    main()
