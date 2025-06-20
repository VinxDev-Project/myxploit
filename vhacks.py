#!/bin/python
#coding: utf-8

import os
import sys 
import time
import json
import hashlib
import requests
import random
import pwinput
import shutil

from faker import Faker as create
from datetime import datetime as dtime
from tabulate import tabulate

sys.path.append(os.path.abspath("assets/scripts"))
sys.path.append(os.path.abspath("assets/modules"))

import core
import anonymous

def __get_data(user):
    return requests.get(f"{core.url}?key=getdata&target={user}").json()
    
def __add_data(username, password):
    return requests.post(core.url, data={
        "key": "createdata",
        "username": username,
        "password": password,
        "lhost": create().ipv4()
    }).json()

def __check_session():
    if os.path.exists("assets/session.json"):
        try:
            get_data_session = json.loads(open("assets/session.json", "r").read())
            get_data_self = __get_data(get_data_session["username"])
            if get_data_self["username"] == get_data_session["username"]:
                if get_data_self["password"] == get_data_session["password"]:
                    return {
                        "msg": "auto_login"
                    }
                else:
                    return {
                        "msg": "login"
                    }
            else:
                return {
                    "msg": "login"
                }
        except json.decoder.JSONDecodeError:
            return {
                "msg": "login"
            }
        except KeyError:
            return {
                "msg": "register"
            }
    else:
        return {
            "msg": "register"
        }
        
def __form_register():
    while True:
        time.sleep(3)
        os.system("clear")
        print(" [ R E G I S T E R - M Y X P L O I T ]")
        print()
        new_username = input(" [?] New Username: ")
        if new_username.lower() == "login":
            open("assets/session.json", "w").write("")
            break
        if __get_data(new_username)["msg"] == "No data result!":
            new_password = pwinput.pwinput(prompt=" [?] New Password: ", mask="*")
            if len(new_password) >= 8:
                print()
                anonymous.loadingScreen(" [*] Create a new account", 200)
                if __add_data(new_username, new_password)["msg"] == "Create data successfully":
                    open("assets/session.json", "w").write(json.dumps({
                        "username": new_username,
                        "password": new_password
                    }, indent=4))
                    print(" [*] Create account successfully")
                    break
                else:
                    print(" [*] Failed to create account")
            else:
                print(" [*] The password you entered is too short!")
        else:
            print(" [*] Username already in use!")

def __form_login():
    while True:
        time.sleep(3)
        os.system("clear")
        print(" [ L O G I N - M Y X P L O I T ]")
        print()
        username = input(" [?] Username: ")
        if username.lower() == "register":
            os.remove("assets/session.json")
            break
        get_data_self = __get_data(username)
        if get_data_self["msg"] == "Data found":
            password = pwinput.pwinput(prompt=" [?] Password: ", mask="*")
            if get_data_self["password"] == password:
                print()
                open("assets/session.json", "w").write(json.dumps({
                    "username": username,
                    "password": password
                }, indent=4))
                print(" [*] Signed in successfully")
                break
            else:
                print(" [*] Incorrect password!")
        else:
            print(" [*] Username not registered!")

def __net_analyzer_prompt(username):
    pass

