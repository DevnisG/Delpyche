import os
import sys
import time
import click
import psutil
import shutil
import subprocess
from tqdm import tqdm
from config import (
    PID_FILE,
    LOG_DIR,
    CONFIG_FILE,
    t,
    load_config,
    save_config,
    CURRENT_LANG,
    set_current_lang,
    HELP_TEXT
)

def ask_for_restart():
    ctx = click.get_current_context()
    respuesta = input(t("ask_restart")).strip().lower()
    if respuesta == 'y':
        ctx.invoke(restart)

@click.group()
def cli():
    pass

@cli.command(name="start")
def start():
    click.clear()

    click.secho(t("start_banner"), fg="white", bold=True)
    click.secho(t("start_ok"), fg="white", bold=True)

    if os.path.exists(PID_FILE):
        click.secho(t("start_already"), fg="red")
        return

    click.secho(t("start_bg"), fg="white")

    p = subprocess.Popen(
        [sys.argv[0], '--internal-monitor'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=False
    )

    for _ in tqdm(
        range(20),
        desc=t("start_init_desc"),
        bar_format="{desc}: {percentage:3.0f}%|{bar:30}|",
        ascii=False,
        ncols=70
    ):
        time.sleep(0.1)
        if p.poll() is not None:
            break

    if p.poll() is not None:
        err = p.stderr.read().decode('utf-8', errors='replace')
        out = p.stdout.read().decode('utf-8', errors='replace')
        click.secho(t("start_end_immediately"), fg="red")
        if err.strip():
            click.secho(f"\nSTDERR:\n{err}", fg="red")
        if out.strip():
            click.secho(f"\nSTDOUT:\n{out}", fg="white")
        return

    pid = p.pid
    with open(PID_FILE, "w", encoding="utf-8") as f:
        f.write(str(pid))

    click.secho(f"{t('start_monitoring_ok')}{pid}", fg="white", bold=True)

@cli.command(name="stop")
def stop():
    click.clear()
    if not os.path.exists(PID_FILE):
        click.secho(t("no_monitor_active"), fg="red")
        return

    with open(PID_FILE, 'r', encoding='utf-8') as f:
        pid_str = f.read().strip()

    if not pid_str.isdigit():
        click.secho(t("pid_invalid"), fg="red")
        os.remove(PID_FILE)
        return

    pid = int(pid_str)
    try:
        proc = psutil.Process(pid)
        proc.terminate()
        proc.wait(2)
        click.secho(f"{t('stop_ok')} (PID {pid})", fg="white")
    except psutil.NoSuchProcess:
        click.secho(t("process_not_exist"), fg="yellow")
    except psutil.TimeoutExpired:
        click.secho(t("process_kill"), fg="red")
        proc.kill()
    except Exception as e:
        click.secho(f"{t('process_stop_error')}: {e}", fg="red")

    if os.path.exists(PID_FILE):
        os.remove(PID_FILE)

@cli.command(name="restart")
def restart():
    click.clear()
    click.secho(t("restart_stopping"), fg="yellow")
    ctx = click.get_current_context()
    ctx.invoke(stop)

    time.sleep(2)

    click.secho(t("restart_starting"), fg="yellow")
    ctx.invoke(start)

@cli.command(name="status")
def status():
    click.clear()
    if not os.path.exists(PID_FILE):
        click.secho(t("status_not_running"), fg="red")
        return

    with open(PID_FILE, 'r', encoding='utf-8') as f:
        pid_str = f.read().strip()

    if pid_str.isdigit():
        pid = int(pid_str)
        if psutil.pid_exists(pid):
            click.secho(f"{t('status_running')} {pid}).", fg="green")
        else:
            click.secho(t("status_pid_exists_no_proc"), fg="yellow")
    else:
        click.secho(t("status_pid_invalid"), fg="red")

@cli.command(name="config")
def show_config():
    click.clear()
    cfg = load_config()
    if not cfg.sections():
        click.secho(t("config_not_found"), fg="red")
        return

    click.secho(t("config_current"), fg="white", bold=True)
    for section in cfg.sections():
        click.secho(f"[{section}]", fg="white", bold=True)
        for key, value in cfg[section].items():
            click.echo(f"{key} = {value}")
        click.echo()

@cli.command(name="info")
def info():
    click.clear()
    if not os.path.exists(LOG_DIR):
        click.secho(t("logs_not_found"), fg="red")
        return

    log_file = os.path.join(LOG_DIR, "monitor.log")
    if not os.path.exists(log_file):
        click.secho(t("logs_not_found"), fg="red")
        return

    with open(log_file, 'r', encoding='utf-8') as f:
        content = f.read()
        if content.strip():
            click.secho(content, fg="white")
        else:
            click.secho(t("logs_empty"), fg="red")

@cli.command(name="clean")
def clean():
    click.clear()
    if os.path.exists(LOG_DIR):
        shutil.rmtree(LOG_DIR)
        click.secho(t("logs_deleted"), fg="white")

    if os.path.exists(PID_FILE):
        os.remove(PID_FILE)
        click.secho(t("pid_deleted"), fg="white")

    if os.path.exists(CONFIG_FILE):
        os.remove(CONFIG_FILE)
        click.secho(t("config_deleted"), fg="white")

    click.secho(t("clean_done"), fg="white")

@cli.command(name="set")
@click.argument('seconds', type=int)
def set_delay(seconds):
    click.clear()
    cfg = load_config()
    cfg['delpyche']['delay'] = str(seconds)
    save_config(cfg)

    click.secho(f"{t('delay_set')} {seconds}.", fg="yellow")
    ask_for_restart()

@cli.command(name="path")
@click.argument('ruta', type=str)
def set_path(ruta):
    click.clear()
    cfg = load_config()
    cfg['delpyche']['path'] = ruta
    save_config(cfg)

    click.secho(f"{t('path_set')} {ruta}.", fg="yellow")
    ask_for_restart()

@cli.command(name="lang")
@click.argument('lang_code', type=str)
def set_language(lang_code):
    click.clear()
    lang_code = lang_code.upper()
    if lang_code not in ["ES", "EN"]:
        click.secho(t("lang_invalid"), fg="red")
        return

    cfg = load_config()
    cfg['delpyche']['lang'] = lang_code
    save_config(cfg)

    set_current_lang(lang_code)

    click.secho(f"{t('lang_changed_to')} {lang_code}", fg="green")
    ask_for_restart()
