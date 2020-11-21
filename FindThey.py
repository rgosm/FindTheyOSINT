import re
import sys
import argparse
import threading
import requests
from datetime import datetime

log = open("log.txt", "w")
log.close()

try:
    from googlesearch import search
except ImportError:
    print("A biblioteca Google não está instalada, digite 'pip install google' para instala-la")


def main():
    parser = argparse.ArgumentParser(description='FindTheyOSINT-- '
                                                 '\n--> Digite um ou dois dados a respeito do alvo para que seja realizada a busca'
                                                 '\n--> Adicione novos sites a lista siteusers adionando _user onde normalmente estaria o '
                                                 'nome de usuário'
                                                 '\n--> Adicione novos sites para realizar buscas convencionais na lista sitelist')
    parser.add_argument('-n', "--nome",
                        required=False,
                        help="Nome do alvo a ser procurado")

    parser.add_argument('-e', "--email",
                        required=False,
                        help="E-mail do alvo a ser procurado")

    parser.add_argument('-N', "--docnum",
                        required=False,
                        help="Numero de algum documento do alvo a ser procurado")

    parser.add_argument('-s', "--site",
                        required=False,
                        help="Site onde procurar. Uma lista com -l pode tornar a pesquisa mais confiavel")

    parser.add_argument('-l', "--list",
                        required=False,
                        help="Especifique a lista de sites onde será realizada a pesquisa. Temos uma disponivel, para usa-la digite '-l sitelist.txt'")

    args = parser.parse_args()

    if args.nome is None:
        args.nome = " "
    if args.email is None:
        args.email = " "
    if args.docnum is None:
        args.docnum = " "

    emailSplit = args.email.split("@")
    username = re.sub(r'[^0A-Za-z0-9]', '', emailSplit[0])

    def simples():
        pesquisar1 = "allintext: " + args.nome + " " + args.email + " " + args.docnum

        for jm in search(pesquisar1, tld='com', lang='en', num=7, start=0, stop=15, pause=2):
            log = open("log.txt", "a")
            horalocal = datetime.now()
            datalocal = horalocal.strftime('%d/%m/%Y %H:%M:%S')
            log.write(datalocal + " " + jm + "\n")
            log.close()
            print(jm + "\n")

    def complicada():
        opcoes = [emailSplit[0], args.email, args.docnum, username]
        for item in opcoes:
            pesquisar2 = "allintext: " + item

            for lm in search(pesquisar2, tld='com', lang='en', num=7, start=0, stop=15, pause=2):
                log = open("log.txt", "a")
                horalocal = datetime.now()
                datalocal = horalocal.strftime('%d/%m/%Y %H:%M:%S')
                log.write(datalocal + " " + lm + "\n")
                log.close()
                print(lm + "\n")

    def listaSites():
        lista = open(args.list, 'r')
        for linha in lista:
            pesquisar3 = "allintext:" + args.nome + " " + args.email + " " + args.docnum + " " + "site:" + linha

            for m in search(pesquisar3, tld='com', lang='en', num=7, start=0, stop=15, pause=2):
                log = open("log.txt", "a")
                horalocal = datetime.now()
                datalocal = horalocal.strftime('%d/%m/%Y %H:%M:%S')
                log.write(datalocal + " " + m + "\n")
                log.close()
                print(m + "\n")

            opcoes = [args.email, args.docnum, emailSplit[0], username]
            for item in opcoes:
                pesquisar2 = "allintext: " + item + " " + "site: " + linha

                for ln in search(pesquisar2, tld='com', lang='en', num=7, start=0, stop=15, pause=2):
                    log = open("log.txt", "a")
                    horalocal = datetime.now()
                    datalocal = horalocal.strftime('%d/%m/%Y %H:%M:%S')
                    log.write(datalocal + " " + ln + "\n")
                    log.close()

    def sitesUsers():
        lista = open('siteusers.txt', 'r')
        for linha in lista:
            site = re.sub(r'_user', username, linha)
            try:
                request = requests.get(site, verify=True)
                if str(request) == "<Response [200]>":
                    logsitesusers = open("log.txt", "a")
                    horalocal = datetime.now()
                    datalocal = horalocal.strftime('%d/%m/%Y %H:%M:%S')
                    logsitesusers.write(datalocal + " " + site + "\n")
            except:
                request = requests.get(site, verify=False)
                if str(request) == '<Response [200]>':
                    horalocal = datetime.now()
                    datalocal = horalocal.strftime('%d/%m/%Y %H:%M:%S')
                    logsitesusers = open("log.txt", "a")
                    logsitesusers.write(datalocal + " " + site + "\n")

    t1 = threading.Thread(target=simples)
    t2 = threading.Thread(target=complicada)
    t3 = threading.Thread(target=listaSites)
    t4 = threading.Thread(target=sitesUsers)

    if args.site is None:
        t1.start()
        t2.start()
    elif args.list is not None:
        t3.start()
    else:
        pesquisar = "allintext: " + args.nome + " " + args.email + " " + args.docnum + " " + "site: " + args.site
        for j in search(pesquisar, tld='com', lang='en', num=7, start=0, stop=15, pause=2):
            log = open("log.txt", "a")
            log.write(j + "\n")
            log.close()

    if args.email is not None:
        t4.start()


if __name__ == '__main__':
    sys.exit(main())
