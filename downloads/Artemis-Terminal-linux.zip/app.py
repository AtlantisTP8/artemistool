from flask import Flask
from flask import render_template
from flask import request
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from flask import Flask, render_template, request, jsonify
from datetime import datetime
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address


from prompts import SYSTEM_PROMPT

import subprocess
import requests
import ollama
import whois
import dns.resolver
import socket
import ssl
import re
import os
import tempfile
import psutil
import winreg
import hashlib

API_KEY = "AJGH572KSBNF462HHBV5"

app = Flask(__name__)

ALLOWED_IPS = [
    "127.0.0.1"
]

limiter = Limiter(
    get_remote_address,
    app=app
)

def ip_allowed():

    ip = request.remote_addr

    if ip in ALLOWED_IPS:
        return True

    return False

def check_auth():
    key = request.headers.get("X-API-Key")

    if key != API_KEY:
        return False

    return True

@app.route("/recon")
def recon():

    if not check_auth():
        return jsonify({
            "error": "unauthorized"
        }), 401

    return {"ok": True}

@app.route("/login", methods=["POST"])
def login():

    data = request.json

    if (
        data["username"] == USERNAME
        and
        data["password"] == PASSWORD
    ):
        return {"ok": True}

    return {"ok": False}

@app.route("/")
def home():

    return render_template("index.html")

@app.route("/source")
def source():

    site = request.args.get("site")


    try:

        if not site.startswith("http"):
            site = "https://" + site

        response = requests.get(site)

        html = response.text.lower()

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        title = soup.title.string if soup.title else "Yok"

        teknolojiler = []

        if "react" in html:
            teknolojiler.append("React")

        if "vue" in html:
            teknolojiler.append("Vue")

        if "next" in html:
            teknolojiler.append("Next.js")

        if "wordpress" in html:
            teknolojiler.append("WordPress")

        if "bootstrap" in html:
            teknolojiler.append("Bootstrap")

        if "cloudflare" in html:
            teknolojiler.append("Cloudflare")

        scripts = []

        for script in soup.find_all("script"):

            src = script.get("src")

            if src:
                scripts.append(src)

        css_files = []

        for css in soup.find_all("link"):

            href = css.get("href")

            if href:
                css_files.append(href)

        sonuc = f"""

========================
TEKNOLOJILER
========================

"""
        for tech in teknolojiler:
            sonuc += f"{tech}\n"

        sonuc += f"""

========================
ARTEMIS SOURCE ANALYZER
========================

SITE:
{site}

TITLE:
{title}

========================
JAVASCRIPT
========================

"""

        for js in scripts[:15]:
            sonuc += f"{js}\n"

        sonuc += f"""

========================
CSS
========================

"""

        for css in css_files[:15]:
            sonuc += f"{css}\n"

        return sonuc

    except Exception as e:

        return str(e)
    
    
    
    


@app.route("/ai", methods=["POST"])
def ai():

    data = request.json

    prompt = data.get("prompt")

    try:

        response = ollama.chat(

            model="llama3",

            messages=[

                {
                    "role":"system",

                    "content": SYSTEM_PROMPT
                },

                {
                    "role":"user",
                    "content":prompt
                }
            ]
        )

        cevap = response["message"]["content"]

        return cevap

    except Exception as e:

        return str(e)
    


@app.route("/cloudflare")
def cloudflare():

    site = request.args.get("site")

    try:

        if not site.startswith("http"):
            site = "https://" + site

        response = requests.get(
            site,
            timeout=5
        )

        server = response.headers.get(
            "server",
            ""
        ).lower()

        cf = response.headers.get(
            "cf-ray"
        )

        if "cloudflare" in server or cf:

            return f"""

☁️ CLOUDFLARE TESPİT EDİLDİ

Site:
{site}

Koruma:
AKTİF

Server:
{server}

"""

        else:

            return f"""

✓ CLOUDFLARE YOK

Site:
{site}

"""

    except Exception as e:

        return str(e)


