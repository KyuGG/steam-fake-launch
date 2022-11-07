from time import sleep
from json import load
from msvcrt import getch, putch
from os import system, symlink
import keyboard
from colorama import Fore
from colorama import Style
import pathlib

path = str(pathlib.Path(__file__).parent.resolve()) + '\game.exe'


def print_menu(game_chosen):
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

    system('cls')
    print_menu(current_chosen_game)


def on_enter(game_chosen):
    exe_path = library[game_chosen - 1].get('exe_path')
    if exe_path == None:
        print(f'{Fore.RED}add "exe_path" parameter to config.json{Style.RESET_ALL}')
        return
    try:
        # first arg - cmd, second arg - game file
        symlink(exe_path, path)
    except:
        print(f'{Fore.RED}run program with admin user{Style.RESET_ALL}')


with open('config.json') as file:
    library = load(file)


current_chosen_game = 1
main(current_chosen_game)
keyboard.on_press_key('up', lambda _: main(current_chosen_game - 1))
keyboard.on_press_key('down', lambda _: main(current_chosen_game + 1))
keyboard.on_press_key('enter', lambda _: on_enter(current_chosen_game))

keyboard.wait('escape')