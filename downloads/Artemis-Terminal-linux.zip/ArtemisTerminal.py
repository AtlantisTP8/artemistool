logo = """

 █████╗ ██████╗ ████████╗███████╗███╗   ███╗██╗███████╗
██╔══██╗██╔══██╗╚══██╔══╝██╔════╝████╗ ████║██║██╔════╝
███████║██████╔╝   ██║   █████╗  ██╔████╔██║██║███████╗
██╔══██║██╔══██╗   ██║   ██╔══╝  ██║╚██╔╝██║██║╚════██║
██║  ██║██║  ██║   ██║   ███████╗██║ ╚═╝ ██║██║███████║
╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═╝     ╚═╝╚═╝╚══════╝

"""

print(logo)

import requests
import webbrowser
import socket
import random
import string
import hashlib
import os
import platform
import re
import importlib
from collections import Counter
from datetime import datetime
from bs4 import BeautifulSoup

url = input("URL: ")

html = requests.get(url).text

print(html)

os.system("color 0a")
plugins = {}

def temizle():
        os.system('cls' if os.name == 'nt' else 'clear')


def source():

    url = input("URL gir: ")

    try:

        response = requests.get(url)

        soup = BeautifulSoup(response.text, "html.parser")

        print(soup.prettify())

    except Exception as e:
        print(e)

def passwordcreator():
        
    while True:
        try:

            password = input("Şifrenizde özel karakter istiyormusunuz").lower().strip()
            
            if password == "evet":
        
                sifre = ""
                kelimelist = string.ascii_letters + string.digits + string.punctuation
                
                uzunluk = int(input("Bi rakam giriniz: "))

                for i in range(uzunluk):
                    harf = random.choice(kelimelist)
                    sifre += harf
            
                print(sifre)

            elif password == "hayır":

                sifre = ""
                kelimelist = string.ascii_letters + string.digits
                
                uzunluk = int(input("Bi rakam giriniz: "))

                for i in range(uzunluk):
                    harf = random.choice(kelimelist)
                    sifre += harf
            
                print(sifre)

            else:
                print("Evet yada Hayır giriniz")

            komut = input("Devam etmek için ENTER | Çıkmak için exit : ")
            if komut in ["exit", "h"]:
                break
            
        except ValueError:
            print("Lütfen Sayı Girin.")

        except Exception as e:
            print(e)
                



def hash_tool():
        
    while True:
        try:

            metin = input("Hashlemek Istediginiz metni giriniz: ")

            sha256_hash = hashlib.sha256(metin.encode()).hexdigest()
            md5_hash = hashlib.md5(metin.encode()).hexdigest()

            print(f"MD5: {md5_hash}")
            print(f"SHA256: {sha256_hash}")

            komut = input("Devam etmek için ENTER | Çıkmak için exit : ")
            if komut in ["exit", "h"]:
                break
                
        except ValueError:
            print("Lütfen Metin Girin.")

        except Exception as e:
            print(e)
            


def system_Info():
    try:

        print(platform.system())
        print(platform.processor())
        print(platform.python_version())
        print(os.getcwd())
            
    except ValueError:
        print("Lütfen Metin Girin.")

    except Exception as e:
        print(e)

def network():
    os.system("ipconfig")
        
def python_version():
    print(platform.python_version())

def VCC():
    while True:
        domain = input("Domain giriniz: ")

        if domain == "exit":
            break

        try:
            ip_adresi = socket.gethostbyname(domain)

            print(f"{domain} adresinin IP'si: {ip_adresi}")

        except socket.gaierror:
            print("Domain bulunamadi")

        except Exception as e:
            print(e)

def RYY():
    ip = input("Hedefin ip adresini giriniz: ")

    for port in range(20,101):
    
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.1)

        result = sock.connect_ex((ip, port))
        if result == 0:
            print(f"Port {port} açık")
        sock.close()

