import csv
import datetime
import os

# CONSTANTS ##################################################################
TIMESTAMP_ROW = "timestamp"
CATEGORY_ROW = "category"
DESCRIPTION_ROW = "description"
AMOUNT_ROW = "amount"
FIELDNAMES = (TIMESTAMP_ROW, CATEGORY_ROW, DESCRIPTION_ROW, AMOUNT_ROW)
CSV_HEADER = {
    FIELDNAMES[0]: FIELDNAMES[0],
    FIELDNAMES[1]: FIELDNAMES[1],
    FIELDNAMES[2]: FIELDNAMES[2],
    FIELDNAMES[3]: FIELDNAMES[3],
}

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


def create_deposit_record(category, description, amount):
    """
    str, str, float -> dict

    category is category of purchase (e.g., income, reimbursement)
    description is a description of the purchase (e.g., "paycheck for March")
    amount is a float of the amount to deposit

    return dictionary of withdraw record
    """
    timestamp = datetime.datetime.now()
    return {
        TIMESTAMP_ROW: timestamp,
        CATEGORY_ROW: category,
        DESCRIPTION_ROW: description,
        AMOUNT_ROW: amount,
    }


def create_withdraw_record(category, description, amount):
    """
    str, str, float -> dict

    category is category of purchase (e.g., grocery, child care)
    description is a description of the purchase (e.g., "beer for party")
    amount is a float of the amount to withdraw

    return dictionary of withdraw record
    """
    timestamp = datetime.datetime.now()
    return {
        TIMESTAMP_ROW: timestamp,
        CATEGORY_ROW: category,
        DESCRIPTION_ROW: description,
        AMOUNT_ROW: -1 * amount,
    }


def is_valid_amount(amount):
    """
    str -> bool

    amount is inputted value from user for debit/credit
    function ensures input is valid and not a negative value
    """
    amount_tokens = amount.split(".")
    if len(amount_tokens) == 1:
        return amount_tokens[0].isdigit()
    elif len(amount_tokens) == 2:
        if amount_tokens[0].isdigit():
            if amount_tokens[1].isdigit and len(amount_tokens[1]) == 2:
                return True

    return False


def get_valid_amount(prompt):
    """
    str -> float

    amount is inputted value from user for debit/credit
    function ensures input is valid and not a negative value
    """
    input_amount = input(prompt)
    while not is_valid_amount(input_amount):
        input_amount = input("Please enter a dollar value (e.g., $50.50): ")
    return float(input_amount)


def checkbook_loop():
    curr_bal = view_balance
    prompt = (
        "What would you like to do?\n\n"
        "1) View current balance\n"
        "2) Record a debit (withdraw)\n"
        "3) Record a credit (deposit)\n"
        "4) Exit\n\n"
        "Your choice? "
    )
    action_choice = input(prompt)

    while action_choice not in ("1234"):
        action_choice = input(
            f"Invalid choice: {action_choice}\n\nPlease enter 1-4: "
        )

    # process menu choice #####################################################
    if int(action_choice) == 1:
        curr_bal = view_balance(LEDGER_FILENAME)
        print("\nYour current balance is : ${}".format(curr_bal))
        print()

    elif int(action_choice) == 2:
        category = input("\nEnter a category for withdrawal: ")
        description = input("Enter a description for withdrawal: ")

        withdraw_prompt = "Enter amount for withdrawal in dollars: $"
        debit_value = get_valid_amount(withdraw_prompt)

        withdraw_record = create_withdraw_record(
            category, description, debit_value
        )
        write_record(LEDGER_FILENAME, withdraw_record)

    elif int(action_choice) == 3:
        category = input("\nEnter a category for deposit: ")
        description = input("Enter a description for deposit: ")

        deposit_prompt = "Enter amount for deposit in dollars: $"
        credit_value = get_valid_amount(deposit_prompt)

        deposit_record = create_deposit_record(
            category, description, credit_value
        )
        write_record(LEDGER_FILENAME, deposit_record)

    elif int(action_choice) == 4:
        exit()
    ##########################################################################

    return checkbook_loop()


if __name__ == "__main__":
    if not os.path.isfile(LEDGER_FILENAME):
        with open(LEDGER_FILENAME, "w") as lf:
            writer = csv.DictWriter(lf, FIELDNAMES)
            writer.writerow(CSV_HEADER)

    print("\n~~~ Welcome to your terminal checkbook! ~~~\n")
    checkbook_loop()
