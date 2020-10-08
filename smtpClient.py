"""Implementação de um client de SMTP."""

import smtplib
import email.utils
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
from dns_server import dns

ADDR = "127.0.0.1"


def saveSentMessage(nome, msg):
    """Salva a mansagem na pasta de Enviados do remetente"""

    # Cria a pasta de domínio caso não exista
    if not os.path.isdir("dominios/"+nome[1]):
        os.mkdir("dominios/"+nome[1])

    # Cria a pasta do usuáiro caso não exista
    if not os.path.isdir("dominios/"+nome[1]+"/"+nome[0]):
        os.mkdir("dominios/" + nome[1] + "/"+nome[0])
        os.mkdir("dominios/" + nome[1] + "/"+nome[0] + "/Enviados")
        os.mkdir("dominios/" + nome[1] + "/"+nome[0] + "/Inbox")

    # Salva o email propriamente dito
    with open(f"dominios/"+nome[1] + "/" + nome[0] + "/Enviados/"
              + msg.get_all("subject", [])[0].replace(" ", "_")
              + ".txt", "w") as f:
        f.write(msg.as_string())


def sendMessage(msg):
    """Função responsável por enviar as mensagens"""

    for x in msg.get_all('to', []):
        portDest = dns(x.split("@")[-1])
        server = smtplib.SMTP(ADDR, int(portDest))
        # server.set_debuglevel(True)

        server.sendmail(msg.get_all('from', [])[0], msg.get_all('to', []),
                        msg.as_string())
        server.quit()


def main():
    """Função principal do programa"""

    ###########################################################################
    # Pega as entradas do usuário

    emailDestinatario = input("Digite o email do destinatário: ")
    emailRemetente = input("Digite o email do remetente: ")

    corpo = input("Digite o corpo da mensagem: ")
    assunto = input("Digite o assunto: ")

    print("""\nDigite o endereço absoluto dos arquivos a serem anexados.
Em caso de estar no mesmo diretório do executável, basta apenas o nome.
Digite 0 para sair""")

    anexos = []
    while True:
        entrada = input(">>> ")
        if entrada == "0":
            break
        anexos.append(entrada)

    ###########################################################################

    ###########################################################################
    # Usa as informações coletadas pra montar a mensagem

    msg = MIMEMultipart()
    msg["To"] = email.utils.formataddr(("", emailDestinatario))
    msg["From"] = email.utils.formataddr(("", emailRemetente))
    msg["Subject"] = assunto

    msg.attach(MIMEText(corpo, 'plain'))

    for anexo in anexos:
        attachment = open(anexo, 'rb')
        obj = MIMEBase('application', 'octet-stream')
        obj.set_payload((attachment).read())
        encoders.encode_base64(obj)
        obj.add_header('Content-Disposition', "attachment; filename= " +
                       anexo.split("/")[-1])
        msg.attach(obj)

    ###########################################################################

    saveSentMessage(emailRemetente.split("@"), msg)

    sendMessage(msg)


if __name__ == "__main__":
    main()
