import time
import logging
import reply_bro as rb
import vax as v
import config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()
def main():
    api = config.create_api()
    user = 1196797894717632513
    while True:
        sleep_time = 10*60
        text_update = v.vax_main()
        print(text_update)
        logger.info("sending dm")
        if len(text_update) > 0 :
            rb.reply_bro(api, user, str(text_update))
        else:
            pass
        logger.info("sleeping...")
        time.sleep(sleep_time)

if __name__ == "__main__":
    main()