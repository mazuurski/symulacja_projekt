import unittest

from src.models.student import Student
from src.models.employee import Employee


class TestStudentModel(unittest.TestCase):
    def setUp(self):
        # Przed każdym testem tworzymy instancję studenta
        self.student = Student(
            student_id=1,
            case_type="documents",
            major="engineering",
            service_time=15.0,
            arrival_time=10.0
        )

    def test_set_service_start_time(self):
        # Testowanie funkcji set_service_start_time
        self.student.set_service_start_time(20.0)
        self.assertEqual(self.student.service_start_time, 20.0)

    def test_set_service_end_time(self):
        # Testowanie funkcji set_service_end_time
        self.student.set_service_end_time(35.0)
        self.assertEqual(self.student.service_end_time, 35.0)

    def test_waiting_time(self):
        # Testowanie właściwości waiting_time
        self.student.set_service_start_time(20.0)
        self.assertEqual(self.student.waiting_time, 10.0)  # 20.0 - 10.0 = 10.0

    def test_total_time_in_system(self):
        # Testowanie właściwości total_time_in_system
        self.student.set_service_start_time(20.0)
        self.student.set_service_end_time(35.0)
        self.assertEqual(self.student.total_time_in_system, 25.0)  # 35.0 - 10.0 = 25.0


class TestEmployeeModel(unittest.TestCase):
    def setUp(self):
        # Przed każdym testem tworzymy instancję pracownika
        self.employee = Employee(
            employee_id=1,
            case_types=["documents", "applications"],
            specializations=["engineering", "IT"]
        )

    def test_can_handle_student_with_matching_case_type_and_major(self):
        student = Student(
            student_id=1,
            case_type="documents",
            major="engineering",
            service_time=15.0,
            arrival_time=10.0
        )
        self.assertTrue(self.employee.can_handle(student))

    def test_can_handle_student_with_non_matching_case_type(self):
        student = Student(
            student_id=1,
            case_type="information",  # Nie obsługuje typu 'information'
            major="engineering",
            service_time=15.0,
            arrival_time=10.0
        )
        self.assertFalse(self.employee.can_handle(student))

    def test_can_handle_student_with_non_matching_major(self):
        student = Student(
            student_id=1,
            case_type="documents",
            major="biology",  # Pracownik obsługuje tylko 'engineering' i 'IT'
            service_time=15.0,
            arrival_time=10.0
        )
        self.assertFalse(self.employee.can_handle(student))

    def test_employee_availability(self):
        # Testowanie dostępności pracownika
        self.employee.is_available = False  # Pracownik jest niedostępny
        self.assertFalse(self.employee.is_available)
        self.employee.is_available = True  # Pracownik staje się dostępny
        self.assertTrue(self.employee.is_available)


if __name__ == '__main__':
    unittest.main()
