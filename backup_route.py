#!/usr/bin/env python3

import os
import shutil
import datetime
import logging

KAMAILIO_CFG = '/etc/kamailio/kamailio.cfg'
BASE_DIR = os.path.dirname(KAMAILIO_CFG)
BACKUP_DIR = '/opt/backup'
LOG_FILE = '/var/log/kamailio_backup.log'

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)

def get_last_include(cfg_path):
    last = None
    with open(cfg_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line.startswith('include_file') and line.endswith('.cfg"'):
                fname = line.split(None, 1)[1].strip('"').strip("'")
                last = fname
    return last

def make_backup(src_file, backup_dir):
    if not os.path.isfile(src_file):
        logging.error(f"Не найден файл: {src_file}")
        return False

    os.makedirs(backup_dir, exist_ok=True)
    base = os.path.splitext(os.path.basename(src_file))[0]
    date = datetime.datetime.now().strftime('%Y%m%d')
    dst_name = f'{base}{date}.cfg'
    dst = os.path.join(backup_dir, dst_name)

    try:
        shutil.copy2(src_file, dst)
        logging.info(f"Скопирован {src_file} → {dst}")
        return True
    except Exception as e:
        logging.error(f"Ошибка копирования {src_file} → {dst}: {e}")
        return False

def main():
    last = get_last_include(KAMAILIO_CFG)
    if not last:
        logging.error("Не найден include_file с .cfg")
        return
    src = os.path.join(BASE_DIR, last)
    make_backup(src, BACKUP_DIR)

if __name__ == '__main__':
    main()
