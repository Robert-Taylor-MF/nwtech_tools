import ctypes
import sys
import os

def is_admin():
    """Verifica se o programa está rodando como administrador"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    """Reinicia o programa com privilégios de administrador"""
    if not is_admin():
        try:
            # Reinicia o script com privilégios elevados
            script = sys.argv[0]
            params = ' '.join([script] + sys.argv[1:])
            
            ret = ctypes.windll.shell32.ShellExecuteW(
                None,
                "runas",
                sys.executable,
                params,
                None,
                1
            )
            
            if ret > 32:
                sys.exit(0)
            else:
                return False
        except:
            return False
    return True
