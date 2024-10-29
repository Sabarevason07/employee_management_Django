import os
from faker import Faker
from random import *
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE','Django_Project.settings')
import django
django.setup()

from Admin_Panel.models import Emp_Data  


faker = Faker()

for _ in range(20):
    Emp_Data.objects.create(
        EmpId=randint(100, 9999),
        Email=faker.unique.email(),
        FirstName=faker.first_name(),
        LastName=faker.last_name(),
        Age=faker.random_int(min=18, max=65),
        Department=faker.job(),
        Address=faker.address(),
        ProfilePicture=f"https://picsum.photos/200?random={randint(1, 1000)}",  
        CTC=Decimal(faker.random_number(digits=5)),
        GrossSalary=Decimal(faker.random_number(digits=5))
    )

print("100 records created successfully!")
