import os

def run(args, env):
    path = args[0] if args else env.get('cwd', os.getcwd())
    if not os.path.isabs(path):
        path = os.path.join(env.get('cwd', os.getcwd()), path)
    try:
        for name in os.listdir(path):
            print(name)
    except Exception as e:
        print('ls error:', e)
