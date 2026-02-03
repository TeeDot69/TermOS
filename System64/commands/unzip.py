import zipfile
import os

def run(args, env):
    if len(args) < 1:
        print('unzip: usage unzip archive.zip [dest]')
        return
    archive = args[0]
    dest = args[1] if len(args)>1 else env.get('cwd', os.getcwd())
    archive_path = archive if os.path.isabs(archive) else os.path.join(env.get('cwd', os.getcwd()), archive)
    try:
        with zipfile.ZipFile(archive_path, 'r') as z:
            z.extractall(dest)
        print('Extracted to', dest)
    except Exception as e:
        print('unzip error:', e)
