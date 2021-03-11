import time
import reply_bro as rb

def main():
    while True:
        sleep_time = 60*60*3
        rb.reply_bro()
        time.sleep(sleep_time)