def ping():

    hedef = input("IP veya domain giriniz: ").strip()

    pattern = r"^[a-zA-Z0-9.-]+$"

    if re.match(pattern, hedef):

        if os.name == "nt":
            os.system(f"ping {hedef}")
        else:
            os.system(f"ping -c 4 {hedef}")

    else:
        print("Geçersiz hedef")

def saat():
    print(datetime.now())

def ls():
    print(os.listdir())

def mkdir():
    try:
        klasor = input("Klasor adi: ")
        os.mkdir(klasor)
        print("Klasor olusturuldu")
    except FileExistsError:
        print("Bu klasor zaten var")
    except Exception as e:
        print(e)

def cd():
    try:
        yol = input("Yol gir: ")
        os.chdir(yol)
    except FileNotFoundError:
        print("Klasor bulunamadi")
    except Exception as e:
        print(e)

def pwd():
    print(os.getcwd())

def banner():
    print(logo)

def prompt():
    kullanici = os.getlogin()
    klasor = os.getcwd()
    return f"{kullanici}@artemis:{klasor}$"

def cat():
    dosya = input("Dosya adı: ")

    try:
        with open(dosya, "r", encoding="utf-8") as f:
            print(f.read())

    except FileNotFoundError:
        print("Dosya Bulunamadı")
        
def rm():
    dosya = input("Silinecek dosya: ")

    try:
        os.remove(dosya)
        print("Dosya silindi")

    except FileNotFoundError:
        print("Dosya bulunamadı")

def run():
    dosya = input("PY dosyasının adını giriniz: ")
    os.system(f"python {dosya}")

def load_plugins():

    plugin_klasoru = "plugins"

    if not os.path.exists(plugin_klasoru):
        os.mkdir(plugin_klasoru)

    for dosya in os.listdir(plugin_klasoru):

        if dosya.endswith(".py"):

            plugin_adi = dosya[:-3]

            try:

                module = importlib.import_module(f"plugins.{plugin_adi}")

                plugins[plugin_adi] = module

                print(f"[PLUGIN LOADED] {plugin_adi}")

            except Exception as e:

                print(f"[PLUGIN ERROR] {plugin_adi} -> {e}")

def search():
    site_adi = input("Şirket Adı: ")

    webbrowser.open(f"https://google.com/search?q = (site_adi)")


load_plugins()
history = []

while True:

    os.system("color 0a")

    try:
        komut = input(prompt()).lower().strip()
        history.append(komut)
        parcalar = komut.split()

        parcalar = komut.split()

        if len(parcalar) > 0:
            komut_adi = parcalar[0]
            argumanlar = parcalar[1:]


    except ValueError:
        print("Lütfen Sayı Gir")
        continue
    except Exception as n :
        print(n)

    match komut_adi:
        
        case "password":
            passwordcreator()

        case "hash":
            hash_tool()

        case "systeminfo":
            system_Info()

        case "clear":
            temizle()
            banner()

        case "exit":
            break
        
        case "help":
            print("""
        password --- sifre uretir
        hash --- hash olusturur
        systeminfo --- sistem bilgisi verir
        clear --- ekrani temizler
        exit --- cikis yapar
        network --- tum aglari listeler
        python --- python surumunu yazdirir
        VCC --- WEB ip bulmak icin
        RYY --- PORT taramak icin
        ping --- hedefe ping atmak icin
        history --- kullanilan komutlari gormek icin
        saat --- saati gormek icin
        cd
        ls
        mkdir
        pwd
        cat
        rm
        run
        """)
            
        case "network":
            network()

        case "python":
            python_version()

        case "vcc":
            VCC()

        case "ryy":
            RYY()

        case "history":
            print(history)

        case "saat":
            saat()

        case "ls":
            ls()

        case "mkdir":
            mkdir()

        case "cd":
            cd()

        case "pwd":
            pwd()

        case "ping":
            ping()

        case "cat":
            cat()

        case "rm":
            rm()

        case _:

            if komut in plugins:

                try:
                    plugins[komut].run()

                except Exception as e:
                    print(e)

            else:
                os.system(komut)
        
