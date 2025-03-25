from time import sleep, time

def sleep_ms(ms):
    sleep(ms/1000)

def ticks_ms():
    return int(time() * 1000)

def ticks_diff(new, old):
    return new - old
