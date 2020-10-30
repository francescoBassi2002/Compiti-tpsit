import socket as sck
import sqlite3 as sq
ip = 'localhost'
port = 6300
tupla = (ip,port)
server = sck.socket(sck.AF_INET, sck.SOCK_STREAM)
server.bind(tupla)

server.listen()
conn, tupla_mittente = server.accept()

database = sq.connect('percorsi.db')
cursore = database.cursor()

while(1):

    richiesta = conn.recv(4096).decode()
    if(richiesta == 'close'):
        break
    
    inizio = richiesta.split(',')[1]
    fine = richiesta.split(',')[0]

    print(f"inizio: {inizio}, fine: {fine}")

    print(f"SELECT percorso FROM percorsi INNER JOIN inizio_fine ON inizio_fine.id_percorso = percorsi.id WHERE (id_start = {inizio}) AND (id_end = {fine})")

    for a in cursore.execute(f"SELECT percorso FROM percorsi INNER JOIN inizio_fine ON inizio_fine.id_percorso = percorsi.id WHERE (id_start = {inizio}) AND (id_end = {fine})"):
        print(a[0]) #è una tupla, mi serve solo il primo elemento che è la stringa
        informazione = a[0]
    
    
    conn.sendto(informazione.encode(), tupla)


server.close()


