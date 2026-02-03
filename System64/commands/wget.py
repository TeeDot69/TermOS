import urllib.request
import os

def run(args, env):
    if not args:
        print('wget: missing url')
        return
    url = args[0]
    filename = args[1] if len(args)>1 else os.path.basename(url) or 'download'
    out = filename if os.path.isabs(filename) else os.path.join(env.get('cwd', os.getcwd()), filename)
    try:
        urllib.request.urlretrieve(url, out)
        print('Saved to', out)
    except Exception as e:
        print('wget error:', e)
