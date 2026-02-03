import os

def run(args, env):
    if not args:
        print('mk: missing name')
        return
    name = args[0]
    if args and args[0] == '-d':
        # mk -d dirname
        if len(args) < 2:
            print('mk -d: missing dirname')
            return
        name = args[1]
        path = name if os.path.isabs(name) else os.path.join(env.get('cwd', os.getcwd()), name)
        try:
            os.makedirs(path, exist_ok=True)
        except Exception as e:
            print('mk error:', e)
        return
    path = name if os.path.isabs(name) else os.path.join(env.get('cwd', os.getcwd()), name)
    try:
        open(path, 'a').close()
    except Exception as e:
        print('mk error:', e)
