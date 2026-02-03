import os
import importlib


def find_command(cmd):
    """Find and return a command module from the system paths"""
    # Search order: System64/commands, user bin directories
    search_paths = [
        'System64.commands',
    ]
    
    for path in search_paths:
        try:
            mod = importlib.import_module(f'{path}.{cmd}')
            return mod
        except ModuleNotFoundError:
            continue
    
    return None


def get_user_home(username):
    """Get the home directory for a user"""
    workspace_root = os.path.dirname(os.path.dirname(__file__))
    base_users = os.path.join(workspace_root, 'users', username)
    return base_users


def init_user_directories(username):
    """Create user directory structure if it doesn't exist"""
    home = get_user_home(username)
    subdirs = ['documents', 'downloads', 'pictures', 'videos', 'music']
    
    os.makedirs(home, exist_ok=True)
    for subdir in subdirs:
        os.makedirs(os.path.join(home, subdir), exist_ok=True)
    
    return home


def linux_path(abs_path):
    """Convert absolute path to Linux-style format (no drive letters)"""
    # Replace backslashes with forward slashes
    path = abs_path.replace('\\', '/')
    # Remove drive letter if on Windows (e.g., C: becomes empty)
    if len(path) > 1 and path[1] == ':':
        path = path[2:]
    # Ensure it starts with /
    if not path.startswith('/'):
        path = '/' + path
    return path

