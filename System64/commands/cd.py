import os
from System64 import PATH


def run(args, env):
    if not args:
        # Go to home directory
        target = env.get('home', os.path.expanduser('~'))
    else:
        target = args[0]
    
    if not os.path.isabs(target):
        target = os.path.join(env.get('cwd', os.getcwd()), target)
    
    try:
        target = os.path.abspath(target)
        if os.path.isdir(target):
            os.chdir(target)
            env['cwd'] = os.getcwd()
        else:
            print('cd: directory not found:', target)
    except Exception as e:
        print('cd error:', e)
