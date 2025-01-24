import os
import configparser

WARNING_EMOJI = "⚠️"
ERROR_EMOJI   = "❌"
OK_EMOJI      = "✅"
START_EMOJI   = "🚀"
STOP_EMOJI    = "⛔"
RESTART_EMOJI = "🔄"
CLEAN_EMOJI   = "🗑 "
INFO_EMOJI    = "🧾"
CONFIG_EMOJI  = "⚙️"
PATH_EMOJI    = "📍"
STATUS_EMOJI  = "💡"
SET_EMOJI     = "🔧"
LANG_EMOJI    = "🌐"

CONFIG_FILE = "config.ini"
LOG_DIR     = "logs"
PID_FILE    = ".delpyche.pid"

LANG_TEXTS = {
    "ES": {
        "no_monitor_active": f"{ERROR_EMOJI} No se encontró un monitor activo.",
        "pid_invalid": f"{ERROR_EMOJI} El PID del archivo es inválido. Se eliminará el archivo PID.",
        "process_not_exist": f"{WARNING_EMOJI} El proceso no existe. Se eliminará el archivo PID.",
        "process_kill": f"{ERROR_EMOJI} El proceso no se detuvo a tiempo. Se procederá a kill.",
        "process_stop_error": "Error deteniendo el proceso",
        "logs_not_found": f"{ERROR_EMOJI} No se encontraron logs.",
        "logs_empty": f"{ERROR_EMOJI} El archivo de log está vacío.",
        "logs_deleted": f"{ERROR_EMOJI} Carpeta de logs eliminada.",
        "pid_deleted": f"{ERROR_EMOJI} Archivo PID eliminado.",
        "config_deleted": f"{ERROR_EMOJI} Archivo config eliminado.",
        "delay_set": f"{WARNING_EMOJI} Tiempo de retraso establecido a",
        "path_set": f"{WARNING_EMOJI} Ruta de monitoreo establecida a",
        "start_banner": r"""
            __,__
   .--.  .-"     "-.  .--.
  / .. \/  .-. .-.  \/ .. \
 | |  '|  /   Y   \  |'  | |
 | \   \  \ 0 | 0 /  /   / |
  \ '- ,\.-"`` ``"-./, -' /
   `'-' /_   ^ ^   _\ '-'`
       |  \._   _./  |
       \   \ `~` /   /
        '._ '-=-' _.'  
           '~---~'
 ____       _                  _          
|  _ \  ___| |_ __  _   _  ___| |__   ___ 
| | | |/ _ \ | '_ \| | | |/ __| '_ \ / _ \
| |_| |  __/ | |_) | |_| | (__| | | |  __/
|____/ \___|_| .__/ \__, |\___|_| |_|\___|By_DevnisG
             |_|    |___/                                   
""",
        "start_ok": f"{OK_EMOJI} ¡Eliminador de __pycache__ está en marcha!\n",
        "start_already": f"{ERROR_EMOJI} Parece que el monitor ya está en ejecución.",
        "start_bg": f"{WARNING_EMOJI} Iniciando el monitor en segundo plano...\n",
        "start_init_desc": "Inicializando Delpyche",
        "start_end_immediately": f"{ERROR_EMOJI} El proceso de monitoreo finalizó inmediatamente.",
        "start_monitoring_ok": f"{OK_EMOJI} Monitoreo iniciado en segundo plano. PID=",

        # stop
        "stop_ok": f"{OK_EMOJI} Monitor detenido correctamente.",

        # restart
        "restart_stopping": f"{WARNING_EMOJI} Reiniciando monitor: Deteniendo...",
        "restart_starting": f"{WARNING_EMOJI} Iniciando nuevamente...",

        # status
        "status_running": f"{OK_EMOJI} El monitoreo está en ejecución (PID",
        "status_not_running": f"{ERROR_EMOJI} El monitoreo NO está en ejecución.",
        "status_pid_exists_no_proc": f"{WARNING_EMOJI} El archivo PID existe, pero el proceso no está corriendo.",
        "status_pid_invalid": f"{ERROR_EMOJI} El archivo PID es inválido.",

        # config
        "config_current": f"{CONFIG_EMOJI} Configuración actual:\n",
        "config_not_found": f"{ERROR_EMOJI} No se encontró ninguna configuración en config.ini.",

        # info
        "logs_contents": "",

        # clean
        "clean_done": f"{CLEAN_EMOJI} Eliminaciones realizadas.",

        # lang
        "lang_changed_to": f"{LANG_EMOJI} Idioma cambiado a",
        "lang_invalid": f"{ERROR_EMOJI} Idioma no válido. Usa ES o EN.",
        "ask_restart": "¿Deseas reiniciar ahora? [Y/N]: ",

        # logs
        "monitor_started": "Monitor iniciado.",
        "monitor_stopped_keyboard": "Monitor detenido por KeyboardInterrupt.",
        "monitor_log_new_pycache": "Detectado nuevo __pycache__",
        "monitor_log_removed": "Eliminado",

        # help
        "help_start":    "Inicia el monitoreo en segundo plano.",
        "help_stop":     "Detiene el monitoreo activo.",
        "help_restart":  "Reinicia el monitoreo (stop + start).",
        "help_status":   "Muestra el estado actual del monitoreo.",
        "help_config":   "Muestra la configuración almacenada en config.ini.",
        "help_info":     "Muestra los logs generados por el monitor.",
        "help_clean":    "Elimina logs, PID y archivo de configuración (si existen).",
        "help_set":      "Establece el tiempo de retraso (en segundos) para eliminar __pycache__.",
        "help_path":     "Establece la ruta que será monitoreada en busca de __pycache__.",
        "help_lang":     "Cambia el idioma de la aplicación (ES o EN).",
    },
    "EN": {
        "no_monitor_active": f"{ERROR_EMOJI} No active monitor found.",
        "pid_invalid": f"{ERROR_EMOJI} The PID file is invalid. It will be removed.",
        "process_not_exist": f"{WARNING_EMOJI} The process does not exist. The PID file will be removed.",
        "process_kill": f"{ERROR_EMOJI} The process did not stop in time. Proceeding with kill.",
        "process_stop_error": "Error stopping the process",
        "logs_not_found": f"{ERROR_EMOJI} No logs found.",
        "logs_empty": f"{ERROR_EMOJI} The log file is empty.",
        "logs_deleted": f"{ERROR_EMOJI} Logs folder deleted.",
        "pid_deleted": f"{ERROR_EMOJI} PID file deleted.",
        "config_deleted": f"{ERROR_EMOJI} Config file deleted.",
        "delay_set": f"{WARNING_EMOJI} Delay time set to",
        "path_set": f"{WARNING_EMOJI} Monitoring path set to",
        "start_banner": r"""
            __,__
   .--.  .-"     "-.  .--.
  / .. \/  .-. .-.  \/ .. \
 | |  '|  /   Y   \  |'  | |
 | \   \  \ 0 | 0 /  /   / |
  \ '- ,\.-"`` ``"-./, -' /
   `'-' /_   ^ ^   _\ '-'`
       |  \._   _./  |
       \   \ `~` /   /
        '._ '-=-' _.'  
           '~---~'
 ____       _                  _          
|  _ \  ___| |_ __  _   _  ___| |__   ___ 
| | | |/ _ \ | '_ \| | | |/ __| '_ \ / _ \
| |_| |  __/ | |_) | |_| | (__| | | |  __/
|____/ \___|_| .__/ \__, |\___|_| |_|\___|By_DevnisG
             |_|    |___/                                   
""",
        "start_ok": f"{OK_EMOJI} __pycache__ remover is now running!\n",
        "start_already": f"{ERROR_EMOJI} It seems the monitor is already running.",
        "start_bg": f"{WARNING_EMOJI} Starting the monitor in the background...\n",
        "start_init_desc": "Initializing Delpyche",
        "start_end_immediately": f"{ERROR_EMOJI} The monitoring process ended immediately.",
        "start_monitoring_ok": f"{OK_EMOJI} Monitoring started in the background. PID=",

        # stop
        "stop_ok": f"{OK_EMOJI} Monitor stopped successfully.",

        # restart
        "restart_stopping": f"{WARNING_EMOJI} Restarting monitor: Stopping...",
        "restart_starting": f"{WARNING_EMOJI} Starting again...",

        # status
        "status_running": f"{OK_EMOJI} Monitoring is running (PID",
        "status_not_running": f"{ERROR_EMOJI} Monitoring is NOT running.",
        "status_pid_exists_no_proc": f"{WARNING_EMOJI} PID file exists, but process is not running.",
        "status_pid_invalid": f"{ERROR_EMOJI} The PID file is invalid.",

        # config
        "config_current": f"{CONFIG_EMOJI} Current configuration:\n",
        "config_not_found": f"{ERROR_EMOJI} No configuration found in config.ini.",

        # info
        "logs_contents": "",

        # clean
        "clean_done": f"{CLEAN_EMOJI} Cleanup done.",

        # lang
        "lang_changed_to": f"{LANG_EMOJI} Language changed to",
        "lang_invalid": f"{ERROR_EMOJI} Invalid language. Use ES or EN.",
        "ask_restart": "Do you want to restart now? [Y/N]: ",

        # logs
        "monitor_started": "Monitor started.",
        "monitor_stopped_keyboard": "Monitor stopped by KeyboardInterrupt.",
        "monitor_log_new_pycache": "New __pycache__ detected",
        "monitor_log_removed": "Removed",

        # help
        "help_start":    "Starts the background monitor.",
        "help_stop":     "Stops the currently running monitor.",
        "help_restart":  "Restarts the monitor (stop + start).",
        "help_status":   "Shows the current monitoring status.",
        "help_config":   "Displays the config stored in config.ini.",
        "help_info":     "Shows the logs generated by the monitor.",
        "help_clean":    "Deletes logs, PID, and config file if they exist.",
        "help_set":      "Sets the delay (in seconds) before deleting __pycache__.",
        "help_path":     "Sets the path to monitor for __pycache__ directories.",
        "help_lang":     "Changes the application language (ES or EN).",
    },
}

