import os
from colorama import Fore
from pynput.keyboard import Key, Listener, KeyCode
from src.get_steam_win import get_steam_path
from src.parse_steam_lib import parse_steam_lib, parse_installed_apps
import json


def print_menu(app_chosen):
    global APPS
    os.system('cls')
    print(
        f'{Fore.BLUE}steam fake launch\npress {Fore.LIGHTRED_EX}ESC{Fore.RESET}{Fore.BLUE} to exit\npress {Fore.LIGHTRED_EX}C{Fore.RESET}{Fore.BLUE} to clear app exe path{Fore.RESET}'
    )
    for index, app in enumerate(APPS):
        app_name = app.get('name')
        string = f'{index + 1}. {app_name}'
        string = f'{Fore.MAGENTA}{string}{Fore.RESET} <--' if app_chosen == index + 1 else string
        print(string)


def change_chosen_app(app_chosen):
    global current_chosen_app
    if app_chosen > len(APPS):
        current_chosen_app = 1
    elif app_chosen < 1:
        current_chosen_app = len(APPS)
    else:
        current_chosen_app = app_chosen


import easygui


def clear_exe_path(app_chosen):
    app = APPS[app_chosen - 1]
    app_id = str(app.get('id'))

    with open('config.json', 'r') as file:
        config: dict = json.load(file)

    try:
        config.pop(app_id)
    except:
        return

    with open('config.json', 'w') as file:
        json.dump(config, file, indent=4)


def on_enter(app_chosen):
    app = APPS[app_chosen - 1]
    app_id = str(app.get('id'))
    app_path = app.get('path')

    with open('config.json', 'r') as file:
        config = json.load(file)

    if config.get(app_id) == None:
        exe_path = easygui.fileopenbox(default=f'{app_path}/*.exe')

        if exe_path == None:
            return

        # fmt: off
        app_config = { 
            app_id: exe_path
        }
        # fmt: on

        config.update(app_config)
        print(config)

        with open('config.json', 'w') as file:
            json.dump(config, file, indent=4)

    # print(json.dumps(app_config))

    # print(app_config in config)
    # REWRITE USING INFO ABOUT APP PATH

    # exe_path = library[app_chosen - 1].get('exe_path')
    # game_id = library[app_chosen - 1].get('game_id')

    # # check if exe_path in config.json
    # if exe_path == None:
    #     print(f'{Fore.RED}add "exe_path" parameter to config.json{Fore.RESET}')
    #     return

    # # check if game_id in config.json
    # if game_id == None:
    #     print(f'{Fore.RED}add "game_id" parameter to config.json{Fore.RESET}')
    #     return

    # # check if exe file exists
    # if not os.path.isfile(exe_path):
    #     print(f'{Fore.RED}wrong "exe_path" path in config.json{Fore.RESET}')
    #     return

    # new_exe_name = exe_path.split('/').pop().split('.')[-2] + '_fake.exe'
    # # split without removing delimiter
    # new_exe_path = exe_path.split('/')
    # new_exe_path[-1] = new_exe_name
    # new_exe_path = '/'.join(new_exe_path)
    # try:
    #     os.rename(exe_path, new_exe_path)
    #     os.symlink(CMD_PATH, exe_path)
    #     os.system(f'start steam://run/{game_id}')
    #     print(f'{Fore.GREEN}created symlink{Fore.RESET}')
    # except:
    #     print(f'{Fore.RED}run program with admin user{Fore.RESET}')


def on_press(key):
    global listener, current_chosen_app
    if type(key) == KeyCode:
        key = key.char
    match key:
        case Key.up:
            current_chosen_app -= 1
        case Key.down:
            current_chosen_app += 1
        case Key.enter:
            on_enter(current_chosen_app)
            return
        case 'c':
            clear_exe_path(current_chosen_app)
            return
        case Key.esc:
            return False
        case _:
            return
    change_chosen_app(current_chosen_app)
    print_menu(current_chosen_app)


CMD_PATH = 'C:/Windows/system32/cmd.exe'
STEAM_PATH = get_steam_path()
if STEAM_PATH == None:
    print(f'{Fore.RED}please, install steam first{Fore.RESET}')
    exit()

LIBRARIES = parse_steam_lib(STEAM_PATH)
APPS = parse_installed_apps(LIBRARIES)

current_chosen_app = 1
print_menu(current_chosen_app)


with Listener(on_press=on_press, suppress=True) as listener:
    listener.join()
