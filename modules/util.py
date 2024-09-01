import os
import json
import sys
import time
import ctypes
import datetime
import random
import requests
import discord
from discord import Embed
from rich.console import Console
from pypresence import Presence

# Check and install missing modules
def check_and_install_modules():
    try:
        import fade
        import cursor
        from git import Repo
        from colorama import deinit, init as cinit
    except ImportError as e:
        if "discord" in str(e):
            # Assuming package is a custom module for installing packages
            from modules import package
            package.install_module(module="discord.py-self")
        else:
            from modules import package
            package.install_module(module=e.name)
        print(f"Installed missing module {e.name}, restarting..")
        from modules import package
        package.restart()

check_and_install_modules()

if os.name == "nt":
    console = Console(color_system="auto", legacy_windows=True)
else:
    console = Console(color_system="auto")

utd_api = "https://discord.com/api/v10"
version = 6.06
global rpc

def clear():
    sys.stdout.flush()
    os.system("clear" if os.name != "nt" else "cls")

def check_for_update():
    try:
        with open("./config.json") as f:
            config = json.load(f)
    except FileNotFoundError:
        return
    if config.get("Automatically Check for Updates", False):
        r = requests.get(url="https://raw.githubusercontent.com/coital/nuked/main/version?v=1")
        ver = float(r.text)
        if ver > version:
            if config.get("Auto Update", False):
                auto_update()
            else:
                clear()
                console.bell()
                log(f"[blink][link=https://github.com/coital/nuked]Update for Nuked is available[/link]![/blink] New version: v{ver}, current version: v{version}")
                log("You can update by replacing the core files with the ones at https://github.com/coital/nuked")
                input()

def auto_update():
    r = requests.get("https://raw.githubusercontent.com/coital/nuked/main/version")
    try:
        os.mkdir(f"./{r.text}")
    except:
        return
    repo = Repo.clone_from("git://github.com/coital/nuked.git", f"./{r.text}")
    repo.close()
    log(f"New Nuked version is in ./{r.text}.")

def set_title(title: str):
    if os.name == "nt":
        ctypes.windll.kernel32.SetConsoleTitleW(title)
    elif os.name == "posix":
        print(f"\x1b]2;{title}\x07")

def get_time():
    return datetime.datetime.now().strftime("%H:%M:%S, %m/%d/%y")

def get_config():
    with open("./config.json") as f:
        return json.load(f)

def get_color():
    return 0xfafafa

def toast_message(message: str):
    if os.name == "nt":
        from win10toast import ToastNotifier
        toaster = ToastNotifier()
        toaster.show_toast("Nuked", message, duration=5, threaded=True)

def get_token(email: str, password: str):
    r = requests.post(f"{utd_api}/auth/login", json={"login":email, "password":password, "undelete":False, "captcha_key":None, "login_source":None, "gift_code_sku_id":None}, headers={"content-type": "application/json"})
    try:
        return r.json().get("token")
    except:
        return None

def signal_handler(signal, frame):
    import cursor
    cursor.show()
    clear()
    console.print("Logging out of Nuked", justify="center")
    time.sleep(1)
    clear()
    check_for_update()
    exit(0)

def check_token(token: str):
    headers = {"Content-Type": "application/json", "authorization": token}
    r = requests.get(f"{utd_api}/users/@me/library", headers=headers)
    if r.status_code != 200:
        os.remove(f'{os.getcwd()}/config.json')
        clear()
        log('Invalid token.', error=True)
        time.sleep(1)
        from modules import init
        init.init()

def insert_returns(body):
    if isinstance(body[-1], ast.Expr):
        body[-1] = ast.Return(body[-1].value)
        ast.fix_missing_locations(body[-1])

    if isinstance(body[-1], ast.If):
        insert_returns(body[-1].body)
        insert_returns(body[-1].orelse)

    if isinstance(body[-1], ast.With):
        insert_returns(body[-1].body)

def load_commands() -> dict:
    commands_dict = []
    for folder in ["fun", "malicious", "nsfw", "utility"]:
        for file in os.listdir(f"./commands/{folder}/"):
            if file.endswith(".py"):
                commands_dict.append(f"commands.{folder}.{file[:-3]}")
    for file in os.listdir("./commands/"):
        if file.endswith(".py"):
            commands_dict.append(f"commands.{file[:-3]}")
    for file in os.listdir("./events/"):
        if file.endswith(".py"):
            commands_dict.append(f"events.{file[:-3]}")
    return commands_dict

def enable_light_mode() -> dict:
    light_mode_commands = [cmd for cmd in load_commands() if "light" not in cmd and "event" not in cmd]
    return light_mode_commands

def presplash():
    for letter in "Welcome":
        console.print(letter, justify="center")
        time.sleep(0.155)
    clear()

def splash():
    clear()
    with open("./config.json") as f:
        config = json.load(f)
    functions = [fade.purpleblue]
    if config.get("Random Splash Color", False):
        functions = [fade.fire, fade.greenblue, fade.water, fade.pinkred]
    cinit(convert=True)
    splash = random.choice(functions)("""
                 ███╗   ██╗██╗   ██╗██╗  ██╗███████╗██████╗
                 ████╗  ██║██║   ██║██║ ██╔╝██╔════╝██╔══██╗
                 ██╔██╗ ██║██║   ██║█████╔╝ █████╗  ██║  ██║
                 ██║╚██╗██║██║   ██║██╔═██╗ ██╔══╝  ██║  ██║
                 ██║ ╚████║╚██████╔╝██║  ██╗███████╗██████╔╝
                 ╚═╝  ╚═══╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═════╝""")
    console.print(splash, justify="center", end="")
    deinit()
    r = requests.get("https://raw.githubusercontent.com/coital/nuked/main/motd?v=1")
    if r.status_code in (200, 204):
        console.print(f"[green]MOTD[/green]: [bold]{r.text}[/]\n", justify="center")

def log(content: str, color="cyan", error=False):
    console.print(f"\n[reset][{'red' if error else color}][bright][{get_time()}][/bright][/{'red' if error else color}] {content}[/reset]")

def setup_rich_presence() -> bool:
    global rpc
    try:
        rpc = Presence(client_id="916855918552023081")
        rpc.connect()
        rpc.update(details=f"Connected | {version}",
                large_image="avatar", start=time.time(),
                join="Join")
        return True
    except Exception as e:
        log(f"RPC Failed to initialize: [bold]{e}[/bold].", error=True)
        time.sleep(2.5)
    return False

def disable_rich_presence() -> bool:
    global rpc
    rpc.close()
    return True

def embed_to_str(embed: discord.Embed) -> str:
    embed_str = f"""{embed.title if embed.title else ""}\n{embed.description if embed.description else ""}\n"""
    for field in embed.fields:
        embed_str +=  f"""\n{field.name} : {field.value}\n"""
    embed_str += f"""{embed.footer.text if embed.footer else ""}\n{embed.image.url if embed.image else ""}\n{embed.thumbnail.url if embed.thumbnail else ""}\n"""
    return embed_str
