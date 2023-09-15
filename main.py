#!/usr/bin/python3
from models import base_model, loan_out, user, contribution
from datetime import datetime
from utils import hash_password


dict1 = {
    "first_name": "ola",
    "last_name": "bello",
    "is_member": True,
    "amount": 50000
}
dict2 = {
    "first_name": "ola",
    "last_name": "bello",
    "is_member": False,
    "amount": 50000
}


loan1 =  loan_out.LoanOut(**dict1)
loan2 =  loan_out.LoanOut(**dict2)

print(loan1.to_dict())
print(loan2.to_dict())