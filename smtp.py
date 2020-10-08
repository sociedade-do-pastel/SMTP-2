"""Implementação customizada do servidor SMTP.
Essa implementação NÃO cobre todas suas funcionalidades."""

import smtpd
import asyncore
import os
import email
import sys


def saveReceivedMessage(msg):
    """Salva o email recebido no domínio do servidor"""

    # Pega as informações do email recebido
    nome = msg.split("To: ")[-1].split("@")
    dominio = nome[1].split("\n")[0]
    nome = nome[0]
    assunto = msg.split("Subject: ")[-1].split("\n")[0]

    # Cria o diretório do domínio, caso não exista
    if not os.path.isdir("dominios/"+dominio):
        os.mkdir("dominios/"+dominio)

    # Cria o usuário no domínio, caso não exista
    if not os.path.isdir("dominios/"+dominio+"/"+nome):
        os.mkdir("dominios/"+dominio+"/"+nome)
        os.mkdir("dominios/"+dominio+"/"+nome+"/Enviados")
        os.mkdir("dominios/"+dominio+"/"+nome+"/Inbox")

    # Paths a serem utilizados
    directory = "dominios/"+dominio+"/"+nome+"/Inbox/"
    savedFile = directory + assunto.replace(" ", "_")

    # Cria uma pasta para os anexos usando o assunto, caso não exista
    if not os.path.isdir(savedFile+"_attachments"):
        os.mkdir(savedFile+"_attachments")

    # Salva o email usando o assunto
    with open(savedFile+".txt", "w") as f:
        f.write(msg)

    # Abre o email salvo e resgata seus anexos
    msg = email.message_from_file(open(savedFile+".txt"))
    attachment = msg.get_payload()

    # Salva o corpo da mensagem como anexo
    open(savedFile
         + "_attachments/bodyText.txt",'wb').write(
             attachment[0].get_payload(decode=True))

    # Salva os anexos, convertendo-os
    for x in range(1, len(attachment)):
        open(savedFile+"_attachments/" + attachment[x].get_filename(),
             'wb').write(attachment[x].get_payload(decode=True))


class MySMTPServer(smtpd.SMTPServer):
    """SMTP Server customizado para tratamento manual"""

    def process_message(self, peer, mailfrom, rcpttos, data,
                        mail_options=None, rcpt_options=None):
        saveReceivedMessage(data.decode("UTF-8"))


def main():
    """Script padrão do algoritmo.
Deve receber a porta por argumento."""

    server = MySMTPServer(("127.0.0.1", int(sys.argv[1])), None)
    print(f"Servidor rodando [porta {sys.argv[1]}]")
    asyncore.loop()


if __name__ == "__main__":
    main()
