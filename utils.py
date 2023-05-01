import logging

logging.basicConfig(format='%(asctime)s %(process)d %(levelname)s: %(message)s', level=logging.DEBUG)
logger = logging.getLogger()

CONFIG = {
    "max_transfer": 16,                 # in bytes
    "max_connect_requests": 3,          # normal value
    "transfer_delay": 0.5,              # in sec
    "client_max": 3,                    # tmp, default to 3
    "timeout": 1                        # in sec
}

SERVER_DISCONNECT_KEY = 'wVwPerjVl6HYNSTs'
SERVER_BUSY_KEY = 'wVwPerjV8FiVhauG'
CLIENT_DISCONNECT_KEY = 'hfQf5we98FiVhauG'
CLIENT_CONNECT_KEY = 'erjV8FiVhauGhfQf'
CLIENT_TEST_KEY = 'V8FhfQiVhaerjuGf'