@app.route("/analyze")
def analyze():

    site = request.args.get("site")

    try:

        if not site.startswith("http"):
            site = "https://" + site

        response = requests.get(site)

        html = response.text.lower()

        teknolojiler = []

        if "react" in html:
            teknolojiler.append("React")

        if "vue" in html:
            teknolojiler.append("Vue")

        if "next" in html:
            teknolojiler.append("Next.js")

        if "bootstrap" in html:
            teknolojiler.append("Bootstrap")

        if "wordpress" in html:
            teknolojiler.append("WordPress")

        if "cloudflare" in html:
            teknolojiler.append("Cloudflare")

        skor = 100

        riskler = []

        headers = response.headers

        if "X-Frame-Options" not in headers:
            skor -= 10
            riskler.append("X-Frame-Options eksik")

        if "Content-Security-Policy" not in headers:
            skor -= 15
            riskler.append("CSP eksik")

        if "Strict-Transport-Security" not in headers:
            skor -= 10
            riskler.append("HSTS eksik")

        sonuc = {
            "site": site,
            "guvenlik_skoru": skor,
            "teknolojiler": teknolojiler,
            "riskler": riskler
        }

        return sonuc

    except Exception as e:
        return {"hata": str(e)}
    

@app.route("/whois")
def whois_lookup():

    domain = request.args.get("domain")

    try:

        w = whois.whois(domain)

        return {
            "domain": domain,
            "registrar": str(w.registrar),
            "creation_date": str(w.creation_date),
            "expiration_date": str(w.expiration_date),
            "name_servers": str(w.name_servers)
        }

    except Exception as e:
        return {"hata": str(e)}
    
@app.route("/dns")
def dns_lookup():

    domain = request.args.get("domain")

    sonuc = {}

    try:

        kayitlar = ["A","MX","TXT","NS","CNAME"]

        for tip in kayitlar:

            try:

                answers = dns.resolver.resolve(domain, tip)

                sonuc[tip] = [str(r) for r in answers]

            except:
                sonuc[tip] = []

        return sonuc

    except Exception as e:
        return {"hata": str(e)}
    
@app.route("/network")
def network():

    site = request.args.get("site")

    try:

        if not site.startswith("http"):
            site = "https://" + site

        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        response = requests.get(
            site,
            headers=headers,
            timeout=5
        )

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        kaynaklar = []

        for tag in soup.find_all(["script","link","img"]):

            src = (
                tag.get("src")
                or tag.get("href")
            )

            if src:

                tam_url = urljoin(site, src)

                kaynaklar.append(tam_url)

        return {
            "istek_sayisi": len(kaynaklar),
            "kaynaklar": kaynaklar[:50]
        }

    except Exception as e:
        return {
            "hata": str(e)
        }
    
@app.route("/cookies")
def cookies():

    site = request.args.get("site")

    try:

        if not site.startswith("http"):
            site = "https://" + site

        response = requests.get(site)

        cookies = []

        for c in response.cookies:

            cookies.append({
                "isim": c.name,
                "secure": c.secure
            })

        return {
            "cookies": cookies
        }

    except Exception as e:
        return {"hata": str(e)}
    
@app.route("/headers")
def headers():

    site = request.args.get("site")
    response = requests.get(site)

    try:

        response = requests.get(site)

        headers = dict(response.headers)

        return headers

    except Exception as e:

        return {"error": str(e)}
    
