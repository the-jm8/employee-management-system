class Employee:
    def __init__(self, employee_id, name, department, base_salary):
        self.employee_id = employee_id
        self.name = name
        self.department = department
        self.base_salary = base_salary


class EmployeeManagementSystem:

    def __init__(self):
        self.employees = {}

    # FR1 + FR2: Add employee
    def add_employee(self, employee_id, name, department, base_salary):

        if employee_id is None or employee_id.strip() == "":
            raise ValueError("Employee ID cannot be empty.")

        if name is None or name.strip() == "":
            raise ValueError("Employee name cannot be empty.")

        if base_salary < 0:
            raise ValueError("Base salary cannot be negative.")

        # Duplicate ID
        if employee_id in self.employees:
            return False

        employee = Employee(
            employee_id,
            name,
            department,
            base_salary
        )

        self.employees[employee_id] = employee

        return True

    # FR3: Remove employee
    def remove_employee(self, employee_id):

        if employee_id in self.employees:
            del self.employees[employee_id]
            return True

        return False

    # FR4 + FR5: Process payment
    def process_payment(self, employee_id, hours, overtime_hours):

        # Employee must exist
        if employee_id not in self.employees:
            raise KeyError(
                f"Employee with ID {employee_id} does not exist."
            )

        # Hours cannot be negative
        if hours < 0:
            raise ValueError("Hours cannot be negative.")

        # Overtime cannot be negative
        if overtime_hours < 0:
            raise ValueError(
                "Overtime hours cannot be negative."
            )

        employee = self.employees[employee_id]

        # Standard working hours = 160
        hourly_rate = employee.base_salary / 160

        # Overtime paid at 1.5x hourly rate
        overtime_pay = (
            overtime_hours * hourly_rate * 1.5
        )

        # Calculate gross pay
        gross_pay = employee.base_salary + overtime_pay

        # Management gets 10% bonus
        if employee.department.lower() == "management":
            bonus = gross_pay * 0.10
            gross_pay += bonus

        # Tax rate
        if gross_pay >= 5000:
            tax_rate = 0.25
        else:
            tax_rate = 0.15

        tax = gross_pay * tax_rate

        # Net pay
        net_pay = gross_pay - tax

        return net_pay

    # FR6: Generate payroll report
    def generate_payroll_report(self):

        if not self.employees:
            return "No employees to report."

        report = []
        report.append("PAYROLL REPORT")
        report.append("====================")

        total_payroll = 0
        top_earner = None
        highest_net_pay = float("-inf")

        for employee in self.employees.values():

            # Regular 160 hours and no overtime
            net_pay = self.process_payment(
                employee.employee_id,
                160,
                0
            )

            report.append(
                f"Employee ID: {employee.employee_id}"
            )

            report.append(
                f"Name: {employee.name}"
            )

            report.append(
                f"Department: {employee.department}"
            )

            report.append(
                f"Net Pay: {net_pay:.2f}"
            )

            report.append("--------------------")

            total_payroll += net_pay

            if net_pay > highest_net_pay:
                highest_net_pay = net_pay
                top_earner = employee

        average_net_pay = (
            total_payroll / len(self.employees)
        )

        report.append(
            f"Total Payroll: {total_payroll:.2f}"
        )

        report.append(
            f"Average Net Pay: {average_net_pay:.2f}"
        )

        report.append(
            f"Top Earner: {top_earner.name} "
            f"({top_earner.employee_id}) - "
            f"{highest_net_pay:.2f}"
        )

        return "\n".join(report)

    # FR7: Employee count
    def get_employee_count(self):
        return len(self.employees)


# ============================================================
# Console Menu
# ============================================================

def main():

    system = EmployeeManagementSystem()

    while True:

        print("\n===== Employee Management System =====")
        print("1. Add Employee")
        print("2. Remove Employee")
        print("3. Process Payment")
        print("4. Generate Payroll Report")
        print("5. Employee Count")
        print("6. Exit")

        choice = input("Choose an option: ")

        try:

            if choice == "1":

                employee_id = input("Employee ID: ")
                name = input("Name: ")
                department = input("Department: ")
                base_salary = float(
                    input("Base Salary: ")
                )

                result = system.add_employee(
                    employee_id,
                    name,
                    department,
                    base_salary
                )

                if result:
                    print("Employee added successfully.")
                else:
                    print("Employee ID already exists.")

            elif choice == "2":

                employee_id = input(
                    "Employee ID to remove: "
                )

                result = system.remove_employee(
                    employee_id
                )

                if result:
                    print("Employee removed successfully.")
                else:
                    print("Employee ID does not exist.")

            elif choice == "3":

                employee_id = input("Employee ID: ")

                hours = float(
                    input("Hours worked: ")
                )

                overtime_hours = float(
                    input("Overtime hours: ")
                )

                net_pay = system.process_payment(
                    employee_id,
                    hours,
                    overtime_hours
                )

                print(f"Net Pay: {net_pay:.2f}")

            elif choice == "4":

                print(
                    system.generate_payroll_report()
                )

            elif choice == "5":

                print(
                    "Number of employees:",
                    system.get_employee_count()
                )

            elif choice == "6":

                print("Exiting system...")
                break

            else:
                print("Invalid option.")

        except (ValueError, KeyError) as error:
            print("Error:", error)


if __name__ == "__main__":
    main()
