import vdf
from os.path import isfile


def parse_steam_lib(path):
    with open(f'{path}/config/libraryfolders.vdf', encoding='utf-8') as file:
        steam_libraries = vdf.load(file).get('libraryfolders')

    steam_libraries_parsed = []
    for index in range(len(steam_libraries)):
        steam_library = steam_libraries[str(index)]

        # fmt: off
        steam_library_parsed = {
            'path': steam_library.get('path'),
            'apps': steam_library.get('apps')
        }
        # fmt: on
        steam_libraries_parsed.append(steam_library_parsed)
    return steam_libraries_parsed


def parse_installed_apps(libraries):
    apps_parsed = []
    for library in libraries:
        apps = library.get('apps').keys()
        library_path = library.get('path').replace('\\', '/')
        for app in apps:

            manifest_path = f'{library_path}/steamapps/appmanifest_{app}.acf'
            if not isfile(manifest_path):
                continue

            with open(manifest_path) as manifest:
                app_info = vdf.load(manifest).get('AppState')

            # fmt: off
            app_parsed = {
                'id': int(app),
                'path': f'{library_path}/steamapps/common/{app_info.get("installdir")}',
                'name': app_info.get('name')
            }
            # fmt: on

            apps_parsed.append(app_parsed)

    return apps_parsed
