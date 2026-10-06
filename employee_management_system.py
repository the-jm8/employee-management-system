class Employee:
    def __init__(self, employee_id, name, department, base_salary):
        self.employee_id = employee_id.strip()
        self.name = name.strip()
        self.department = department.strip()
        self.base_salary = base_salary


class EmployeeManagementSystem:
    def __init__(self):
        self.employees = {}

    def add_employee(self, employee_id, name, department, base_salary):
        employee_id = (employee_id or "").strip()
        name = (name or "").strip()
        department = (department or "").strip()

        if not employee_id:
            raise ValueError("Employee ID cannot be empty.")

        if not name:
            raise ValueError("Employee name cannot be empty.")

        if base_salary < 0:
            raise ValueError("Base salary cannot be negative.")

        if employee_id in self.employees:
            return False

        self.employees[employee_id] = Employee(
            employee_id,
            name,
            department,
            base_salary,
        )
        return True

    def remove_employee(self, employee_id):
        employee_id = (employee_id or "").strip()

        if employee_id in self.employees:
            del self.employees[employee_id]
            return True

        return False

    def process_payment(self, employee_id, hours, overtime_hours):
        if employee_id not in self.employees:
            raise KeyError(f"Employee with ID {employee_id} does not exist.")

        if hours < 0:
            raise ValueError("Hours cannot be negative.")

        if overtime_hours < 0:
            raise ValueError("Overtime hours cannot be negative.")

        employee = self.employees[employee_id]
        hourly_rate = employee.base_salary / 160
        overtime_pay = overtime_hours * hourly_rate * 1.5
        gross_pay = employee.base_salary + overtime_pay

        if employee.department.lower() == "management":
            gross_pay += gross_pay * 0.10

        tax_rate = 0.25 if gross_pay >= 5000 else 0.15
        tax = gross_pay * tax_rate
        return gross_pay - tax

    def generate_payroll_report(self):
        if not self.employees:
            return "No employees to report."

        report = [
            "PAYROLL REPORT",
            "====================",
        ]

        total_payroll = 0.0
        top_earner = None
        highest_net_pay = float("-inf")

        for employee in self.employees.values():
            net_pay = self.process_payment(employee.employee_id, 160, 0)

            report.extend(
                [
                    f"Employee ID: {employee.employee_id}",
                    f"Name: {employee.name}",
                    f"Department: {employee.department}",
                    f"Net Pay: {net_pay:.2f}",
                    "--------------------",
                ]
            )

            total_payroll += net_pay

            if net_pay > highest_net_pay:
                highest_net_pay = net_pay
                top_earner = employee

        average_net_pay = total_payroll / len(self.employees)
        report.append(f"Total Payroll: {total_payroll:.2f}")
        report.append(f"Average Net Pay: {average_net_pay:.2f}")

        if top_earner is not None:
            report.append(
                f"Top Earner: {top_earner.name} ({top_earner.employee_id}) - {highest_net_pay:.2f}"
            )
        else:
            report.append("Top Earner: N/A")

        return "\n".join(report)

    def get_employee_count(self):
        return len(self.employees)


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

        choice = input("Choose an option: ").strip()

        try:
            if choice == "1":
                employee_id = input("Employee ID: ").strip()
                name = input("Name: ").strip()
                department = input("Department: ").strip()
                base_salary = float(input("Base Salary: "))

                if system.add_employee(employee_id, name, department, base_salary):
                    print("Employee added successfully.")
                else:
                    print("Employee ID already exists.")

            elif choice == "2":
                employee_id = input("Employee ID to remove: ").strip()

                if system.remove_employee(employee_id):
                    print("Employee removed successfully.")
                else:
                    print("Employee ID does not exist.")

            elif choice == "3":
                employee_id = input("Employee ID: ").strip()
                hours = float(input("Hours worked: "))
                overtime_hours = float(input("Overtime hours: "))

                net_pay = system.process_payment(employee_id, hours, overtime_hours)
                print(f"Net Pay: {net_pay:.2f}")

            elif choice == "4":
                print(system.generate_payroll_report())

            elif choice == "5":
                print("Number of employees:", system.get_employee_count())

            elif choice == "6":
                print("Exiting system...")
                break

            else:
                print("Invalid option.")

        except (ValueError, KeyError) as error:
            print("Error:", error)


if __name__ == "__main__":
    main()
