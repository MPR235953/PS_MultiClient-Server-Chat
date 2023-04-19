import logging

logging.basicConfig(format='%(asctime)s %(process)d %(levelname)s: %(message)s', level=logging.DEBUG)
logger = logging.getLogger()

CONFIG = {
    "max_transfer": 16,                 # in bytes
    "max_connect_requests": 3,          # normal value
    "transfer_delay": 0.5,              # in sec
    "client_max": 3  # tmp, default to 3
}

SERVER_DISCONNECT_KEY = 'wVwPerjVl6HYNSTs'
SERVER_BUSY_KEY = 'wVwPerjV8FiVhauG'
CLIENT_DISCONNECT_KEY = 'hfQf5we98FiVhauG'
