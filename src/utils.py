import logging
import os

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def plot_performance(csv_file_path: Path, output_dir: Path):
    """
    Plots performance comparisons (average_waiting_time and average_service_time) for all setups.

    :param csv_file_path: Path to the CSV file containing simulation results.
    :param output_dir: Directory to save the plot images.
    """
    # Load results from the CSV file
    try:
        results = pd.read_csv(csv_file_path, encoding='utf-8', skipinitialspace=True)
        logging.info(f"Successfully loaded CSV file: {csv_file_path}")
    except FileNotFoundError:
        logging.error(f"CSV file not found at {csv_file_path}")
        return
    except pd.errors.EmptyDataError:
        logging.error(f"CSV file at {csv_file_path} is empty or invalid.")
        return
    except Exception as e:
        logging.error(f"Unexpected error while loading CSV file: {e}")
        return

    # Create output directory if it doesn't exist
    try:
        os.makedirs(output_dir, exist_ok=True)
        logging.info(f"Output directory ensured: {output_dir}")
    except Exception as e:
        logging.error(f"Failed to create output directory: {e}")
        return

    # Extract unique setups and iterations
    setups = results['name'].unique()
    logging.info(f"Found {len(setups)} setups in the CSV file.")

    try:
        # Compare average waiting time
        plt.figure(figsize=(12, 8))
        for setup in setups:
            setup_results = results[results['name'] == setup]
            plt.plot(
                setup_results['iteration'],
                setup_results['average_waiting_time'],
                marker='o', label=f'{setup} - Avg Waiting Time'
            )
        plt.title("Comparison of Average Waiting Time Across Setups")
        plt.xlabel("Iteration")
        plt.ylabel("Average Waiting Time (minutes)")
        plt.legend()
        plt.grid(True)
        plot_file = os.path.join(output_dir, "comparison_average_waiting_time.png")
        plt.savefig(plot_file)
        logging.info(f"Saved plot for average waiting time comparison to {plot_file}")
        plt.close()

        # Compare average service time
        plt.figure(figsize=(12, 8))
        for setup in setups:
            setup_results = results[results['name'] == setup]
            plt.plot(
                setup_results['iteration'],
                setup_results['average_service_time'],
                marker='s', label=f'{setup} - Avg Service Time'
            )
        plt.title("Comparison of Average Service Time Across Setups")
        plt.xlabel("Iteration")
        plt.ylabel("Average Service Time (minutes)")
        plt.legend()
        plt.grid(True)
        plot_file = os.path.join(output_dir, "comparison_average_service_time.png")
        plt.savefig(plot_file)
        logging.info(f"Saved plot for average service time comparison to {plot_file}")
        plt.close()
    except Exception as e:
        logging.error(f"Error while plotting comparisons: {e}")

