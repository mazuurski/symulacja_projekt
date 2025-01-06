import json
import logging
import random

from typing import List

from src.models.deanery import Deanery
from src.models.employee import Employee
from src.models.student import Student


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        # logging.FileHandler("simulation.log"),
        logging.StreamHandler()
    ]
)


class Simulation:
    """
    Main simulation class for managing the deanery system.
    """

    def __init__(self, config_path: str) -> None:
        """
        Initialize the simulation using the configuration from a JSON file.

        :param config_path: Path to the configuration JSON file.
        """
        with open(config_path, "r") as config_file:
            self.config = json.load(config_file)

        self.num_students = self.config["num_students"]
        self.opening_hours = self.config["opening_hours"]
        self.case_types = self.config["case_types"]
        self.majors = self.config["majors"]
        self.service_time_range = tuple(self.config["service_time_range"])
        self.deanery = Deanery(self._generate_employees(self.config["employees_config"]))
        self.current_time = 0
        self.student_arrivals = self._generate_student_arrival_times()
        self.finished_students: List[Student] = []

    @staticmethod
    def _generate_employees(employees_config: List[dict]) -> List[Employee]:
        """
        Generate a list of employees based on the configuration.

        :param employees_config: List of dictionaries defining employee configurations.
        :return: List of Employee objects.
        """
        return [
            Employee(employee_id=config["employee_id"], specialization=config["specialization"])
            for config in employees_config
        ]

    def _generate_student_arrival_times(self) -> List[int]:
        """
        Generate random arrival times for students within the deanery's working hours.

        :return: List of arrival times (minutes from the start of the day).
        """
        return sorted(random.randint(0, self.opening_hours * 60) for _ in range(self.num_students))

    def _generate_student(self, arrival_time: int) -> Student:
        """
        Generate a new student with random attributes.

        :param arrival_time: Time the student arrives at the deanery.
        :return: A Student object.
        """
        return Student(
            student_id=len(self.finished_students) + len(self.deanery.queue) + 1,
            case_type=random.choice(self.case_types),
            major=random.choice(self.majors),
            service_time=random.randint(*self.service_time_range),  # Random service time
            arrival_time=arrival_time
        )

    def run(self) -> None:
        """
        Execute the simulation step by step until the deanery closes.
        """
        logging.info("Simulation starts.")
        for arrival_time in self.student_arrivals:
            # Advance time to the next student's arrival
            self.current_time = arrival_time

            # Generate a new student and add them to the queue
            new_student = self._generate_student(self.current_time)
            self.deanery.add_student(new_student)
            logging.info(f"Student {new_student.student_id} arrives at {self.current_time} minutes.")

            # Assign students to employees
            self.deanery.assign_students_to_employees()

            # Finish serving students who are done
            finished = self.deanery.finish_serving_students()
            self.finished_students.extend(finished)

        # Close the deanery and process the remaining queue
        self.deanery.close_deanery()
        # logging.info("Deanery is now closed. Finishing remaining students in the queue.")
        while not self.deanery.is_queue_empty():
            self.deanery.assign_students_to_employees()
            finished = self.deanery.finish_serving_students()
            self.finished_students.extend(finished)

        logging.info("Simulation ends.")

    def report(self) -> None:
        """
        Generate a report of the simulation results.
        """
        # logging.info("Generating simulation report.")
        total_students_served = len(self.finished_students)
        average_service_time = (
            sum(student.service_time for student in self.finished_students) / total_students_served
            if total_students_served > 0 else 0
        )
        remaining_students = len(self.deanery.queue)

        logging.info(f"Total students served: {total_students_served}")
        logging.info(f"Average service time: {average_service_time:.2f} minutes.")
        logging.info(f"Remaining students in queue: {remaining_students}")
