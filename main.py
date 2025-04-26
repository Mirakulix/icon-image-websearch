import os
import time
from io import BytesIO
import requests
from urllib.parse import urlencode
from googleapiclient.discovery import build

# Google Bildersuche API-Keys
API_KEY = os.getenv("API_KEY")
CSE_ID = os.getenv("CSE_ID")

def search_bilder(query, limit=10):
    service = build("customsearch", "v1", developerKey=API_KEY)
    res = service.cse().list(q=query, cx=CSE_ID, num=limit).execute()
    Bilder = []
    for item in res['items']:
        link = item['link']
        bild = requests.get(link)
        mit_bild = Image.open(BytesIO(bild.content))
        Bilder.append((item['title'], mittel_bild))
    return Bilder

def main():
    # Benutzerfragung
    query = input("Gib einen Suchbegriff ein: ")
    query = query.replace(" ", "+")

    # Suche nach Bildern
    Bilder = search_bilder(query)

    if not Bilder:
        print(f"Keine Bilder gefunden für '{query}'")
        return

    # Vorschau anzeigen und Auswahl treffen
    i = 1
    for titel, bild in Bilder[:10]:
        os.makedirs("./bilder", exist_ok=True)
        bild.save("./bilder/" + titel)
        print(titel)
        input("Drücke eine Taste, um zur nächsten Bild zu gehen...")
        i += 1

    # Benutzerentscheidung treffen
    while True:
        choice = input(f"Beenden Sie die Suche für '{query}' mit 'n' oder suchen Sie weiter mit 'j'? ")
        if choice.lower() == "n":
            break
        elif choice.lower() == "j":
            query = input("Gib einen neuen Suchbegriff ein: ")
            query = query.replace(" ", "+")
            Bilder = search_bilder(query)
            i = 1
            for titel, bild in Bilder[:10]:
                os.makedirs("./bilder", exist_ok=True)
                bild.save("./bilder/" + titel)
                print(titel)
                input("Drücke eine Taste, um zur nächsten Bild zu gehen...")
                i += 1
        else:
            print("Fehlerhafte Eingabe. Bitte versuchen Sie es noch einmal.")

if __name__ == "__main__":
    main()