#!/usr/bin/env python3

import csv
from datetime import datetime

import pywhatkit as kit
import colorama

colorama.init()

CSV_FILE = 'clients.csv'
DT_FORMAT = '%d/%m/%Y %H:%M:%S'
TODAY = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0) # Get today's date and normalize it to midnight

def getTemplate(template_name):
    with open(f'src/resources/templates/{template_name}.template', encoding='utf-8') as file:
        return file.read()
    
WELCOME_TEMPLATE = getTemplate('welcome')

def get_arrivals(csv_file):
    
    arrivals_today = []
    
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
            
            arrival = datetime.strptime(row['Przyjazd'], DT_FORMAT)
            
            if (TODAY == arrival):
                arrivals_today.append([name, phone])
    
    return arrivals_today

def send_welcome_messages(departures):

    vertical_sep = "="*18
    
    print("\n{0}\n ARRIVALS TODAY \n{0}\n".format(vertical_sep))
    
    for i, client in enumerate(departures):
        print("\t", end="")
        print(f"{i}. {client[0]} - {client[1]}")

    excluded_str = input(f"\nSelect the clients to {colorama.Fore.GREEN} exclude from the welcome messages {colorama.Fore.RESET} in the list above (separated by commas): ").strip()
    
    excluded_indexes = []
    try:
        excluded_indexes = list(map(int, excluded_str.split(",")))
    except Exception:
        pass

    for i, client in enumerate(departures):
        
        if i in excluded_indexes:
            continue
                
        try:
            kit.sendwhatmsg_instantly(client[1], WELCOME_TEMPLATE.format(client[0].strip().split()[0]), tab_close=True)
        except Exception:
            print(f"Error sending message to {client[0]}")

if __name__ == '__main__':
    departures = get_arrivals(CSV_FILE)
    send_welcome_messages(departures)