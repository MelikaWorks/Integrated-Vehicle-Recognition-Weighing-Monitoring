"""Selected settings-generation function from Make-Settings.py.
This copies JSON configuration into settings.py as Python dictionaries.
It does NOT hash or encrypt passwords. Generated settings.py remains private.
Imports and script entry point are intentionally omitted; documentation excerpt.
Required imports: json, pathlib.Path and pprint.pformat.
"""

def main():
    folder = Path(__file__).resolve().parent
    camera = json.loads((folder / 'camera_config.json').read_text(encoding='utf-8-sig'))
    database = json.loads((folder / 'db_config.json').read_text(encoding='utf-8-sig'))
    for key in ('ip', 'username', 'password'):
        if not str(camera.get(key, '')).strip():
            raise ValueError('Camera configuration is missing: ' + key)
    for key in ('server', 'database'):
        if not str(database.get(key, '')).strip():
            raise ValueError('Database configuration is missing: ' + key)
    text = ('"""Private build settings. Do not share or commit this file."""\n\n'
            + 'CAMERA_CONFIG = ' + pformat(camera, sort_dicts=True) + '\n\n'
            + 'DATABASE_CONFIG = ' + pformat(database, sort_dicts=True) + '\n')
    (folder / 'settings.py').write_text(text, encoding='utf-8')
    print('settings.py created. No credentials were printed. Build the EXE now.')
