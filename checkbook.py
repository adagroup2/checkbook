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


def record_transaction(ledger_file, record):
    """
    str, dict -> None

    ledger_file is the name of the ledger file
    record is a dictionary of "column": data
    """
    with open(ledger_file, "a") as lf:
        writer = csv.DictWriter(lf, FIELDNAMES)
        writer.writerow(record)


def withdraw(ledger_file, amount):
    """
    str, float -> None

    ledger_file is the name of the ledger file
    float is the amount of the withdrawal
    """
    with open(ledger_file, "a") as lf:
        writer = csv.DictWriter(lf, FIELDNAMES)
        timestamp = datetime.datetime.now()
        writer.writerow({TIMESTAMP_ROW: timestamp, AMOUNT_ROW: amount})

