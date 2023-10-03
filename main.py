import os, time, ctypes, random, string, sys, json, threading

try:
    import requests
    from bs4 import BeautifulSoup
    from colorama import Fore, Style
    from pystyle import Write, System, Colors, Colorate
    from datetime import datetime
except ModuleNotFoundError:
    os.system("pip install requests")
    os.system("pip install bs4")
    os.system("pip install colorama")
    os.system("pip install pystyle")
    os.system("pip install datetime")

red = Fore.RED
yellow = Fore.YELLOW
green = Fore.GREEN
blue = Fore.BLUE
orange = Fore.RED + Fore.YELLOW
pretty = Fore.LIGHTMAGENTA_EX + Fore.LIGHTCYAN_EX
magenta = Fore.MAGENTA
lightblue = Fore.LIGHTBLUE_EX
cyan = Fore.CYAN
gray = Fore.LIGHTBLACK_EX + Fore.WHITE
reset = Fore.RESET
pink = Fore.LIGHTGREEN_EX + Fore.LIGHTMAGENTA_EX
dark_green = Fore.GREEN + Style.BRIGHT
total = 0

def get_time():
    date = datetime.now()
    hour, minute, second = date.hour, date.minute, date.second
    timer = "{:02d}:{:02d}:{:02d}".format(hour, minute, second)
    return timer

ctypes.windll.kernel32.SetConsoleTitleW(f'[ Combolist Downloader ] Made By H4cK3dR4Du (.gg/radutool) | https://github.com/H4cK3dR4Du')
def update_title():
    global total
    ctypes.windll.kernel32.SetConsoleTitleW(f'[ Combolist Downloader ] Made By H4cK3dR4Du (.gg/radutool) | https://github.com/H4cK3dR4Du | Total Accounts Saved : {total}')

urls_saved = []
with open("config.json") as f:
    data = json.load(f)

    shopping, gaming, mix, streaming = data['shopping'], data['gaming'], data['mix'], data['streaming']
    if shopping == "y" or shopping == "yes":
        find_these = ["combolist Shopping", "combolist shopping"]
        yourtype = "Shopping"
    elif gaming == "y" or gaming == "yes":
        find_these = ["combolist Gaming", "combolist gaming"]
        yourtype = "Gaming"
    elif mix == "y" or mix == "yes":
        find_these = ["combolist MIX", "combolist mix"]
        yourtype = "MIX"
    elif streaming == "y" or streaming == "yes":
        find_these = ["combolist Streaming", "combolist streaming"]
        yourtype = "Streaming"

def combolist_gen():
    for page_number in range(2, 16):
        url = f'https://combolist.co/list/{page_number}/'
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            links = soup.find_all('a', href=True)

            for link in links:
                href = link['href']
                for term in find_these:
                    if term in link.text:
                        t = term.replace("combolist ", "").capitalize()
                        time_rn = get_time()
                        print(f"{reset}[ {gray}{time_rn}{reset} ] {reset}({green}+{reset}) {pretty}Downloading Combolist {gray}---> {cyan}{href}")
                        response = requests.get(href)
                        response.raise_for_status()

                        soup = BeautifulSoup(response.text, 'html.parser')
                        links = soup.find_all('a', href=True)
                        for link in links:
                            href2 = link['href']
                            if href2.startswith('https://www.upload.ee/files/'):
                                try:
                                    response = requests.get(href2)
                                    response.raise_for_status()

                                    soup = BeautifulSoup(response.text, 'html.parser')
                                    links = soup.find_all('a', href=True)

                                    for link in links:
                                        href3 = link['href']
                                        if href3.startswith('https://www.upload.ee/download/'):
                                            urls_saved.append(href3)
                                    else:
                                        link_element = soup.find('a', href=True)
                                        if link_element:
                                            url = link_element['href']
                                        else:
                                            pass
                                except requests.exceptions.RequestException:
                                    pass
                        else:
                            pass
        except requests.exceptions.RequestException:
            pass
        else:
            pass

def menu_bro():
    System.Clear()
    Write.Print(f"""
            ╔═╗╔═╗╔╦╗╔╗ ╔═╗  ╦  ╦╔═╗╔╦╗  ╔═╗╔═╗╔╗╔╔═╗╦═╗╔═╗╔╦╗╔═╗╦═╗  ╔╦╗╔═╗╔╦╗╔═╗  ╔╗ ╦ ╦  ╦═╗╔═╗╔╦╗╦ ╦
            ║  ║ ║║║║╠╩╗║ ║  ║  ║╚═╗ ║   ║ ╦║╣ ║║║║╣ ╠╦╝╠═╣ ║ ║ ║╠╦╝  ║║║╠═╣ ║║║╣   ╠╩╗╚╦╝  ╠╦╝╠═╣ ║║║ ║
            ╚═╝╚═╝╩ ╩╚═╝╚═╝  ╩═╝╩╚═╝ ╩   ╚═╝╚═╝╝╚╝╚═╝╩╚═╩ ╩ ╩ ╚═╝╩╚═  ╩ ╩╩ ╩═╩╝╚═╝  ╚═╝ ╩   ╩╚═╩ ╩═╩╝╚═╝

""", Colors.cyan_to_blue, interval=0.000)

menu_bro()
combolist_gen()

def download_and_write_account(url, copy):
    global total
    name = url.split("/")[-1]

    response = requests.get(url)

    if response.status_code == 200:
        with open(name, 'wb') as f2:
            f2.write(response.content)

        try:
            accounts = len(open(name, encoding='utf-8').readlines())
            time_rn = get_time()
            print(f"{reset}[ {gray}{time_rn}{reset} ] {reset}({green}+{reset}) {pretty}Added Accounts {gray}---> [{cyan}{accounts}{gray}]")
            total += accounts
            update_title()
        except:
            pass

        with open(name, 'rb') as f:
            content = f.read()
            copy.write('\n\n' + content.decode('utf-8', errors='ignore'))

        os.remove(name)

with open("combolist.txt", 'a', encoding='utf-8') as copy:
    threads = []
    
    for url in urls_saved:
        thread = threading.Thread(target=download_and_write_account, args=(url, copy))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

def remove_lines():
    abc = "combolist.txt"
    with open(abc, "r", encoding='utf-8') as f:
        lines = f.readlines()

    abc2 = [pizda for pizda in lines if pizda.strip()]

    with open(abc, "w", encoding='utf-8') as f:
        f.writelines(abc2)

def remove_randomthing():
    a = "combolist.txt"

    with open(a, "r", encoding='utf-8') as f:
        lines = f.readlines()

    def delete_thing(radu):
        abc = [
            "**** Combolist ****",
            "https://combolist.co/",
            "**************************"
        ]
        return any(radu2 in radu for radu2 in abc)

    fixed = [radu for radu in lines if not delete_thing(radu)]

    with open(a, "w", encoding='utf-8') as f:
        f.writelines(fixed)

remove_lines()
remove_randomthing()

accounts = len(open('combolist.txt').readlines())
time_rn = get_time()
print(f"\n\n{reset}[ {gray}{time_rn}{reset} ] {reset}({green}+{reset}) {pretty}Total Accounts {gray}---> {green}{accounts}")
input()