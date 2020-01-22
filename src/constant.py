# TODO: set profile picture
# TODO: always female in fb

from os.path import join, dirname
from datetime import datetime as dt

SCOPE = [
    'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive.file',
    'https://www.googleapis.com/auth/drive'
]

# --- numbers ---
WINDOW_WAIT = 20
FB_CODE_WAIT = 60
ACCOUNTS = 1

# --- paths ---
PROJECT_ROOT = dirname(dirname(__file__))
KEY_FILE = join(PROJECT_ROOT, 'resources', 'FaceBot-a87958597f24.json')
LOG_DIR = join(PROJECT_ROOT, 'log')
LOG_PATH = join(PROJECT_ROOT, 'log', 'log_{}.log'.format(str(dt.now().date())))
ID_PATH = join(PROJECT_ROOT, 'resources', 'id.txt')

# --- URLs ---
FAKE_IDENTITY_URL = 'https://www.fakepersongenerator.com/?new=fresh'
FB_HOME_URL = 'https://www.facebook.com'
TEMP_MAIL_URL = 'https://temp-mail.org/en'
DELETE_MAIL_URL = 'https://temp-mail.org/en/option/delete'
REFRESH_MAIL_URL = 'https://temp-mail.org/en/option/refresh'
CHANGE_MAIL_URL = 'https://temp-mail.org/en/option/change'
