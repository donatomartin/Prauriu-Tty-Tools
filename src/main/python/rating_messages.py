#!/usr/bin/env python3

import csv
from datetime import datetime, timedelta

import pywhatkit as kit
import colorama

colorama.init()

CSV_FILE = 'clients.csv'
DT_FORMAT = '%d/%m/%Y %H:%M:%S'
TODAY = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0) # Get today's date and normalize it to midnight

def getTemplate(template_name):
    with open(f'src/resources/templates/{template_name}.template', encoding='utf-8') as file:
        return file.read()
    
BOOKING_TEMPLATE = getTemplate('booking')
GOOGLE_TEMPLATE = getTemplate('google')

def get_departures(csv_file):
    
    departures_today = []
    
    with open(csv_file, mode='r', encoding='utf-16') as file:
    
        reader = csv.DictReader(file, delimiter="\t")
        
        # Procesar cada fila
        for row in reader:
            
            name = row['Name']
            phone = row['Phone']
            
            if not phone.startswith('+') and phone != '':
                phone = '+34 ' + phone
                
            if phone == '':
                phone = f'{colorama.Fore.RED}NO PHONE{colorama.Fore.RESET}'
            
            departure = datetime.strptime(row['Wyjazd'], DT_FORMAT)
            departure += timedelta(days=1)
            
            if (TODAY == departure):
                departures_today.append([name, phone])
    
    return departures_today

def send_rate_messages(departures):

    vertical_sep = "="*18
    
    print("\n{0}\n DEPARTURES TODAY \n{0}\n".format(vertical_sep))
    
    for i, client in enumerate(departures):
        print("\t", end="")
        print(f"{i}. {client[0]} - {client[1]}")

    not_from_booking_str = input(f"\nSelect which clients are {colorama.Fore.GREEN} not from booking.com {colorama.Fore.RESET} in the list above (separated by commas): ")
    
    not_from_booking_indexes = []
    try:
        not_from_booking_indexes = list(map(int, not_from_booking_str.split(",")))
    except Exception:
        pass

    for i, client in enumerate(departures):
        
        TEMPLATE = BOOKING_TEMPLATE if i not in not_from_booking_indexes else GOOGLE_TEMPLATE
        
        try:
            kit.sendwhatmsg_instantly(client[1], TEMPLATE.format(client[0].strip().split()[0]), tab_close=True)
        except Exception:
            print(f"Error sending message to {client[0]}")

if __name__ == '__main__':
    departures = get_departures(CSV_FILE)
    send_rate_messages(departures)