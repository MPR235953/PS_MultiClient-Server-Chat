import logging

logging.basicConfig(format='%(asctime)s %(process)d %(levelname)s: %(message)s', level=logging.DEBUG)
logger = logging.getLogger()

cfg = {
    "max_transfer": 16,                 # in bytes
    "max_connect_requests": 5,          # normal value
    "transfer_delay": 0.3               # in sec
}