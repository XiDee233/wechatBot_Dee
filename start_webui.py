import os
import shutil
import sys
import webbrowser
from pathlib import Path
from werkzeug.serving import make_server

ROOT = Path(__file__).resolve().parent
os.chdir(ROOT)
os.environ['PATH'] = str(Path(sys.executable).parent) + os.pathsep + os.environ.get('PATH', '')
os.environ['PYTHONUTF8'] = '1'

# First checkout: create private local configuration and editable prompts.
if not (ROOT / 'config.py').exists():
    shutil.copyfile(ROOT / 'config.example.py', ROOT / 'config.py')
if not (ROOT / 'prompts').exists():
    shutil.copytree(ROOT / 'examples' / 'prompts', ROOT / 'prompts')

import config_editor

if __name__ == '__main__':
    config_editor.validate_config()
    port = int(config_editor.parse_config().get('PORT', 5000))
    server = make_server('127.0.0.1', port, config_editor.app, threaded=True)
    url = f'http://127.0.0.1:{port}/'
    print(f'WeChatBot WebUI: {url}', flush=True)
    if '--no-browser' not in sys.argv:
        webbrowser.open(url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
