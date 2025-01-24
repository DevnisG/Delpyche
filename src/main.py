import sys
import click
from config import load_config, set_current_lang, CURRENT_LANG, HELP_TEXT, t
from cli import cli
from watcher import start_monitor

def inject_dynamic_help():
    for cmd_name, mapping in HELP_TEXT.items():
        cmd = cli.get_command(None, cmd_name)
        if cmd is not None:
            key_for_lang = mapping[CURRENT_LANG]
            cmd.help = t(key_for_lang)

def main():

    cfg = load_config()
    lang_in_config = cfg['delpyche'].get('lang', 'ES')
    set_current_lang(lang_in_config)

    inject_dynamic_help()

    if '--internal-monitor' in sys.argv:
        sys.argv.remove('--internal-monitor')
        start_monitor()
    else:
        cli()

if __name__ == '__main__':
    main()
