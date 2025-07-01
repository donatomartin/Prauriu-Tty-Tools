import webbrowser
import urllib.parse
from sys import argv

def send_custom_messages():

    if len(argv) != 2:
        print("Expected 1 argument but received " + len(argv)-1)


    phones = []
    with open(argv[1], encoding="utf-8") as file:

        phones += [x.split(",")[1].replace(" ", "").strip(" ") for x in file.readlines()[1:] if x.split(",")[1]]
    
    for i in range(len(phones)):
        if phones[i][:3] == "+34":
            phones[i] = phones[i][3:] 
        elif phones[i][0] == "+":
            phones[i] = phones[i][1:]
    
    print(phones)

    message = input("\nEnter message:\n\n")
    encoded_message = urllib.parse.quote(message)

    for phone in phones:
        phone = phone.strip()
        url = f"https://web.whatsapp.com/send?phone={phone}&text={encoded_message}"
        webbrowser.open(url)
        print(f"Opened chat with: {phone}")
        input("\nPresiona enter para continuar")

    print("Finished.")

def main():
    send_custom_messages()

if __name__ == "__main__":
    main()
