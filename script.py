"""Script para teste da implementação do servidor SMTP.
Permite as operações de criação de servidores e escrita de emails.
Os emails podem ser visualizados dentro de seus arquivos."""

import time
import threading
import asyncore
import smtpClient
import smtp

ADDR = "127.0.0.1"


def writeDomains(servers):
    """Salva os domínios no arquivo dominios.txt, que servirá de data base"""

    with open("dominios.txt", "w") as f:
        for x in servers:
            f.write(x+"\n")


def startServer(port):
    """Inicia os servidores com as portas inseridas pelo usuário"""

    server = smtp.MySMTPServer((ADDR, int(port)), None)
    print(f"Servidor rodando [porta {port}]")
    asyncore.loop()


def main():
    """Script principal do algoritmo"""

    ###########################################################################
    # Entrada de dados do usuário

    qtServ = int(input("Digite a quantidade de servidores que deseja: "))

    print("""Digite o domínio e porta de cada servidor:
Exemplo: \"email.com 5050\"\n""")
    servers = []
    for x in range(qtServ):
        servers.append(input(f"Servidor {x+1}>> "))

    ###########################################################################

    writeDomains(servers)       # Salva os domínios para consulta pelo DNS

    # Cria threads para cada servidor
    threads = []
    for x in servers:
        threads.append(threading.Thread(target=startServer,
                                        args=(x.split(" ")[1],)))

    # Inicia as threads
    print()
    for x in threads:
        x.start()

    time.sleep(1)               # Delay por motivos de sincronização de output

    # Dará continuamente a opção de produzir um novo email
    while True:
        print("""
#################### Novo Email ####################""")
        smtpClient.main()       # Utiliza o client pra produzir o email


if __name__ == "__main__":
    main()
