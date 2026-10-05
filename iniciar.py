"""Carga la configuración local excluida de Git y ejecuta comandos de Django."""
import os
import sys
from pathlib import Path

def main():
    env_file=Path(__file__).resolve().parent/'.env'
    if env_file.exists():
        for line in env_file.read_text(encoding='utf-8').splitlines():
            if line.strip() and not line.lstrip().startswith('#') and '=' in line:
                key,value=line.split('=',1)
                os.environ.setdefault(key.strip(),value.strip())
    os.environ.setdefault('DJANGO_SETTINGS_MODULE','config.settings')
    from django.core.management import execute_from_command_line
    execute_from_command_line([sys.argv[0],*(sys.argv[1:] or ['runserver'])])

if __name__=='__main__':
    main()
