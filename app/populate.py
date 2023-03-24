import random
import sqlite3
from datetime import datetime
from pathlib import Path
from faker import Faker
from faker.providers import BaseProvider


BASE_DIR = Path(__file__).parent.parent.resolve()


class EmployeeProvider(BaseProvider):
    __provider__ = "department"
    departments = [
        'Asset Management', 'Board of Directors', 'Business Development',
        'Corporate Communications', 'Creative Services',
        'Customer Service / Customer Experience', 'Engineering',
        'Finance / Accounting', 'General Management', 'Human Resources',
        'Information Technology / Technology', 'Investor Relations', 'Legal',
        'Marketing', 'Operations', 'Product Management', 'Production',
        'Project Management Office', 'Purchasing / Sourcing',
        'Quality Assurance', 'Risk Management', 'Sales',
        'Strategic Initiatives & Programs', 'Technology'
    ]

    def department(self):
        return self.random_element(self.departments)

    @staticmethod
    def salary():
        return random.randint(0, 100000)


if __name__ == '__main__':
    fake = Faker()
    fake.add_provider(EmployeeProvider)
    fake_data = list()
    for _ in range(100_000):
        fake_data.append((
            fake.name(),
            fake.department(),
            fake.salary(),
            fake.date_time_between(
                datetime(2020, 1, 1), datetime(2023, 3, 24)
            )
        ))

    conn = sqlite3.connect(f'{BASE_DIR / "empls.db"}')
    cur = conn.cursor()
    cur.executemany(
        "INSERT INTO employees (name, department, salary, hire_date) "
        "VALUES(?, ?, ?, ?)",
        fake_data
    )
    res = cur.execute("SELECT count(*) FROM employees")
    print(res.fetchone())
    conn.commit()
    conn.close()
