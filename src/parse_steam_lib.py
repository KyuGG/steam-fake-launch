import vdf


def parse_steam_lib(path):
    with open(f'{path}/config/libraryfolders.vdf', encoding='utf-8') as file:
        steam_libraries = vdf.load(file).get('libraryfolders')

    for index in range(len(steam_libraries)):
        steam_library = steam_libraries[str(index)]

        # fmt: off
        steam_library_parsed = {
            'path': steam_library.get('path'),
            'apps': steam_library.get('apps')
        }
        # fmt: on
        print(steam_library_parsed, end='\n\n')
        
