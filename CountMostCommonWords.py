import time
# Startzeit messen
start_time = time.time()

import csv
import os
os.system("cls")
import sqlite3



class WortAnz:
    def __init__(self, wort, anzahl):
        self.wort = wort
        self.anzahl = anzahl

    def __repr__(self):
        return f"WortAnz(wort='{self.wort}', anzahl={self.anzahl})"
    
wortAnzList = []
    
### Lese Datei
pfad = "C:\\Users\\Andre\\AppData\\Roaming\\Development\\Cousera\\PythonForEverybody\\Projects\\CountMostCommon\\"
# with open(pfad + 'input1.txt', 'r', encoding='utf-8') as file:
#     text = file.read()
with open(pfad + 'input2.txt', 'r', encoding='utf-8') as file:
    text = file.read()

### Filter for text
text = text.lower()
zeichen_liste = ['”', '“', '.', ',', '!', '?', ':', ';', '-', '(', ')', '[', ']', '{', '}', "'", '"', '...', '–', '—', '@', '#', '$', '%', '&', '*', '/', '\\', '|', '~', '`', '^', '<', '>', '=', '+']
for zeichen in zeichen_liste:
    text = text.replace(zeichen, "")

woerter_liste = text.split() # Nehme Text und teile ihn in die einzelnen Worte 

for wort in woerter_liste:
    if len(wort) > 4:
        wortAnzList.append(WortAnz(wort, text.count(wort)))

connection = sqlite3.connect(':memory:') # Erstelle Connection zu In-Memory DB
cursor = connection.cursor() # Erstelle Cursor um DB_Operationen auszuführen
# Erdstlle Tabelle
cursor.execute('''CREATE TABLE WortAnzahlListe (
                    wort TEXT PRIMARY KEY,
                    anzahl INTEGER
                )''')

# Füge mit einer Schleife die Datensätze ein 
for wortAnz in wortAnzList:
    cursor.execute("SELECT COUNT(*) FROM WortAnzahlListe WHERE wort = '" + wortAnz.wort + "'")
    rowsExists = str(cursor.fetchall())
    rowsExists = rowsExists.replace('[(', '')
    rowsExists = rowsExists.replace(',)]', '')
    if int(rowsExists) == 0:        
        cursor.execute("INSERT INTO WortAnzahlListe VALUES ('" + wortAnz.wort + "', " + str(wortAnz.anzahl) + ")")
        connection.commit()

os.system("cls")
print("-----   Jetzt kommt die Liste   -----")
cursor.execute("SELECT * FROM WortAnzahlListe ORDER BY anzahl DESC LIMIT 100")

top100 = []
top100.append("Nr;Name;Anzahl\n")
nr = 1
rows = cursor.fetchall()
for row in rows:
    row = str(row)
    row = row.replace("('", "").replace("',", "").replace(")", "")
    row = row.replace(" ", ";")
    top100.append(str(nr) + ";" + row + "\n")
    nr += 1

# Step 4: Close the database connection
connection.close()

open('C:\\Users\\Andre\\AppData\\Roaming\\Development\\Cousera\\PythonForEverybody\\Projects\\CountMostCommon\\output.csv', 'w').close()
with open('C:\\Users\\Andre\\AppData\\Roaming\\Development\\Cousera\\PythonForEverybody\\Projects\\CountMostCommon\\output.csv', 'a') as f:
    f.writelines(top100)

os.startfile('C:\\Users\\Andre\\AppData\\Roaming\\Development\\Cousera\\PythonForEverybody\\Projects\\CountMostCommon\\output.csv')

# Endzeit messen
end_time = time.time()

# Dauer berechnen
elapsed_time = end_time - start_time
print("--------------------------------------")
print(f"Der Code hat {elapsed_time:.3f} Sekunden gebraucht.")
print("--------------------------------------")