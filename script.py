from time import sleep
from json import load
from msvcrt import getch, putch
import os
from datatypes.Game import Game
import re

from colorama import Fore
from colorama import Style
import pathlib
from pynput.keyboard import Key, Listener

path = str(pathlib.Path(__file__).parent.resolve()) + '\game.exe'

CMD_PATH = 'C:/Windows/system32/cmd.exe'


def print_menu(game_chosen):
    os.system('cls')
    print('steam fake launch\npress ESC to exit')
    for index, game in enumerate(library):
        game_name = game.get('game_name')
        string = f'{index + 1}. {game_name}'
        if game_chosen == index + 1:
            string += ' <'
        print(string)


def main(game_chosen):
    global current_chosen_game
    if game_chosen > len(library):
        current_chosen_game = 1
    elif game_chosen < 1:
        current_chosen_game = len(library)
    else:
        current_chosen_game = game_chosen


def on_enter(game_chosen):
    exe_path = library[game_chosen - 1].get('exe_path')

    # check if exe_path in config.json
    if exe_path == None:
        print(f'{Fore.RED}add "exe_path" parameter to config.json{Style.RESET_ALL}')
        return

    # check if exe file exists
    if not os.path.isfile(exe_path):
        print(f'{Fore.RED}wrong "exe_path" path in config.json{Style.RESET_ALL}')
        return

    try:
        new_exe_name = exe_path.split('/').pop().split('.')[-2] + '_fake.exe'
        # split without removing delimiter
        new_exe_path = exe_path.split('/')
        new_exe_path[-1] = new_exe_name
        new_exe_path = '/'.join(new_exe_path)

        os.rename(exe_path, new_exe_path)
        os.symlink(CMD_PATH, exe_path)
        # os.system('start steam://run/322170')
        print(f'{Fore.GREEN}created symlink{Style.RESET_ALL}')
    except:
        print(f'{Fore.RED}run program with admin user{Style.RESET_ALL}')


def on_press(key):
    global listener, current_chosen_game
    match key:
        case Key.up:
            current_chosen_game -= 1
        case Key.down:
            current_chosen_game += 1
        case Key.enter:
            on_enter(current_chosen_game)
            return
        case Key.esc:
            return False
    main(current_chosen_game)
    print_menu(current_chosen_game)


with open('config.json') as file:
    library: list[Game] = load(file)
current_chosen_game = 1
print_menu(current_chosen_game)


with Listener(on_press=on_press) as listener:
    listener.join()
