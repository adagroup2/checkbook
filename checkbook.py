import copy
import csv
import datetime
import os
import sys


# CONSTANTS ##################################################################
ID_COL = "ID"
TIMESTAMP_COL = "Timestamp"
CATEGORY_COL = "Category"
DESCRIPTION_COL = "Description"
AMOUNT_COL = "Amount"
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


def print_ledger_stats(ledg_list):
    """
    dict -> None

    ledg_list is a list of dictionaries representing transactions

    print statistics for the ledg_list
    """
    deb_list = []
    cred_list = []
    for transaction in ledg_list:
        amount = transaction[AMOUNT_COL]
        if amount.startswith("-"):
            deb_list.append(float(amount.replace("-", "")))
        else:
            cred_list.append(float(amount))

    average_dep = sum(deb_list) / len(deb_list)
    average_cred = sum(cred_list) / len(cred_list)
    print(
        f'\n{"Max Credit":<15}|{"Min Credit":<15}|'
        f'{"Max Debit":<15}|{"Min Debit":<15}|'
        f'{"Avg Credit":<15}|{"Avg Debit":<15}\n'
        f"{'-'*15}|{'-'*15}|{'-'*15}|{'-'*15}|{'-'*15}|{'-'*15}\n"
        f"${max(cred_list):<14,.2f}|${min(cred_list):<14,.2f}|"
        f"${max(deb_list):<14,.2f}|${min(deb_list):<14,.2f}|"
        f"${average_cred:<14,.2f}|${average_dep:<14,.2f}"
    )


def print_transaction(transaction):
    """
    dict -> None

    transaction is a dict of the transaction

    print the transaction
    """
    transaction_id = transaction[ID_COL]
    timestamp = transaction[TIMESTAMP_COL]
    category = transaction[CATEGORY_COL]
    description = transaction[DESCRIPTION_COL]
    amount = transaction[AMOUNT_COL]

    print(
        f"{'-'*4}|{'-'*20}|{'-'*20}|{'-'*50}|{'-'*15}\n"  # 14 + '$' for amount
        f"{transaction_id:<4}|{timestamp:<20}|{category[:20]:<20}|"
        f"{description[:50]:<50}|${float(amount):<14,.2f}"
    )


def print_ledger(ledg_list):
    """
    list of dict -> None

    ledg_list is a list of dictionaries representing transactions

    print all transactions from ledg_list to console
    """
    # print header
    print(
        f"\n{ID_COL:<4}|{TIMESTAMP_COL:<20}|{CATEGORY_COL:<20}|"
        f"{DESCRIPTION_COL:<50}|{AMOUNT_COL:<15}"
    )

    for transaction in ledg_list:
        print_transaction(transaction)


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


def create_deposit_record(date, time, category, description, amount):
    """
    str, str, str, str, float -> dict

    date is the date of the transaction
    time is the time of the transaction
    category is category of the deposit (e.g., income, reimbursement)
    description is a description of the deposit (e.g., "paycheck for March")
    amount is the amount to deposit

    return dictionary of deposit record
    """
    row_id = last_row_id(LEDGER_FILENAME) + 1
    return {
        ID_COL: row_id,
        TIMESTAMP_COL: date + " " + time,
        CATEGORY_COL: category,
        DESCRIPTION_COL: description,
        AMOUNT_COL: f"{amount:.2f}",
    }


def create_withdraw_record(date, time, category, description, amount):
    """
    str, str, str, str, float -> dict

    date is the date of the transaction
    time is the time of the transaction
    category is category of the withdrawal (e.g., grocery, child care)
    description is a description of the withdrawal
    (e.g., "food and drinks for party")
    amount is the amount to withdraw

    return dictionary of withdraw record
    """
    row_id = last_row_id(LEDGER_FILENAME) + 1
    return {
        ID_COL: row_id,
        TIMESTAMP_COL: date + " " + time,
        CATEGORY_COL: category,
        DESCRIPTION_COL: description,
        AMOUNT_COL: f"{-1 * amount:.2f}",
    }


