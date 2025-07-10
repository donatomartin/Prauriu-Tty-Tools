import csv

import colorama
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (PageBreak, Paragraph, SimpleDocTemplate,
                                Spacer, Table, TableStyle)

colorama.init(autoreset=True, strip=False, convert=False)

pdf_output_data = dict()

with open("tax_records_output.csv", newline="", encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:

        if row["Category"] not in pdf_output_data:
            pdf_output_data[row["Category"]] = dict()

        if row["Date"][3:] not in pdf_output_data[row["Category"]]:
            pdf_output_data[row["Category"]][row["Date"][3:]] = []

        pdf_output_data[row["Category"]][row["Date"][3:]].append(
            {
                "Id": row["Id"],
                "Date": row["Date"],
                "Amount": row["Amount"],
                "Description": row["Description"],
            }
        )


# Print formatted data structure
def print_formatted_data():
    for category, records in pdf_output_data.items():
        print(f"\n{colorama.Fore.YELLOW}{"-" * 40}")
        print(f"{colorama.Fore.YELLOW}Category: {category}")
        print(f"{colorama.Fore.YELLOW}{"-" * 40}\n")
        for date, entries in records.items():
            print(f"  {colorama.Fore.BLUE}Date: {date}")
            for entry in entries:
                print(
                    f"{colorama.Fore.BLUE}{entry["Id"]:>4}.{colorama.Fore.RESET} "
                    + f"{entry["Date"]} "
                    + f"{colorama.Fore.GREEN}{entry["Amount"]:>10}€{colorama.Fore.RESET} "
                    + f"   {entry["Description"]}"
                )
            print(
                f"  Total: "
                + f"{colorama.Fore.RED}{sum(float(e['Amount']) for e in entries):.2f}€{colorama.Fore.RESET}\n"
            )


def generate_pdf():
    doc = SimpleDocTemplate("output.pdf", pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()

    # PDF Header
    header_lines = [
        "TITULAR DE LA ACTIVIDAD: MANUEL A. MARTÍN TORNERO (PRAU RÍU)",
        "LOCALIDAD: LLANES",
        "HOJAS DE GESTIÓN DE CAJA",
    ]
    for line in header_lines:
        elements.append(Paragraph(line, styles["Heading4"]))
    elements.append(Spacer(1, 12))

    for category, records in pdf_output_data.items():
        for month, entries in records.items():
            # Add section header
            section_title = f"CATEGORÍA: {category} | MES: {month}"
            elements.append(Paragraph(section_title, styles["Heading5"]))
            elements.append(Spacer(1, 6))

            # Table data: headers
            data = [["FECHA", "CONCEPTO", "COBROS"]]

            # Add entry rows
            for entry in entries:
                data.append(
                    [month, "Estancia Habitación", f'{float(entry["Amount"]):.2f} €']
                )

            # Total
            total = sum(float(e["Amount"]) for e in entries)
            data.append(["", "Total:", f"{total:.2f} €"])

            # Table styling
            table = Table(data, colWidths=[100, 300, 100])
            table.setStyle(
                TableStyle(
                    [
                        ("BACKGROUND", (0, 0), (-1, 0), "#aaaaaa"),
                        ("GRID", (0, 0), (-1, -1), 0.25, "#000"),
                        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                        ("ALIGN", (2, 1), (2, -1), "RIGHT"),
                        ("ALIGN", (0, 0), (-1, 0), "CENTER"),
                        ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
                    ]
                )
            )

            elements.append(table)
            elements.append(Spacer(1, 24))

        elements.append(PageBreak())

    doc.build(elements)


if __name__ == "__main__":
    print_formatted_data()

    if input("Generate PDF? (y/n): ").strip().lower() == "y":
        generate_pdf()
