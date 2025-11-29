from fastapi import FastAPI
from pydantic import BaseModel

class User(BaseModel):
    pin: int
    balance: float

# In-memory user storage
users = {
   "mehwish":{"pin":7777, "balance":10000},
   "Aabis":{"pin":6666, "balance":7000},
   "Adeeba":{"pin":5555,"balance":15000}
}

app = FastAPI()

@app.post("/bank-transfer")
def bank_transfer(sender_name: str, sender_pin: int, recipient_name: str, amount: float):
    if sender_name not in users or users[sender_name]["pin"] != sender_pin:
        return {"message": "Transfer failed", "error": "Authentication failed for sender"}

    if recipient_name not in users:
        return {"message": "Transfer failed", "error": "Recipient not found"}

    if amount <= 0:
        return {"message": "Transfer failed", "error": "Amount must be positive"}

    if users[sender_name]["balance"] < amount:
        return {"message": "Transfer failed", "error": "Insufficient funds"}

    users[sender_name]["balance"] -= amount
    users[recipient_name]["balance"] += amount

    return {
        "message": "Transfer successful",
        "sender_updated_balance": users[sender_name]["balance"],
        "recipient_updated_balance": users[recipient_name]["balance"],
    }


@app.post("/deposit")
def deposit_funds(name: str, amount: float):
    if name not in users:
        return {"message": "Deposit failed", "error": "User not found"}
    
    if amount <= 0:
        return {"message": "Deposit failed", "error": "Amount must be positive"}

    users[name]["balance"] += amount
    return {"bank_balance": users[name]["balance"]}

@app.post("/authenticate")
def authenticate_user(name: str, pin_number: int):
    if name in users and users[name]["pin"] == pin_number:
        return {"name": name, "bank_balance": users[name]["balance"]}
    return {"message": "Authentication failed", "error": "Invalid credentials"}

@app.get("/")
def read_root():
    return {"message": "Bank API running"}


