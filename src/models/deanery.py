from typing import List
from collections import deque

from src.models.student import Student
from src.models.employee import Employee


class Deanery:
    """
    Represents the deanery, which manages employees and the queue of students.
    """

    def __init__(self, employees: List[Employee]) -> None:
        """
        Initialize the deanery with a list of employees and an empty student queue.

        :param employees: List of Employee objects available in the deanery.
        """
        self.employees = employees  # List of employees
        self.queue = deque()  # Queue of students
        self.closed = False  # Whether the deanery is closed for the day

    def __str__(self) -> str:
        """
        String representation of the deanery.
        """
        employee_statuses = "\n".join(str(emp) for emp in self.employees)
        queue_status = ", ".join(str(student.employee_id) for student in self.queue)
        queue_status = queue_status if queue_status else "No students in the queue"
        return f"Deanery:\nEmployees:\n{employee_statuses}\nQueue: {queue_status}"

    def add_student(self, student: Student) -> None:
        """
        Add a student to the queue.

        :param student: The student to be added to the queue.
        """
        if self.closed:
            raise ValueError("The deanery is closed. No more students can be added.")
        self.queue.append(student)

    def assign_students_to_employees(self) -> None:
        """
        Assign students in the queue to available employees, following FIFO rules.
        """
        for employee in self.employees:
            if not employee.is_available or not self.queue:
                continue  # Skip busy employees or stop if no students are waiting

            student = self.queue.popleft()  # Get the next student from the queue
            employee.start_serving(student)

    def finish_serving_students(self) -> List[Student]:
        """
        Finish serving all students currently being attended to by employees.

        :return: List of students who have completed their service.
        """
        finished_students = []
        for employee in self.employees:
            if not employee.is_available:  # If the employee is busy
                finished_students.append(employee.finish_serving())
        return finished_students

    def close_deanery(self) -> None:
        """
        Close the deanery, preventing new students from entering the queue.
        """
        self.closed = True

    def is_queue_empty(self) -> bool:
        """
        Check if the student queue is empty.

        :return: True if the queue is empty, otherwise False.
        """
        return len(self.queue) == 0
