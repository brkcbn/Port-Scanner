import socket
import argparse
import requests
import sys
from bs4 import BeautifulSoup

# python PortTarama.py -h
# python PortTarama.py -ip 192.168.1.0-192.168.1.255
# python PortTarama.py -ip 192.168.1.0-192.168.1.255 -v True

ipAddressList = []
port = 80


def scanPort(start_ip, finish_ip, v):
    st_ip = int(start_ip[3])
    fn_ip = int(finish_ip[3])

    for i in range(st_ip, fn_ip+1):
        ip = start_ip[0] + "." + start_ip[1] + "." + start_ip[2] + "." + str(i)
        addBanner(ip)

        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1.2)
            resp = s.connect_ex((ip, port))

            if resp == 0:
                print("Port {} OPEN, IP adresi : {} ".format(port, ip))
                writeToReport(ip, port)
                s.close()

            if v:
                http = "http://" + ip + "/" + "80"
                title = str(getHTTPTitle(http))
                print("IP = " + http + " Title = " + title)
                writeToHTTPReport(http, title)

        except KeyboardInterrupt:
            print("CTRL+C ile process sonlandirildi.")
            sys.exit()
        except socket.error:
            print("Hedef IP'ye baglanilamadi. IP : {}".format(ip))
            sys.exit()


def getHTTPTitle(conn):
    r = requests.get(conn)
    source = BeautifulSoup(r.content, "html.parser")
    return source.title


def addBanner(ip):
    print("Taranan IP : {}".format(ip))


def writeToReport(ip, port):
    with open("portTaramaRaporu.txt", "a") as file:
        file.write(str(ip) + ":" + str(port) + " OPEN" + "\n")

def writeToHTTPReport(http, title):
    with open("portVeHTTPTitleRaporu.txt", "a") as file:
        file.write(http + " -- " + " OPEN" + " -- Title : " + title + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-ip", required=True, help="IP baslangic ve bitisini belirtiniz. Ornek : 192.168.1.0-192.168.1.255")
    parser.add_argument("-v", help="TCP port 80 HTTP sayfasinin title bilgisini yazdir. (-v True)", type=bool)

    args = parser.parse_args()

    for i in args.ip.split("-"):
        ipAddressList.append(i)

    ip_start = str(ipAddressList[0]).split(".")
    ip_finish = str(ipAddressList[1]).split(".")

    scanPort(ip_start, ip_finish, args.v)
