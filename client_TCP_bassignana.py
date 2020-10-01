#Client UDP 
import socket
ip = '127.0.0.1'
porta = 2512

#socket TCP IPv4
client = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
#bind del server
client.connect((ip,porta))

while(True):
    #chiedo messaggio
    messaggio = input("messaggio: ")
    #lo invio al server
    client.sendall(messaggio.encode())
    #se si scrive "close" si ferma il processo di richiesta del messaggio
    if(messaggio == "close"):
        break
    #lettura del risultato
    risultato = client.recv(4096) 
    #output del risultato
    print("risultato: " + risultato.decode())


client.close()