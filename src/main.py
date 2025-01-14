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
    """
    Returns the absolute path for the given relative path components.

    :param args: Relative path components.
    :return: Absolute Path object.
    """
    try:
        return Path(__file__).resolve().parents[1].joinpath(*args)
    except Exception as e:
        logging.error(f"Error generating path: {e}")
        raise


def get_employee_setups(setups_path):
    """
    Loads and returns the list of employee setups from the setups.json file.

    :param setups_path: Path to the setups.json file.
    :return: Dictionary containing employee setups.
    """
    try:
        setups_path = get_path('src', setups_path)
        if not setups_path.exists():
            logging.error(f"Employee setups file not found at: {setups_path}")
            return {}
        with open(setups_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        logging.error(f"Setup file {setups_path} not found.")
        return {}
    except json.JSONDecodeError as e:
        logging.error(f"Error decoding JSON in setups file: {e}")
        return {}
    except Exception as e:
        logging.error(f"Unexpected error reading setups file: {e}")
        return {}


def run_simulations_with_setup(name, setup, iterations, config_path, verbose=False):
    """
    Run multiple simulations for a specific setup and return the results.

    :param name: Name of the simulation setup.
    :param setup: Configuration for employees and deanery.
    :param iterations: Number of iterations to run the simulation.
    :param config_path: Path to the configuration JSON file.
    :param verbose: If True, log detailed simulation output.
    :return: List of dictionaries containing results for each iteration.
    """
    results = []
    for i in range(iterations):
        try:
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
        except Exception as e:
            logging.error(f"Error during iteration {i + 1} for setup {name}: {e}")
            continue
    return results


def main():
    """
    Main function to execute the simulation process:
    - Load employee setups.
    - Run simulations for all setups.
    - Save results to CSV.
    - Generate performance plots.
    """
    try:
        # Load setups
        setups = get_employee_setups(setups_path="setups.json")
        if not setups:
            logging.error("No setups loaded. Exiting program.")
            return

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
                try:
                    logging.info(f"Starting simulations for setup: {name}")
                    results = run_simulations_with_setup(name, setup, iterations, config_path)
                    writer.writerows(results)
                except Exception as e:
                    logging.error(f"Error running simulations for setup {name}: {e}")

        # Plot performance results
        try:
            plot_performance(csv_file, output_dir=results_path.joinpath("plots"))
        except Exception as e:
            logging.error(f"Error generating performance plots: {e}")

        logging.info(f"All results saved to {csv_file}")

    except Exception as e:
        logging.critical(f"Critical error in main execution: {e}")


if __name__ == "__main__":
    main()
