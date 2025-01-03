import json
from datetime import datetime

def load_accounts():
    try:
        with open("bank-db.json", "r") as file:
            data = json.load(file)
            if "accounts" not in data:
                data["accounts"] = {}
            return data
    except (FileNotFoundError, json.JSONDecodeError):
        return {"accounts": {}}

def save_accounts(accounts):
    with open("bank-db.json", "w") as file:
        json.dump(accounts, file, indent=4)

def create_account(accounts, account_number, name, initial_balance=0):
    if str(account_number) in accounts["accounts"]:
        return "Account already exists."
    accounts["accounts"][str(account_number)] = {
        "name": name,
        "balance": initial_balance,
        "transactions": []
    }
    save_accounts(accounts)
    return "Account created successfully."

def deposit(accounts, account_number, amount):
    if str(account_number) not in accounts["accounts"]:
        return "Account does not exist."
    accounts["accounts"][str(account_number)]["balance"] += amount
    accounts["accounts"][str(account_number)]["transactions"].append({
        "type": "Deposit",
        "amount": amount,
        "timestamp": datetime.now().isoformat()
    })
    save_accounts(accounts)
    return "Deposit successful."

def withdraw(accounts, account_number, amount):
    if str(account_number) not in accounts["accounts"]:
        return "Account does not exist."
    if accounts["accounts"][str(account_number)]["balance"] < amount:
        return "Insufficient balance."
    accounts["accounts"][str(account_number)]["balance"] -= amount
    accounts["accounts"][str(account_number)]["transactions"].append({
        "type": "Withdrawal",
        "amount": amount,
        "timestamp": datetime.now().isoformat()
    })
    save_accounts(accounts)
    return "Withdrawal successful."

def check_balance(accounts, account_number):
    if str(account_number) not in accounts["accounts"]:
        return "Account does not exist."
    return accounts["accounts"][str(account_number)]["balance"]

def print_statement(accounts, account_number):
    if str(account_number) not in accounts["accounts"]:
        return "Account does not exist."
    return accounts["accounts"][str(account_number)]["transactions"]

def main():
    accounts = load_accounts()
    while True:
        print("\n1. Create Account\n2. Deposit\n3. Withdraw\n4. Check Balance\n5. Print Statement\n6. Exit")
        choice = input("Enter your choice: ")
        if choice == '1':
            account_number = int(input("Enter account number: "))
            name = input("Enter name: ")
            initial_balance = float(input("Enter initial balance: "))
            print(create_account(accounts, account_number, name, initial_balance))
        elif choice == '2':
            account_number = int(input("Enter account number: "))
            amount = float(input("Enter amount to deposit: "))
            print(deposit(accounts, account_number, amount))
        elif choice == '3':
            account_number = int(input("Enter account number: "))
            amount = float(input("Enter amount to withdraw: "))
            print(withdraw(accounts, account_number, amount))
        elif choice == '4':
            account_number = int(input("Enter account number: "))
            print("Balance:", check_balance(accounts, account_number))
        elif choice == '5':
            account_number = int(input("Enter account number: "))
            print("Transaction Statement:", print_statement(accounts, account_number))
        elif choice == '6':
            break
        else:
            print("Invalid choice. Please try again.")

main()