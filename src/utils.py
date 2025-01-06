import json

import matplotlib.pyplot as plt

from src.simulation import Simulation


def run_simulation_with_employees_config(config, verbose=False):
    """
    Runs the simulation with a given configuration and returns the results.
    Args:
        config (dict): The configuration dictionary (e.g., employees_config).
        verbose (bool): Whether to print additional logs.
    Returns:
        dict: Simulation results with performance metrics.
    """
    # Create the simulation object with the provided config
    simulation = Simulation(config_path="", verbose=verbose)  # Assuming config_path is empty for now
    simulation.config["employees_config"] = config  # Override with the new employee configuration

    simulation.run()  # Run the simulation
    simulation.report()  # Generate the report

    # Collect performance metrics (this depends on how you structure your simulation reports)
    # For simplicity, let's assume we track average wait times and employee utilization here
    results = {
        "average_wait_time": simulation.get_average_wait_time(),  # Hypothetical method to calculate average wait time
        "average_queue_length": simulation.get_average_queue_length(),  # Hypothetical method to calculate average queue length
        "average_service_time": simulation.get_average_service_time(),  # Hypothetical method to calculate average service time
    }

    return results


def compare_different_configurations(configurations, output_file='performance_comparison.png'):
    """
    Compares different employee configurations and generates a performance plot.
    Args:
        configurations (list): List of configurations (list of employee configs).
        output_file (str): Path where the performance plot will be saved.
    """
    wait_times = []
    utilizations = []
    employee_counts = []

    # Loop through the different configurations
    for config in configurations:
        print(f"Running simulation with {len(config)} employees...")
        results = run_simulation_with_employees_config(config)

        # Capture results for plotting
        wait_times.append(results["average_wait_time"])
        utilizations.append(results["employee_utilization"])
        employee_counts.append(len(config))  # Number of employees in this configuration

    # Plot the performance scatter plot
    plt.figure(figsize=(10, 6))
    plt.scatter(employee_counts, wait_times, c=utilizations, cmap='viridis', s=100, edgecolors="black")
    plt.colorbar(label="Employee Utilization")
    plt.title('Performance Comparison of Different Employee Configurations')
    plt.xlabel('Number of Employees')
    plt.ylabel('Average Wait Time (minutes)')
    plt.grid(True)

    # Save the figure
    plt.savefig(output_file)
    plt.show()


# Updated code in utils.py for generate_performance_scatter
def generate_performance_scatter(results, output_file):
    """
    Generate a scatter plot comparing the average wait time and service time for different configurations.

    Args:
        results (list): The list of results from the simulation, where each result is a dictionary
                        containing performance metrics and configuration information.
        output_file (str): Path to save the generated scatter plot image.
    """
    # Prepare the data for plotting
    employee_ids = [str(result["employee_config_combination"]) for result in results]  # Use the updated key
    avg_wait_times = [result["average_wait_time"] for result in results]
    avg_service_times = [result["average_service_time"] for result in results]

    # Create the scatter plot
    plt.figure(figsize=(10, 6))
    plt.scatter(avg_wait_times, avg_service_times)

    # Annotate each point with the employee configuration combination (as a string)
    for i, employee_id in enumerate(employee_ids):
        plt.annotate(employee_id, (avg_wait_times[i], avg_service_times[i]), fontsize=8)

    # Add labels and title
    plt.xlabel("Average Wait Time")
    plt.ylabel("Average Service Time")
    plt.title("Performance Scatter Plot")

    # Save the plot to the output file
    plt.tight_layout()
    plt.savefig(output_file)
    plt.close()


def generate_results_report(results, file_path="results.raw"):
    """
    Generates a raw results report (e.g., in JSON format).
    Args:
        results (dict): The results of the simulation (performance metrics).
        file_path (str): Path to store the raw results file.
    """
    with open(file_path, 'w') as f:
        json.dump(results, f, indent=4)
    print(f"Results saved to {file_path}")

