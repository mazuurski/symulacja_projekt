import json
import logging
import random
from queue import Queue
from tabulate import tabulate
from typing import List, Dict

import numpy as np

from src.models.employee import Employee
from src.models.student import Student

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)


class Simulation:
    """
    Main simulation class for managing the deanery system.
    """

    def __init__(self, config_path: str, verbose: bool = False) -> None:
        """
        Initialize the simulation using the configuration from a JSON file.

        :param config_path: Path to the configuration JSON file.
        :param verbose: If True, enables logging of events during simulation.
        """
        try:
            with open(config_path, "r") as config_file:
                self.config = json.load(config_file)
        except FileNotFoundError as e:
            logging.error(f"Configuration file not found: {e}")
            raise
        except json.JSONDecodeError as e:
            logging.error(f"Error decoding JSON from configuration file: {e}")
            raise
        except Exception as e:
            logging.error(f"Unexpected error while loading configuration: {e}")
            raise

        self.lambda_rate = self.config.get("lambda", 0) / 60  # Students per minute
        self.service_rate = self.config.get("mu", 0) / 60  # Service rate per minute
        self.num_servers = len(self.config.get("employees_config", []))
        self.opening_hours = self.config.get("opening_hours", 0)
        self.case_types = self.config.get("case_types", [])
        self.majors_distribution = self.config.get("majors_distribution", {})

        self.employees = self._generate_employees(self.config.get("employees_config", []))
        self.queue = Queue()  # Queue to hold waiting students
        self.time = 0  # Current simulation time
        self.num_in_queue = 0  # Current number of students in the queue
        self.finished_students: List[Student] = []  # List to store completed students
        self.queue_length_data = []  # For tracking queue length over time
        self.wait_times = []  # For tracking wait times
        self.verbose = verbose  # Logging toggle

        # Keep track of when employees become available
        self.employee_availability = [0] * self.num_servers

    @staticmethod
    def _generate_employees(employees_config: List[Dict]) -> List[Employee]:
        """
        Generate a list of Employee objects from configuration.

        :param employees_config: List of employee configurations.
        :return: List of Employee objects.
        """
        try:
            return [
                Employee(
                    employee_id=emp_config["id"],
                    case_types=emp_config["case_types"],
                    specializations=emp_config["case_types"]
                )
                for emp_config in employees_config
            ]
        except KeyError as e:
            logging.error(f"Missing key in employee configuration: {e}")
            raise
        except Exception as e:
            logging.error(f"Unexpected error while generating employees: {e}")
            raise

    def _generate_student(self, arrival_time: int) -> Student:
        """
        Generate a student with random attributes.

        :param arrival_time: Time of student arrival.
        :return: A Student object.
        """
        try:
            case_type = random.choices(self.case_types, k=1)[0]
            major = random.choices(
                list(self.majors_distribution.keys()),
                weights=list(self.majors_distribution.values()),
                k=1
            )[0]
            service_time = random.expovariate(1 / self.service_rate)

            return Student(
                student_id=len(self.finished_students) + 1,
                case_type=case_type,
                major=major,
                service_time=service_time,
                arrival_time=arrival_time,
            )
        except Exception as e:
            logging.error(f"Unexpected error while generating student: {e}")
            raise

    def log(self, message: str, level: str = "info") -> None:
        """
        Log a message if verbose mode is enabled.

        :param message: Message to log.
        :param level: Logging level ('info', 'warning', etc.).
        """
        if self.verbose:
            if level == "info":
                logging.info(message)
            elif level == "warning":
                logging.warning(message)

    def run(self):
        """
        Run the simulation using a continuous time approach.
        """
        try:
            self.log("Simulation started.", level="info")

            # Initialize simulation variables
            next_arrival = np.random.exponential(1 / self.lambda_rate)  # First student's arrival time
            next_service_time = np.inf  # No students being served initially
            opening_hours_in_minutes = self.opening_hours * 60

            while self.time < opening_hours_in_minutes:
                if next_arrival < next_service_time:  # Arrival happens before service ends
                    self.time = next_arrival
                    student = self._generate_student(self.time)

                    # Add the student to the queue
                    self.queue.put(student)

                    # Record the queue length at arrival (after adding the student)
                    student.queue_length_at_arrival = self.queue.qsize()
                    self.log(
                        f"Student {student.student_id} arrived at {self.time:.2f}. Queue length: {student.queue_length_at_arrival}.",
                        level="info")

                    # Update queue length data
                    self.queue_length_data.append(self.queue.qsize())

                    self.num_in_queue += 1

                    # Schedule the next arrival
                    next_arrival = self.time + np.random.exponential(1 / self.lambda_rate)

                    # Check if any employee is available
                    available_employee_time = min(self.employee_availability)
                    if self.time >= available_employee_time:  # Employee is available
                        # Start service for the next student
                        next_student = self.queue.get()
                        self.num_in_queue -= 1

                        # Record wait time for the student
                        self.wait_times.append(self.time - next_student.arrival_time)

                        # Assign service details
                        next_student.set_service_start_time(self.time)
                        service_end_time = self.time + next_student.service_time
                        next_student.set_service_end_time(service_end_time)

                        # Assign the student to the employee
                        employee_index = self.employee_availability.index(available_employee_time)
                        next_student.employee_id = employee_index + 1
                        self.employee_availability[employee_index] = service_end_time

                        self.finished_students.append(next_student)
                        self.log(
                            f"Student {next_student.student_id} started service at {next_student.service_start_time:.2f} "
                            f"and will finish at {next_student.service_end_time:.2f}.", level="info"
                        )

                else:  # Service ends before the next arrival
                    self.time = next_service_time

                    # Update the availability of the employee who finished serving
                    finished_employee_index = self.employee_availability.index(self.time)
                    self.employee_availability[finished_employee_index] = self.time

                    # Record queue length at this time
                    self.queue_length_data.append(self.queue.qsize())
                    self.log(f"Queue length updated: {self.queue.qsize()} students.", level="info")

                    # If queue is not empty, start serving the next student
                    if not self.queue.empty():
                        next_student = self.queue.get()
                        self.num_in_queue -= 1

                        # Service starts for the next student
                        next_student.set_service_start_time(self.time)
                        next_student.set_service_end_time(self.time + next_student.service_time)
                        next_student.employee_id = finished_employee_index + 1
                        self.finished_students.append(next_student)

                        # Update employee's availability
                        self.employee_availability[finished_employee_index] = next_student.service_end_time
                        self.log(
                            f"Student {next_student.student_id} started service at {next_student.service_start_time:.2f} "
                            f"and will finish at {next_student.service_end_time:.2f}.", level="info"
                        )

                        # Update next service time
                        next_service_time = next_student.service_end_time
                    else:
                        next_service_time = np.inf

            self.log("Simulation ended.", level="info")

        except Exception as e:
            logging.error(f"Unexpected error during simulation: {e}")
            raise

    def get_average_wait_time(self):
        """
        Get the average wait time for students in the simulation.
        """
        try:
            return np.mean(self.wait_times) if self.wait_times else 0
        except Exception as e:
            logging.error(f"Error calculating average wait time: {e}")
            raise

    def get_average_queue_length(self):
        """
        Get the average queue length over time.
        """
        try:
            return np.mean(self.queue_length_data) if self.queue_length_data else 0
        except Exception as e:
            logging.error(f"Error calculating average queue length: {e}")
            raise

    def get_average_service_time(self):
        """
        Get the average service time for students in the simulation.
        """
        try:
            return np.mean([student.service_time for student in self.finished_students]) if self.finished_students else 0
        except Exception as e:
            logging.error(f"Error calculating average service time: {e}")
            raise

    def report(self):
        """
        Generate a report of all students served during the simulation.
        """
        try:
            self.log("Generating simulation report.", level="info")

            table_data = []
            for student in self.finished_students:
                table_data.append([
                    student.student_id,
                    student.major,
                    student.case_type,
                    f"{student.arrival_time:.2f}",
                    f"{student.service_start_time:.2f}",
                    f"{student.service_end_time:.2f}",
                    f"{student.total_time_in_system:.2f}",
                    f"{student.waiting_time:.2f}",
                    student.employee_id,
                    student.queue_length_at_arrival
                ])

            headers = [
                "ID", "Major", "Case Type", "Arrival Time", "Service Start Time",
                "Service End Time", "Time of Service", "Waiting Time", "Employee ID", "Queue at Arrival"
            ]

            # Log the tabulated report
            self.log("\n" + tabulate(table_data, headers=headers, tablefmt="pretty"), level="info")
            # Log average statistics
            self.log(f"Average Wait Time: {self.get_average_wait_time():.2f} minutes", level="info")
            self.log(f"Average Service Time: {self.get_average_service_time():.2f} minutes", level="info")
            self.log(f"Average Queue Length: {self.get_average_queue_length():.2f}", level="info")

        except Exception as e:
            logging.error(f"Error generating report: {e}")
            raise
