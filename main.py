import time
import reply_bro as rb
import config

def main():
    api = config.create_api()
    user = 67611162
    since_id = 1
    while True:
        sleep_time = 60*60*2
        since_id = rb.reply_bro(api, since_id, user)
        time.sleep(sleep_time)

if __name__ == "__main__":
    main()