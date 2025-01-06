from dataclasses import dataclass
from typing import Optional

@dataclass
class Student:
    """
    Represents a student entering the system.

    Attributes:
        student_id (int): Unique identifier for the student.
        case_type (str): Type of case (e.g., 'documents', 'applications', 'information').
        major (str): Student's study program (e.g., 'engineering', 'IT', 'cybersecurity').
        service_time (float): The time required to process the student's case.
        arrival_time (float): The time when the student arrives at the office.
    """
    student_id: int
    case_type: str
    major: str
    service_time: float
    arrival_time: float
    service_start_time: Optional[float] = None  # Time when the student starts being served
    service_end_time: Optional[float] = None  # Time when the service for the student ends
    queue_length_at_arrival: Optional[int] = None  # Queue length when the student arrives
    employee_id: Optional[int] = None  # ID of the employee serving the student

    def set_service_start_time(self, time: float) -> None:
        """
        Sets the time when the student starts being served.

        Args:
            time (float): The time when the service begins.
        """
        self.service_start_time = time

    def set_service_end_time(self, time: float) -> None:
        """
        Sets the time when the student's service is completed.

        Args:
            time (float): The time when the service ends.
        """
        self.service_end_time = time

    @property
    def waiting_time(self) -> float:
        """
        Calculates the waiting time for the student before service starts.

        Returns:
            float: Waiting time in the queue.
        """
        if self.service_start_time is not None:
            return self.service_start_time - self.arrival_time
        return 0.0

    @property
    def total_time_in_system(self) -> float:
        """
        Calculates the total time the student spends in the system.

        Returns:
            float: Total time in the system (waiting + service).
        """
        if self.service_end_time is not None:
            return self.service_end_time - self.arrival_time
        return 0.0