@app.route("/tech")
def tech():

    site = request.args.get("site")

    try:

        response = requests.get(site)

        html = response.text.lower()

        bulunanlar = []

        if "react" in html:
            bulunanlar.append("React")

        if "vue" in html:
            bulunanlar.append("Vue")

        if "angular" in html:
            bulunanlar.append("Angular")

        if "bootstrap" in html:
            bulunanlar.append("Bootstrap")

        if "jquery" in html:
            bulunanlar.append("jQuery")

        server = response.headers.get("server", "")

        if "cloudflare" in server.lower():
            bulunanlar.append("Cloudflare")

        if "nginx" in server.lower():
            bulunanlar.append("Nginx")

        if "apache" in server.lower():
            bulunanlar.append("Apache")

        return {
            "site": site,
            "technologies": bulunanlar
        }

    except Exception as e:

        return {
            "error": str(e)
        }
    
@app.route("/subdomains")
def subdomains():

    domain = request.args.get("domain")

    sublar = [

        "www",
        "mail",
        "api",
        "admin",
        "test",
        "dev",
        "panel",
        "cdn",
        "beta"

    ]

    bulunanlar = []

    for sub in sublar:

        host = f"{sub}.{domain}"

        try:

            socket.gethostbyname(host)

            bulunanlar.append(host)

        except:
            pass

    return {
        "subdomains": bulunanlar
    }

@app.route("/security")
def security():

    site = request.args.get("site")

    response = requests.get(site)

    headers = response.headers

    security_headers = {

        "Content-Security-Policy":
        headers.get("Content-Security-Policy"),

        "Strict-Transport-Security":
        headers.get("Strict-Transport-Security"),

        "X-Frame-Options":
        headers.get("X-Frame-Options"),

        "X-Content-Type-Options":
        headers.get("X-Content-Type-Options")

    }

    return security_headers

@app.route("/adminfinder")
def adminfinder():

    site = request.args.get("site")

    if not site.startswith("http"):
        site = "https://" + site

    yollar = [

        "admin",
        "login",
        "panel",
        "dashboard",
        "cpanel",
        "adminpanel",
        "moderator",
        "user"

    ]

    bulunanlar = []

    for yol in yollar:

        url = f"{site}/{yol}"

        try:

            response = requests.get(
                url,
                timeout=3
            )

            if response.status_code == 200:

                bulunanlar.append({

                    "url":url,
                    "status":response.status_code

                })

        except:
            pass

    return {
        "bulunanlar": bulunanlar
    }

@app.route("/robots")
def robots():

    site = request.args.get("site")

    if not site.startswith("http"):
        site = "https://" + site

    try:

        response = requests.get(
            site + "/robots.txt"
        )

        return response.text

    except Exception as e:

        return str(e)
    
@app.route("/portscan")
@limiter.limit("5 per minute")
def portscan():
    
    

    host = request.args.get("host")

    bulunanlar = []

    for port in range(1,1025):

        sock = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )

        sock.settimeout(0.3)

        result = sock.connect_ex(
            (host, port)
        )

        if result == 0:

            bulunanlar.append(port)

        sock.close()

        if not check_auth():
            return {
                "error": "unauthorized"
            }, 401

        return {
            "ok": True
        }

    return {
        "open_ports": bulunanlar
    }

    



@app.route("/protection")
def protection():

    site = request.args.get("site")

    try:

        if not site.startswith("http"):
            site = "https://" + site

        response = requests.get(site, timeout=5)

        headers = response.headers

        protections = []

        # CLOUDFLARE

        server = headers.get("server", "").lower()

        if "cloudflare" in server or headers.get("cf-ray"):
            protections.append("☁️ Cloudflare")

        # SECURITY HEADERS

        if "Content-Security-Policy" in headers:
            protections.append("🛡️ CSP Protection")

        if "Strict-Transport-Security" in headers:
            protections.append("🔒 HSTS")

        if "X-Frame-Options" in headers:
            protections.append("🪟 X-Frame-Options")

        if "X-Content-Type-Options" in headers:
            protections.append("📦 X-Content-Type-Options")

        if "Referrer-Policy" in headers:
            protections.append("🔗 Referrer Policy")

        if "Permissions-Policy" in headers:
            protections.append("⚙️ Permissions Policy")

        if "Cross-Origin-Opener-Policy" in headers:
            protections.append("🌍 COOP")

        if "Cross-Origin-Embedder-Policy" in headers:
            protections.append("🧩 COEP")

        if "Cross-Origin-Resource-Policy" in headers:
            protections.append("📡 CORP")

        if "set-cookie" in headers:
            protections.append("🍪 Secure Cookies")

        if not protections:
            protections.append("❌ Koruma bulunamadı")

        return {
            "site": site,
            "protections": protections
        }

    except Exception as e:

        return {
            "error": str(e)
        }
    
