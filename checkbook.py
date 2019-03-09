import csv
import datetime
import os

# CONSTANTS ##################################################################
ID_ROW = "id"
TIMESTAMP_ROW = "timestamp"
CATEGORY_ROW = "category"
DESCRIPTION_ROW = "description"
AMOUNT_ROW = "amount"
FIELDNAMES = (ID_ROW, TIMESTAMP_ROW, CATEGORY_ROW, DESCRIPTION_ROW, AMOUNT_ROW)
CSV_HEADER = {
    FIELDNAMES[0]: FIELDNAMES[0],
    FIELDNAMES[1]: FIELDNAMES[1],
    FIELDNAMES[2]: FIELDNAMES[2],
    FIELDNAMES[3]: FIELDNAMES[3],
    FIELDNAMES[4]: FIELDNAMES[4],
}

LEDGER_FILENAME = "ledger.csv"
##############################################################################


def get_trans(ledger_file):
    '''
    str -> list
    ledger_file is name of the ledger file
    composes a list of dictionaries from ledger
    '''
    with open(ledger_file) as lf:
        transact_list = [{k: v for k, v in row.items()}
                         for row in csv.DictReader(lf, skipinitialspace=True)]
        return transact_list


def print_all(ledg_list):
    '''
    list -> str
    prints all transactions to console
    '''
    for dict in ledg_list:
        for key in dict:
            print('{}: {}'.format(key, dict[key]))


def view_balance(ledger_file):
    """
    str -> float

    ledger_file is the name of the ledger file

    return balance calculated from ledger file
    """
    with open(ledger_file) as lf:
        reader = csv.DictReader(lf)
        amounts = [float(row[AMOUNT_ROW]) for row in reader]
        return sum(amounts)


def write_record(ledger_file, record):
    """
    str, dict -> None

    ledger_file is the name of the ledger file
    record is a dictionary of "column_name": data

    write record to end of ledger file
    """
    with open(ledger_file, "a") as lf:
        writer = csv.DictWriter(lf, FIELDNAMES)
        writer.writerow(record)


def create_deposit_record(category, description, amount):
    """
    str, str, float -> dict

    category is category of purchase (e.g., income, reimbursement)
    description is a description of the purchase (e.g., "paycheck for March")
    amount is the amount to deposit

    return dictionary of deposit record
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
    amount is the amount to withdraw

    return dictionary of withdraw record
    """
    timestamp = datetime.datetime.now()
    return {
        TIMESTAMP_ROW: timestamp,
        CATEGORY_ROW: category,
        DESCRIPTION_ROW: description,
        AMOUNT_ROW: -1 * amount,
    }


def modify_transaction():
    pass


def last_row_id(ledger_file):
    """
    str -> int

    ledger_file is the name of the ledger file

    return id of the last row in ledger file or 0 if no last row
    """
    with open(ledger_file) as lf:
        reader = csv.DictReader(lf, FIELDNAMES)
        rows = [row for row in reader]
        return int(reader[-1][ID_ROW]) if len(rows) > 0 else 0


def is_valid_amount(amount):
    """
    str -> bool

    amount is inputted value from user for debit/credit

    return True if amount is valid; otherwise, False
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

    prompt is prompt to present to user

    return the amount user inputs cast to a float
    """
    input_amount = input(prompt)
    while not is_valid_amount(input_amount):
        input_amount = input("Please enter a dollar value (e.g., $50.50): ")
    return float(input_amount)


def get_date(prompt):
    '''
    str -> str
    prompt is string user input

    returns a date string formatted for searching through ledger dictionary
    '''
    pass


def checkbook_loop():
    """
    implements CLI for checkbook application
    """
    curr_bal = view_balance
    prompt = (
        "What would you like to do?\n\n"
        "1) View current balance\n"
        "2) Record a debit (withdraw)\n"
        "3) Record a credit (deposit)\n"
        "4) View Transaction History\n"
        "5) Exit\n\n"
    )
    action_choice = input(prompt)

    while action_choice not in ("12345"):
        action_choice = input(
            f"Invalid choice: {action_choice}\n\nPlease enter 1-5: "
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
        ledger_list = get_trans(LEDGER_FILENAME)
        print_all(ledger_list)
        history_choice = input(
            '\nWould you like to search transactions? y/n: \n\n')
        if history_choice.startswith('y'.lower()):
            search_choice = input(
                '1) Select By Date\n2) Select By Category\n3) Select By Description\n4) Exit to main menu \nYour Choice? \n''')
            while search_choice not in ("1234"):
                search_choice = input(
                    f"Invalid choice: {action_choice}\n\nPlease enter 1-4: ")
            if int(search_choice) == 1:
                print('1: Search by Date\n')
            elif int(search_choice) == 2:
                print('2: Search by Category\n')
            elif int(search_choice) == 3:
                print('3: Search by Description keyword\n')
            elif int(search_choice) == 4:
                print('returning to main menu\n')

    elif int(action_choice) == 5:
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
