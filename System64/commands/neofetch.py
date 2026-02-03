import platform
import registry
import os
import shutil


def get_cpu_info():
    try:
        return platform.processor() or 'N/A'
    except Exception:
        return 'N/A'


def get_ram_info():
    try:
        # Try Linux /proc/meminfo first
        with open('/proc/meminfo', 'r') as f:
            lines = f.readlines()
        mem_total = next((int(l.split()[1]) for l in lines if l.startswith('MemTotal:')), 0)
        mem_free = next((int(l.split()[1]) for l in lines if l.startswith('MemAvailable:')), 0)
        mem_used = mem_total - mem_free
        return f"{mem_used // 1024}MB / {mem_total // 1024}MB"
    except Exception:
        pass
    
    # Try psutil
    try:
        import psutil
        mem = psutil.virtual_memory()
        used_mb = mem.used // 1024 // 1024
        total_mb = mem.total // 1024 // 1024
        return f"{used_mb}MB / {total_mb}MB"
    except Exception:
        pass
    
    # Try Windows API via ctypes
    try:
        import ctypes
        kernel32 = ctypes.windll.kernel32
        c_ulong = ctypes.c_ulong
        
        class MEMORYSTATUS(ctypes.Structure):
            _fields_ = [
                ("dwLength", c_ulong),
                ("dwMemoryLoad", c_ulong),
                ("dwTotalPhys", c_ulong),
                ("dwAvailPhys", c_ulong),
                ("dwTotalPageFile", c_ulong),
                ("dwAvailPageFile", c_ulong),
                ("dwTotalVirtual", c_ulong),
                ("dwAvailVirtual", c_ulong)
            ]
        
        mem_status = MEMORYSTATUS()
        mem_status.dwLength = ctypes.sizeof(MEMORYSTATUS)
        kernel32.GlobalMemoryStatus(ctypes.byref(mem_status))
        
        total_mb = mem_status.dwTotalPhys // 1024 // 1024
        used_mb = (mem_status.dwTotalPhys - mem_status.dwAvailPhys) // 1024 // 1024
        return f"{used_mb}MB / {total_mb}MB"
    except Exception:
        pass
    
    return 'N/A'


def get_storage_info():
    try:
        total, used, free = shutil.disk_usage(os.getcwd())
        return f"{used // 1024 // 1024}MB / {total // 1024 // 1024}MB"
    except Exception:
        return 'N/A'


def right_align_text(ascii_art, info_lines, width=46):
    """Align info lines to the right of the ASCII art"""
    lines = ascii_art.split('\n')
    result = []
    for i, line in enumerate(lines):
        if i < len(info_lines):
            info = info_lines[i]
            result.append(f"{line} {info}")
        else:
            result.append(line)
    return '\n'.join(result)


def run(args, env):
    version = getattr(registry, 'VERSION', '3.0')
    lime = "\033[38;5;155m"
    white = "\033[97m"
    reset = "\033[0m"
    user = env.get('user', 'user')
    
    # Get hostname safely
    try:
        host = platform.node() or 'TermOS'
    except Exception:
        host = 'TermOS'
    
    shell = 'Python CLI'
    terminal = os.environ.get('TERM', 'terminal')
    cpu = get_cpu_info()
    ram = get_ram_info()
    storage = get_storage_info()

    ascii_art = ()

    info_lines = [
        f"{lime}OS: {white}TermOS {version}{reset}"
        f"{lime}Host: {white}{host}{reset}",
        f"{lime}Shell: {white}{shell}{reset}",
        f"{lime}Terminal: {white}{terminal}{reset}",
        f"{lime}CPU: {white}{cpu}{reset}",
        f"{lime}RAM: {white}{ram}{reset}",
        f"{lime}Storage: {white}{storage}{reset}",
    ]

    print(f"{lime}{user}{white}@{lime}{host}{reset}")
    print(f"{white}{'-'*46}{reset}")
    
    for i, line in enumerate(ascii_art):
        if i < len(info_lines):
            print(f"{line} {info_lines[i]}")
        else:
            print(line)
