from typing import Optional
from dataclasses import dataclass

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
    start_service_time: Optional[float] = None  # Time when the student starts being served
    end_service_time: Optional[float] = None  # Time when the service for the student ends

    def __str__(self) -> str:
        """
        Returns a string representation of the student.

        Returns:
            str: Student details.
        """
        return (f"Student({self.student_id}, Case: {self.case_type}, Program: {self.major}, "
                f"Service Time: {self.service_time}, Arrival Time: {self.arrival_time})")

    def set_start_service_time(self, time: float) -> None:
        """
        Sets the time when the student starts being served.

        Args:
            time (float): The time when the service begins.
        """
        self.start_service_time = time

    def set_end_service_time(self, time: float) -> None:
        """
        Sets the time when the student's service is completed.

        Args:
            time (float): The time when the service ends.
        """
        self.end_service_time = time

    @property
    def waiting_time(self) -> float:
        """
        Calculates the waiting time for the student before service starts.

        Returns:
            float: Waiting time in the queue.
        """
        if self.start_service_time is not None:
            return self.start_service_time - self.arrival_time
        return 0.0

    @property
    def total_time_in_system(self) -> float:
        """
        Calculates the total time the student spends in the system.

        Returns:
            float: Total time in the system (waiting + service).
        """
        if self.end_service_time is not None:
            return self.end_service_time - self.arrival_time
        return 0.0
