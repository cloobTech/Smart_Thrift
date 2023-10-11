from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import user, user_profile, contribution, loan, loan_out, loan_profile, loan_refund, interest, auth

app = FastAPI()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,  # Allow sending cookies in cross-origin requests
    # Allow all HTTP methods, you can specify specific methods if needed
    allow_methods=["*"],
    # Allow all headers, you can specify specific headers if needed
    allow_headers=["*"],
)


app.include_router(user.router)
app.include_router(user_profile.router)
app.include_router(contribution.router)
app.include_router(loan.router)
app.include_router(loan_out.router)
app.include_router(loan_profile.router)
app.include_router(loan_refund.router)
app.include_router(loan_refund.router)
app.include_router(interest.router)
app.include_router(auth.router)


@app.get("/")
def read_root():
    return {"Smart Thrift": "A smarter way to save..."}
