from src.simulation import Simulation

if __name__ == "__main__":
    # Load the simulation configuration
    CONFIG_PATH = "config.json"
    simulation = Simulation(config_path=CONFIG_PATH)
    simulation.run()
    simulation.report()
