import copy
import csv
import datetime
import os

# CONSTANTS ##################################################################
ID_COL = "id"
TIMESTAMP_COL = "timestamp"
CATEGORY_COL = "category"
DESCRIPTION_COL = "description"
AMOUNT_COL = "amount"
COL_NAMES = (ID_COL, TIMESTAMP_COL, CATEGORY_COL, DESCRIPTION_COL, AMOUNT_COL)

LEDGER_FILENAME = "ledger.csv"

OPTION_VIEW_BALANCE = "1"
OPTION_WITHDRAW = "2"
OPTION_DEPOSIT = "3"
OPTION_VIEW_HISTORY = "4"
OPTION_MODIFY_TRANSACTION = "5"
OPTION_EXIT = "6"

OPTIONS = (
    OPTION_VIEW_BALANCE,
    OPTION_WITHDRAW,
    OPTION_DEPOSIT,
    OPTION_VIEW_HISTORY,
    OPTION_MODIFY_TRANSACTION,
    OPTION_EXIT,
)
##############################################################################


def get_trans(ledger_file):
    """
    str -> list
    ledger_file is name of the ledger file
    composes a list of dictionaries from ledger
    """
    with open(ledger_file) as lf:
        transact_list = [
            {k: v for k, v in row.items()}
            for row in csv.DictReader(lf, skipinitialspace=True)
        ]
        return transact_list


def print_all(ledg_list):
    """
    list -> str
    prints all transactions to console
    """
    for dict in ledg_list:
        for key in dict:
            print("{}: {}".format(key, dict[key]))


def view_balance(ledger_file):
    """
    str -> float

    ledger_file is the name of the ledger file

    return balance calculated from ledger file
    """
    with open(ledger_file) as lf:
        reader = csv.DictReader(lf)
        amounts = [float(row[AMOUNT_COL]) for row in reader]
        return sum(amounts)


def write_record(ledger_file, record):
    """
    str, dict -> None

    ledger_file is the name of the ledger file
    record is a dictionary of "column_name": data

    write record to end of ledger file
    """
    with open(ledger_file, "a") as lf:
        writer = csv.DictWriter(lf, COL_NAMES)
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
    row_id = last_row_id(LEDGER_FILENAME) + 1
    return {
        ID_COL: row_id,
        TIMESTAMP_COL: timestamp,
        CATEGORY_COL: category,
        DESCRIPTION_COL: description,
        AMOUNT_COL: f"{amount:.2f}",
    }


def create_withdraw_record(category, description, amount):
    """
    str, str, float -> dict

    category is category of purchase (e.g., grocery, child care)
    description is a description of the purchase
    (e.g., "food and drinks for party")
    amount is the amount to withdraw

    return dictionary of withdraw record
    """
    row_id = last_row_id(LEDGER_FILENAME) + 1
    timestamp = datetime.datetime.now()
    return {
        ID_COL: row_id,
        TIMESTAMP_COL: timestamp,
        CATEGORY_COL: category,
        DESCRIPTION_COL: description,
        AMOUNT_COL: f"{-1 * amount:.2f}",
    }


def modify_transaction(
    ledger_file, row_id, timestamp, category, description, amount
):
    """
    str, int, datetime, str, str, float-> None

    overwrites the row at row_id in ledger_file
    """
    temp_filename = "modified_ledger.csv"

    rows = []
    with open(ledger_file) as lf:
        reader = csv.DictReader(lf, COL_NAMES)
        rows += [row for row in reader]

    modified_rows = []
    for row in rows:
        modified_row = copy.deepcopy(row)
        if modified_row[ID_COL] == str(row_id):
            modified_row[TIMESTAMP_COL] = timestamp
            modified_row[CATEGORY_COL] = category
            modified_row[DESCRIPTION_COL] = description
            if modified_row[AMOUNT_COL][0] == "-":
                modified_row[AMOUNT_COL] = -1 * amount
            else:
                modified_row[AMOUNT_COL] = amount
        modified_rows.append(modified_row)

    with open(temp_filename, "w") as mlf:
        writer = csv.DictWriter(mlf, COL_NAMES)
        writer.writerows(modified_rows)

    os.remove(ledger_file)
    os.rename(temp_filename, ledger_file)


