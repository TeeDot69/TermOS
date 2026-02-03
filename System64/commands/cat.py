import os

def run(args, env):
    if not args:
        print('cat: missing file')
        return
    path = args[0]
    if not os.path.isabs(path):
        path = os.path.join(env.get('cwd', os.getcwd()), path)
    try:
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            print(f.read())
    except Exception as e:
        print('cat error:', e)
