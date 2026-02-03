import os


def run(args, env):
    if args:
        path = args[0]
    else:
        path = input('ohedit file: ').strip()
    if not path:
        print('No file specified.')
        return
    # resolve relative to cwd
    if not os.path.isabs(path):
        path = os.path.join(env.get('cwd', os.getcwd()), path)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    existing = ''
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            existing = f.read()
    print('--- current content ---')
    print(existing)
    print('--- Enter new content. End with a single line containing only a dot (.) ---')
    lines = []
    while True:
        try:
            ln = input()
        except EOFError:
            break
        if ln == '.':
            break
        lines.append(ln)
    with open(path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    print('Saved', path)
