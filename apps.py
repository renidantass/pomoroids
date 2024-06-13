import sys

from enum import Enum
from subprocess import run, check_output, CompletedProcess


type Processo = str

status_processo = {0: 'O execução foi finalizado.',
                   128: 'O execução não foi encontrado.'}


class OperationalSystem(Enum):
    linux   = 'linux' 
    windows = 'win32'
    mac     = 'darwin'

def finalizar_processo(processo: Processo) -> int:
    returncode = 0
    platform = sys.platform

    match platform:
        case OperationalSystem.linux.value:
            output = check_output(['pgrep', processo])
            pid = output.decode('utf-8').split('\n')[0]
            returncode = run(['kill', pid]).returncode
            return returncode 
        case OperationalSystem.windows.value:
            returncode = run(["taskkill", "/F", "/IM", processo]).returncode
            return returncode 
        case OperationalSystem.mac.value:
            return -1
        case default:
            return -1
    

def notificacao_desktop(em_processo: list) -> None:

    # tratar multiplas entradas de execução em uma só notification
    mensagem_detalhes: str

    match len(em_processo):
        case 1: mensagem_detalhes = f"O programa {em_processo[0].args[3]} não está autorizado a abrir agora."
        case varios_apps: mensagem_detalhes = f"Os programas {em_processo} em questão não estão autorizados a abrir agora."

    toast("App Restrictor",
          mensagem_detalhes)


def notificar_finalizacao(apps: list):

    apenas_um_app = (len(apps) == 1)

    if apenas_um_app:
        processo = finalizar_execucao(apps[0])
        notificacao_desktop(em_processo=[execucao])

    else:
        execucoes = []

        for app in apps:
            processo = finalizar_execucao(app)
            execucoes.append(processo.returncode)
        
        notificacao_desktop(em_processo=execucoes)
