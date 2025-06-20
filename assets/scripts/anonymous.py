import os
import sys
import random
import time
import json

def loadingScreen(message, delay=300):
    try:
        dots = ["   ", ".  ", ".. ", "...", "   "]
        num_dot = 0
        for x in range(delay):
            sys.stdout.write(f"\r{message} {dots[num_dot]}")
            sys.stdout.write(f"\r")
            sys.stdout.flush()
            if random.randint(10, 90) >= 80:
                time.sleep(80/100)
                num_dot += 1
            else:
                time.sleep(10/100)
                num_dot += 1
            if num_dot == 4:
                num_dot = 0
        sys.stdout.write(f"\r{message} {dots[3]} done")
        print()
        time.sleep(2)
    except KeyboardInterrupt:
        print("\nAbort.")

def installingScreen(msg, delay=300):
    try:
        spinner = ["-", "\\", "|", "/"]
        num_spinner = 0
        for x in range(delay):
            sys.stdout.write(f"\r{msg}... {spinner[num_spinner]}")
            sys.stdout.write(f"\r")
            sys.stdout.flush()
            if random.randint(10, 90) >= 80:
                time.sleep(80/100)
                num_spinner += 1
            else:
                time.sleep(10/100)
                num_spinner += 1
            if num_spinner == 3:
                num_spinner = 0
        sys.stdout.write(f"\r{msg}... Done")
        print()
        time.sleep(1)
    except KeyboardInterrupt:
        print("\nAbort.")

def downloadingScreen(module):
    block = "█"
    proccesed = 50
    for i in range(proccesed):
        sys.stdout.write(f"\r [*] Downloading ... {module} [{block*i}{' '*proccesed}] {i*2}%")
        sys.stdout.write(f"\r")
        sys.stdout.flush()
        if random.randint(10, 90) >= 80:
            time.sleep(80/100)
            proccesed -= 1
        else:
            time.sleep(10/100)
            proccesed -= 1
    time.sleep(1)
    proccesed = 50
    sys.stdout.write(f"\r [*] Downloading ... {module} [{block*proccesed}] Done")
    print()
    time.sleep(1)

def uninstallingScreen(module):
    print(f" [*] Uninstalling {module}")
    prompt = input(" [?] Do you want to continue? [Y/n]: ").split()
    if prompt[0].lower() == "y":
        block = "█"
        proccesed = 50
        for i in range(proccesed):
            sys.stdout.write(f"\r [*] Uninstalling ... {module} [{block*i}{' '*proccesed}] {i*2}%")
            sys.stdout.write(f"\r")
            sys.stdout.flush()
            if random.randint(10, 90) >= 80:
                time.sleep(80/100)
                proccesed -= 1
            else:
                time.sleep(10/100)
                proccesed -= 1
        time.sleep(1)
        proccesed = 50
        sys.stdout.write(f"\r [*] Uninstalling ... {module} [{block*proccesed}] Done")
        print()
        time.sleep(1)
    else:
        print(" [*] Canceled")

def check_module(name):
    path = json.loads(open("assets/modules/list-modules.json", "r").read())
    for i in path["modules"]:
        if name == i[1]:
            return True
            break
    return False

def get_module(number):
    modules = json.loads(open("assets/modules/list-modules.json", "r").read())["modules"][number]
    return modules[1]

def get_detail_module(name):
    modules = json.loads(open("assets/modules/list-modules.json", "r").read())
    for module in modules["modules"]:
        if name == module[1]:
            return {
                "name": module[0],
                "version": module[2],
                "description": module[3]
            }
            break
    return "N/A"

def help_myxploit():
    print()
    print(" Myxploit Commands")
    print(" =================")
    print()
    print("     Command             Description")
    print("     -------             -----------")
    for i in json.loads(open("assets/modules/list-command.json", "r").read())["commands"]:
        print(f"{' '*len('     Command             ')}{i[1]}")
        print(f"\033[A{' '*len('     ')}{i[0]}")
    print()