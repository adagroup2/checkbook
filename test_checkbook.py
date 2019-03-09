import checkbook
import csv
import datetime
import os


def test_create_deposit_record():
    deposit1 = checkbook.create_deposit_record(
        "income", "paycheck for March", 1.00
    )
    assert isinstance(deposit1[checkbook.TIMESTAMP_ROW], datetime.datetime)
    assert deposit1[checkbook.CATEGORY_ROW] == "income"
    assert deposit1[checkbook.DESCRIPTION_ROW] == "paycheck for March"
    assert deposit1[checkbook.AMOUNT_ROW] == "1.00"

    deposit2 = checkbook.create_deposit_record(
        "reimbursement", "reimbursement for beer for party", 20.14
    )
    assert isinstance(deposit2[checkbook.TIMESTAMP_ROW], datetime.datetime)
    assert deposit2[checkbook.CATEGORY_ROW] == "reimbursement"
    assert (
        deposit2[checkbook.DESCRIPTION_ROW]
        == "reimbursement for beer for party"
    )
    assert deposit2[checkbook.AMOUNT_ROW] == "20.14"


def test_create_withdraw_record():
    withdraw1 = checkbook.create_withdraw_record("grocery", "gum", 1.00)
    assert isinstance(withdraw1[checkbook.TIMESTAMP_ROW], datetime.datetime)
    assert withdraw1[checkbook.CATEGORY_ROW] == "grocery"
    assert withdraw1[checkbook.DESCRIPTION_ROW] == "gum"
    assert withdraw1[checkbook.AMOUNT_ROW] == "-1.00"

    withdraw2 = checkbook.create_withdraw_record(
        "child care", "babysitter for one hour", 20.14
    )
    assert isinstance(withdraw2[checkbook.TIMESTAMP_ROW], datetime.datetime)
    assert withdraw2[checkbook.CATEGORY_ROW] == "child care"
    assert withdraw2[checkbook.DESCRIPTION_ROW] == "babysitter for one hour"
    assert withdraw2[checkbook.AMOUNT_ROW] == "-20.14"


def test_view_balance():
    assert checkbook.view_balance("dummy_ledger_file1.csv") == 100.00
    assert checkbook.view_balance("dummy_ledger_file2.csv") == 40.00
    assert checkbook.view_balance("dummy_ledger_file3.csv") == -20.00


def test_write_record():
    dummy_filename = "write_record_dummy.csv"
    checkbook.write_record(
        dummy_filename,
        checkbook.create_withdraw_record("test1", "test1", 20.50),
    )
    checkbook.write_record(
        dummy_filename,
        checkbook.create_withdraw_record("test2", "test2 test2", 60.33),
    )
    checkbook.write_record(
        dummy_filename,
        checkbook.create_withdraw_record("test3", "test3 test3 test3", 1.98),
    )

    with open(dummy_filename) as df:
        reader = csv.DictReader(df, checkbook.FIELDNAMES)

        categories = []
        descriptions = []
        amounts = []
        for row in reader:
            categories.append(row[checkbook.CATEGORY_ROW])
            descriptions.append(row[checkbook.DESCRIPTION_ROW])
            amounts.append(row[checkbook.AMOUNT_ROW])

        assert categories[0] == "test1"
        assert categories[1] == "test2"
        assert categories[2] == "test3"

        assert descriptions[0] == "test1"
        assert descriptions[1] == "test2 test2"
        assert descriptions[2] == "test3 test3 test3"

        assert float(amounts[0]) == -20.50
        assert float(amounts[1]) == -60.33
        assert float(amounts[2]) == -1.98

    os.remove(dummy_filename)


def test_last_row_id():
    assert checkbook.last_row_id("dummy_ledger_file4.csv") == 0
    assert checkbook.last_row_id("dummy_ledger_file5.csv") == 2


def test_is_valid_amount():
    assert not checkbook.is_valid_amount("abcd")
    assert not checkbook.is_valid_amount("1.03.45")
    assert not checkbook.is_valid_amount("abcd.efg")
    assert not checkbook.is_valid_amount("34.586")

    assert checkbook.is_valid_amount("1.23")
    assert checkbook.is_valid_amount("34.56")
    assert checkbook.is_valid_amount("2345.23")


def test_file_exists():
    assert checkbook.file_exists("dummy_ledger_file1.csv")
    assert not checkbook.file_exists("nonexistentfile.csv")


def test_create_ledger_file():
    test_csv_filename = "test_ledger_file.csv"
    checkbook.create_ledger_file(test_csv_filename)
    with open("test_ledger_file.csv") as tlf:
        reader = csv.DictReader(tlf, checkbook.FIELDNAMES)
        first_row = [row for row in reader][0]
        assert first_row[checkbook.ID_ROW] == "id"
        assert first_row[checkbook.TIMESTAMP_ROW] == "timestamp"
        assert first_row[checkbook.CATEGORY_ROW] == "category"
        assert first_row[checkbook.DESCRIPTION_ROW] == "description"
        assert first_row[checkbook.AMOUNT_ROW] == "amount"

    os.remove(test_csv_filename)


def test_is_valid_action_choice():
    assert checkbook.is_valid_action_choice(checkbook.OPTION_VIEW_BALANCE)
    assert checkbook.is_valid_action_choice(checkbook.OPTION_DEPOSIT)

    assert not checkbook.is_valid_action_choice("12")
    assert not checkbook.is_valid_action_choice("a")
    assert not checkbook.is_valid_action_choice("abc")
    assert not checkbook.is_valid_action_choice("")
    assert not checkbook.is_valid_action_choice("@")
