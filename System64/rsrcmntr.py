import os
import platform
import shutil
import time


def run(args, env):
    print('TermOS Resource Monitor')
    print('User:', env.get('user'))
    print('Platform:', platform.platform())
    try:
        total, used, free = shutil.disk_usage(env.get('cwd', os.getcwd()))
        print('Disk total:', total//1024//1024, 'MB')
        print('Disk used:', used//1024//1024, 'MB')
        print('Disk free:', free//1024//1024, 'MB')
    except Exception:
        pass
    # Memory info from /proc/meminfo if available
    try:
        with open('/proc/meminfo') as f:
            lines = f.readlines()
        mem_total = next((int(l.split()[1]) for l in lines if l.startswith('MemTotal:')), None)
        mem_free = next((int(l.split()[1]) for l in lines if l.startswith('MemAvailable:')), None)
        if mem_total:
            print('Memory total:', mem_total//1024, 'MB')
        if mem_free:
            print('Memory available:', mem_free//1024, 'MB')
    except Exception:
        pass
    # uptime
    try:
        with open('/proc/uptime') as f:
            up = float(f.read().split()[0])
        print('Uptime (s):', int(up))
    except Exception:
        pass
    time.sleep(0.1)
