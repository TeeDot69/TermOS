import os

def read_battery_termux():
    # Try reading common linux battery path
    candidates = [
        '/sys/class/power_supply/BAT0/capacity',
        '/sys/class/power_supply/battery/capacity',
    ]
    for p in candidates:
        if os.path.exists(p):
            try:
                with open(p) as f:
                    return f.read().strip() + '%'
            except Exception:
                pass
    return None


def run(args, env):
    val = read_battery_termux()
    if val:
        print('Battery:', val)
    else:
        print('Battery: unknown')
