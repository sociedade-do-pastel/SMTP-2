import requests as rqt

DIC_DOMINIOS = {}


def getDomains():
    """Abre o arquivo dominios.txt e salva seus elementos em um dicionário"""

    with open("dominios.txt", "r") as f:
        for x in f.readlines():
            domi, addr = x[:-1].split(" ")
            DIC_DOMINIOS[domi] = addr


def dns(domain):
    """Simula o funcionamento de um DNS"""
    getDomains()

    # Checa se o domínio está presente na database offline
    if domain in DIC_DOMINIOS.keys():
        return DIC_DOMINIOS.get(domain)

    # Caso não encontre, procura na internet
    verification = rqt.get("https://{}".format(domain), stream=True)
    if verification.status_code in [404, 400]:
        return "NOT FOUND"

    found_ip = verification.raw._connection.sock.getpeername()
    string_to_send = "{}:{}".format(found_ip[0], found_ip[1])
    DIC_DOMINIOS.update({domain: string_to_send})

    return string_to_send