@app.route("/ssl")
def ssl_info():

    domain = request.args.get("domain")

    try:

        context = ssl.create_default_context()

        with context.wrap_socket(
            socket.socket(),
            server_hostname=domain
        ) as s:

            s.settimeout(5)

            s.connect((domain, 443))

            cert = s.getpeercert()

        return {

            "domain": domain,

            "issuer": str(cert.get("issuer")),

            "subject": str(cert.get("subject")),

            "version": cert.get("version"),

            "expires": cert.get("notAfter")

        }

    except Exception as e:

        return {
            "error": str(e)
        }
    
@app.route("/jsextract")
def jsextract():

    site = request.args.get("site")

    try:

        if not site.startswith("http"):
            site = "https://" + site

        response = requests.get(site)

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        js_files = []

        for script in soup.find_all("script"):

            src = script.get("src")

            if src:

                if src.startswith("http"):

                    js_files.append(src)

                else:

                    js_files.append(
                        urljoin(site, src)
                    )

        bulunanlar = []

        pattern = r'\/[A-Za-z0-9_\-\/]+'

        for js in js_files[:10]:

            try:

                js_content = requests.get(
                    js,
                    timeout=3
                ).text

                matches = re.findall(
                    pattern,
                    js_content
                )

                for m in matches:

                    if len(m) > 5:

                        bulunanlar.append(m)

            except:
                pass

        bulunanlar = list(set(bulunanlar))

        return {
            "site": site,
            "endpoints": bulunanlar[:50]
        }

    except Exception as e:

        return {
            "error": str(e)
        }
    
@app.route("/surface")
def surface():

    site = request.args.get("site")

    try:

        if not site.startswith("http"):
            site = "https://" + site

        response = requests.get(site)

        headers = response.headers

        risks = []

        score = 100

        # CSP

        if "Content-Security-Policy" not in headers:

            risks.append({
                "risk":"CSP eksik",
                "level":"MEDIUM"
            })

            score -= 15

        # HSTS

        if "Strict-Transport-Security" not in headers:

            risks.append({
                "risk":"HSTS eksik",
                "level":"MEDIUM"
            })

            score -= 10

        # XFO

        if "X-Frame-Options" not in headers:

            risks.append({
                "risk":"Clickjacking koruması yok",
                "level":"LOW"
            })

            score -= 10

        # COOKIE

        cookies = response.headers.get(
            "Set-Cookie",
            ""
        )

        if "Secure" not in cookies:

            risks.append({
                "risk":"Secure Cookie eksik",
                "level":"HIGH"
            })

            score -= 20

        # SERVER

        server = headers.get(
            "server",
            ""
        )

        if server:

            risks.append({
                "risk":f"Server bilgisi açık: {server}",
                "level":"LOW"
            })

        return {

            "site": site,

            "security_score": score,

            "risks": risks
        }

    except Exception as e:

        return {
            "error": str(e)
        }
    
