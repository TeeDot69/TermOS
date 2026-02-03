import os
import json
import hashlib

USERS_PATH = os.path.join(os.path.dirname(__file__), 'users.json')


def _ensure_users_file():
    if not os.path.exists(USERS_PATH):
        with open(USERS_PATH, 'w') as f:
            json.dump({'users': {}}, f)


def hash_password(pw: str) -> str:
    return hashlib.sha256(pw.encode('utf-8')).hexdigest()


def load_users():
    try:
        with open(USERS_PATH, 'r') as f:
            content = f.read().strip()
            if not content:
                # If the file is empty, generate default data
                default_data = {'users': {}}
                with open(USERS_PATH, 'w') as wf:
                    json.dump(default_data, wf, indent=2)
                return default_data
            return json.loads(content)
    except FileNotFoundError:
        # Return default structure if file doesn't exist
        default_data = {'users': {}}
        with open(USERS_PATH, 'w') as wf:
            json.dump(default_data, wf, indent=2)
        return default_data
    except json.JSONDecodeError:
        # Return default structure if JSON is invalid
        default_data = {'users': {}}
        with open(USERS_PATH, 'w') as wf:
            json.dump(default_data, wf, indent=2)
        return default_data


def save_users(data):
    with open(USERS_PATH, 'w') as f:
        json.dump(data, f, indent=2)


def create_user(name, password, is_root=False):
    data = load_users()
    data['users'][name] = {'password': hash_password(password), 'is_root': bool(is_root)}
    save_users(data)


def verify_login(name, password):
    data = load_users()
    u = data['users'].get(name)
    if not u:
        return False, None
    if u['password'] == hash_password(password):
        return True, {'name': name, 'is_root': u.get('is_root', False)}
    return False, None


def has_users():
    data = load_users()
    return bool(data.get('users'))
