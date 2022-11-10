from json import load
import os
from datatypes.Game import Game
from colorama import Fore
import pathlib
from pynput.keyboard import Key, Listener
from get_steam_win import get_steam_path
from parse_steam_lib import parse_steam_lib

path = str(pathlib.Path(__file__).parent.resolve()) + '\game.exe'

CMD_PATH = 'C:/Windows/system32/cmd.exe'
STEAM_PATH = get_steam_path()
if STEAM_PATH == None:
    print(f'{Fore.RED}please, install steam first{Fore.RESET}')
    exit()
STEAM_PATH = STEAM_PATH[0]


def print_menu(game_chosen):
    os.system('cls')
    print(f'{Fore.BLUE}steam fake launch\npress ESC to exit{Fore.RESET}')
    for index, game in enumerate(library):
        game_name = game.get('game_name')
        string = f'{index + 1}. {game_name}'
        string = f'{Fore.MAGENTA}{string}{Fore.RESET} <--' if game_chosen == index + 1 else string
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
    game_id = library[game_chosen - 1].get('game_id')

    # check if exe_path in config.json
    if exe_path == None:
        print(f'{Fore.RED}add "exe_path" parameter to config.json{Fore.RESET}')
        return

    # check if game_id in config.json
    if game_id == None:
        print(f'{Fore.RED}add "game_id" parameter to config.json{Fore.RESET}')
        return

    # check if exe file exists
    if not os.path.isfile(exe_path):
        print(f'{Fore.RED}wrong "exe_path" path in config.json{Fore.RESET}')
        return

    try:
        new_exe_name = exe_path.split('/').pop().split('.')[-2] + '_fake.exe'
        # split without removing delimiter
        new_exe_path = exe_path.split('/')
        new_exe_path[-1] = new_exe_name
        new_exe_path = '/'.join(new_exe_path)

        os.rename(exe_path, new_exe_path)
        os.symlink(CMD_PATH, exe_path)
        os.system(f'start steam://run/{game_id}')
        print(f'{Fore.GREEN}created symlink{Fore.RESET}')
    except:
        print(f'{Fore.RED}run program with admin user{Fore.RESET}')


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
        case _:
            return
    main(current_chosen_game)
    print_menu(current_chosen_game)


with open('config.json') as file:
    library: list[Game] = load(file)
current_chosen_game = 1
print_menu(current_chosen_game)
print(STEAM_PATH)
parse_steam_lib(STEAM_PATH)


with Listener(on_press=on_press, suppress=True) as listener:
    listener.join()