@app.route("/sensitive")
def sensitive():

    site = request.args.get("site")

    try:

        if not site.startswith("http"):
            site = "https://" + site

        paths = [

            ".env",
            ".git",
            "backup.zip",
            "config.json",
            "debug.log",
            ".env.bak",
            "phpinfo.php",
            "admin.bak",
            "database.sql",
            "dump.sql"

        ]

        bulunanlar = []

        for path in paths:

            url = f"{site}/{path}"

            try:

                response = requests.get(
                    url,
                    timeout=3
                )

                if response.status_code in [200,401,403]:

                    bulunanlar.append({

                        "file": path,
                        "status": response.status_code

                    })

            except:
                pass

        return {

            "site": site,

            "found": bulunanlar

        }

    except Exception as e:

        return {

            "error": str(e)

        }
    
@app.route("/advisor")
def advisor():

    site = request.args.get("site")

    try:

        if not site.startswith("http"):
            site = "https://" + site

        response = requests.get(site)

        headers = response.headers

        analiz = []

        if "Content-Security-Policy" not in headers:

            analiz.append(
                "CSP eksik"
            )

        if "Strict-Transport-Security" not in headers:

            analiz.append(
                "HSTS eksik"
            )

        if "X-Frame-Options" not in headers:

            analiz.append(
                "X-Frame-Options eksik"
            )

        cookies = headers.get(
            "Set-Cookie",
            ""
        )

        if "Secure" not in cookies:

            analiz.append(
                "Secure cookie kullanılmıyor"
            )

        prompt = f"""
Sadece aşağıdaki güvenlik bulgularını yorumla.

BULGULAR:
{analiz}

Kurallar:
- Türkçe Yaz
- Yeni açık UYDURMA
- Sadece verilen bulguları yorumla
- Eğer bulgu yoksa:
"Sistem güvenli görünüyor"
yaz.

Kısa yaz.
"""

        ai_response = ollama.chat(

            model="llama3",

            messages=[

                {
                    "role":"system",

                    "content":
                    "Sen profesyonel cyber security analyst AI'sın."
                },

                {
                    "role":"user",

                    "content":prompt
                }
            ]
        )

        return {

            "site": site,

            "analysis": analiz,

            "ai_comment":
            ai_response["message"]["content"]

        }

    except Exception as e:

        return {

            "error": str(e)

        }
    
@app.route("/sandbox")
def sandbox():

    site = request.args.get("site")

    try:

        if not site.startswith("http"):
            site = "https://" + site

        # WORKSPACE ANA KLASÖRÜ

        base_dir = "workspace"

        if not os.path.exists(base_dir):

            os.mkdir(base_dir)

        # ZAMAN

        now = datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )

        # KLASÖR ADI

        folder_name = site.replace(
            "https://",
            ""
        ).replace(
            "/",
            "_"
        )

        workspace = os.path.join(

            base_dir,

            f"{folder_name}_{now}"

        )

        os.mkdir(workspace)

        # SITE REQUEST

        response = requests.get(
            site,
            timeout=5
        )

        html = response.text

        # HTML KAYDET

        with open(

            os.path.join(
                workspace,
                "source.html"
            ),

            "w",

            encoding="utf-8"

        ) as f:

            f.write(html)

        # HEADERS KAYDET

        with open(

            os.path.join(
                workspace,
                "headers.txt"
            ),

            "w",

            encoding="utf-8"

        ) as f:

            for k,v in response.headers.items():

                f.write(f"{k}: {v}\n")

        return {

            "status":"success",

            "workspace": workspace,

            "saved":[

                "source.html",

                "headers.txt"

            ]

        }

    except Exception as e:

        return {

            "error": str(e)

        }
    
