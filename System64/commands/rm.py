import os

PROTECTED = ['System64']

def is_protected(path):
    # if path contains a protected folder at top level
    parts = os.path.normpath(path).split(os.sep)
    return any(p in PROTECTED for p in parts)


def run(args, env):
    if not args:
        print('rm: missing path')
        return
    path = args[0]
    if not os.path.isabs(path):
        path = os.path.join(env.get('cwd', os.getcwd()), path)
    if is_protected(path) and not env.get('is_root'):
        print('Permission denied: protected system file')
        return
    try:
        if os.path.isdir(path):
            os.rmdir(path)
        else:
            os.remove(path)
    except Exception as e:
        print('rm error:', e)
