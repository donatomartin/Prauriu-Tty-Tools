import csv
import re
from datetime import datetime

import colorama
import xlrd

colorama.init(autoreset=True, strip=False, convert=False)


class Source:
    def __init__(
        self, sourcename, filename, start_row, date_col, amount_col, description_col
    ):
        self.sourcename = sourcename
        self.filename = filename
        self.start_row = start_row
        self.date_col = date_col
        self.amount_col = amount_col
        self.description_col = description_col


id_counter = 0


class Record:
    def __init__(self, date, amount, description):

        self.date = date
        self.amount = amount
        self.description = description

    def __repr__(self):

        global id_counter
        self.id = id_counter
        id_counter += 1

        color = colorama.Fore.RED if self.amount < 0 else colorama.Fore.GREEN
        return (
            f"{colorama.Fore.BLUE}{self.id:>4}.{colorama.Fore.RESET} "
            + f"{self.date.strftime('%d/%m/%Y')} "
            + f"{color}{self.amount:>10.2f}€{colorama.Fore.RESET} "
            + f"   {self.description}"
        )

    def serialize(self, category):
        return f"{self.id},{category},{self.date.strftime('%d/%m/%Y')},{self.amount:.2f},{self.description}"


sabadell = Source(
    sourcename="Sabadell",
    filename="sabadell.xls",
    start_row=9,
    date_col=0,
    amount_col=3,
    description_col=1,
)

santander = Source(
    sourcename="Santander",
    filename="santander.xls",
    start_row=8,
    date_col=0,
    amount_col=3,
    description_col=2,
)

airbnb1 = Source(
    sourcename="Airbnb",
    filename="airbnb1.csv",
    start_row=0,
    date_col="Fecha de inicio",
    amount_col="Ingresos",
    description_col="Nombre de la persona",
)

airbnb2 = Source(
    sourcename="Airbnb",
    filename="airbnb2.csv",
    start_row=0,
    date_col="Fecha de inicio",
    amount_col="Ingresos",
    description_col="Nombre de la persona",
)

airbnb3 = Source(
    sourcename="Airbnb",
    filename="airbnb3.csv",
    start_row=0,
    date_col="Fecha de inicio",
    amount_col="Ingresos",
    description_col="Nombre de la persona",
)


def get_values_from_xls(source):

    book = xlrd.open_workbook(source.filename)
    sheet = book.sheet_by_index(0)

    records = []
    for row in range(source.start_row, sheet.nrows):
        date = datetime.strptime(sheet.cell_value(row, source.date_col), "%d/%m/%Y")
        amount = float(sheet.cell_value(row, source.amount_col))
        description = (
            source.sourcename + ": " + sheet.cell_value(row, source.description_col)
        ).strip()

        records.append(Record(date, amount, description))

    return records


def get_values_from_csv(source):
    records = []
    with open(source.filename, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            date = datetime.strptime(row[source.date_col], "%d/%m/%Y")
            text = row[source.amount_col].replace(",", ".")
            match = re.search(r"\d+\.\d+", text)
            amount = float(match.group()) if match else None
            description = (
                source.sourcename + ": " + row[source.description_col]
            ).strip()

            records.append(Record(date, amount, description))

    return records


def get_values(source):

    if source.filename.endswith(".xls"):
        return get_values_from_xls(source)
    elif source.filename.endswith(".csv"):
        return get_values_from_csv(source)
    else:
        return []


def filter_income(records):
    filtered_records = []
    for record in records:
        if record.amount > 0:
            filtered_records.append(record)
    return filtered_records


def filter_by_description(records, regex_pattern):
    filtered_records = []
    for record in records:
        if re.search(regex_pattern, record.description):
            filtered_records.append(record)
    return filtered_records


def split_by_months(records):
    months = {}
    for record in records:
        month_key = record.date.strftime("%m/%Y")
        if month_key not in months:
            months[month_key] = []
        months[month_key].append(record)
    return months


def sum_amounts(records):
    total = 0
    for record in records:
        total += record.amount
    return total


def print_records(records):
    for record in records:
        print(record)


def print_monthly_records(records, title="unknown"):

    print(f"\n{colorama.Fore.YELLOW}{"-" * 40}")
    print(f"{colorama.Fore.YELLOW}{"Category: " + title}")
    print(f"{colorama.Fore.YELLOW}{"-" * 40}\n")

    # Split records by months
    monthly_records = split_by_months(records)

    for month, records in monthly_records.items():
        print(f"{colorama.Fore.BLUE}Date: {month}")
        print_records(records)
        total = sum_amounts(records)

        print(f"Total: {colorama.Fore.RED}{total:.2f}€{colorama.Fore.RESET}\n")


def main():

    # Load records from all sources
    records = []
    records += get_values(sabadell)
    records += get_values(santander)
    records += get_values(airbnb1)
    records += get_values(airbnb2)
    records += get_values(airbnb3)

    # Sort records by date (assuming date is in 'dd/mm/yyyy' format)
    records.sort(key=lambda x: x.date)

    # Filter only income records
    records = filter_income(records)

    # Filter records by description containing "smart"
    smartbox_records = filter_by_description(records, r"^.*(SMART).*$")

    # Filter records by description containing "Airbnb"
    airbnb_records = filter_by_description(records, r"^.*(Airbnb).*$")

    # Filter records by description containing "Multipass"
    multipass_records = filter_by_description(records, r"^.*(MULTIPASS).*$")

    # Filter records by description containing "Colectivia"
    colectivia_records = filter_by_description(records, r"^.*(COLECTIVIA).*$")

    # Filter records by description containing "TPV" or "Liquidacion"
    tpv_records = filter_by_description(records, r"^.*(TPV|Liquidacion).*$")

    # Filter all the remaining records who don't match the above patterns
    other_records = filter_by_description(
        records, r"^(?!.*(SMART|Airbnb|MULTIPASS|COLECTIVIA|TPV|Liquidacion)).*$"
    )

    # Print all records
    print_monthly_records(smartbox_records, title="smartbox")
    print_monthly_records(tpv_records, title="ventas")
    print_monthly_records(airbnb_records, title="airbnb")
    print_monthly_records(multipass_records, title="multipass")
    print_monthly_records(colectivia_records, title="colectivia")
    print_monthly_records(other_records, title="other")

    # Serialize all records to a CSV file
    with open("tax_records_output.csv", "w", encoding="utf-8") as csvfile:
        csvfile.write("Id,Category,Date,Amount,Description\n")
        for records in smartbox_records:
            csvfile.write(records.serialize("smartbox") + "\n")
        for records in tpv_records:
            csvfile.write(records.serialize("ventas") + "\n")
        for records in airbnb_records:
            csvfile.write(records.serialize("airbnb") + "\n")
        for records in multipass_records:
            csvfile.write(records.serialize("multipass") + "\n")
        for records in colectivia_records:
            csvfile.write(records.serialize("colectivia") + "\n")
        for records in other_records:
            csvfile.write(records.serialize("other") + "\n")


if __name__ == "__main__":
    main()