def modify_transaction(
    ledger_file, row_id, date, time, category, description, amount
):
    """
    str, int, str, str, str, str, float-> None

    ledger_file is the name of the ledger file to modify
    row_id is the ID of the transaction to modify
    date is the date of the transaction
    time is the time of the transaction
    category is category of the transaction
    description is a description of the transaction
    amount is the amount of the transaction

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
            modified_row[TIMESTAMP_COL] = date + " " + time
            modified_row[CATEGORY_COL] = category
            modified_row[DESCRIPTION_COL] = description
            if modified_row[AMOUNT_COL][0] == "-":
                modified_row[AMOUNT_COL] = f"{-1 * amount:.2f}"
            else:
                modified_row[AMOUNT_COL] = f"{amount:.2f}"
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
        print("\nPlease enter a valid dollar value (e.g., $50.50)\n")
        return get_valid_amount(prompt)


def print_by_date(some_date, ledg_list):
    """
    str-> str

    some_date is string inputted date
    ledg_list is a list of dictionaries representing transactions

    returns string transactions from dictionary where date matches parameters
    presented
    """
    val_list = []
    for transaction in ledg_list:
        if transaction[TIMESTAMP_COL].startswith(some_date):
            for key in transaction:
                if key == AMOUNT_COL:
                    val_list.append(float(transaction[key]))
                    print("{}: ${:,.2f}".format(key, float(transaction[key])))
                else:
                    print("{}: {}".format(key, transaction[key]))
            print("--------------------")
    if len(val_list) > 0:
        average = sum(val_list) / len(val_list)
        print(
            "Maximum transaction in {}: ${:,.2f}".format(
                some_date, max(val_list)
            )
        )
        print(
            "Minimum transaction in {}: ${:,.2f}".format(
                some_date, min(val_list)
            )
        )
        print("Average transaction in {}: ${:,.2f}".format(some_date, average))
        print("------------------")
    else:
        print("\nNo results.")


def print_by_cat(some_cat, ledg_list):
    """
    str-> str

    some_cat is string inputted category
    ledg_list is a list of dictionaries representing transactions

    returns string transactions from dictionary where category matches
    parameters presented
    """
    val_list = []
    for transaction in ledg_list:
        if transaction[CATEGORY_COL] == some_cat:
            for key in transaction:
                if key == AMOUNT_COL:
                    val_list.append(float(transaction[key]))
                    print("{}: ${:,.2f}".format(key, float(transaction[key])))
                else:
                    print("{}: {}".format(key, transaction[key]))
            print("--------------------")
    if len(val_list) > 0:
        average = sum(val_list) / len(val_list)
        print(
            "Maximum transaction in {}: ${:,.2f}".format(
                some_cat, max(val_list)
            )
        )
        print(
            "Minimum transaction in {}: ${:,.2f}".format(
                some_cat, min(val_list)
            )
        )
        print("Average transaction in {}: ${:,.2f}".format(some_cat, average))
        print("------------------")
    else:
        print("\nNo results.")


def print_by_desc(some_desc, ledg_list):
    """
    str-> str

    some_cat is string inputted category
    ledg_list is a list of dictionaries representing transactions

    returns string transactions from dictionary where category matches
    parameters presented
    """
    val_list = []
    for transaction in ledg_list:
        if some_desc in transaction[DESCRIPTION_COL]:
            for key in transaction:
                if key == AMOUNT_COL:
                    val_list.append(float(transaction[key]))
                    print("{}: ${:,.2f}".format(key, float(transaction[key])))
                else:
                    print("{}: {}".format(key, transaction[key]))

            print("--------------------\n")

    if len(val_list) > 0:
        average = sum(val_list) / len(val_list)
        print(
            "Maximum transaction in {}: ${:,.2f}".format(
                some_desc, max(val_list)
            )
        )
        print(
            "Minimum transaction in {}: ${:,.2f}".format(
                some_desc, min(val_list)
            )
        )
        print("Average transaction in {}: ${:,.2f}".format(some_desc, average))
        print("------------------")
    else:
        print("\nNo results.")


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
    else:
        print("\nInvalid transaction ID.")
        return get_transaction_id(prompt, ledger_filename)


def is_valid_date(date):
    """
    str -> bool

    date is the date to validate

    return True if date is valid (YYYY-MM-DD); otherwise, False
    """
    try:
        datetime.datetime.strptime(date, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def get_date_input(prompt):
    """
    str -> str

    prompt is prompt to present to user

    return valid date inputted by user
    """
    date = input(prompt)

    if is_valid_date(date):
        return date
    else:
        print("\nInvalid date.")
        return get_date_input(prompt)


def is_valid_time(time):
    """
    str -> bool

    time is the time to validate

    return True if time is in valid 24-hour clock format; otherwise, False
    """
    try:
        datetime.datetime.strptime(time, "%H:%M:%S")
        return True
    except ValueError:
        return False


def get_time_input(prompt):
    """
    str -> str

    prompt is prompt to present to user

    return valid time inputted by user
    """
    time = input(prompt)

    if is_valid_time(time):
        return time
    else:
        print("\nInvalid time.\n")
        return get_time_input(prompt)


def checkbook_loop():
    """
    implements CLI for checkbook application
    """
    menu = (
        f"\nWhat would you like to do?\n\n"
        f"{OPTION_VIEW_BALANCE}) View current balance\n"
        f"{OPTION_WITHDRAW}) Record a debit (withdraw)\n"
        f"{OPTION_DEPOSIT}) Record a credit (deposit)\n"
        f"{OPTION_VIEW_HISTORY}) View and search transaction history\n"
        f"{OPTION_MODIFY_TRANSACTION}) Modify a transaction\n"
        f"{OPTION_EXIT}) Exit\n"
    )
    print(menu)
    prompt = "Your choice? "
    action_choice = get_action_choice(prompt)

    date_prompt = "\nEnter date (YYYY-MM-DD): "
    time_prompt = "Enter time (HH:MM:SS in 24-hour clock format): "
    category_prompt = "Enter a category: "
    description_prompt = "Enter a description: "
    amount_prompt = "Enter amount: $"

    # process menu choice #####################################################
    if action_choice == OPTION_VIEW_BALANCE:
        balance = view_balance(LEDGER_FILENAME)
        print(f"\nYour current balance is : ${balance:,.2f}")
        print()

    elif action_choice == OPTION_WITHDRAW:
        date = get_date_input(date_prompt)
        time = get_time_input(time_prompt)
        category = input(category_prompt)
        description = input(description_prompt)

        debit_value = get_valid_amount(amount_prompt)

        withdraw_record = create_withdraw_record(
            date, time, category, description, debit_value
        )
        write_record(LEDGER_FILENAME, withdraw_record)

    elif action_choice == OPTION_DEPOSIT:
        date = get_date_input(date_prompt)
        time = get_time_input(time_prompt)
        category = input(category_prompt)
        description = input(description_prompt)

        credit_value = get_valid_amount(amount_prompt)

        deposit_record = create_deposit_record(
            date, time, category, description, credit_value
        )
        write_record(LEDGER_FILENAME, deposit_record)

    elif action_choice == OPTION_VIEW_HISTORY:
        ledger_list = get_trans(LEDGER_FILENAME)
        print_ledger(ledger_list)
        print_ledger_stats(ledger_list)
        history_choice = input("\nSearch transactions (y/n)? ")
        if history_choice.lower().startswith("y"):
            search_choice = input(
                "\n1) Select By Date\n2) Select By Category\n3) Select By "
                "Description\n4) Exit to main menu\n\nYour Choice? "
            )
            while search_choice not in ("1", "2", "3", "4"):
                search_choice = input(
                    f"\nInvalid choice: {action_choice}\n\nPlease enter 1-4: "
                )
            if int(search_choice) == 1:
                print("\n1: Search by date")
                day = get_date_input(date_prompt)
                print_by_date(day, ledger_list)
            elif int(search_choice) == 2:
                print("\n2: Search by category\n")
                category = input(category_prompt)
                print_by_cat(category, ledger_list)
            elif int(search_choice) == 3:
                print("\n3: Search by description keyword\n")
                descript = input("Search descriptions with word or phrase: ")
                print_by_desc(descript, ledger_list)
            elif int(search_choice) == 4:
                print("\nReturning to main menu")

    elif action_choice == OPTION_MODIFY_TRANSACTION:
        tid_prompt = "Enter id of transaction to modify: "
        transaction_id = int(get_transaction_id(tid_prompt, LEDGER_FILENAME))

        date = get_date_input(date_prompt)
        time = get_time_input(time_prompt)
        category = input(category_prompt)
        description = input(description_prompt)
        amount = get_valid_amount(amount_prompt)

        modify_transaction(
            LEDGER_FILENAME,
            transaction_id,
            date,
            time,
            category,
            description,
            amount,
        )

    elif action_choice == OPTION_EXIT:
        exit(0)
    ##########################################################################

    return checkbook_loop()


def set_winsize(rows, cols):
    sys.stdout.write(f"\x1b[8;{rows};{cols}t")


if __name__ == "__main__":
    if not file_exists(LEDGER_FILENAME):
        create_ledger_file(LEDGER_FILENAME)

    set_winsize(24, 125)
    print("\n~~~ Welcome to your terminal checkbook! ~~~")
    checkbook_loop()