def last_row_id(ledger_file):
    """
    str -> int

    ledger_file is the name of the ledger file

    return id of the last row in ledger file or 0 if no last row
    """
    with open(ledger_file) as lf:
        reader = csv.DictReader(lf, COL_NAMES)
        rows = [row for row in reader]
        return int(rows[-1][ID_COL]) if len(rows) > 1 else 0


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
    if is_valid_amount(input_amount):
        return float(input_amount)
    else:
        print("\nPlease enter a dollar value (e.g., $50.50)\n")
        return get_valid_amount(prompt)


def get_date():
    """
     -> str
    prompts for string user input

    returns a date string formatted for searching through ledger dictionary
    """
    year_val = input("Please enter a year in form XXXX: ")
    while not len(year_val) == 4 or not year_val.isdigit():
        year_val = input("Please enter a year in form XXXX: ")
    month_val = input("Please enter a month in form XX: ")
    while not len(month_val) == 2 or not month_val.isdigit():
        month_val = input("Please enter a month in form XX: ")
    day_val = input("Please enter a day in form XX: ")
    while not len(day_val) == 2 or not day_val.isdigit():
        month_val = input("Please enter a day in form XX: ")
    date_string = year_val + "-" + month_val + "-" + day_val
    return date_string


def get_cat():
    """

    --> str
    prompts user for string input
    returns a string

    """
    cat_value = input("Please enter a category: ")
    return cat_value


def print_by_date(some_date, ledg_list):
    """
    str-> str

    some_date is string inputted date
    returns  string transactions from dictionary where date matches parameters presented
    """
    for dict in ledg_list:
        if dict["timestamp"].startswith(some_date):
            for key in dict:
                print("{}: {}".format(key, dict[key]))
            print("--------------------")


def print_by_cat(some_cat, ledg_list):
    """
    str-> str

    some_cat is string inputted category
    returns  string transactions from dictionary where category matches parameters presented
    """
    for dict in ledg_list:
        if dict["category"] == some_cat:
            for key in dict:
                print("{}: {}".format(key, dict[key]))
            print("--------------------")


def file_exists(ledger_filename):
    """
    str -> bool

    ledger_filename is the name of the ledger file

    return True if ledger file exists; otherwise, False
    """
    return os.path.isfile(ledger_filename)


def create_ledger_file(ledger_filename):
    """
    str -> None

    ledger_filename is the name of the ledger file

    create ledger file
    CAUTION: will overwrite the ledger file if it exists
    """
    with open(ledger_filename, "w") as lf:
        writer = csv.DictWriter(lf, COL_NAMES)
        writer.writeheader()


def is_valid_action_choice(action_choice):
    """
    str -> bool

    action_choice is the user's inputted action choice

    return True if user's action choice is valid; otherwise, False
    """
    return action_choice.isdigit() and action_choice in OPTIONS


def get_action_choice(prompt):
    """
    str -> str

    prompt is the prompt to present to the user

    return user's action choice
    """
    action_choice = input(prompt)
    if is_valid_action_choice(action_choice):
        return action_choice
    else:
        print(
            f"\nInvalid choice: {action_choice}\n"
            f"Please enter {OPTION_VIEW_BALANCE}-{OPTION_EXIT}\n"
        )
        return get_action_choice(prompt)


def is_valid_transaction_id(ledger_filename, transaction_id):
    """
    str, int - > bool

    transaction_id is the id whose validity will be determined
    ledger_filename is the file whose transaction ids will be calculated

    return True if
    """
    with open(ledger_filename) as lf:
        reader = csv.reader(lf)
        return 1 <= transaction_id <= len([row for row in reader]) - 1


