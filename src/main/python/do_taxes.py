import re

import xlrd


class Bank:
    def __init__(
        self, bankname, filename, start_row, date_col, amount_col, description_col
    ):
        self.bankname = bankname
        self.filename = filename
        self.start_row = start_row
        self.date_col = date_col
        self.amount_col = amount_col
        self.description_col = description_col


class BankRecord:
    def __init__(self, bankname, date, amount, description):
        self.bankname = bankname
        self.date = date
        self.amount = amount
        self.description = description

    def __repr__(self):
        return f"{self.bankname}\t{self.date}\t{self.amount},\t{self.description}"


sabadell = Bank(
    bankname="Sabadell",
    filename="09072025_5230_0001235234.xls",
    start_row=9,
    date_col=0,
    amount_col=3,
    description_col=1,
)

santander = Bank(
    bankname="Santander",
    filename="export202579.xls",
    start_row=8,
    date_col=0,
    amount_col=3,
    description_col=2,
)


def get_values(bank):
    book = xlrd.open_workbook(bank.filename)
    sheet = book.sheet_by_index(0)

    bank_records = []
    for row in range(bank.start_row, sheet.nrows):
        date = sheet.cell_value(row, bank.date_col)
        amount = sheet.cell_value(row, bank.amount_col)
        description = sheet.cell_value(row, bank.description_col)

        bank_records.append(BankRecord(bank.bankname, date, amount, description))

    return bank_records


def filter_income(bank_records):
    income_records = []
    for record in bank_records:
        if record.amount > 0:
            income_records.append(record)
    return income_records


def filter_by_month(bank_records, month, year):
    filtered_records = []
    for record in bank_records:
        if (
            int(record.date.split("/")[1]) == month
            and int(record.date.split("/")[2]) == year
        ):
            filtered_records.append(record)
    return filtered_records


def filter_by_description(bank_records, regex_pattern):
    filtered_records = []
    for record in bank_records:
        if re.search(regex_pattern, record.description):
            filtered_records.append(record)
    return filtered_records


def sum_amounts(bank_records):
    total = 0
    for record in bank_records:
        total += record.amount
    return total


def main():
    bank_records = []
    bank_records += get_values(sabadell)
    bank_records += get_values(santander)

    bank_records = filter_income(bank_records)
    bank_records = filter_by_month(bank_records, 4, 2025)
    bank_records = filter_by_description(bank_records, r"^.*(TPV).*$")

    for record in bank_records:
        print(record)

    print(sum_amounts(bank_records))


if __name__ == "__main__":
    main()
