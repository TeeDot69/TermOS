import zipfile
import os

def run(args, env):
    if len(args) < 2:
        print('zip: usage zip archive.zip file1 [file2 ...]')
        return
    archive = args[0]
    files = args[1:]
    archive_path = archive if os.path.isabs(archive) else os.path.join(env.get('cwd', os.getcwd()), archive)
    try:
        with zipfile.ZipFile(archive_path, 'w') as z:
            for f in files:
                path = f if os.path.isabs(f) else os.path.join(env.get('cwd', os.getcwd()), f)
                z.write(path, arcname=os.path.basename(path))
        print('Created', archive_path)
    except Exception as e:
        print('zip error:', e)
