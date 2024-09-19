import csv
from datetime import datetime, timedelta
import pywhatkit as kit
import colorama

colorama.init()

csv_file = 'clients.csv'
datetime_format = '%d/%m/%Y %H:%M:%S'
today = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0) # Get today's date and normalize it to midnight

with open('templates/press.template', encoding='utf-8') as file:
    PRESS_TEMPLATE = file.read()
    
with open('templates/magazines.template', encoding='utf-8') as file:
    MAGAZINES = file.read()

def get_current_clients(csv_file):
    
    current_clients = []
    
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
            
            arrival = datetime.strptime(row['Przyjazd'], datetime_format)
            
            departure = datetime.strptime(row['Wyjazd'], datetime_format)
            departure += timedelta(days=1)
            
            if (arrival <= today <= departure):
                current_clients.append([name, phone])
    
    return current_clients

def send_daily_messages(departures):

    vs = "="*18
    
    print("\n{0}\n CLIENTS TODAY \n{0}\n".format(vs))
    
    for i, client in enumerate(departures):
        print("\t", end="")
        print(f"{i}. {client[0]} - {client[1]}")

    excluded_str = input(f"\nSelect the clients to {colorama.Fore.GREEN} exclude from the daily messages {colorama.Fore.RESET} in the list above (separated by commas): ").strip()
    
    excluded_indexes = []
    try:
        excluded_indexes = list(map(int, excluded_str.split(",")))
    except Exception:
        pass
    
    url_press = input("Paste the Press Folder URL to be included in the message: ")
    
    also_magazines_str = input("Do you want to send the magazines aswell? (y/n): ").strip().lower()
    also_magazines_bool = also_magazines_str == 'y'
    
    if also_magazines_bool:
        url_magazines = input("Paste the Magazines Folder URL to be included in the message: ")

    for i, client in enumerate(departures):
        
        if i in excluded_indexes:
            continue
                
        try:
            kit.sendwhatmsg_instantly(client[1], PRESS_TEMPLATE.format(client[0].strip().split()[0], url_press), tab_close=True)
            
            if also_magazines_bool:
                kit.sendwhatmsg_instantly(client[1], MAGAZINES.format(url_magazines), tab_close=True)
            
        except Exception:
            print(f"Error sending message to {client[0]}")

if __name__ == '__main__':
    departures = get_current_clients(csv_file)
    send_daily_messages(departures)