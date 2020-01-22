import gspread
from oauth2client.service_account import ServiceAccountCredentials
import logging as log
from os import path, makedirs

from src.constant import *


def get_new_id():
    with open(ID_PATH, 'r') as file:
        pid = int(file.read())
    with open(ID_PATH, 'w') as file:
        file.write(str(pid + 1))
    return pid



def connect_to_table():
    credentials = ServiceAccountCredentials.from_json_keyfile_name(KEY_FILE, SCOPE)
    client = gspread.authorize(credentials)
    return client.open('FaceBot').sheet1



def create_logging():
    if not path.exists(LOG_DIR):
        makedirs(LOG_DIR)
    # logging to log file
    log.basicConfig(format='%(asctime)s | %(levelname)s | %(message)s', filename=LOG_PATH, level=log.INFO)