import csv
import datetime

TIMESTAMP_ROW = "timestamp"
AMOUNT_ROW = "amount"
FIELDNAMES = (TIMESTAMP_ROW, AMOUNT_ROW)


def view_balance(ledger_file):
    """
    str -> float

    ledger_file is the name of the ledger file
    read balance calculated from ledger file
    """
    with open(ledger_file) as lf:
        reader = csv.DictReader(lf)
        return sum([float(row[AMOUNT_ROW]) for row in reader])


def write_record(ledger_file, record):
    """
    str, dict -> None

    ledger_file is the name of the ledger file
    record is a dictionary of "column": data
    """
    with open(ledger_file, "a") as lf:
        writer = csv.DictWriter(lf, FIELDNAMES)
        writer.writerow(record)


def create_withdraw_record(amount):
    """
    str, float -> None

    ledger_file is the name of the ledger file
    float is the amount of the withdrawal
    """
    timestamp = datetime.datetime.now()
    return {TIMESTAMP_ROW: timestamp, AMOUNT_ROW: -1 * amount}


def is_valid_amount(amount):
    """
    str --> bool

    amount is inputted value from user for debit/credit
    function ensures input is valid and not a negative value
    """
    while not amount.isdigit() or amount.startswith("-"):
        amount = input("Please enter a non-negative dollar value: ")
    return amount == True


if __name__ == "__main__":
    print("~~~ Welcome to your terminal checkbook! ~~~\n")

    action_choice = input(
        """What would you like to do?
    1) View current balance
    2) record a debit (withdraw)
    3) record a credit (deposit)
    4) exit
    """
    )
    while not action_choice in ("1234"):
        action_choice = input("Invalid choice. Please enter 1-4: ")

    if int(action_choice) == 1:
        print(action_choice)
        # view_balance()
    elif int(action_choice) == 2:
        print(action_choice)
        # debit()
    elif int(action_choice) == 3:
        print(action_choice)
        # credit()
    elif int(action_choice) == 4:
        exit()

    action_choice = input("Would you like to make another transaction (y/n)? ")
    while action_choice == "y" or action_choice.lower() == "yes":
        action_choice = input(
            "What would you like to do? \n1) View current balance\n2) record a debit withdraw\n3) record a credit deposit\n4) exit \n "
        )
        while not action_choice in ("1234"):
            action_choice = input("Invalid choice. Please enter 1-4: ")

        if int(action_choice) == 1:
            print(action_choice)
            # view_balance()
        elif int(action_choice) == 2:
            print(action_choice)
            # debit()
        elif int(action_choice) == 3:
            print(action_choice)
            # credit()
        elif int(action_choice) == 4:
            exit()
        action_choice = input(
            "Would you like to make another transaction (y/n)? "
        )
