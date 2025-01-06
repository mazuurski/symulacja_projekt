import json
import unittest
from io import StringIO
from unittest.mock import patch, MagicMock

from src.simulation import Simulation
from src.models.student import Student


class TestSimulation(unittest.TestCase):
    @patch('src.simulation.random.expovariate')
    @patch('src.simulation.random.choices')
    @patch('builtins.open', new_callable=MagicMock)  # Mock open function to prevent FileNotFoundError
    def setUp(self, mock_open, mock_choices, mock_expovariate):
        # Mocking random.choices and random.expovariate
        # This ensures we have control over random values, making the tests deterministic

        # Mock the random.choices function to always return a predefined case type ("documents")
        mock_choices.side_effect = lambda population, weights=None, k=1: ['documents']  # Case type
        # Mock the random.expovariate function to return a fixed service time (5.0)
        mock_expovariate.return_value = 5.0  # Service time

        # Mock configuration for the simulation (must be valid JSON)
        self.config = {
            "lambda": 10,  # Students per hour
            "mu": 15,  # Service rate per hour
            "employees_config": [
                {"id": 1, "case_types": ["documents"]},
                {"id": 2, "case_types": ["applications"]}
            ],
            "opening_hours": 8,  # 8 hours of operation
            "case_types": ["documents", "applications"],
            "majors_distribution": {"engineering": 0.5, "IT": 0.5}
        }

        # Convert the config dictionary to a valid JSON string
        mock_open.return_value.__enter__.return_value.read.return_value = json.dumps(self.config)

        # Create the simulation instance with the mocked config path (empty string here)
        self.simulation = Simulation(config_path='', verbose=False)

        # Capturing the logs to test later
        self.log_output = StringIO()
        self.simulation.log = MagicMock(side_effect=lambda msg, level="info": self.log_output.write(f"{msg}\n"))

    @patch('src.simulation.Queue.put')
    def test_generate_student(self):
        # Testing student generation
        self.simulation._generate_student(arrival_time=10)

        # Check if the student is generated with correct values
        self.assertEqual(len(self.simulation.finished_students), 0)  # The student should not be handled yet
        student = self.simulation.queue.get()
        self.assertEqual(student.case_type, "documents")  # Student's case type should be "documents"
        self.assertEqual(student.service_time, 5.0)  # Service time should be 5.0
        self.assertEqual(student.major, "engineering")  # Student's major should be "engineering"

    def test_simulation_run(self):
        # Testing if the simulation runs correctly
        with patch('src.simulation.Simulation._generate_student') as mock_generate_student:
            # Mocking student generation to return the same student every time
            mock_generate_student.return_value = Student(
                student_id=1, case_type="documents", major="engineering", service_time=5.0, arrival_time=10.0)

            self.simulation.run()

            # After running the simulation, there should be one finished student
            self.assertEqual(len(self.simulation.finished_students), 1)

    @patch('src.simulation.tabulate')
    def test_report_generation(self, mock_tabulate):
        # Testing the generation of the report
        self.simulation.finished_students = [
            Student(
                student_id=1, case_type="documents", major="engineering", service_time=5.0, arrival_time=10.0,
                service_start_time=15.0, service_end_time=20.0, employee_id=1, queue_length_at_arrival=0
            )
        ]

        # Mocking the tabulate function to prevent printing large tables
        mock_tabulate.return_value = "Mocked Table"

        # Run the report
        report = self.simulation.report()

        # Check if the report contains "ID", "Major", and other required data
        self.assertIn("ID", report)  # Checking if the report contains "ID"
        self.assertIn("Major", report)  # Checking if the report contains "Major"
        self.assertIn("documents", report.lower())  # Case type should be present

    def test_employee_assignment(self):
        # Testing if the student is correctly assigned to an employee
        student = Student(
            student_id=1, case_type="documents", major="engineering", service_time=5.0, arrival_time=10.0)

        # Mock the employees' availability and simulate the assignment
        self.simulation.employee_availability = [0, float('inf')]  # Mocking the availability of two employees
        self.simulation.queue.put(student)

        # Run the simulation
        self.simulation.run()

        # After running the simulation, check if the student is assigned to the correct employee
        self.assertEqual(student.employee_id, 1)  # The student should be assigned to employee 1

    @patch('src.simulation.Simulation.log')
    def test_logging(self, mock_log):
        # Testing if the logging function works as expected
        self.simulation.log("Test message", level="info")
        mock_log.assert_called_with("Test message", level="info")  # Check if log was called with the expected message


# Run the test cases
if __name__ == '__main__':
    unittest.main()
