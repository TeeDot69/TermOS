import datetime

def run(args, env):
    print(datetime.datetime.now().time().isoformat(timespec='seconds'))