@app.route("/hostscan")
def host_scan():
    sonuc = {}

    # WINDOWS DEFENDER
    try:
        defender = subprocess.check_output(
            'powershell "Get-MpComputerStatus | Select AntivirusEnabled,RealTimeProtectionEnabled,AntispywareEnabled"',
            shell=True,
            text=True
        )
    except:
        defender = "Bilgi alınamadı"

    # FIREWALL
    try:
        firewall = subprocess.check_output(
            'netsh advfirewall show allprofiles',
            shell=True,
            text=True
        )
    except:
        firewall = "Bilgi alınamadı"

    # SECURE BOOT
    try:
        secureboot = subprocess.check_output(
            'powershell "Confirm-SecureBootUEFI"',
            shell=True,
            text=True
        )
    except:
        secureboot = "Desteklenmiyor / Yetki yok"

    # BIOS / UEFI
    try:
        bios = subprocess.check_output(
            'powershell "(Get-ComputerInfo).BiosFirmwareType"',
            shell=True,
            text=True
        )
    except:
        bios = "Bilgi alınamadı"

    # BITLOCKER
    try:
        bitlocker = subprocess.check_output(
            'manage-bde -status',
            shell=True,
            text=True
        )
    except:
        bitlocker = "Bilgi alınamadı"

    sonuc["windows_defender"] = defender
    sonuc["firewall"] = firewall
    sonuc["secure_boot"] = secureboot
    sonuc["bios_mode"] = bios
    sonuc["bitlocker"] = bitlocker

    return sonuc
    
@app.route("/processmonitor")
def processmonitor():

    processes = []

    try:

        for proc in psutil.process_iter([

            'pid',
            'name',
            'cpu_percent',
            'memory_percent'

        ]):

            try:

                info = proc.info

                risk = "NORMAL"

                name = str(info['name']).lower()

                # ŞÜPHELİ PROCESSLER

                suspicious = [

                    "mimikatz",
                    "powershell",
                    "cmd",
                    "wscript",
                    "cscript",
                    "unknown"
                ]

                for s in suspicious:

                    if s in name:

                        risk = "MEDIUM"

                # YÜKSEK RAM

                if info['memory_percent'] > 10:

                    risk = "HIGH"

                processes.append({

                    "pid": info['pid'],

                    "name": info['name'],

                    "cpu": info['cpu_percent'],

                    "ram": round(
                        info['memory_percent'],
                        2
                    ),

                    "risk": risk

                })

            except:
                pass

        return {

            "processes": processes[:80]

        }

    except Exception as e:

        return {

            "error": str(e)

        }
    
@app.route("/tpmcheck")
def tpmcheck():

    try:

        result = subprocess.check_output(

            'powershell "Get-Tpm"',

            shell=True,

            text=True
        )

        return {

            "tpm": result

        }

    except Exception as e:

        return {

            "error": str(e)

        }
    
    
@app.route("/startup")
def startup():
    startup_apps = []

    try:

        key = winreg.OpenKey(

            winreg.HKEY_CURRENT_USER,

            r"Software\Microsoft\Windows\CurrentVersion\Run"

        )

        i = 0

        while True:

            try:

                name, value, _ = winreg.EnumValue(key, i)

                risk = "NORMAL"

                val = str(value).lower()

                if "temp" in val:

                    risk = "HIGH"

                if "powershell" in val:

                    risk = "MEDIUM"

                startup_apps.append({

                    "name": name,

                    "path": value,

                    "risk": risk

                })

                i += 1

            except OSError:

                break

        return {

            "startup_apps": startup_apps

        }

    except Exception as e:

        return {

            "error": str(e)

        }
    
@app.route("/eventlogs")
def eventlogs():

    try:

        cmd = '''
powershell "Get-WinEvent -LogName Security -MaxEvents 20 |
Select TimeCreated, Id, LevelDisplayName, Message"
'''

        result = subprocess.check_output(
            cmd,
            shell=True,
            text=True
        )

        return {
            "security_logs": result
        }

    except Exception as e:

        return {
            "error": str(e)
        }
    
@app.route("/connections")
def connections():

    data = []

    try:

        for conn in psutil.net_connections():

            try:

                data.append({

                    "local":
                    str(conn.laddr),

                    "remote":
                    str(conn.raddr),

                    "status":
                    conn.status,

                    "pid":
                    conn.pid
                })

            except:
                pass

        return {
            "connections": data[:100]
        }

    except Exception as e:

        return {
            "error": str(e)
        }
    
