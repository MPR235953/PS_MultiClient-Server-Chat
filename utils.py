import logging

logging.basicConfig(format='%(asctime)s %(process)d %(levelname)s: %(message)s', level=logging.DEBUG)
logger = logging.getLogger()

CONFIG = {
    "max_transfer": 16,                 # in bytes
    "max_connect_requests": 3,          # normal value
    "transfer_delay": 0.3,              # in sec
    "client_max": 3
}

SERVER_DISCONNECT_CLIENT_KEY = 'wVwPerjVl6HYNSTs'
CLIENT_DISCONNECT_FROM_SERVER_KEY = 'hfQf5we98FiVhauG'