def __myxploit_prompt(username):
    while True:
        try:
            get_data_self = __get_data(username)
            if get_data_self["rhost"] == None:
                prompt = input(f"{get_data_self['username']}@myxploit /{get_data_self['cwd']} $ ")
            else:
                prompt = input(f"{get_data_self['username']}@{get_data_self['rhost']} /{get_data_self['cwd']} $ ")
            
            prompt = prompt.split()
            if prompt[0].lower() == "help" or prompt[0].lower() == "?":
                # print()
                # print(tabulate(
                #     json.loads(open("assets/modules/list-command.json", "r").read())["commands"],
                #     ["Command", "Description"],
                #     tablefmt="simple"
                # ))
                # print()
                anonymous.help_myxploit()
            elif prompt[0].lower() == "clear" or prompt[0].lower() == "cls":
                os.system("clear")
            elif prompt[0].lower() == "ls" or prompt[0].lower() == "dir":
                get_dir_self = requests.get(f"{core.url}?key=getdirectory&paths={get_data_self['cwd']}").json()
                print()
                print(f"Total {get_dir_self['total_bytes']}")
                print(tabulate(get_dir_self["directory"], ["Mode", "Count", "User", "Group", "Size", "Last Modified", "Name"], tablefmt="simple", numalign="left"))
                print()
            elif prompt[0].lower() == "net-analyzer":
                if anonymous.check_module(prompt[0].lower()):
                    __net_analyzer_prompt(get_data_self["username"])
                else:
                    print()
                    print(f" [*] Command not found: {prompt[0].lower()}")
            elif prompt[0].lower() == "mdl" or prompt[0].lower() == "module":
                try:
                    if prompt[1].lower() == "list-all":
                        try:
                            print()
                            print(tabulate(
                                json.loads(open("assets/modules/list-modules.json", "r").read())["modules"],
                                ["Module Name", "Alias", "Version", "Description"],
                                tablefmt="simple"
                            ))
                            print()
                        except IOError:
                            print(" [*] File error!")
                    elif prompt[1].lower() == "list-installed":
                        print()
                        try:
                            installed = []
                            for file in os.listdir("assets/modules"):
                                if os.path.isdir(f"assets/modules/{file}"):
                                    installed.append([
                                        anonymous.get_detail_module(file)["name"],
                                        f"modules/{file}",
                                        anonymous.get_detail_module(file)["version"]
                                    ])
                                else:
                                    pass
                            if len(installed) == 0:
                                print(" [*] No modules installed")
                                print()
                            else:
                                print(tabulate(
                                    installed,
                                    ["Module Name", "Module Path", "Version"],
                                    tablefmt="simple"
                                ))
                                print()
                        except IOError:
                            pass
                    elif prompt[1].lower() == "install" or prompt[1].lower() == "i":
                        print()
                        try:
                            if anonymous.check_module(prompt[2].lower()):
                                try:
                                    anonymous.installingScreen(f" [*] Reading module {prompt[2].lower()}", delay=50)
                                    if os.path.exists(f"assets/modules/{prompt[2].lower()}"):
                                        print(" [*] The module has been installed")
                                        print()
                                    else:
                                        anonymous.installingScreen(f" [*] Building {prompt[2].lower()}", delay=50)
                                        os.mkdir(f"assets/modules/{prompt[2].lower()}")
                                        anonymous.installingScreen(f" [*] Building dependency {prompt[2].lower()}", delay=50)
                                        if prompt[2].lower() == anonymous.get_module(0):
                                            open(f"assets/modules/{prompt[2].lower()}/setup.json", "w").write(json.dumps({
                                                "payload": "assets/payload/worm.x",
                                                "lhost": None,
                                                "rhost": None,
                                                "lport": "4444",
                                                "done": 0
                                            }, indent=4))
                                        elif prompt[2].lower() == anonymous.get_module(1):
                                            open(f"assets/modules/{prompt[2].lower()}/log.txt", "w").write("")
                                        anonymous.downloadingScreen(f"{prompt[2].lower()} {anonymous.get_detail_module(prompt[2].lower())}")
                                        print()
                                except IndexError:
                                    pass
                            else:
                                print(f" [*] Module {prompt[2].lower()} does not exists")
                                print()
                        except IndexError:
                            pass
                    elif prompt[1].lower() == "uninstall":
                        print()
                        try:
                            if anonymous.check_module(prompt[2].lower()):
                                try:
                                    anonymous.installingScreen(f" [*] Reading module {prompt[2].lower()}", delay=50)
                                    if os.path.exists(f"assets/modules/{prompt[2].lower()}"):
                                        anonymous.uninstallingScreen(prompt[2].lower())
                                        shutil.rmtree(f"assets/modules/{prompt[2].lower()}")
                                        print()
                                    else:
                                        print(" [*] Module not installed")
                                        print()
                                except IndexError:
                                    pass
                            else:
                                print(f" [*] Module {prompt[2].lower()} does not exists")
                                print()
                        except IndexError:
                            pass
                    else:
                        print()
                        print(" [*] Option not found!")
                        print()
                except IndexError:
                    print()
                    print(" Usage: module [options...]")
                    print("  list-all                      - List all module available")
                    print("  list-installed                - List installed module")
                    print("  install <module>              - Install specified module")
                    print("  uninstall <module>            - Uninstall specified module")
                    print()
            else:
                print()
                print(f" [*] Command not found: {prompt[0].lower()}")
                print()
        except IndexError:
            pass
        except KeyboardInterrupt:
            print()

def __main_session():
    while True:
        data_session = __check_session()["msg"]
        if data_session == "register":
            __form_register()
        elif data_session == "login":
            __form_login()
        else:
            break
    time.sleep(3)
    os.system("clear")
    get_data_session = json.loads(open("assets/session.json", "r").read())
    __myxploit_prompt(get_data_session["username"])

def __main():
    os.system("clear")
    anonymous.loadingScreen(" [*] Checking the session", 50)
    __main_session()
    
__main()
