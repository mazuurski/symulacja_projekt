import json
import logging
from src.simulation import Simulation
from src.utils import generate_performance_scatter
import os

# Set up logging
logging.basicConfig(level=logging.INFO)


def get_project_root():
    """Returns the absolute path to the 'src' directory."""
    src_root = os.path.abspath(os.path.dirname(__file__))
    return src_root


def get_config_path():
    """Returns the path to the config.json file located inside the 'src' directory."""
    src_root = get_project_root()  # Get the src directory
    config_path = os.path.join(src_root, 'config.json')  # Append config.json inside the 'src' directory
    return config_path


def get_setups_path():
    """Returns the path to the setup.json file located inside the 'src' directory."""
    src_root = get_project_root()
    return os.path.join(src_root, 'setups.json')


def get_results_path():
    """Returns the path to the results.raw file."""
    src_root = get_project_root()
    return os.path.join(src_root, '..', 'results', 'results.raw')  # Adjust path to place results outside src


def get_employee_setups():
    """Returns the list of employee setups from the setup.json file."""
    setups_path = get_setups_path()
    if not os.path.exists(setups_path):
        logging.error(f"Employee setups file not found at: {setups_path}")
        return []

    with open(setups_path, "r") as file:
        employee_setups = json.load(file)

    return employee_setups


def run_simulation_with_config(config, employee_configs):
    """
    Run the simulation for a specific configuration and employee setup.

    Args:
        config (dict): The base configuration dict.
        employee_configs (list): The list of employee configurations to test.

    Returns:
        tuple: Average wait time, average service time, and average queue length for the simulation.
    """
    # Update the configuration with the specific employee setup
    config_copy = config.copy()
    config_copy["employees_config"] = employee_configs

    # Save the updated config to a temporary file
    temp_config_path = os.path.join(get_project_root(), 'temp_config.json')  # Save temp config in the project root
    with open(temp_config_path, "w") as config_file:
        json.dump(config_copy, config_file)

    # Now, run the simulation with this temporary config file
    simulation = Simulation(config_path=temp_config_path, verbose=False)
    simulation.run()

    # Calculate and return the average wait time, average service time, and average queue length
    average_wait_time = simulation.get_average_wait_time()
    average_service_time = simulation.get_average_service_time()
    average_queue_length = simulation.get_average_queue_length()

    # Clean up temporary config file after simulation
    os.remove(temp_config_path)

    return average_wait_time, average_service_time, average_queue_length


def main():
    # # Load the configuration from the config.json file located inside the 'src' folder
    # config_path = get_config_path()  # Use the updated config path
    # if not os.path.exists(config_path):
    #     logging.error(f"Config file not found at: {config_path}")
    #     return
    #
    # with open(config_path, "r") as file:
    #     config = json.load(file)
    #
    # # The list of employee configurations that we want to test
    # employee_configs = config["employees_config"]
    #
    # # Generate all combinations of employee configurations (subsets of the employee configs)
    # # For example: combinations(1), combinations(2), combinations(3), ..., combinations(len(employee_configs))
    # all_employee_config_combinations = []
    # for r in range(1, len(employee_configs) + 1):
    #     all_employee_config_combinations.extend(combinations(employee_configs, r))
    #
    # # Run simulations for different configurations
    # results = []
    # for i, employee_config_combination in enumerate(all_employee_config_combinations):
    #     logging.info(f"Running simulation with employee configuration combination {i + 1}: {employee_config_combination}")
    #     average_wait_time, average_service_time, average_queue_length = run_simulation_with_config(config, list(employee_config_combination))
    #
    #     # Store the results with employee ID combination and performance metrics
    #     results.append({
    #         "employee_config_combination": [emp['id'] for emp in employee_config_combination],
    #         "average_wait_time": average_wait_time,
    #         "average_service_time": average_service_time,
    #         "average_queue_length": average_queue_length
    #     })
    #
    # # Generate the performance scatter plot
    # generate_performance_scatter(results, os.path.join(get_project_root(), '..', 'results', 'performance.png'))
    #
    # # Optionally, save the results to a raw results file
    # results_path = get_results_path()  # Get correct results path
    # with open(results_path, "w") as results_file:
    #     for i, result in enumerate(results):
    #         # Write the configuration index and the key metrics
    #         results_file.write(f"Configuration {i + 1}: "
    #                            f"Avg Wait Time = {result['average_wait_time']}, "
    #                            f"Avg Service Time = {result['average_service_time']}, "
    #                            f"Avg Queue Length = {result['average_queue_length']}\n")
    #
    # logging.info(f"Simulation completed and results have been saved to {results_path}")
    pass


def test():
    setups = get_employee_setups()
    for name, setup in setups.items():
        logging.info(f"Running simulation with setup: {name}")
        simulation = Simulation(config_path=get_config_path(), setup=setup, verbose=True)
        simulation.run()
        simulation.report()


if __name__ == "__main__":
    # main()
    test()
