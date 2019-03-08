import csv
import datetime
import os

# CONSTANTS ##################################################################
TIMESTAMP_ROW = "timestamp"
DESCRIPTION_ROW = "description"
AMOUNT_ROW = "amount"
CSV_HEADER = {
    TIMESTAMP_ROW: TIMESTAMP_ROW,
    DESCRIPTION_ROW: DESCRIPTION_ROW,
    AMOUNT_ROW: AMOUNT_ROW,
}
FIELDNAMES = (TIMESTAMP_ROW, DESCRIPTION_ROW, AMOUNT_ROW)
LEDGER_FILENAME = "ledger.csv"
##############################################################################


def view_balance(ledger_file):
    """
    str -> float

    ledger_file is the name of the ledger file
    read balance calculated from ledger file
    """
    with open(ledger_file) as lf:
        reader = csv.DictReader(lf)
        amounts = [float(row[AMOUNT_ROW]) for row in reader]
        return sum(amounts)


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
    str -> bool

    amount is inputted value from user for debit/credit
    function ensures input is valid and not a negative value
    """
    pass


def get_valid_amount(prompt):
    """
    str -> float

    amount is inputted value from user for debit/credit
    function ensures input is valid and not a negative value
    """
    input_amount = input(prompt)
    while not is_valid_amount(input_amount):
        input_amount = input("Please enter a non-negative dollar value: ")

    return float(input_amount)


def checkbook_loop():
    curr_bal = view_balance
    prompt = (
        "What would you like to do?\n"
        "1) View current balance\n"
        "2) Record a debit (withdraw)\n"
        "3) Record a credit (deposit)\n"
        "4) Exit\n"
        "Your choice? "
    )
    action_choice = input(prompt)

    while action_choice not in ("1234"):
        action_choice = input("Invalid choice. Please enter 1-4: ")

    # process user input #####################################################
    if int(action_choice) == 1:
        curr_bal = view_balance()
        print("Your current balance is : ${}".format(curr_bal))

    elif int(action_choice) == 2:
        debit_value = input("Enter amount for withdrawal in dollars: $")
        if is_valid_amount(debit_value):
            withdraw_record = create_withdraw_record(debit_value)
            # write_record(ledger_file, record)
    elif int(action_choice) == 3:
        credit_value = input("Enter amount for deposit in dollars: $")
        if is_valid_amount(credit_value):
            # deposit_record = create_deposit_record(credit_value)
            # write_record(ledger_file, record)
            pass
    elif int(action_choice) == 4:
        exit()
    ##########################################################################

    action_choice = input("Would you like to make another transaction (y/n)? ")
    if action_choice.lower() == "y" or action_choice.lower() == "yes":
        print()
        checkbook_loop()


if __name__ == "__main__":
    if not os.path.isfile(LEDGER_FILENAME):
        with open(LEDGER_FILENAME, "w") as lf:
            writer = csv.DictWriter(lf, FIELDNAMES)
            writer.writerow(CSV_HEADER)

    print("~~~ Welcome to your terminal checkbook! ~~~\n")
    checkbook_loop()
