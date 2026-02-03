import os
import sys

def run(args, env):
    # Try to clear terminal in Termux
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')
