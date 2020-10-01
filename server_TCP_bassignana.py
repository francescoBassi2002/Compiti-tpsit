
#server UDP 

import socket
import threading

ip = '127.0.0.1'
porta = 2512

#creazione del socket TCP IPv4
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#bind del server per esporlo sulla rete
server.bind((ip, porta))   

#comunicazione dei dati del server all'utente
print(f"\nIl Server è online \t {ip}:{porta}")


def cliente(connessione,ind_client):
    while(True):
        #lettura dati inviati dal client
        data = connessione.recv(4096).decode()  
        #comando di chiusura
        if(data == "close()"):
            break
        #print dei dati all'utente
        print(str(ind_client) + ": \t" + data)    

        #ritorno il risultato al client
        connessione.sendall(data.encode())
    server.close()

def main():
    clienti = []
    while (True):
        server.listen()
        connessione, ind_client = server.accept()
        clienti.append(threading.Thread(target = cliente, args=(connessione,ind_client)))
        clienti[-1].start()
        #chiusura thread
    for c in clienti:
        c.join()

if __name__ == "__main__":
    main()
