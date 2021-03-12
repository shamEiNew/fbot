import time
import logging
import reply_bro as rb
import config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()
def main():
    api = config.create_api()
    user = 67611162
    since_id = 1370204145987190788
    while True:
        sleep_time = 60*60*2
        since_id = rb.reply_bro(api, since_id, user)
        logger.info(f"{since_id}")
        logger.info("sleeping...")
        time.sleep(sleep_time)

if __name__ == "__main__":
    main()