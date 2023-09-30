from fastapi import FastAPI, APIRouter, Depends
from typing import Union
from .routes import user, user_profile, contribution, loan, loan_out, loan_profile, loan_refund, interest

app = FastAPI()

app.include_router(user.router)
app.include_router(user_profile.router)
app.include_router(contribution.router)
app.include_router(loan.router)
app.include_router(loan_out.router)
app.include_router(loan_profile.router)
app.include_router(loan_refund.router)
app.include_router(loan_refund.router)
app.include_router(interest.router)


@app.get("/")
def read_root():
    return {"Smart Thrift": "A smarter way to save..."}
