from dataclasses import dataclass
from typing import Optional


@dataclass
class Employee:
    """
    Represents an employee in the deanery.
    """
    employee_id: int  # Unique identifier for the employee
    specialization: Optional[
        str] = None  # Type of cases the employee specializes in (e.g., "documents", "applications")
    is_available: bool = True  # Availability status of the employee
    current_student: Optional["Student"] = None  # The student currently being served (None if idle)

    def __str__(self) -> str:
        """
        String representation of the employee.
        """
        status = "Available" if self.is_available else f"Serving student {self.current_student.employee_id}"
        specialization = self.specialization if self.specialization else "General"
        return f"Employee {self.employee_id} | Specialization: {specialization} | Status: {status}"

    def start_serving(self, student: "Student") -> None:
        """
        Assign a student to this employee for processing.

        :param student: The student to be served
        """
        if not self.is_available:
            raise ValueError(f"Employee {self.employee_id} is currently busy and cannot serve another student.")

        self.current_student = student
        self.is_available = False

    def finish_serving(self) -> Optional["Student"]:
        """
        Finish serving the current student and make the employee available again.

        :return: The student who was served, or None if no student was being served
        """
        if self.is_available:
            raise ValueError(f"Employee {self.employee_id} is already available and not serving any student.")

        served_student = self.current_student
        self.current_student = None
        self.is_available = True
        return served_student
