from dataclasses import dataclass

@dataclass
class Employee:
    employee_id: int
    case_types: list[str]
    specializations: list[str]
    service_coefficient: float
    is_available: bool = True

    def can_handle(self, student):
        """
        Check if the employee can handle the given student.
        """
        return (student.major in self.specializations) and (student.case_type in self.case_types)
