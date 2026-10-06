import unittest

from employee_management_system import EmployeeManagementSystem


class TestEmployeeManagementSystem(unittest.TestCase):

    # --------------------------------------------------------
    # BB-01
    # Add a valid employee
    # --------------------------------------------------------
    def test_BB01_add_valid_employee(self):

        system = EmployeeManagementSystem()

        result = system.add_employee(
            "E001",
            "Alice Uwase",
            "Engineering",
            3000
        )

        self.assertTrue(result)
        self.assertEqual(
            system.get_employee_count(),
            1
        )

    # --------------------------------------------------------
    # BB-02
    # Duplicate employee ID
    # --------------------------------------------------------
    def test_BB02_duplicate_employee_id(self):

        system = EmployeeManagementSystem()

        system.add_employee(
            "E001",
            "Alice Uwase",
            "Engineering",
            3000
        )

        result = system.add_employee(
            "E001",
            "Bob",
            "Engineering",
            4000
        )

        self.assertFalse(result)
        self.assertEqual(
            system.get_employee_count(),
            1
        )

    # --------------------------------------------------------
    # BB-03
    # Empty employee ID
    # --------------------------------------------------------
    def test_BB03_empty_employee_id(self):

        system = EmployeeManagementSystem()

        with self.assertRaises(ValueError):
            system.add_employee(
                "",
                "Alice",
                "Engineering",
                3000
            )

    # --------------------------------------------------------
    # BB-04
    # Negative salary
    # --------------------------------------------------------
    def test_BB04_negative_salary(self):

        system = EmployeeManagementSystem()

        with self.assertRaises(ValueError):
            system.add_employee(
                "E001",
                "Alice",
                "Engineering",
                -100
            )

    # --------------------------------------------------------
    # BB-05
    # Remove existing employee
    # --------------------------------------------------------
    def test_BB05_remove_existing_employee(self):

        system = EmployeeManagementSystem()

        system.add_employee(
            "E001",
            "Alice",
            "Engineering",
            3000
        )

        result = system.remove_employee("E001")

        self.assertTrue(result)
        self.assertEqual(
            system.get_employee_count(),
            0
        )

    # --------------------------------------------------------
    # BB-06
    # Remove non-existing employee
    # --------------------------------------------------------
    def test_BB06_remove_non_existing_employee(self):

        system = EmployeeManagementSystem()

        result = system.remove_employee("E999")

        self.assertFalse(result)

    # --------------------------------------------------------
    # BB-07
    # Normal employee below tax threshold
    # --------------------------------------------------------
    def test_BB07_normal_employee_payment(self):

        system = EmployeeManagementSystem()

        system.add_employee(
            "E001",
            "Alice",
            "Engineering",
            3000
        )

        net_pay = system.process_payment(
            "E001",
            160,
            0
        )

        # Gross = 3000
        # Tax = 15% = 450
        # Net = 2550
        self.assertAlmostEqual(
            net_pay,
            2550.00,
            places=2
        )

    # --------------------------------------------------------
    # BB-08
    # Management employee at high-income threshold
    # --------------------------------------------------------
    def test_BB08_management_high_income(self):

        system = EmployeeManagementSystem()

        system.add_employee(
            "E001",
            "Alice",
            "Management",
            6000
        )

        net_pay = system.process_payment(
            "E001",
            160,
            0
        )

        # Salary = 6000
        # Bonus = 600
        # Gross = 6600
        # Tax = 25% = 1650
        # Net = 4950
        self.assertAlmostEqual(
            net_pay,
            4950.00,
            places=2
        )

    # --------------------------------------------------------
    # BB-09
    # Negative hours
    # --------------------------------------------------------
    def test_BB09_negative_hours(self):

        system = EmployeeManagementSystem()

        system.add_employee(
            "E001",
            "Alice",
            "Engineering",
            3000
        )

        with self.assertRaises(ValueError):
            system.process_payment(
                "E001",
                -10,
                0
            )

    # --------------------------------------------------------
    # BB-10
    # Non-existing employee payment
    # --------------------------------------------------------
    def test_BB10_non_existing_employee_payment(self):

        system = EmployeeManagementSystem()

        with self.assertRaises(KeyError):
            system.process_payment(
                "E999",
                160,
                0
            )

    # --------------------------------------------------------
    # BB-11
    # Generate payroll report
    # --------------------------------------------------------
    def test_BB11_generate_payroll_report(self):

        system = EmployeeManagementSystem()

        system.add_employee(
            "E001",
            "Alice",
            "Engineering",
            3000
        )

        system.add_employee(
            "E002",
            "Bob",
            "Management",
            6000
        )

        system.process_payment(
            "E001",
            160,
            0
        )

        system.process_payment(
            "E002",
            160,
            0
        )

        report = system.generate_payroll_report()

        self.assertIn("Alice", report)
        self.assertIn("Bob", report)
        self.assertIn(
            "Total Payroll",
            report
        )
        self.assertIn(
            "Average Net Pay",
            report
        )
        self.assertIn(
            "Top Earner",
            report
        )

    # --------------------------------------------------------
    # BB-12
    # Empty payroll report
    # --------------------------------------------------------
    def test_BB12_empty_payroll_report(self):

        system = EmployeeManagementSystem()

        report = system.generate_payroll_report()

        self.assertEqual(
            report,
            "No employees to report."
        )


if __name__ == "__main__":
    unittest.main()
