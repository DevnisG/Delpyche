import time
import shutil
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from config import (
    ERROR_EMOJI,
    t,
    get_delay_time,
    get_monitor_path,
    LOG_DIR
)

class PycacheHandler(FileSystemEventHandler):
    def __init__(self, delay):
        self.delay = delay

    def on_created(self, event):
        if event.is_directory and event.src_path.endswith('__pycache__'):
            logging.info(f"{t('monitor_log_new_pycache')}: {event.src_path}")
            time.sleep(self.delay)
            try:
                shutil.rmtree(event.src_path)
                logging.info(f"{t('monitor_log_removed')}: {event.src_path}")
            except Exception as e:
                logging.error(f"{ERROR_EMOJI} {t('process_stop_error')} {event.src_path}: {e}")

def start_monitor():
    import os

    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)

    logging.basicConfig(
        filename=os.path.join(LOG_DIR, 'monitor.log'),
        level=logging.INFO,
        format='%(asctime)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    logging.info(t("monitor_started"))

    delay = get_delay_time()
    mon_path = get_monitor_path()

    handler = PycacheHandler(delay)
    observer = Observer()
    observer.schedule(handler, path=mon_path, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        logging.info(t("monitor_stopped_keyboard"))
    observer.join()