CURRENT_LANG = "ES" 

def t(key):
    return LANG_TEXTS.get(CURRENT_LANG, LANG_TEXTS["ES"]).get(key, key)

HELP_TEXT = {
    "start":   {"ES": "help_start",   "EN": "help_start"},
    "stop":    {"ES": "help_stop",    "EN": "help_stop"},
    "restart": {"ES": "help_restart", "EN": "help_restart"},
    "status":  {"ES": "help_status",  "EN": "help_status"},
    "config":  {"ES": "help_config",  "EN": "help_config"},
    "info":    {"ES": "help_info",    "EN": "help_info"},
    "clean":   {"ES": "help_clean",   "EN": "help_clean"},
    "set":     {"ES": "help_set",     "EN": "help_set"},
    "path":    {"ES": "help_path",    "EN": "help_path"},
    "lang":    {"ES": "help_lang",    "EN": "help_lang"},
}

def load_config():
    config = configparser.ConfigParser()
    config['delpyche'] = {
        'delay': '3',
        'path': '.',
        'lang': 'ES'
    }
    if os.path.exists(CONFIG_FILE):
        config.read(CONFIG_FILE, encoding='utf-8')
    return config

def save_config(config):
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        config.write(f)

def get_delay_time():
    try:
        cfg = load_config()
        return int(cfg['delpyche']['delay'])
    except:
        return 3

def get_monitor_path():
    try:
        cfg = load_config()
        return cfg['delpyche']['path']
    except:
        return '.'

def set_current_lang(lang):
    global CURRENT_LANG
    CURRENT_LANG = lang
