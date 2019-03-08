import checkbook
import datetime


def test_create_withdraw_record():
    withdraw1 = checkbook.create_withdraw_record(1.00)
    assert isinstance(withdraw1[checkbook.TIMESTAMP_ROW], datetime.datetime)
    assert withdraw1[checkbook.AMOUNT_ROW] == -1.00

    withdraw2 = checkbook.create_withdraw_record(20.14)
    assert isinstance(withdraw2[checkbook.TIMESTAMP_ROW], datetime.datetime)
    assert withdraw2[checkbook.AMOUNT_ROW] == -20.14


def test_view_balance():
    assert checkbook.view_balance("dummy_ledger_file1.csv") == 100.00
    assert checkbook.view_balance("dummy_ledger_file2.csv") == 40.00
    assert checkbook.view_balance("dummy_ledger_file3.csv") == -20.00


# def test_withdraw():
#     assert withdraw