def get_transaction_id(prompt, ledger_filename):
    """
    str -> str

    prompt is prompt to present to user
    ledger_filename is the ledger's filename

    return the transaction id inputted by user
    """
    transaction_id = input("\n" + prompt)

    if transaction_id.isdigit() and is_valid_transaction_id(
        ledger_filename, int(transaction_id)
    ):
        return transaction_id

    print("\nEnter a valid transaction_id.")
    return get_transaction_id(prompt, ledger_filename)


def checkbook_loop():
    """
    implements CLI for checkbook application
    """
    menu = (
        f"\nWhat would you like to do?\n\n"
        f"{OPTION_VIEW_BALANCE}) View current balance\n"
        f"{OPTION_WITHDRAW}) Record a debit (withdraw)\n"
        f"{OPTION_DEPOSIT}) Record a credit (deposit)\n"
        f"{OPTION_VIEW_HISTORY}) View transaction history\n"
        f"{OPTION_MODIFY_TRANSACTION}) Modify a transaction\n"
        f"{OPTION_EXIT}) Exit\n"
    )
    print(menu)
    prompt = "Your choice? "
    action_choice = get_action_choice(prompt)

    # process menu choice #####################################################
    if action_choice == OPTION_VIEW_BALANCE:
        balance = view_balance(LEDGER_FILENAME)
        print(f"\nYour current balance is : ${balance:,.2f}")
        print()

    elif action_choice == OPTION_WITHDRAW:
        category = input("\nEnter a category for withdrawal: ")
        description = input("Enter a description for withdrawal: ")

        withdraw_prompt = "Enter amount for withdrawal in dollars: $"
        debit_value = get_valid_amount(withdraw_prompt)

        withdraw_record = create_withdraw_record(
            category, description, debit_value
        )
        write_record(LEDGER_FILENAME, withdraw_record)

    elif action_choice == OPTION_DEPOSIT:
        category = input("\nEnter a category for deposit: ")
        description = input("Enter a description for deposit: ")

        deposit_prompt = "Enter amount for deposit in dollars: $"
        credit_value = get_valid_amount(deposit_prompt)

        deposit_record = create_deposit_record(
            category, description, credit_value
        )
        write_record(LEDGER_FILENAME, deposit_record)

    elif action_choice == OPTION_VIEW_HISTORY:
        ledger_list = get_trans(LEDGER_FILENAME)
        print_all(ledger_list)
        history_choice = input(
            "\nWould you like to search transactions? y/n: \n\n"
        )
        if history_choice.startswith("y".lower()):
            search_choice = input(
                "1) Select By Date\n2) Select By Category\n3) Select By Description\n4) Exit to main menu \nYour Choice? \n"
                ""
            )
            while search_choice not in ("1234"):
                search_choice = input(
                    f"Invalid choice: {action_choice}\n\nPlease enter 1-4: "
                )
            if int(search_choice) == 1:
                print("1: Search by Date\n")
                day = get_date()
                print_by_date(day, ledger_list)
            elif int(search_choice) == 2:
                print("2: Search by Category\n")
                category = get_cat()
                print_by_cat(category, ledger_list)
            elif int(search_choice) == 3:
                print("3: Search by Description keyword\n")
            elif int(search_choice) == 4:
                print("returning to main menu\n")

    elif action_choice == OPTION_MODIFY_TRANSACTION:
        tid_prompt = "Enter id of transaction to modify: "
        transaction_id = int(get_transaction_id(tid_prompt, LEDGER_FILENAME))

        amount = input("\nTimestamp: ")
        category = input("Category: ")
        description = input("Description: ")
        amount = get_valid_amount("Amount: ")

        modify_transaction(
            LEDGER_FILENAME,
            transaction_id,
            amount,
            category,
            description,
            amount,
        )

    elif action_choice == OPTION_EXIT:
        exit(0)
    ##########################################################################

    return checkbook_loop()


if __name__ == "__main__":
    if not file_exists(LEDGER_FILENAME):
        create_ledger_file(LEDGER_FILENAME)

    print("\n~~~ Welcome to your terminal checkbook! ~~~")
    checkbook_loop()
