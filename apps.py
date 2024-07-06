import sys
from enum import Enum
from subprocess import run, check_output


type Processo = str


class OperatingSystem(Enum):
    linux   = 'linux' 
    windows = 'win32'
    mac     = 'darwin'


def finalizar_processo(processo: Processo) -> int:
    returncode = -1
    platform   = sys.platform

    print(f'A finalizar {processo}')

    try:
        match platform:
            case OperatingSystem.linux.value:
                output = check_output(['pgrep', processo])
                pid = output.decode('utf-8').split('\n')[0]
                returncode = run(['kill', pid]).returncode
                return returncode 
            case OperatingSystem.windows.value:
                returncode = run(["taskkill", "/F", "/IM", processo]).returncode
                return returncode 
            case OperatingSystem.mac.value:
                raise Exception('Ainda não implementado')
            case _:
                return -1
    except Exception:
        print('Não foi possível encerrar o processo')
        return -1

