import threading 
import socket as sck
import sqlite3 as sq

messaggio_errore_senza_percorso = "spiacente, non ci sono percorsi disponibili per le due destinazioni"
mutex = threading.Lock()
mutex.acquire()
database = sq.connect('percorsi.db', 5.0, 0, None, False)
cursore = database.cursor()

threads = []
ip = 'localhost'
port = 6300
tupla = (ip,port)
server = sck.socket(sck.AF_INET, sck.SOCK_STREAM)

class ClientThread (threading.Thread):
    def __init__(self,connessione,tupla):
       threading.Thread.__init__(self)
       self.conn = connessione
       self.tupla_mittente = tupla
    def run(self):       
       
        while(1):
            richiesta = self.conn.recv(4096).decode()
            if(richiesta == 'close'):
                break
            
            inizio = richiesta.split(',')[1]
            fine = richiesta.split(',')[0]
            print(f"client: {self.tupla_mittente}")
            print(f"inizio: {inizio}, fine: {fine}")

            print(f"Istruzione: SELECT percorso FROM percorsi INNER JOIN inizio_fine ON inizio_fine.id_percorso = percorsi.id WHERE (id_start = {inizio}) AND (id_end = {fine})")

            

            cursore.execute(f"SELECT percorso FROM percorsi INNER JOIN inizio_fine ON inizio_fine.id_percorso = percorsi.id WHERE (id_start = {inizio}) AND (id_end = {fine})")
            lista_tuple = cursore.fetchall()

            

            if(len(lista_tuple)==0):
                self.conn.sendto(messaggio_errore_senza_percorso.encode(), tupla)
            else:
                for a in lista_tuple:       
                    print(a) #è una tupla, mi serve solo il primo elemento che è la stringa
                    informazione = a
                        
                self.conn.sendto(informazione[0].encode(), tupla)

            informazione = None
        server.close()




server.bind(tupla)

server.listen()

while(1):
    conn, tupla_mittente = server.accept()
    threads.append(ClientThread(conn,tupla_mittente))
    threads[len(threads)-1].start()

