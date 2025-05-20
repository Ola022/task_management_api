from fastapi import status
from sqlalchemy.orm import Session
from db.models import DbTransaction, DbUser
from routers.schemas import Transaction
import datetime

class AccountController:
    
    def __init__(self, db: Session, user_id: int):
        self.db = db
        self.user_info = db.query(DbUser).filter(DbUser.id == user_id).first()
        
        if not self.user_info:
            self.response_error("User with this ID does not exist", status.HTTP_404_NOT_FOUND)

    def response_success(self, message: str, data: dict = {}):
        """Helper to structure success responses."""
        return {
            "message": "Success",
            "status_code": 200,
            "data": {**data, "message": message},
        }

    def response_error(self, error: str, status_code: int):
        """Helper to structure error responses."""
        return {
            "message": "Failed",
            "status_code": status_code,
            "data": {"error": error},
        }

    def check_balance(self):
        """Returns the current balance."""
        return self.response_success("Balance fetched successfully", {
            "balance": self.user_info.money,
        })
        
    def save_transaction(self, transaction_type: str, money: int, to: str ):
        new_transaction = DbTransaction(            
            money = money, #request.money,
            to = to, #request.to,
            transaction_type = transaction_type,
            timestamp = datetime.datetime.now(),
            user_id = self.user_info.id            
        )
        self.db.add(new_transaction)
        self.db.commit()
        self.db.refresh(new_transaction)
        return new_transaction
       
    
    def transfer(self, amount: int, recipient_account_number: int):
        """Transfers money to another user's account."""
        if amount <= 0:
            return self.response_error(
                "Transfer amount must be greater than zero", status.HTTP_400_BAD_REQUEST
            )
        
        recipient = self.db.query(DbUser).filter(DbUser.account_number == recipient_account_number).first()
        if not recipient:
            return self.response_error(
                "Recipient account does not exist", status.HTTP_404_NOT_FOUND
            )

        if self.user_info.money < amount:
            return self.response_error(
                "Insufficient balance for transfer", status.HTTP_400_BAD_REQUEST
            )

        # Deduct amount from sender and add to recipient
        self.user_info.money -= amount
        recipient.money += amount
        self.db.commit()
        
        
        # Save transaction using the helper method
        self.save_transaction(
        transaction_type="transfer",
        money=amount,
        to= str(self.user_info.phone_number)
    )
        return self.response_success("Transfer successful", {
            "amount_transferred": amount,
            "recipient_account_number": recipient_account_number,
        })

    def withdraw(self, amount: int):
        """Withdraws money from the account."""
        if amount <= 0:
            return self.response_error(
                "Withdrawal amount must be greater than zero", status.HTTP_400_BAD_REQUEST
            )

        if self.user_info.money < amount:
            return self.response_error(
                "Insufficient balance for withdrawal", status.HTTP_400_BAD_REQUEST
            )

        # Deduct amount from user's balance
        self.user_info.money -= amount
        self.db.commit()
        
        self.save_transaction(
        transaction_type="withdraw",
        money=amount,
        to= "withdraw",
    )
        return self.response_success("Withdrawal successful", {
            "amount_withdrawn": amount,
            "remaining_balance": self.user_info.money,
        })

    def deposit(self, amount: int):
        """Deposits money into the account."""
        if amount <= 0:
            return self.response_error(
                "Deposit amount must be greater than zero", status.HTTP_400_BAD_REQUEST
            )

        # Add amount to user's balance
        self.user_info.money += amount
        self.db.commit()                
        self.save_transaction(
        transaction_type="deposit",
        money=amount,
        to= str(self.user_info.account_number),
    )
        return self.response_success("Deposit successful", {
            "amount_deposited": amount,
            "new_balance": self.user_info.money,
        })

    def airtime_self(self, amount: int):
        """Buys airtime for the user's phone number."""
        if amount <= 0:
            return self.response_error(
                "Airtime amount must be greater than zero", status.HTTP_400_BAD_REQUEST
            )

        if self.user_info.money < amount:
            return self.response_error(
                "Insufficient balance for airtime purchase", status.HTTP_400_BAD_REQUEST
            )
        # Deduct airtime amount from user's balance
        self.user_info.money -= amount
        self.db.commit()
        self.save_transaction(
        transaction_type="buy airtime",
        money=amount,
        to= str(self.user_info.phone_number),
    )
        return self.response_success("Airtime purchase successful", {
            "airtime_amount": amount,
            "remaining_balance": self.user_info.money,
            "phone_number": self.user_info.phone_number,
        })

    def airtime_other(self, amount: int, phone_no: str):
        """Buys airtime for another phone number."""
        if amount <= 0:
            return self.response_error(
                "Airtime amount must be greater than zero", status.HTTP_400_BAD_REQUEST
            )

        if self.user_info.money < amount:
            return self.response_error(
                "Insufficient balance for airtime purchase", status.HTTP_400_BAD_REQUEST
            )

        # Deduct airtime amount from user's balance
        self.user_info.money -= amount
        self.db.commit()
        self.save_transaction(
        transaction_type="buy airtime",
        money=amount,
        to= str(phone_no),
    )
        return self.response_success("Airtime purchase successful", {
            "airtime_amount": amount,
            "remaining_balance": self.user_info.money,
            "phone_number": phone_no,
        })


    def buy_data_self(self, amount: int):
        """Buy data for the user's phone number."""
        if amount <= 0:
            return {
                "status": "error",
                "message": "Data amount must be greater than zero",
                "code": 400  # HTTP status code
            }

        if self.user_info.money < amount:
            return {
                "status": "error",
                "message": "Insufficient balance for data purchase",
                "code": 400  # HTTP status code
            }

        # Deduct data amount from user's balance
        self.user_info.money -= amount
        self.db.commit()
        self.save_transaction(
        transaction_type="buy data self",
        money=amount,
        to= str(self.user_info.phone_number),
    )
        return self.response_success("Data purchase successful", {
            "data_amount": amount,
            "remaining_balance": self.user_info.money,            
        })


    def buy_data_other(self, amount: int, phone_no: str):
        """Buy data for another phone number."""
        if amount <= 0:
            return {
                "status": "error",
                "message": "Data amount must be greater than zero",
                "code": 400  # HTTP status code
            }

        if self.user_info.money < amount:
            return {
                "status": "error",
                "message": "Insufficient balance for data purchase",
                "code": 400  # HTTP status code
            }

        # Deduct data amount from user's balance
        self.user_info.money -= amount
        self.db.commit()
        self.save_transaction(
        transaction_type="buy data",
        money=amount,
        to= str(phone_no),
    )
        return self.response_success("Data purchase successful", {
            "data_amount": amount,
            "remaining_balance": self.user_info.money,
            "phone_number": phone_no,
        })

        
        
def get_transaction_by_id(db: Session, user_id: int):
    trans = db.query(DbTransaction).filter(DbTransaction.user_id == user_id).all()
    if trans:
        return {
                "message": "Success",
                "status_code": 200,
                "data": trans
            }