@app.route("/integrity")
def integrity():

    files = [

        r"C:\Windows\System32\drivers\etc\hosts"

    ]

    hashes = []

    try:

        for path in files:

            if os.path.exists(path):

                with open(path, "rb") as f:

                    content = f.read()

                sha = hashlib.sha256(
                    content
                ).hexdigest()

                hashes.append({

                    "file": path,

                    "sha256": sha

                })

        return {
            "files": hashes
        }

    except Exception as e:

        return {
            "error": str(e)
        }
    
@app.route("/admins")
def admins():

    try:

        result = subprocess.check_output(

            'net localgroup administrators',

            shell=True,

            text=True
        )

        return {

            "admins": result

        }

    except Exception as e:

        return {

            "error": str(e)

        }
    
@app.route("/defender")
def defender():

    try:

        result = subprocess.check_output(

            'powershell "Get-MpComputerStatus"',
            shell=True,
            text=True
        )

        return {

            "defender": result

        }

    except Exception as e:

        return {

            "error": str(e)

        }

# PowerShell komutu çalıştır
def run_ps(command):
    try:
        result = subprocess.check_output(
            ["powershell", "-Command", command],
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="ignore"
        )
        return result.strip()
    except subprocess.CalledProcessError as e:
        return e.output.strip()


# UEFI / Secure Boot
@app.route("/bios_uefi", methods=["POST"])
def bios_uefi():
    return jsonify({
        "bios_uefi": run_ps(
            "Confirm-SecureBootUEFI"
        )
    })


# TPM Check
@app.route("/tpm_check", methods=["POST"])
def tpm_check():
    return jsonify({
        "tpm_check": run_ps(
            "Get-Tpm"
        )
    })


# Core Isolation / Device Guard
@app.route("/coreisolation")
def coreisolation():

    try:
        result = subprocess.check_output(
            'powershell "Get-CimInstance Win32_DeviceGuard"',
            shell=True,
            text=True
        )

        return jsonify({
            "core_isolation": result
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        })


# Defender Status
@app.route("/defender_status", methods=["POST"])
def defender_status():
    return jsonify({
        "defender_status": run_ps(
            "Get-MpComputerStatus"
        )
    })


# Admin Users
@app.route("/admin_users", methods=["POST"])
def admin_users():
    return jsonify({
        "admin_users": run_ps(
            "net localgroup administrators"
        )
    })


# Full Scan
@app.route("/full_scan", methods=["POST"])
@limiter.limit("3 per minute")
def full_scan():

    if not check_auth():
        return jsonify({
            "error": "unauthorized"
        }), 401

    data = request.get_json(
        silent=True
    ) or {}

    ip = (
        data.get("ip") or ""
    ).strip()

    if not ip:
        return jsonify({
            "error": "IP girilmedi"
        }), 400

    results = {
        "host_scan": run_ps(
            f'ping {ip}'
        ),

        "process_monitor": run_ps(
            "Get-Process | Select-Object -First 15 Name,Id"
        ),

        "event_logs": run_ps(
            "Get-WinEvent -LogName Security -MaxEvents 10"
        ),

        "connections": run_ps(
            "Get-NetTCPConnection | Select-Object -First 15"
        ),

        "file_integrity": run_ps(
            r"Get-ChildItem C:\Windows\System32 | Select-Object -First 10 Name"
        ),

        "admin_users": run_ps(
            "net localgroup administrators"
        ),

        "defender_status": run_ps(
            "Get-MpComputerStatus"
        ),

        "bios_uefi": run_ps(
            "Confirm-SecureBootUEFI"
        ),

        "tpm_check": run_ps(
            "Get-Tpm"
        ),

        "core_isolation": run_ps(
            "Get-CimInstance Win32_DeviceGuard"
        )
    }

    return jsonify(results)



if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False,
        use_reloader=False
    )